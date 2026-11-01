"""Build the materialized TPD-0.1 master index from the real geo event table."""
from __future__ import annotations

import argparse
import csv
import hashlib
import math
from pathlib import Path


FIELDS = [
    "sample_id", "module", "modality", "source_dataset_id", "source_sample_id",
    "relative_uri", "raw_label", "unified_label", "hazard_type", "group_id",
    "split", "split_seed", "license", "provenance_hash", "provenance_class",
    "synthetic", "derived", "own_captured", "quality_flags", "notes",
]


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--geo", default="results/geo_large/geo_events.csv")
    parser.add_argument("--out", default="data_manifests/tpd_index.csv")
    parser.add_argument("--cell-deg", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)
    source, target = Path(args.geo), Path(args.out)
    with source.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    output = []
    for index, row in enumerate(rows):
        label = int(float(row["label"]))
        lat, lon = float(row["lat"]), float(row["lon"])
        block = f"{math.floor(lat / args.cell_deg)}_{math.floor(lon / args.cell_deg)}"
        canonical = "|".join(row.get(key, "") for key in sorted(row))
        output.append({
            "sample_id": f"tpd01-geo-{index:04d}",
            "module": "geohazard",
            "modality": "tabular_geo_weather",
            "source_dataset_id": "P38+P39+P42",
            "source_sample_id": f"{row['event_id']}:{row['day']}",
            "relative_uri": f"{source.as_posix()}#row={index + 2}",
            "raw_label": str(label),
            "unified_label": "landslide_event" if label else "no_catalog_event_control",
            "hazard_type": "landslide",
            "group_id": block,
            "split": "spatial_cv_oof",
            "split_seed": str(args.seed),
            "license": "mixed-open; verify source terms before redistribution",
            "provenance_hash": hashlib.sha256(canonical.encode()).hexdigest(),
            "provenance_class": "SOURCE+DERIVED",
            "synthetic": "0",
            "derived": "1",
            "own_captured": "0",
            "quality_flags": "case_control;artificial_prevalence;soil_parameters_assumed",
            "notes": "Real catalog/rain/DEM inputs; controls and physics columns are derived.",
        })
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    target.with_suffix(target.suffix + ".sha256").write_text(f"{digest}  {target.as_posix()}\n")
    print(f"[tpd] rows={len(output)} groups={len({row['group_id'] for row in output})} out={target}")


if __name__ == "__main__":
    main()
