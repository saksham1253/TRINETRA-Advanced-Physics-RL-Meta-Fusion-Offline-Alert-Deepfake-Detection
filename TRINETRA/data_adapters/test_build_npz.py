"""Smoke test for build_npz.py on SYNTHETIC files (no real data). Run: python data_adapters/test_build_npz.py
Needs numpy + pillow. Checks: contracts, group-safe splits, near-duplicate grouping, iot sessions."""
import csv
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_npz as B  # noqa: E402


def _img(path, seed, dup_of=None):
    from PIL import Image
    rng = np.random.default_rng(seed)
    if dup_of is None:  # smooth random blobs (realistic for camera frames; noise would not survive JPEG)
        yy, xx = np.mgrid[0:40, 0:40]
        cx, cy, r = rng.uniform(5, 35, 3)
        blob = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * (3 + r) ** 2))
        arr = (np.stack([blob, blob * rng.random(), 1 - blob], -1) * 255).astype("uint8")
    else:
        arr = dup_of
    Image.fromarray(arr).save(path)
    return arr


def main():
    tmp = Path(tempfile.mkdtemp())
    # folder dataset with 2 classes + a near-duplicate pair
    for cls in ("fire_images", "non_fire_images"):
        (tmp / "ds" / cls).mkdir(parents=True)
    base = _img(tmp / "ds/fire_images/WEB001.jpg", 1)
    _img(tmp / "ds/fire_images/WEB002.png", 0, dup_of=base)          # exact duplicate -> same group
    for k in range(8):
        _img(tmp / f"ds/fire_images/vid7_frame{k:03d}.jpg", 10 + k)   # one video -> one group
        _img(tmp / f"ds/non_fire_images/img_{k:03d}x.jpg", 50 + k)
    out = tmp / "fire.npz"
    B.main(["folder", "--root", str(tmp / "ds"), "--map", "fire_images=fire", "non_fire_images=none",
            "--task", "fire", "--size", "32", "--out", str(out), "--manifest", str(tmp / "m.csv")])
    d = np.load(out, allow_pickle=True)
    assert d["images"].shape[1:] == (1, 3, 32, 32), d["images"].shape
    assert d["labels"].shape[1] == 2
    blk = dict(zip([r["path"].split("/")[-1] for r in csv.DictReader(open(tmp / "m.csv"))], d["block"]))
    assert blk["WEB001.jpg"] == blk["WEB002.png"], "near-duplicates must share a group"
    assert len({blk[f"vid7_frame{k:03d}.jpg"] for k in range(8)}) == 1, "video frames must share a group"
    assert B.check(type("A", (), {"npz": str(out)})) == 0

    # iot csv with two sessions (counter reset)
    rows = [{"": i, "UTC": 1000 + i, "Temperature[C]": 20 + i % 3, "Humidity[%]": 50, "CNT": i % 50,
             "Fire Alarm": int(i % 50 > 40)} for i in range(100)]
    with open(tmp / "iot.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    B.main(["iot", "--csv", str(tmp / "iot.csv"), "--window", "10", "--stride", "5", "--out", str(tmp / "t.npz")])
    t = np.load(tmp / "t.npz", allow_pickle=True)
    assert t["X"].shape[1:] == (2, 10) and len(set(t["block"])) == 2
    assert B.check(type("A", (), {"npz": str(tmp / "t.npz")})) == 0
    print("ALL ADAPTER TESTS PASSED")


if __name__ == "__main__":
    main()


def test_new_features():
    """aug/seq grouping, yolo --classes auto, dedupe, video (needs opencv)."""
    import tempfile
    from PIL import Image
    t = Path(tempfile.mkdtemp())
    assert B.group_key_from_name("fake_12_aug_3.jpg") == B.group_key_from_name("fake_12_aug_7.jpg")
    B.SEQ_BUCKET = 50
    assert B.group_key_from_name("AoF06701.jpg") == B.group_key_from_name("AoF06720.jpg") != B.group_key_from_name("AoF06760.jpg")
    B.SEQ_BUCKET = 0
    # yolo with data.yaml (names: ['smoke','fire'] like D-Fire style)
    (t / "y/data/train/images").mkdir(parents=True); (t / "y/data/train/labels").mkdir(parents=True)
    (t / "y/data.yaml").write_text("train: x\nnc: 2\nnames: ['smoke', 'fire']\n")
    for i in range(6):
        _img(t / f"y/data/train/images/AoF{i:05d}.jpg", 100 + i)
        (t / f"y/data/train/labels/AoF{i:05d}.txt").write_text("1 0.5 0.5 0.2 0.2\n" if i % 2 else "0 0.5 0.5 0.2 0.2\n")
    B.main(["yolo", "--root", str(t / "y"), "--classes", "auto", "--size", "32", "--out", str(t / "y.npz"), "--seq-bucket", "50"])
    d = np.load(t / "y.npz", allow_pickle=True)
    assert d["labels"].sum(0).tolist() == [3.0, 3.0], d["labels"]          # 3 fire, 3 smoke
    assert len(set(d["block"])) == 1                                         # one camera bucket
    # dedupe: test == train -> everything removed
    B.main(["dedupe", "--train", str(t / "y.npz"), "--test", str(t / "y.npz"), "--out", str(t / "dd.npz")])
    assert len(np.load(t / "dd.npz", allow_pickle=True)["block"]) == 0
    try:
        import cv2
    except ImportError:
        print("[skip] opencv missing -> video test skipped"); return
    for cls in ("fire/pos", "fire/neg"):
        (t / "v" / cls).mkdir(parents=True)
        w = cv2.VideoWriter(str(t / "v" / cls / "clip1.avi"), cv2.VideoWriter_fourcc(*"MJPG"), 10, (48, 48))
        for k in range(40):
            w.write(np.full((48, 48, 3), (k * 5) % 255, np.uint8))
        w.release()
    B.main(["video", "--root", str(t / "v"), "--map", "fire/pos=fire", "fire/neg=none", "--every", "2", "--clip", "4",
            "--size", "32", "--out", str(t / "v.npz")])
    v = np.load(t / "v.npz", allow_pickle=True)
    assert v["images"].shape[1:] == (4, 3, 32, 32) and len(set(v["block"])) == 2, v["images"].shape
    print("NEW FEATURE TESTS PASSED")


if __name__ == "__main__":
    test_new_features()
