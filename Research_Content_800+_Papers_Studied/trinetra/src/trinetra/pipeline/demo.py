"""End-to-end advisory demo (synthetic). Run:  python demo.py   (from the trinetra/ root)

Shows the full offline-first advisory path on a Joshimath-like slow landslide scenario:
  readings -> geo physics gate + anomaly -> fusion -> single decision -> shield -> operator -> CAP
plus the cloud-down offline path (local siren + DTN), and an HONEST hindcast report (Rule 16).
Nothing here is a performance claim; it is a wiring demonstration on synthetic data.
"""
from __future__ import annotations

import numpy as np

from ..common.config import Config
from ..common.types import Hazard
from ..ws1b_geophys import GeoInputs, inverse_velocity_fit
from ..ws5_fusion_rl import ShieldSignals
from ..ws3_alert import DTNQueue, SirenBus, present, approve, build_cap
from ..ws7_iot import node_local_edge_flag
from .orchestrator import run_geo_cycle, offline_dispatch
from .hindcast import run_hindcast


def main() -> int:
    cfg = Config()
    print("=" * 78)
    print("TRINETRA / HIMKAVACH — end-to-end ADVISORY demo (synthetic, no performance claims)")
    print("=" * 78)

    # --- Scenario: saturated steep slope, heavy multi-day rain, accelerating creep -----------------
    creep_t = np.array([0, 6, 12, 18, 24, 30, 36])          # hours
    creep_v = np.array([0.2, 0.25, 0.33, 0.5, 0.8, 1.4, 2.6])  # mm/h accelerating
    fk = inverse_velocity_fit(creep_t, creep_v, alpha=2.0)
    print(f"\n[Fukuzono] forecast failure t_f ≈ {fk.t_failure:.1f} h (r2={fk.r2:.3f})")

    gi = GeoInputs(c_prime=4.0, phi_prime_deg=30.0, gamma=19.0, z=2.5, beta_deg=38.0,
                   D0=2e-4, K_z=1e-5, I_z=9e-6, t_hours=24.0, psi_steady=0.3,
                   I_mm_h=22.0, D_hours=18.0, caine_a=cfg.get("geophys.caine_a"),
                   caine_b=cfg.get("geophys.caine_b"), fukuzono=fk, now_hours=24.0)

    # anomaly features: a telemetry window with a late excursion
    rng = np.random.default_rng(0)
    feats = rng.normal(size=(48, 4)); feats[-3:] += 3.0
    series = np.concatenate([rng.normal(0, 0.2, 44), [0.6, 1.1, 1.8, 2.5]])

    shield = ShieldSignals(FS=None, tilt_rate_deg_per_day=6.0, nodes_agree=3,
                           rain_24h_mm=180.0, high_susceptibility=True)

    decision = run_geo_cycle(gi, shield, feats, series=series, cfg=cfg, zone_id="UK-CHX-07")

    print("\n--- OPERATOR BRIEFING -------------------------------------------------------")
    print(present(decision))

    # --- Offline path (cloud down) ---------------------------------------------------------------
    edge = node_local_edge_flag({"tilt_rate_dps": 6.0, "rain_mm_15m": 25.0})
    dtn, siren = DTNQueue(L=8), SirenBus()
    actions = offline_dispatch(decision, edge["level"], dtn, siren)
    print("\n--- OFFLINE PATH (cloud down) -----------------------------------------------")
    print(f"node edge flag = {edge['level']} ({edge['rule']})")
    print(f"siren events   = {[ (e.source,e.level) for e in siren.log ]}")
    print(f"DTN pending    = {dtn.pending()}")
    print(f"note           = {actions.note}")

    # --- Human-gated public alert ----------------------------------------------------------------
    print("\n--- HUMAN-GATED PUBLIC ALERT ------------------------------------------------")
    if decision.level.name != "GREEN":
        token = approve(decision, operator_id="SDMA-UK-14")
        cap = build_cap(decision, approval_token=token, sender="TRINETRA-SDMA-UK",
                        area_polygon=None, key=b"demo-cap-key")
        print(cap[:600] + ("...\n" if len(cap) > 600 else "\n"))
    else:
        print("level GREEN -> no public alert (correct, no action).")

    # --- Honest hindcast report (Rule 16) --------------------------------------------------------
    print("--- HINDCAST (honesty gate) -------------------------------------------------")
    n = 600
    blocks = np.array([f"z{i%20}" for i in range(n)])
    sig = rng.random(n); y = (sig > 0.85).astype(int)
    X = np.column_stack([sig, rng.normal(size=n)])
    # (i) a useless model -> must be reported NOT ADMITTED
    useless = run_hindcast("synthetic-noise-model", X, y, blocks, p_model=rng.random(n))
    print(f"noise model : admitted={useless.report['admitted']}  "
          f"value_scores={ {k: round(v,3) for k,v in useless.value_scores.items()} }")
    # (ii) an informative model -> may be admitted
    good = run_hindcast("synthetic-informative-model", X, y, blocks, p_model=sig)
    print(f"informative : admitted={good.report['admitted']}  "
          f"value_scores={ {k: round(v,3) for k,v in good.value_scores.items()} }")
    print("\nNote: 'admitted' only means it beat baselines on spatial-CV with CI on THIS synthetic data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
