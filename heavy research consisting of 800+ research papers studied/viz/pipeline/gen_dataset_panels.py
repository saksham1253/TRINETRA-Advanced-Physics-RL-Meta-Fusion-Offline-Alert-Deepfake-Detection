#!/usr/bin/env python
"""viz/pipeline/gen_dataset_panels.py — L8 dataset panels, parsed verbatim from DATASETS.md.

Honesty contract: numbers/licenses/status are copied EXACTLY from the registry table (no rounding, no
inference). The verification tag ([V]/[V*]/[D]) and STATUS (selected/candidate/rejected) are preserved so
the visualization mirrors the docs' honesty (candidates are NOT shown as downloaded/owned data).

Run: python viz/pipeline/gen_dataset_panels.py
Writes: viz/render/public/data/l8_datasets.json
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(WORKSPACE, "DATASETS.md")
OUT = os.path.join(WORKSPACE, "viz", "render", "public", "data", "l8_datasets.json")

HEADERS = ["id", "name", "ws", "link", "cost", "license", "access", "size_n", "kaggle_hf", "status", "ver"]


def parse_quick_links(text: str):
    rows = []
    in_table = False
    for line in text.splitlines():
        if line.startswith("## QUICK LINKS"):
            in_table = True
            continue
        if in_table and line.startswith("## FULL ENTRIES"):
            break
        if not in_table:
            continue
        # a data row looks like: | D01 | Name | WS1/WS8 | http... | ... |
        if re.match(r"^\|\s*D\d+\s*\|", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= len(HEADERS):
                cells = cells[: len(HEADERS)]
                rows.append(dict(zip(HEADERS, cells)))
    return rows


def main():
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    rows = parse_quick_links(text)

    # group by primary workstream token (first WS listed) for the 3D panel layout
    groups: dict[str, list] = {}
    for r in rows:
        ws_primary = r["ws"].split("/")[0].strip() or "misc"
        groups.setdefault(ws_primary, []).append(r)

    status_counts: dict[str, int] = {}
    ver_counts: dict[str, int] = {}
    for r in rows:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
        ver_counts[r["ver"]] = ver_counts.get(r["ver"], 0) + 1

    doc = {
        "provenance": {
            "layer": "L8 — dataset registry",
            "kind": "REAL(metadata) / ILLUSTRATIVE(panel geometry)",
            "origin": "Parsed VERBATIM from DATASETS.md QUICK LINKS table (no inference).",
            "disclaimer": "Counts/licenses/status copied exactly from the registry. [V]=verified, "
                          "[V*]=one fact unverified, [D]=discovery-only. 'candidate' datasets are NOT "
                          "downloaded or owned — shown honestly as registry entries, not as held data.",
            "source_file": "DATASETS.md",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "generator": "viz/pipeline/gen_dataset_panels.py",
        },
        "counts": {"total_in_quick_links": len(rows), "by_status": status_counts, "by_verification": ver_counts},
        "groups": [{"workstream": ws, "datasets": ds} for ws, ds in sorted(groups.items())],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
    print("wrote", OUT)
    print(f"  parsed {len(rows)} dataset rows from QUICK LINKS")
    print(f"  by status: {status_counts}")
    print(f"  by verification: {ver_counts}")


if __name__ == "__main__":
    main()
