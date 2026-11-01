"""Build src/console/data/params_registry.json from the TRINETRA repo.

Every entry is tied to a repo file and a regex; the line number is RESOLVED from the source each run, so references never
go stale silently. An entry whose pattern is not found is dropped and logged (the UI only shows resolved parameters).
SURROGATE entries (no repo model exists) carry an external citation instead and are marked cls=SURROGATE.
Run: python3 tools/extract_params.py
"""
import json, re, sys
from pathlib import Path

ROOT = Path("TRINETRA/trinetra")
P = []


def p(id, group, label, unit, default, file, pattern, rng, step, cls, module, eq, lower, raise_, *, hard=None, scale="linear",
      regime=None, live=False, kind="number", options=None):
    P.append(dict(id=id, group=group, label=label, unit=unit, default=default, file=file, pattern=pattern, range=rng,
                  hard=hard or rng, step=step, scale=scale, cls=cls, module=module, equation=eq, lower=lower, raise_=raise_,
                  regime=regime, live=live, kind=kind, options=options))


F_EF = "src/trinetra/ws1a_firephys/established_ef.py"; F_FG = "src/trinetra/ws1a_firephys/gate.py"
F_ND = "src/trinetra/ws1a_firephys/novel_nd.py"; F_GG = "src/trinetra/ws1b_geophys/gate.py"
F_NF = "src/trinetra/ws5_fusion_rl/nf.py"; F_PH = "src/trinetra/ws5_fusion_rl/pharaoh.py"
F_GMF = "src/trinetra/ws5_fusion_rl/gmf.py"; F_DEC = "src/trinetra/ws5_fusion_rl/decision.py"
F_SH = "src/trinetra/ws5_fusion_rl/shield.py"; F_AD = "src/trinetra/ws5_fusion_rl/adapters.py"
F_CFG = "src/trinetra/common/config.py"; F_FUS = "configs/fusion.json"; F_DEF = "configs/default.json"
F_CCTV = "src/trinetra/ws4_cctv/__init__.py"; F_LM = "src/trinetra/ws3_alert/last_mile.py"; F_DTN = "src/trinetra/ws3_alert/dtn.py"
F_GMFK = "kaggle/geo_meta_fusion.py"

# ---------------- Fire physics (ws1a, Class A) ----------------
p("fire.Q_kW", "Fire physics", "Heat release rate Q", "kW", 2000, F_EF, r"def flame_height_heskestad", [50, 50000], 50, "A", "fire_phys",
  "L = 0.235 Q^{2/5} - 1.02 D  (Heskestad)", "Smaller flames, lower plume, weaker Byram buoyancy", "Taller flames, stronger plume", scale="log",
  regime="Heskestad correlation is for pool / area fires; very small Q with large D gives negative L (outside regime)")
p("fire.D_m", "Fire physics", "Fire base diameter D", "m", 3.0, F_EF, r"def strouhal_puffing_frequency", [0.3, 30], 0.1, "A", "fire_phys",
  "f = 1.5 D^{-1/2}  (puffing frequency)", "Faster flicker, shorter flame", "Slower flicker, flame height drops by 1.02 per m")
p("fire.Qc_kW_m", "Fire physics", "Convective intensity per front length Q_c", "kW/m", 800, F_EF, r"def byram_convection_number", [10, 20000], 10, "A",
  "fire_phys", "N_c = 2 g Q_c / (rho c_p T_inf U^3)", "Lower N_c: wind-dominated, physics consistency drops", "Higher N_c: plume-dominated",
  scale="log")
p("fire.wind_ms", "Fire physics", "Wind speed U", "m/s", 4.0, F_FG, r"wind_U_ms: float \| None", [0.2, 25], 0.1, "A", "fire_phys",
  "N_c ∝ U^{-3};  c = clip(N_c / 2, 0.3, 1)", "Plume-dominated regime, full consistency", "Wind-dominated regime, consistency falls toward 0.3")
