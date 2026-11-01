"""Focused smoke tests for TPD profiling and index conversion."""
from __future__ import annotations

import csv
import hashlib
import tempfile
from pathlib import Path

import build_tpd_index
import profile_tables


def main():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        source = root / "geo.csv"
        fields = ["event_id", "lat", "lon", "day", "label", "dfs"]
        rows = [
            {"event_id": "1", "lat": "30.01", "lon": "79.01", "day": "2020-07-01", "label": "1", "dfs": "0.1"},
            {"event_id": "1", "lat": "30.01", "lon": "79.01", "day": "2019-07-01", "label": "0", "dfs": "0.0"},
            {"event_id": "2", "lat": "30.25", "lon": "79.25", "day": "2020-08-01", "label": "1", "dfs": ""},
        ]
        with source.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        report = profile_tables.profile(source)
        assert report["rows"] == 3 and report["columns"] == 6
        assert report["column_profile"]["dfs"]["missing"] == 1
        target = root / "tpd.csv"
        args = ["--geo", str(source), "--out", str(target)]
        build_tpd_index.main(args)
        first = hashlib.sha256(target.read_bytes()).hexdigest()
        build_tpd_index.main(args)
        assert hashlib.sha256(target.read_bytes()).hexdigest() == first
        indexed = list(csv.DictReader(target.open()))
        assert len(indexed) == 3
        assert len({row["group_id"] for row in indexed}) == 2
        assert all(row["synthetic"] == "0" for row in indexed)
    print("TPD TESTS PASSED")


if __name__ == "__main__":
    main()
