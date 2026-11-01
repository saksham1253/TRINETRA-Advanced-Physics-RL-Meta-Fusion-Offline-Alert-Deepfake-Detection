"""End-to-end SMOKE TEST of the hackathon chain on SYNTHETIC images (no datasets, ~2-5 min on CPU).

adapter -> fire CNN (2 seeds, held-out) -> colour baseline -> zero-shot (--dry-run) -> deepfake -> fusion cache
-> GMF head -> RL logs -> offline RL (2 seeds) -> collect_results. Pass = prints "SMOKE TEST PASSED".
Numbers produced here are MEANINGLESS (synthetic data, random CLIP weights) and must never be reported.
Run: python kaggle/smoke_test_all.py [--out /tmp/trinetra_smoke] [--skip-zeroshot]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                       # TRINETRA/
PY = sys.executable


def run(*args):
    cmd = [PY, *map(str, args)]
    print("\n$", " ".join(cmd[1:]), flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit(f"FAILED: {' '.join(cmd[1:3])}")
    print("\n".join(r.stdout.strip().splitlines()[-3:]))


def make_images(root: Path, n: int, seed: int, kind: str):
    """fire: warm blob vs cool scene; deepfake: smooth (real) vs high-frequency (fake). Names carry video ids."""
    from PIL import Image
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:48, 0:48]
    for cls in (("fire", "nofire") if kind == "fire" else ("real", "fake")):
        (root / cls).mkdir(parents=True, exist_ok=True)
        for i in range(n):
            cx, cy = rng.uniform(10, 38, 2)
            blob = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * rng.uniform(4, 9) ** 2))
            base = rng.uniform(0.1, 0.4, 3)
            img = np.ones((48, 48, 3)) * base
            if cls == "fire":
                img += blob[..., None] * np.array([0.9, 0.45, 0.05]) * rng.uniform(0.5, 1)
            elif cls == "nofire":
                img += blob[..., None] * np.array([0.2, 0.3, 0.6]) * rng.uniform(0.5, 1)
            elif cls == "fake":
                img += 0.15 * np.sin(xx * rng.uniform(1.5, 2.5))[..., None]
            img = np.clip(img + rng.normal(0, 0.03, img.shape), 0, 1)
            Image.fromarray((img * 255).astype("uint8")).save(root / cls / f"vid{i % 12:02d}_frame{i:04d}.jpg")


def make_videos(root: Path) -> bool:
    """Two synthetic AVIs per class (warm flicker = fire, cool static = neg). Needs opencv."""
    try:
        import cv2
    except ImportError:
        print("[skip] opencv missing -> video eval skipped"); return False
    rng = np.random.default_rng(5)
    for cls, warm in (("fire/pos", True), ("fire/neg", False)):
        (root / cls).mkdir(parents=True, exist_ok=True)
        for v in range(2):
            w = cv2.VideoWriter(str(root / cls / f"v{v}.avi"), cv2.VideoWriter_fourcc(*"MJPG"), 10, (48, 48))
            for k in range(30):
                img = np.full((48, 48, 3), 60, np.uint8)
                if warm:
                    img[14:34, 14:34] = (20, 110 + int(40 * rng.random()), 230)    # BGR orange, flickering
                w.write(img)
            w.release()
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/trinetra_smoke"); ap.add_argument("--skip-zeroshot", action="store_true")
    a = ap.parse_args()
    out = Path(a.out); raw = out / "raw"; npz = out / "npz"; res = out / "out"
    for p in (npz, res):
        p.mkdir(parents=True, exist_ok=True)
    A = ROOT / "data_adapters" / "build_npz.py"
    make_images(raw / "fire_main", 90, 0, "fire"); make_images(raw / "fire_heldout", 30, 1, "fire")
    make_images(raw / "media", 90, 2, "deepfake")
    run(A, "folder", "--root", raw / "fire_main", "--map", "fire=fire", "nofire=none", "--size", 32, "--out", npz / "all.npz")
    run(A, "subset", "--npz", npz / "all.npz", "--keep", "train", "val", "--out", npz / "fire.npz")
    run(A, "folder", "--root", raw / "fire_heldout", "--map", "fire=fire", "nofire=none", "--size", 32, "--out", npz / "heldout.npz")
    run(A, "folder", "--root", raw / "media", "--map", "real=real", "fake=fake", "--task", "deepfake", "--size", 32, "--out", npz / "media.npz")
    make_images(raw / "confusers", 20, 3, "fire")
    run(A, "folder", "--root", raw / "confusers", "--map", "nofire=none", "--size", 32, "--out", npz / "confusers.npz")
    video_ok = make_videos(raw / "videos")
    if video_ok:
        run(A, "video", "--root", raw / "videos", "--map", "fire/pos=fire", "fire/neg=none", "--every", 2, "--clip", 1,
            "--size", 32, "--out", npz / "frames.npz")
    for f in ("fire", "heldout", "media"):
        run(A, "check", "--npz", npz / f"{f}.npz")
    common = ["--epochs", 2, "--batch", 16, "--folds", 3, "--num-workers", 0]
    for s in (0, 1):
        run(HERE / "train_classifier.py", "--model", "fire", "--target", "any", "--data", npz / "fire.npz", "--test", npz / "heldout.npz",
            "--stress", npz / "confusers.npz", "--out", res / "fire", "--seed", s, *common)
        run(HERE / "baseline_colorhist.py", "--data", npz / "fire.npz", "--target", "any", "--out", res / "colorhist", "--folds", 3, "--seed", s)
    if video_ok:
        run(HERE / "eval_video.py", "--frames", npz / "frames.npz", "--models", res / "fire", "--seed", 0, "--out", res / "video")
    run(HERE / "train_classifier.py", "--model", "deepfake", "--data", npz / "media.npz", "--out", res / "deepfake", *common)
    fuse_args = ["--fire", res / "fire/fire_s0_oof.npz", "--deepfake", res / "deepfake/deepfake_s0_oof.npz", "--fake-frac", 0.1,
                 "--n", 800, "--seeds", 0, 1, 2, "--out", res / "fusion"]
    zs_ok = False
    if not a.skip_zeroshot:
        try:
            import open_clip  # noqa: F401
            run(HERE / "eval_zeroshot.py", "--data", npz / "fire.npz", "--test", npz / "heldout.npz", "--folds", 3,
                "--stress", npz / "confusers.npz", "--out", res / "zeroshot", "--dry-run",
                "--model", "ViT-B-32", "--probe", "--probe-out", res / "clip_probe")
            zs_ok = True
        except ImportError:
            print("[skip] open_clip not installed -> zero-shot skipped (pip install open_clip_torch)")
    fuse_args += ["--zeroshot", res / "zeroshot/zeroshot_s0_oof.npz"] if zs_ok else ["--colorhist", res / "colorhist/colorhist_s0_oof.npz"]
    run(HERE / "build_fusion_cache.py", *fuse_args)
    run(HERE / "train_fusion_head.py", "--data", res / "fusion/fusion_cache.npz", "--out", res / "fusion", "--epochs", 20)
    run(ROOT / "data_adapters" / "make_rl_logs.py", "--inp", res / "fusion/fusion_cache.npz", "--out", res / "rl/logs.npz")
    for s in (0, 1):
        run(HERE / "train_offline_rl.py", "--data", res / "rl/logs.npz", "--out", res / "rl", "--epochs", 3, "--seed", s, "--n-boot", 100)
    run(HERE / "collect_results.py", "--inp", res, "--out", res / "results", "--pack", "SYNTHETIC-SMOKE")
    r = json.load(open(res / "results" / "results.json"))
    need = {"fire", "colorhist", "deepfake", "offline_rl"} | ({"zeroshot"} if zs_ok else set()) | ({"video"} if video_ok else set())
    missing = need - set(r["models"])
    if missing or not r["fusion"]:
        raise SystemExit(f"FAILED: missing results {missing} fusion={bool(r['fusion'])}")
    print(f"\nSMOKE TEST PASSED -> {res / 'results' / 'RESULTS.md'} (numbers are synthetic, do not report)")


if __name__ == "__main__":
    main()