p("fire.T_inf", "Fire physics", "Ambient temperature T_inf", "K", 293, F_EF, r"T_inf: float = 293.0", [260, 325], 1, "A", "fire_phys",
  "ΔT0 = 9.1 (T_inf/(g c_p² ρ²))^{1/3} Q_c^{2/3} (z−z0)^{-5/3}", "Slightly lower plume excess temperature", "Slightly higher plume excess temperature")
p("fire.nc_full", "Fire physics", "Byram N_c for full consistency", "-", 2.0, F_FG, r"c \*= float\(np.clip\(N_c / 2.0, 0.3, 1.0\)\)", [0.5, 5], 0.1,
  "A", "fire_phys", "c = clip(N_c / N_full, c_min, 1)", "Fewer scenes down-weighted", "More scenes treated as wind-dominated")
p("fire.c_min", "Fire physics", "Minimum physics consistency", "-", 0.3, F_FG, r"c \*= float\(np.clip\(N_c / 2.0, 0.3, 1.0\)\)", [0, 1], 0.05, "A",
  "fire_phys", "c = clip(N_c / N_full, c_min, 1)", "Implausible regimes can almost silence the fire expert", "Physics can barely down-weight")
p("fire.u_base", "Fire physics", "Fire gate base uncertainty", "-", 0.15, F_FG, r"u = float\(np.clip\(0.15 \+ 0.4", [0, 0.6], 0.01, "A", "fire_phys",
  "u = 0.15 + 0.4 (1 − c) + u_ND2", "Fire expert gets more weight in fusion", "Fire expert gets less weight (exp(−u/τ))")
p("fire.iot_bonus", "Fire physics", "IoT multi-node consistency bonus", "-", 0.1, F_FG, r"c = float\(np.clip\(c \+ 0.1", [0, 0.5], 0.01, "A", "fire_phys",
  "c ← clip(c + bonus) if ≥2 nodes agree", "Corroboration matters less", "Corroboration matters more")
p("fire.nd1_sigma", "Fire physics", "ND-1 flicker tolerance σ (Class C, default off)", "Hz", 0.3, F_ND, r"sigma_hz: float = 0.3", [0.05, 1.5], 0.05, "C",
  "fire_phys", "consistency = exp(−(f_obs − f_alias)² / 2σ²)", "Stricter flicker match", "Looser flicker match")

# ---------------- Landslide physics (ws1b, Class A) ----------------
p("geo.caine_a", "Landslide physics", "Caine I-D coefficient a", "mm/h", 14.0, F_GG, r"caine_a: float = 14.0", [2, 40], 0.5, "A", "geo_phys",
  "I = a D^{-b}  (Caine 1980)", "Threshold lower: more exceedances", "Threshold higher: fewer exceedances",
  regime="Must be re-fitted locally; the global Caine values are a prior only")
p("geo.caine_b", "Landslide physics", "Caine I-D exponent b", "-", 0.39, F_GG, r"caine_b: float = 0.39", [0.1, 0.9], 0.01, "A", "geo_phys",
  "I = a D^{-b}", "Long rains need more intensity", "Long rains trigger at lower intensity")
p("geo.k_fs", "Landslide physics", "FS-to-probability steepness k", "-", 4.0, F_GG, r"def geo_gate\(gi: GeoInputs, k_fs: float = 4.0\)", [0.5, 12], 0.5,
  "A", "geo_phys", "p_FS = σ(k (1 − FS))", "Soft response around FS = 1", "Sharp switch at FS = 1")
p("geo.lead_h", "Landslide physics", "Fukuzono lead horizon", "h", 48, F_GG, r"lead / 48.0", [6, 240], 1, "A", "geo_phys",
  "p_fk = clip(1 − lead / H) · r²", "Only imminent failures count", "Earlier creep forecasts count")
p("geo.phi", "Landslide physics", "Friction angle φ'", "deg", 32.0, F_GMFK, r"phi_prime_deg=32.0", [20, 45], 0.5, "A", "geo_phys",
  "FS = [c' + (γ z cos²β − u_w) tan φ'] / (γ z sinβ cosβ)", "Lower FS (less stable)", "Higher FS (more stable)")
