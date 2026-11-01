# TRINETRA — Kaggle training kernels

Train the deep models on Kaggle GPU, then copy the exported artifacts back to the offline edge/gateway
runtime (which uses only the numpy core in `src/trinetra/`). Nothing here issues alerts; every model only
emits calibrated expert probabilities that feed `trinetra.ws5_fusion_rl.decide`, and NO performance number
may be reported until the eval admission gate (`trinetra.deep.train.admit_model`) returns `admitted=True`
(Rule 16).

## 1. Kaggle setup
- New Notebook/Script → Settings → Accelerator = **GPU T4 x2** (or P100), Internet = **On** (first run only,
  to let pip resolve `requirements-deep.txt`).
- Add this repo (as a Kaggle Dataset or GitHub) so `src/` is importable.
- Attach your downloaded datasets; the loaders default to `/kaggle/input/<slug>` (see `datamodules.KagglePaths`).

```bash
pip install -r requirements-deep.txt
```

## 2. Expected dataset layout (.npz per model — build these from the raw sources you download)
| Model | Slug (default) | Keys in .npz |
|-------|----------------|--------------|
| Geo-PINN | `trinetra-geo` | `Z,t,rain,static[,label,lat,lon]` |
| Fire/smoke | `trinetra-fire` | `images (N,T,C,H,W), labels (N,2), block` |
| EO head | `trinetra-eo` | `images (N,C,H,W), labels (N,), block` |
| Deep anomaly | `trinetra-telemetry` | `X (N,C,T)[, y, block]` (train on NORMAL only) |
| Deepfake | `trinetra-media` | `images (N,C,H,W), labels (N,), block` |
| Offline-RL | `trinetra-rl-logs` | `s,a,r,s_next,done,behavior_prob` |

Build `block` from lat/lon with `datamodules.spatial_block(lat, lon)` so train/val never share a cell.

## 2b. Multi-GPU (Kaggle T4 x2) — ON by default
All training scripts auto-detect both T4s and train with `nn.DataParallel` (`--parallel auto`, the default).
On startup each script prints, e.g. `GPUs visible=2 | DataParallel=True | effective_batch=128 lr=6.00e-04`.

- `--batch N` is the **per-GPU** batch; the effective batch is `N * n_gpus`, and the LR is scaled linearly
  (Goyal et al. 2017 warmup-free rule). Example: `--batch 64` on 2×T4 → effective batch 128.
- fp16 **AMP** + cuDNN autotuning are enabled automatically (big speedup on Turing T4s).
- `--parallel none` forces single-GPU; `--parallel dp` forces DataParallel.
- **Offline-RL** deliberately uses ONE GPU (the Q-net is tiny; scatter/gather would cost more than it saves)
  — it just uses a large batch instead.
- **Geo-PINN caveat:** its physics loss uses `autograd.grad` inside the forward. DataParallel runs this
  per-replica and usually works; if you hit a thread/autograd error, rerun with `--parallel none` or use the
  DDP launcher below.

### Max-throughput path: DistributedDataParallel
For long runs, DDP (one process per GPU, no GIL scatter bottleneck) is faster than DataParallel. Use
`trinetra.deep.ddp` from a plain `.py` script (don't initialize CUDA in the notebook first):
```python
from trinetra.deep.ddp import launch_ddp, ddp_worker, wrap_ddp, ddp_loader, is_main
@ddp_worker                       # handles setup/cleanup/barrier
def worker(rank, world_size, args):
    model = wrap_ddp(build_model(), rank)
    loader = ddp_loader(dataset, batch_size=64)      # DistributedSampler shards per rank
    ...train...                                      # grads all-reduced automatically
    if is_main(): torch.save(model.module.state_dict(), ".../model.pt")
launch_ddp(worker, args)          # spawns 1 process per GPU
```

## 3. Run (one script per model)
```bash
python kaggle/train_geo_pinn.py      --data /kaggle/input/trinetra-geo/geo.npz      --out /kaggle/working
python kaggle/train_classifier.py --model fire     --data /kaggle/input/trinetra-fire/fire.npz --out /kaggle/working
python kaggle/train_classifier.py --model eo       --data /kaggle/input/trinetra-eo/eo.npz     --out /kaggle/working
python kaggle/train_classifier.py --model deepfake --data /kaggle/input/trinetra-media/media.npz --out /kaggle/working
python kaggle/train_anomaly.py       --data /kaggle/input/trinetra-telemetry/tele.npz --out /kaggle/working
python kaggle/train_offline_rl.py    --data /kaggle/input/trinetra-rl-logs/logs.npz   --out /kaggle/working
python kaggle/train_fusion_head.py   --data /kaggle/working/fusion_cache.npz          --out /kaggle/working
```
All training scripts accept `--batch` (per-GPU) and `--parallel {auto,dp,none}`.

## 4. Outputs (copy to the edge runtime)
- `*.pt` checkpoints (per fold + calibrated temperature).
- `*_report.json` — the honesty report; deploy a model ONLY if `"admitted": true`.
- `gmf_head_numpy.json` — the GMF residual head serialized to numpy so the OFFLINE gateway (no torch) can
  run it via `ws5_fusion_rl.gmf.gmf_fuse(..., head=closure)`.

## Honesty / safety reminders (enforced, not optional)
- Class-C novel terms (ND flicker, PHARAOH) stay OFF unless explicitly enabled; Class-A/B is the fallback.
- Deepfake authenticity enters fusion with capped reliability and never gates a life-safety alert (Rule 19).
- Offline-RL action is always raised to the shield floor at deployment; it can only move toward safety.
- `admit_model` must pass on spatial-CV before any accuracy/skill claim leaves the notebook.
