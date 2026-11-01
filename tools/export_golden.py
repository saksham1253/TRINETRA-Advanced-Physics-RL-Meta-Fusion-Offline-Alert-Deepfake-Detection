"""Golden input/output pairs from the TRINETRA Python code for the TypeScript ports (src/console/engine).

Every ported formula is evaluated here with fixed inputs; tests in src/console/engine/__tests__/golden.test.ts assert the TS
results match within 1e-9 relative (1e-6 for iterative ones). A mismatch is a blocker.
Run: python3 tools/export_golden.py
"""
import json, sys
from pathlib import Path
sys.path.insert(0, "TRINETRA/trinetra/src")
from trinetra.ws1a_firephys.established_ef import (flame_height_heskestad, strouhal_puffing_frequency, plume_centerline_dT,
                                                     byram_convection_number, beer_lambert_transmittance)
from trinetra.ws1a_firephys.gate import fire_gate, FireInputs
from trinetra.ws1a_firephys.novel_nd import nd1_dealiased_flicker, aliased_frequency
from trinetra.ws1b_geophys.fs import factor_of_safety
from trinetra.ws1b_geophys.iverson import pressure_head, ierfc, transient_head_multipulse
from trinetra.ws1b_geophys.caine import caine_exceedance
from trinetra.ws1b_geophys.gate import geo_gate, GeoInputs
from trinetra.ws5_fusion_rl.nf import effective_weight, nf1_consistency, nf3_conflict_to_uncertainty, nf4_salience, weighted_dispersion
from trinetra.ws5_fusion_rl.fusion_models import fm1_precision_weighted, fuse
from trinetra.ws5_fusion_rl.pharaoh import pharaoh_fuse
from trinetra.ws5_fusion_rl.gmf import gmf_fuse
from trinetra.ws5_fusion_rl.decision import conformal_level, decide
from trinetra.ws5_fusion_rl.shield import shield_floor, ShieldSignals
from trinetra.common.types import ExpertOutput, PhysicsClass
from trinetra.common.config import Config
from trinetra.ws3_alert import last_mile as lm

G = {}
G["heskestad"] = [[q, d, flame_height_heskestad(q, d)] for q, d in [(100, 0.5), (2000, 3), (50000, 10)]]
G["strouhal"] = [[d, strouhal_puffing_frequency(d)] for d in (0.3, 1, 3, 30)]
G["plume_dT"] = [[q, z, plume_centerline_dT(q, z)] for q, z in [(500, 5), (2000, 10), (20000, 40)]]
G["byram"] = [[q, u, byram_convection_number(q, u)] for q, u in [(800, 4), (50, 10), (5000, 1)]]
G["beer"] = [[k, l, beer_lambert_transmittance(k, l)] for k, l in [(0.1, 5), (1.2, 2)]]
G["aliased"] = [[f, fs, aliased_frequency(f, fs)] for f, fs in [(2.0, 5.0), (0.87, 1.0), (7.3, 3.0)]]
G["nd1"] = [[fo, fs, d, nd1_dealiased_flicker(fo, fs, d).consistency] for fo, fs, d in [(0.5, 2.0, 3.0), (1.1, 5.0, 1.0)]]
fg = []
for conf, q, u, mn in [(0.8, 800, 4, False), (0.6, 50, 10, True), (0.9, None, None, False)]:
    r = fire_gate(FireInputs(detector_conf=conf, multi_node_agree=mn, Q_c_kW_per_m=q, wind_U_ms=u))
    fg.append([conf, q, u, mn, r.p_fire, r.consistency, r.expert.u])
G["fire_gate"] = fg
G["fs"] = [[c, phi, g, z, b, uw, ss, float(factor_of_safety(c, phi, g, z, b, uw, ss))] for c, phi, g, z, b, uw, ss in
           [(5, 32, 19, 2, 35, 0, 0), (8.3, 32, 19, 2, 39.6, 9.81, 0), (2, 30, 18, 3, 30, 15, 4)]]
G["ierfc"] = [[x, float(ierfc(x))] for x in (0.0, 0.3, 1.0, 2.5)]
G["pressure_head"] = [[Z, t, D0, K, I, b, float(pressure_head(Z, t, D0, K, I, b))] for Z, t, D0, K, I, b in
                      [(2, 24, 4.32, 1e-2, 5e-3, 35), (1.5, 6, 1.0, 1e-3, 1e-3, 20)]]
G["multipulse"] = [[Z, t, [list(x) for x in st], D0, K, b, float(transient_head_multipulse(Z, t, [x[0] for x in st], [x[1] for x in st], D0, K, b))]
                   for Z, t, st, D0, K, b in [(2.0, 5.0, [(0, 0.004), (1.5, 0.028), (3.5, 0.012)], 4.32, 0.036, 38),
                                              (1.0, 2.0, [(0, 0.01), (1.0, 0.0)], 1.0, 0.02, 30)]]