p("geo.gamma", "Landslide physics", "Soil unit weight γ", "kN/m³", 19.0, F_GMFK, r"gamma=19.0", [15, 22], 0.1, "A", "geo_phys",
  "FS (infinite slope)", "Slightly higher FS", "Slightly lower FS (driving stress grows)")
p("geo.z", "Landslide physics", "Slip-surface depth z", "m", 2.0, F_GMFK, r"z=2.0", [0.5, 6], 0.1, "A", "geo_phys", "FS (infinite slope)",
  "Cohesion dominates: higher FS", "Deeper slip: lower FS")
p("geo.D0", "Landslide physics", "Hydraulic diffusivity D0 (Iverson)", "m²/h", 4.32, "kaggle/run_hackathon.sh", r"--D0 4.32", [0.1, 50], 0.1, "A",
  "geo_phys", "ψ = (I_z/K_z) √(4 D1 t) ierfc(Z/√(4 D1 t)),  D1 = D0 / cos²β", "Slower pore-pressure rise", "Faster pore-pressure rise",
  scale="log")

# ---------------- Fusion (ws5, Class B / C) ----------------
p("fusion.model", "Fusion", "Averaging technique", "", "FM-1", F_FUS, r'"model": "FM-1"', [0, 0], 1, "B", "fusion",
  "FM-1: p = Σ w̃_i p_i / Σ w̃_i", "", "", kind="enum", live=True,
  options=["FM-1", "PHARAOH", "GMF", "STACK", "MEAN", "MEDIAN", "MAX"])
p("fusion.tau", "Fusion", "Uncertainty temperature τ", "-", 0.5, F_FUS, r'"tau": 0.5', [0.05, 2], 0.05, "B", "fusion",
  "w̃_i = r_i c_i exp(−u_i / τ)", "Uncertain experts are suppressed hard", "Uncertainty barely changes weights", live=True)
p("fusion.lambda", "Fusion", "Conflict-to-uncertainty λ (NF-3)", "-", 0.3, F_FUS, r'"lambda": 0.3', [0, 1.5], 0.05, "B", "fusion",
  "U* = Σ w_i u_i + λ D(p)", "Disagreement adds little uncertainty", "Disagreement quickly marks alerts uncertain", live=True)
p("fusion.kappa", "Fusion", "PHARAOH order gain κ (Class C)", "-", 2.0, F_PH, r"def pharaoh_order\(ps, weights, salience: float, kappa: float = 2.0\)",
  [0, 8], 0.1, "C", "fusion", "ρ = 1 + κ D S;  F_ρ = (Σ w_i p_i^ρ)^{1/ρ}", "Closer to the weighted mean", "Bends toward max when a credible alarm exists",
  live=True)
p("fusion.nf1_sigma", "Fusion", "NF-1 physics-consistency σ", "-", 0.25, F_NF, r"sigma: float = 0.25", [0.05, 1], 0.01, "B", "fusion",
  "c_i = exp(−((p_i − φ)_+)² / 2σ²)", "Experts claiming more than physics are penalised hard", "Physics penalty is mild", live=True)
p("fusion.residual_cap", "Fusion", "GMF residual cap", "-", 0.1, F_GMF, r"residual_cap: float = 0.1, head=None\) -> float", [0, 0.3], 0.01, "B",
  "fusion", "p = clip(base + clip(r, ±cap))", "Learned head can barely move the base", "Learned head can move the base more", live=True)
p("trust.fire_cnn", "Fusion", "Reliability r: fire CNN", "-", 0.80, F_AD, r'"fire_cnn":\s+\(0.80, 0.95', [0, 0.95], 0.01, "SYSTEM", "fusion",
  "w̃_i = r_i c_i exp(−u_i/τ),  r ≤ cap 0.95", "Fire CNN counts less", "Fire CNN counts more (capped)", live=True)
