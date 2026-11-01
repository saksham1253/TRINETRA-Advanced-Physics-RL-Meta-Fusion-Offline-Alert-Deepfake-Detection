"""Deterministic CSV/TSV profiler for TPD-0.1 manifests (stdlib only)."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


MISSING = {"", "na", "n/a", "nan", "null", "none", "-999", "-9999"}


def _kind(values: list[str]) -> str:
    nonempty = [v for v in values if v.strip().lower() not in MISSING]
    if not nonempty:
        return "empty"
    try:
        for value in nonempty:
            int(value)
        return "integer"
    except ValueError:
        pass
    try:
        for value in nonempty:
            float(value)
        return "number"
    except ValueError:
        return "string"


def profile(path: Path) -> dict:
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        fields = reader.fieldnames or []
        rows = list(reader)
    columns = {}
    for field in fields:
        values = [(row.get(field) or "").strip() for row in rows]
        kind = _kind(values)
        present = [v for v in values if v.lower() not in MISSING]
        item = {
            "type": kind,
            "missing": len(values) - len(present),
            "unique": len(set(present)),
        }
        if kind in {"integer", "number"} and present:
            numeric = [float(v) for v in present]
            item["min"] = min(numeric)
            item["max"] = max(numeric)
        columns[field] = item
    fingerprints = [
        hashlib.sha256(json.dumps(row, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        for row in rows
    ]
    candidate_groups = [
        field for field in fields
        if any(token in field.lower() for token in ("group", "event", "site", "frame", "video", "camera", "block"))
    ]
    return {
        "path": path.as_posix(),
        "delimiter": "\\t" if delimiter == "\t" else ",",
        "encoding": "utf-8-sig",
        "rows": len(rows),
        "columns": len(fields),
        "field_names": fields,
        "duplicate_rows": len(rows) - len(set(fingerprints)),
        "candidate_group_keys": candidate_groups,
        "column_profile": columns,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--out-dir", default="data_manifests/profiles")
    args = parser.parse_args(argv)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    index = []
    for raw in args.paths:
        path = Path(raw)
        report = profile(path)
        target = out / f"{path.parent.name}_{path.stem}_profile.json"
        target.write_text(json.dumps(report, indent=2) + "\n")
        index.append({"input": path.as_posix(), "profile": target.as_posix(), "rows": report["rows"]})
        print(f"[profile] {path}: {report['rows']} rows, {report['columns']} columns")
    (out / "index.json").write_text(json.dumps(index, indent=2) + "\n")


if __name__ == "__main__":
    main()
