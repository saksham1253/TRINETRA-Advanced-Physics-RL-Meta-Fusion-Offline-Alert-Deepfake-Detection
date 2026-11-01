"""Precompute the Last-Mile alert planner for every toggle combination (single source of truth = ws3_alert/last_mile.py).

Writes public/anim/data/last_mile.js (window.LAST_MILE) and TRINETRA/results/last_mile_demo.json.
Run: python3 TRINETRA/ANIM/tools/extract_last_mile.py   (stdlib only; layout is SYNTHETIC)
"""
import importlib.util, itertools, json, sys
from dataclasses import asdict, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("last_mile", ROOT / "TRINETRA/trinetra/src/trinetra/ws3_alert/last_mile.py")
lm = importlib.util.module_from_spec(spec); sys.modules["last_mile"] = lm; spec.loader.exec_module(lm)

V, N = lm.demo_valley(); P = lm.Params()
base_cond = lm.Conditions()
upgrades = lm.greedy_upgrades(V, N, base_cond, P, k=3)
up_ids = {u["village"] for u in upgrades}
TOGGLES = ["satellite", "cell", "fm", "fail_R1", "fail_R2", "upgrades"]
combos = {}
for bits in itertools.product([0, 1], repeat=len(TOGGLES)):
    t = dict(zip(TOGGLES, bits))
    cond = lm.Conditions(satellite=bool(t["satellite"]), cell=bool(t["cell"]), fm=bool(t["fm"]))
    vs = [replace(v, has_pager=v.has_pager or (t["upgrades"] and v.id in up_ids)) for v in V]
    dis = {n for n, k in (("R1-ridge", "fail_R1"), ("R2-ridge", "fail_R2")) if t[k]}
    res = lm.plan(vs, N, cond, P, disabled=dis)
    combos["".join(map(str, bits))] = {
        "villages": [{"id": r.id, "min": None if r.minutes is None else round(r.minutes, 2), "ch": r.channel, "path": r.path,
                      "n": r.channels_available} for r in res],
        "summary": lm.summary(res, P.deadline_min),
        "mesh_unreachable": lm.mesh_unreachable(vs, N, cond, P, dis)}
out = {
    "generated_by": "TRINETRA/ANIM/tools/extract_last_mile.py", "origin": "ILLUSTRATIVE",
    "note": "SYNTHETIC valley layout; planning physics (Semtech airtime, log-distance link budget, siren attenuation) with assumed terrain exponents. Not a field result.",
    "params": asdict(P), "toggles": TOGGLES,
    "physics": {"airtime_ms": round(lm.lora_airtime_s(P.payload_bytes, P.sf) * 1000, 1),
                "range_km": {t: round(min(lm.lora_range_km(P.sf, t), P.max_hop_km), 2) for t in lm.TERRAIN_N},
                "siren_radius_m": round(lm.siren_radius_m(alpha_db_per_m=P.siren_alpha_db_per_m, contour_db=P.siren_contour_db)),
                "bluetooth_range_m": 100},
    "villages": [asdict(v) for v in V], "nodes": [asdict(n) for n in N],
    "upgrades": upgrades, "spof": lm.single_points_of_failure(V, N, base_cond, P), "combos": combos}
(ROOT / "public/anim/data/last_mile.js").write_text("window.LAST_MILE = " + json.dumps(out, separators=(",", ":")) + ";\n")
(ROOT / "TRINETRA/results/last_mile_demo.json").write_text(json.dumps({k: out[k] for k in out if k != "combos"} | {
    "baseline_internet_cell_off": combos["100000"], "satellite_off_R1_failed": combos["000100"],
    "with_upgrades": combos["100001"]}, indent=1))
print(json.dumps({k: combos[k]["summary"]["share_population_by_deadline"] for k in ("100000", "000000", "000100", "100001", "111001")}))
print("spof", out["spof"], "upgrades", upgrades, "unreach", combos["100000"]["mesh_unreachable"], out["physics"])