p("trust.zeroshot", "Fusion", "Reliability r: CLIP zero-shot", "-", 0.40, F_AD, r'"zeroshot":\s+\(0.40, 0.50', [0, 0.5], 0.01, "SYSTEM", "fusion",
  "r ≤ cap 0.50 (complement only)", "Zero-shot counts less", "Zero-shot counts more (capped)", live=True)
p("trust.clip_probe", "Fusion", "Reliability r: CLIP probe", "-", 0.75, F_AD, r'"clip_probe": \(0.75, 0.90', [0, 0.9], 0.01, "SYSTEM", "fusion",
  "r ≤ cap 0.90", "Probe counts less", "Probe counts more (capped)", live=True)
p("trust.deepfake", "Fusion", "Reliability r: deepfake check", "-", 0.30, F_AD, r'"deepfake":\s+\(0.30, 0.40', [0, 0.4], 0.01, "SYSTEM", "fusion",
  "r ≤ cap 0.40 (low trust, Rule 19)", "Authenticity check counts less", "Authenticity check counts more (capped)", live=True)
p("trust.iot", "Fusion", "Reliability r: IoT smoke/heat", "-", 0.80, F_AD, r'"iot":\s+\(0.80, 0.95', [0, 0.95], 0.01, "SYSTEM", "fusion",
  "r ≤ cap 0.95", "IoT counts less", "IoT counts more (capped)", live=True)

# ---------------- Decision / alerting ----------------
p("cost.C_FA", "Decision", "Cost of a false alarm C_FA", "units", 5.0, F_DEF, r'"C_FA": 5.0', [0.5, 50], 0.5, "SYSTEM", "decision",
  "p* = C_FA / (C_FA + C_miss)", "Lower p*: more alerts", "Higher p*: fewer alerts", live=True)
p("cost.C_miss", "Decision", "Cost of a missed event C_miss", "units", 100.0, F_DEF, r'"C_miss": 100.0', [5, 5000], 5, "SYSTEM", "decision",
  "p* = C_FA / (C_FA + C_miss)", "Higher p*: fewer alerts, more misses", "Lower p*: more alerts, more false alarms", scale="log", live=True)
p("dec.orange_mult", "Decision", "WARNING cut point (× p*)", "×p*", 4.0, F_DEC, r"t_y, t_o, t_r = p_star, 4.0 \* p_star, 10.0 \* p_star", [1.5, 9], 0.1,
  "SYSTEM", "decision", "GREEN < p* ≤ YELLOW < 4p* ≤ ORANGE < 10p* ≤ RED", "More alerts reach WARNING", "Fewer alerts reach WARNING", live=True)
p("dec.red_mult", "Decision", "EMERGENCY cut point (× p*)", "×p*", 10.0, F_DEC, r"t_y, t_o, t_r = p_star, 4.0 \* p_star, 10.0 \* p_star", [4, 20], 0.5,
  "SYSTEM", "decision", "ORANGE < 10p* ≤ RED", "More alerts reach EMERGENCY", "Fewer alerts reach EMERGENCY", live=True)
p("dec.uncertain", "Decision", "Abstain when U* above", "-", 0.6, F_DEC, r"uncertain_threshold: float = 0.6", [0.1, 1], 0.01, "SYSTEM", "decision",
  "uncertain = U* > threshold → escalate to a human", "More alerts flagged for review", "Fewer alerts flagged for review", live=True)
p("shield.tilt", "Decision", "Shield: tilt rate for EMERGENCY", "deg/day", 5.0, F_SH, r"tilt_rate_deg_per_day > 5.0", [1, 20], 0.5, "SYSTEM", "shield",
  "tilt rate > T and ≥ 2 nodes agree → floor RED", "Shield raises earlier", "Shield raises later")
p("shield.rain24", "Decision", "Shield: 24 h rain on high-susceptibility slope", "mm", 150.0, F_SH, r"rain_24h_mm > 150.0", [50, 400], 5, "SYSTEM",
  "shield", "rain_24h > R and high susceptibility → floor ORANGE", "Shield raises earlier", "Shield raises later")

