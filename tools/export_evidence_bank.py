"""Export the REAL per-image expert scores used by the console simulator (src/console/data/evidence_bank.json).

Rows: the 3410 OOF images that fire_cnn (A final s0), CLIP zero-shot and CLIP probe (F final s0) all scored (same block ids,
same order, same labels: TRINETRA/results/fire_meta/inputs). Probabilities are the cross-fit calibrated OOF values (prob_cal).
The simulator draws ONE row per camera observation conditioned on the scenario's ground truth, so every evidence vector is
a real joint output of the three models on one image (REAL pairing). Also exports the stacked meta model (logistic on
[logit p_i, sd, range] of RAW probabilities, fitted on all OOF rows, as in kaggle/crossmodal_fusion.py) so STACK can run
in the browser. Run: python3 tools/export_evidence_bank.py
"""
import json, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, "TRINETRA/trinetra/src"); sys.path.insert(0, "TRINETRA/trinetra/kaggle")
from fire_meta_fusion import features                       # noqa: E402
from trinetra.eval import LogisticNumpy                     # noqa: E402
from trinetra.deep.oof_utils import fit_temperature         # noqa: E402

I = Path("TRINETRA/results/fire_meta/inputs")
E = {n: np.load(I / f, allow_pickle=True) for n, f in
     (("fire_cnn", "fire_s0_oof.npz"), ("zeroshot", "zeroshot_s0_oof.npz"), ("clip_probe", "clip_probe_s0_oof.npz"))}
y = E["fire_cnn"]["y"].astype(int); blk = E["fire_cnn"]["block"].astype(str)
assert all(np.array_equal(E[n]["block"], blk) for n in E)
raw = np.column_stack([E[n]["prob"] for n in E]); cal = np.column_stack([np.where(np.isnan(E[n]["prob_cal"]), E[n]["prob"], E[n]["prob_cal"]) for n in E])
m = LogisticNumpy(seed=0).fit(features(raw), y); T = fit_temperature(m.predict_proba(features(raw)), y)
rows = [[int(y[i]), *[round(float(v), 4) for v in cal[i]], *[round(float(v), 5) for v in raw[i]]] for i in range(len(y))]
meta = {k: json.loads(str(E[k]["meta"]))["run_id"] for k in E}
out = {"source": "TRINETRA/results/fire_meta/inputs (A final fire_s0, F final zeroshot_s0 + clip_probe_s0)", "run_ids": meta,
       "columns": ["y", "cal_fire_cnn", "cal_zeroshot", "cal_clip_probe", "raw_fire_cnn", "raw_zeroshot", "raw_clip_probe"],
       "n": len(rows), "n_pos": int(y.sum()), "n_blocks": int(len(set(blk))),
       "stack": {"w": m.w.tolist(), "b": float(m.b), "mu": m.mu.tolist(), "sd": m.sd.tolist(), "T": float(T),
                 "features": ["logit_fire_cnn", "logit_zeroshot", "logit_clip_probe", "sd", "range"]},
       "rows": rows}
Path("src/console/data/evidence_bank.json").write_text(json.dumps(out, separators=(",", ":")))
print("rows", len(rows), "pos", int(y.sum()), "stack T", round(T, 3), "size KB", round(Path("src/console/data/evidence_bank.json").stat().st_size / 1e3))
