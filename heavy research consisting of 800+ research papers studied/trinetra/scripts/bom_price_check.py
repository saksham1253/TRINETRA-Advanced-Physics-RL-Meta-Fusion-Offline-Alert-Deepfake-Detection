"""scripts/bom_price_check.py — node BOM budget gate (constraint C2 / gate G5). Run standalone.

Validates each node's bill-of-materials total against the <= Rs 2000 budget. Prices here are PLACEHOLDER
estimates and MUST be re-verified against live supplier quotes before any G5 sign-off (honesty note). Exits
non-zero if any node exceeds budget.
"""
from __future__ import annotations

import sys

BUDGET_INR = 2000.0

# Placeholder INR estimates — re-verify with supplier quotes [price-verify].
BOMS = {
    "slope_sentinel": {
        "ESP32-C3 module": 180, "SX1262 LoRa module": 320, "MEMS tilt sensor x2": 240,
        "capacitive soil moisture x2": 120, "piezo/geophone": 150, "tipping-bucket rain": 260,
        "temp sensor": 40, "18650 Li-ion + holder": 180, "small PV panel": 150,
        "enclosure + misc": 180,
    },
    "river_eye": {
        "ESP32-CAM module": 420, "SX1262 LoRa module": 320, "ultrasonic level sensor": 300,
        "18650 Li-ion + holder": 180, "small PV panel": 150, "enclosure + misc": 180,
    },
}


def main() -> int:
    failed = False
    for node, items in BOMS.items():
        total = sum(items.values())
        ok = total <= BUDGET_INR
        failed = failed or not ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {node}: Rs {total} / {BUDGET_INR:.0f}")
    print("-" * 50)
    if failed:
        print("BOM GATE FAILED (a node exceeds Rs2000)")
        return 1
    print("BOM GATE PASSED (placeholder prices; re-verify with supplier quotes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