# ---------------- CCTV temporal validator ----------------
p("cctv.window", "Detection", "Temporal validator window", "frames", 5, F_CCTV, r"def __init__\(self, window: int = 5", [1, 20], 1, "SYSTEM", "cctv",
  "confirm if ≥ m of the last W frames ≥ thr", "Faster but more glint false alarms", "Slower, rejects more transients", live=True)
p("cctv.min_frames", "Detection", "Validator: frames required", "frames", 3, F_CCTV, r"min_frames: int = 3", [1, 20], 1, "SYSTEM", "cctv",
  "confirm if ≥ m of the last W frames ≥ thr", "Confirms faster", "Confirms slower", live=True)
p("cctv.thr", "Detection", "Validator: frame confidence threshold", "-", 0.5, F_CCTV, r"conf_thr: float = 0.5", [0.05, 0.95], 0.01, "SYSTEM", "cctv",
  "frame counts if p ≥ thr", "More frames count as fire", "Fewer frames count as fire", live=True)

# ---------------- LoRa / last mile (ws3_alert, Class A + ASSUMPTION) ----------------
p("lora.sf", "LoRa", "Spreading factor SF", "", 10, F_LM, r"    sf: int = 10", [7, 12], 1, "A", "lora",
  "T_sym = 2^SF / BW;  sensitivity SX1276 (BW 125 kHz)", "Shorter airtime, shorter range", "Longer range, much longer airtime")
p("lora.tx_dbm", "LoRa", "Transmit power", "dBm", 30.0, F_LM, r"tx_dbm: float = 30.0", [2, 30], 1, "A", "lora",
  "budget = P_tx + G_tx + G_rx − L_cable − (S_SF + M_fade);  ≤ 1 W (WPC GSR 1048(E))", "Shorter range, less battery", "Longer range",
  hard=[2, 30], regime="India 865-867 MHz licence-exempt limit: 1 W transmit, 4 W EIRP (as cited in last_mile.py)")
p("lora.fade", "LoRa", "Fade margin", "dB", 15.0, F_LM, r"fade_margin_db: float = 15.0", [0, 30], 1, "A", "lora", "budget − M_fade",
  "Longer planned range, less robust", "Shorter planned range, more robust")
p("lora.n_forest", "LoRa", "Path-loss exponent: hill forest (ASSUMPTION)", "-", 3.0, F_LM, r'"hill_forest": 3.0', [2.0, 4.5], 0.05, "A", "lora",
  "PL(d) = FSPL(1 m) + 10 n log10(d)", "Links reach further", "Links reach less far")
p("lora.payload", "LoRa", "Alert payload size", "bytes", 24, F_LM, r"payload_bytes: int = 24", [8, 51], 1, "A", "lora",
  "Semtech time-on-air (AN1200.13)", "Shorter airtime", "Longer airtime (max 51 B in plan)")
p("lora.deadline", "LoRa", "Warning deadline", "min", 10.0, F_LM, r"deadline_min: float = 10.0", [2, 60], 1, "SYSTEM", "lora",
  "reached if minutes ≤ deadline", "Fewer villages count as reached", "More villages count as reached")
p("lora.max_hop", "LoRa", "Maximum planned hop", "km", 30.0, F_LM, r"max_hop_km: float = 30.0", [2, 60], 1, "A", "lora",
  "hop allowed if d ≤ min(range, cap) and terrain clears", "More hops needed", "Longer hops allowed")
p("lora.runner", "LoRa", "Runner speed (human relay)", "km/h", 2.5, F_LM, r"runner_kmh: float = 2.5", [1, 6], 0.1, "SYSTEM", "lora",
  "t = t_source + d / v", "Slower human relay", "Faster human relay")
p("lora.siren_contour", "LoRa", "Siren alerting contour", "dB", 70.0, F_LM, r"siren_contour_db: float = 70.0", [55, 90], 1, "A", "lora",
  "L(r) = L_ref − 20 log10(r / r_ref) − α (r − r_ref)", "Larger audible radius", "Smaller audible radius")
