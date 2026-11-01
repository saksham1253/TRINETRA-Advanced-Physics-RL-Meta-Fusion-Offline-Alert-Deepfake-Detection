"""Synthetic tests for archive staging, discovery and ready-pack validation."""
from __future__ import annotations

import json
import tempfile
import zipfile
from pathlib import Path

import stage_kaggle_archives as stage

try:
    import numpy as np
    import validate_ready_pack as ready
except ModuleNotFoundError:
    np = ready = None


def main():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        source = root / "input"; source.mkdir()
        archive = source / "team-pack.zip"
        with zipfile.ZipFile(archive, "w") as out:
            out.writestr("dfire/data.yaml", "names: [smoke, fire]\n")
            out.writestr("deep/Training/fire/a.jpg", "")
            out.writestr("deep/Training/nofire/b.jpg", "")
            out.writestr("cifake/train/REAL/a.png", "")
            out.writestr("cifake/train/FAKE/b.png", "")
            out.writestr("weather/fogsmog/a.jpg", "")
            out.writestr("weather/sandstorm/a.jpg", "")
            out.writestr("weather/lightning/a.jpg", "")
            out.writestr("weather/rain/a.jpg", "")
            out.writestr("rain/labeled_cloudburst_imerg.csv", "rain,label\n10,0\n")
            out.writestr("worldcover/ESA_WorldCover_10m.tif", "")
            out.writestr("Avenue Dataset/training_videos/01.avi", "")
            out.writestr("Avenue Dataset/testing_videos/01.avi", "")
        work, env, report = root / "work", root / "env.sh", root / "inventory.json"
        stage.main(["--input", str(source), "--work", str(work), "--env-out", str(env), "--report", str(report)])
        inventory = json.loads(report.read_text())
        assert not inventory["missing_core"], inventory
        assert {"DFIRE", "DEEPFIRE", "WEATHER", "CIFAKE"} <= set(inventory["datasets"])
        assert {"IMERG_CSV", "LULC_ROOT"} <= set(inventory["datasets"])
        assert "AVENUE" in inventory["datasets"]
        unsafe = source / "unsafe.zip"
        with zipfile.ZipFile(unsafe, "w") as out:
            out.writestr("../escape.txt", "no")
        try:
            stage.extract_archive(unsafe, root / "unsafe", 1000, 10)
            raise AssertionError("unsafe path accepted")
        except ValueError:
            pass

        if np is not None:
            data = root / "npz"; data.mkdir()
            images = np.zeros((4, 1, 3, 8, 8), np.float32)
            np.savez_compressed(
                data / "fire.npz", images=images, labels=np.array([[1, 0], [0, 1], [0, 0], [1, 1]], np.float32),
                block=np.array(["a", "b", "c", "d"]), split=np.array(["train", "train", "val", "test"]),
            )
            validation = ready.validate(data / "fire.npz")
            assert validation["valid"] and validation["kind"] == "fire"
            print("READY-PACK VALIDATOR TEST PASSED")
        else:
            print("READY-PACK VALIDATOR TEST SKIPPED: NumPy unavailable (run on Kaggle)")
    print("KAGGLE ARCHIVE PREP TESTS PASSED")


if __name__ == "__main__":
    main()
