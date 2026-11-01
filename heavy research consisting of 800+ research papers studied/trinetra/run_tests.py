"""Lightweight test runner (pytest is unavailable). Runs stdlib unittest over tests/.

Usage:  python run_tests.py            # all tests
        python run_tests.py pattern    # filter by filename glob (e.g. test_geo*)
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))          # make `trinetra` importable
sys.path.insert(0, str(ROOT))         # make `tests` importable


def main() -> int:
    pattern = sys.argv[1] if len(sys.argv) > 1 else "test_*.py"
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"), pattern=pattern, top_level_dir=str(ROOT))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