p("lora.duty", "LoRa", "Duty-cycle limit", "%", 1.0, F_CFG, r'"duty_cycle_pct": 1.0', [0.1, 10], 0.1, "SYSTEM", "lora",
  "airtime per hour ≤ duty × 3600 s", "Fewer retransmissions allowed", "More retransmissions allowed",
  regime="Repo default 1 %; verify the current WPC rule for 865-867 MHz before any field use")

# ---------------- PROPOSED (not in repo): prior-shift correction of calibrated probabilities ----------------
P.append(dict(id="fusion.prior", group="Fusion", label="Deployment base rate (prior-shift correction, PROPOSED)", unit="-", default=0.555,
              file=None, pattern=None, range=[0.001, 0.555], hard=[0.0001, 0.999], step=0.001, scale="log", cls="SURROGATE", module="fusion",
              equation="p' = p·π'/π / (p·π'/π + (1−p)(1−π')/(1−π)),  π = 0.555 (evidence-bank prevalence)",
              lower="Probabilities are rescaled to a rarer-event world: far fewer alerts", raise_="π' = π: no correction (repo behaviour)",
              regime="PROPOSED, not in the repo. The OOF probabilities were calibrated on a set where 55 % of images contain fire; a deployed camera sees fire far less often.",
              live=True, kind="number", options=None, citation="Saerens, Latinne, Decaestecker (2002), Neural Computation 14(1):21-41; proposal, not in repo"))

# ---------------- SURROGATE: fire spread (no spread model exists in the repo) ----------------
SUR = "external: Anderson (1983) USDA INT-305 length-to-breadth; Richards (1990) ellipse; not in repo"
P.append(dict(id="sur.ros", group="Fire spread (SURROGATE)", label="Head rate of spread", unit="m/min", default=8.0, file=None, pattern=None,
              range=[0.5, 60], hard=[0.1, 120], step=0.5, scale="log", cls="SURROGATE", module="fire_spread",
              equation="R_head = R0 × wind and slope factors (scenario input)", lower="Perimeter grows slower", raise_="Perimeter grows faster",
              regime="SURROGATE: TRINETRA has no fire-spread model; this drives the visual perimeter only", live=False, kind="number",
              options=None, citation=SUR))
P.append(dict(id="sur.lb", group="Fire spread (SURROGATE)", label="Use wind-driven ellipse (Anderson L/B)", unit="", default=1, file=None,
              pattern=None, range=[0, 1], hard=[0, 1], step=1, scale="linear", cls="SURROGATE", module="fire_spread",
              equation="L/B = 0.936 e^{0.2566 U} + 0.461 e^{−0.1548 U} − 0.397  (U in mi/h)", lower="Circular perimeter", raise_="Wind-elongated perimeter",
              regime=None, live=False, kind="toggle", options=None, citation=SUR))


def main():
    out, missing = [], []
    for e in P:
        if e["file"] is None:
            out.append({**{k: v for k, v in e.items() if k not in ("pattern",)}, "ref": None}); continue
        src = (ROOT / e["file"]).read_text(encoding="utf-8").splitlines()
        hit = next((i + 1 for i, line in enumerate(src) if re.search(e["pattern"], line)), None)
        if hit is None:
            missing.append(e["id"]); continue
        out.append({**{k: v for k, v in e.items() if k not in ("pattern",)}, "ref": {"file": f"TRINETRA/trinetra/{e['file']}", "line": hit}})
    for e in out:
        e["raise"] = e.pop("raise_")
    Path("src/console/data/params_registry.json").write_text(json.dumps({"generated_by": "tools/extract_params.py",
        "params": out, "unresolved": missing}, indent=1, ensure_ascii=False))
    print(f"resolved {len(out)} params ({sum(1 for e in out if e['cls'] != 'SURROGATE')} with repo refs); unresolved: {missing}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
