"""Validate converted NPZ contracts and leakage groups before Kaggle training."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


META_KEYS = {"features", "feat_mean", "feat_std", "band_mean", "band_std"}


def validate(path: Path) -> dict:
    issues, warnings = [], []
    data = np.load(path, allow_pickle=True)
    keys = set(data.files)
    if {"Z", "t", "rain", "static", "label"} <= keys:
        kind, row_key, target_key = "geo", "label", "label"
    elif "X" in keys:
        kind, row_key, target_key = "telemetry", "X", "y"
    elif "images" in keys and data["images"].ndim == 5:
        kind, row_key, target_key = "fire", "images", "labels"
    elif "images" in keys and data["images"].ndim == 4:
        is_eo = "band_mean" in keys or data["images"].shape[1] != 3 or path.stem.startswith(("l4s", "s1f", "heph"))
        kind, row_key, target_key = ("eo" if is_eo else "deepfake"), "images", "labels"
    else:
        return {"path": str(path), "kind": "unknown", "valid": False, "issues": ["unrecognized contract"]}
    n = len(data[row_key])
    required = {
        "geo": {"Z", "t", "rain", "static", "label", "lat", "lon"},
        "telemetry": {"X", "y", "block"},
        "fire": {"images", "labels", "block"},
        "deepfake": {"images", "labels", "block"},
        "eo": {"images", "labels", "block"},
    }[kind]
    missing = sorted(required - keys)
    if missing:
        issues.append("missing keys: " + ", ".join(missing))
    for key in keys - META_KEYS:
        value = data[key]
        if value.ndim and len(value) != n:
            issues.append(f"row mismatch {key}={len(value)} vs {n}")
    numeric_keys = [key for key in keys if data[key].dtype.kind in "fiu" and key not in META_KEYS]
    for key in numeric_keys:
        if not np.isfinite(data[key]).all():
            issues.append(f"non-finite values in {key}")
    if kind == "fire" and (data["labels"].ndim != 2 or data["labels"].shape[1] != 2):
        issues.append("fire labels must be (N,2)")
    if kind == "eo" and "band_mean" not in keys and not path.stem.endswith("_test"):
        warnings.append("EO normalization metadata absent")
    groups = len(set(map(str, data["block"]))) if "block" in keys else None
    leaks = []
    if {"block", "split"} <= keys:
        assignments = {}
        for group, split in zip(data["block"], data["split"]):
            assignments.setdefault(str(group), set()).add(str(split))
        leaks = sorted(group for group, splits in assignments.items() if len(splits) > 1)
        if leaks:
            issues.append(f"{len(leaks)} groups occur in multiple splits")
    target = data[target_key] if target_key in keys else np.array([])
    return {
        "path": str(path),
        "kind": kind,
        "rows": n,
        "groups": groups,
        "positive_fraction": float(np.asarray(target).mean()) if target.size else None,
        "split_counts": {
            str(split): int((data["split"].astype(str) == str(split)).sum())
            for split in sorted(set(data["split"].astype(str)))
        } if "split" in keys else {},
        "valid": not issues,
        "issues": issues,
        "warnings": warnings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="/kaggle/working/npz")
    parser.add_argument("--report", default="/kaggle/working/ready_pack_report.json")
    args = parser.parse_args(argv)
    paths = sorted(Path(args.data).glob("*.npz"))
    reports = [validate(path) for path in paths]
    summary = {
        "data_dir": args.data,
        "files": len(reports),
        "valid": sum(report["valid"] for report in reports),
        "invalid": sum(not report["valid"] for report in reports),
        "reports": reports,
    }
    Path(args.report).write_text(json.dumps(summary, indent=2) + "\n")
    for report in reports:
        print(f"[{'OK' if report['valid'] else 'FAIL'}] {Path(report['path']).name}: {report.get('kind')} n={report.get('rows')}")
        for issue in report.get("issues", []):
            print("  -", issue)
    if not paths:
        print("[FAIL] no NPZ files found")
        return 2
    return 0 if not summary["invalid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
