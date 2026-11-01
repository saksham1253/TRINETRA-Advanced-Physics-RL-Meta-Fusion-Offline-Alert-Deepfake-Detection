"""Convenience launcher so `python demo.py` works from the repo root (adds src/ to sys.path)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from trinetra.pipeline.demo import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