G["caine"] = [[I, D, float(caine_exceedance(I, D, 14.0, 0.39)[1])] for I, D in [(5, 24), (1, 216), (30, 2)]]
gg = []
for kw in [dict(c_prime=5, phi_prime_deg=32, gamma=19, z=2, beta_deg=35, u_w=0, I_mm_h=5, D_hours=24),
           dict(c_prime=8.3, phi_prime_deg=32, gamma=19, z=2, beta_deg=39.6, D0=4.32, K_z=1e-2, I_z=5e-3, t_hours=24, I_mm_h=1.03, D_hours=216)]:
    r = geo_gate(GeoInputs(**kw)); gg.append([kw, r.FS, r.caine_ratio, r.p_phys, r.expert.u, r.expert.c])
G["geo_gate"] = gg
EXP = [dict(p=0.82, source="fire_cnn", u=0.3, c=0.9, r=0.8), dict(p=0.97, source="zeroshot", u=0.1, c=1.0, r=0.4),
       dict(p=0.4, source="clip_probe", u=0.5, c=0.7, r=0.75), dict(p=0.05, source="iot", u=0.2, c=1.0, r=0.8, available=False)]
ex = [ExpertOutput(**e) for e in EXP]
av = [e for e in ex if e.available]
ws = [effective_weight(e, 0.5) for e in av]
G["fusion"] = {"experts": EXP, "eff_w": [effective_weight(e, t) for e in ex for t in (0.2, 0.5, 1.0)],
               "fm1": [fm1_precision_weighted(ex, t) for t in (0.2, 0.5, 1.0)],
               "nf3": [nf3_conflict_to_uncertainty([e.p for e in av], [e.u for e in av], ws, lam) for lam in (0.0, 0.3, 1.0)],
               "nf4": nf4_salience(ex), "disp": weighted_dispersion([e.p for e in av], ws),
               "nf1": [nf1_consistency(p, phi, s) for p, phi, s in [(0.9, 0.4, 0.25), (0.3, 0.4, 0.25), (0.7, 0.2, 0.1)]],
               "pharaoh": [pharaoh_fuse(ex, k)["p"] for k in (0.0, 2.0, 6.0)],
               "pharaoh_rho": [pharaoh_fuse(ex, k)["rho"] for k in (0.0, 2.0, 6.0)],
               "gmf": gmf_fuse(ex, 0.5).p, "gmf_pharaoh": gmf_fuse(ex, 0.5, use_pharaoh_base=True).p}
ps = 5 / 105
G["conformal"] = [[r, conformal_level(r, ps).name] for r in (0.01, 0.05, 0.2, 0.3, 0.6, 0.99)]
sh = []
for kw in [dict(FS=0.9), dict(tilt_rate_deg_per_day=6, nodes_agree=2), dict(tilt_rate_deg_per_day=6, nodes_agree=1),
           dict(rain_24h_mm=160, high_susceptibility=True), dict(glof_lake_drop=True, downstream_stage_jump=True), dict(fire_multi_node=True), {}]:
    sh.append([kw, shield_floor(ShieldSignals(**kw)).floor.name])
G["shield"] = sh
dec = []
for kw, tau, pharaoh in [({}, 0.5, False), ({"fire_multi_node": True}, 0.5, False), ({}, 0.2, True)]:
    cfg = Config(); cfg.data["fusion"]["tau"] = tau; cfg.data["fusion"]["operator"]["pharaoh"] = pharaoh
    d = decide(ex, ShieldSignals(**kw), cfg)
    dec.append([kw, tau, pharaoh, d.level.name, d.risk, d.uncertain, d.conformal.reliability.value, d.conformal.pred_set,
                fuse(ex, cfg).u_star])
G["decide"] = dec
G["airtime"] = [[n, sf, lm.lora_airtime_s(n, sf)] for n, sf in [(24, 7), (24, 10), (24, 12), (51, 9), (10, 11)]]
G["fspl"] = [[d, lm.fspl_db(d)] for d in (1, 1000, 15000)]
G["range"] = [[sf, t, lm.lora_range_km(sf, t)] for sf, t in [(7, "ridge_los"), (10, "hill_forest"), (12, "valley_nlos")]]
G["siren"] = [[a, c, lm.siren_radius_m(alpha_db_per_m=a, contour_db=c)] for a, c in [(0.01, 70), (0.02, 60)]]
V, N = lm.demo_valley()
cond = lm.Conditions(); par = lm.Params()
G["last_mile"] = {"villages": [vars(v) for v in V], "nodes": [vars(n) for n in N],
                  "plan": [[r.id, r.minutes, r.channel, r.path] for r in lm.plan(V, N, cond, par)],
                  "plan_no_R1": [[r.id, r.minutes, r.channel] for r in lm.plan(V, N, cond, par, disabled={"R1-ridge"})],
                  "plan_sf7": [[r.id, r.minutes, r.channel] for r in lm.plan(V, N, cond, lm.Params(sf=7))]}
Path("src/console/engine/__tests__/golden.json").write_text(json.dumps(G, indent=0, default=float))
print({k: (len(v) if isinstance(v, list) else "obj") for k, v in G.items()})
