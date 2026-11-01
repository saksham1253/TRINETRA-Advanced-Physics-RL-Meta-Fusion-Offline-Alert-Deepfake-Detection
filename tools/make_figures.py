"""TRINETRA figures: physics explainers (docs) + measured results (results/figures) + optional cross-modal / stress (X run).

Physics figures are computed with the REPO'S OWN Python functions (TRINETRA/trinetra/src), so every curve matches the code.
Result figures read only files in TRINETRA/results (OUR RESULTS on the prototype pack) and, if given, out_X_final.zip.
Run:  python3 tools/make_figures.py                       # physics + results
      python3 tools/make_figures.py --x-zip out_X_final.zip  # also cross-modal + stress figures
"""
import argparse, glob, io, json, math, os, sys, zipfile
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "TRINETRA/trinetra/src"))
from trinetra.ws1b_geophys.fs import factor_of_safety                                   # noqa: E402
from trinetra.ws1b_geophys.iverson import pressure_head, transient_head_multipulse      # noqa: E402
from trinetra.ws1b_geophys.caine import caine_threshold                                 # noqa: E402
from trinetra.ws1b_geophys.fukuzono import inverse_velocity_fit                         # noqa: E402
from trinetra.ws1a_firephys.established_ef import (flame_height_heskestad, byram_convection_number,  # noqa: E402
                                                     strouhal_puffing_frequency, plume_centerline_dT)
from trinetra.ws1a_firephys.novel_nd import aliased_frequency                          # noqa: E402
from trinetra.ws3_alert import last_mile as lm                                          # noqa: E402
from trinetra.deep.oof_utils import discrimination                                     # noqa: E402

PHYS = ROOT / "TRINETRA/docs/19_TRINETRA_EXPLAINED/PHYSICS_FROM_ZERO/fig"
RES = ROOT / "TRINETRA/results/figures"
RSD = ROOT / "TRINETRA/results"   # results tree the result figures read (--results overrides; final_bundle passes the merged one)
C = dict(ink="#1E1612", ink2="#54463D", ink3="#8A7A6F", line="#D9CEC4", bg="#FFFFFF", brand="#D9480F", brand2="#FF8A3D", gold="#A16207",
         teal="#0F766E", blue="#2F5FC4", green="#1F8A5B", violet="#6D4FC8", red="#B91C1C", amber="#C98A04")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5, "axes.edgecolor": C["line"], "axes.labelcolor": C["ink2"],
                     "xtick.color": C["ink2"], "ytick.color": C["ink2"], "axes.titleweight": "bold", "axes.titlesize": 12.5,
                     "axes.titlecolor": C["ink"], "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": "#EEE7E0", "grid.linewidth": 0.8, "legend.frameon": False, "figure.dpi": 150, "savefig.bbox": "tight"})


def save(fig, path, note=None):
    if note:
        fig.text(0.01, -0.02, note, fontsize=8.5, color=C["ink3"], ha="left", va="top", wrap=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white"); plt.close(fig); print("  ", path)


# ============================================================================ physics explainers
def fig_fs():
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    psi = np.linspace(0, 2.0, 200)
    for beta, col in ((30, C["teal"]), (35, C["brand"]), (40, C["violet"])):
        fs = [float(factor_of_safety(5, 32, 19, 2, beta, 9.81 * p)) for p in psi]
        ax.plot(psi, fs, color=col, lw=2.2, label=f"slope β = {beta}°")
    ax.axhline(1, color=C["red"], lw=1.4, ls="--"); ax.text(1.98, 1.02, "FS = 1: girne ki seema", color=C["red"], ha="right", fontsize=9)
    ax.fill_between(psi, 0, 1, color=C["red"], alpha=0.05)
    ax.set(xlabel="Pressure head ψ at slip depth (m)  →  mitti me paani ka dabaav", ylabel="Factor of safety FS",
           title="Barish ka paani FS ko kaise girata hai (infinite slope, c′=5 kPa, φ′=32°, z=2 m)", ylim=(0.3, 1.8))
    ax.legend(loc="upper right")
    save(fig, PHYS / "01_fs_vs_pore_pressure.png", "Computed with ws1b_geophys/fs.py factor_of_safety(); u_w = 9.81·ψ kPa. Steeper slope = less margin.")


def fig_iverson():
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.0))
    t = np.linspace(0.01, 6, 200)
    for Z, col in ((0.5, C["brand2"]), (1.0, C["brand"]), (2.0, C["violet"])):
        axs[0].plot(t, [float(pressure_head(Z, x, 4.32, 0.864, 0.12, 35)) for x in t], color=col, lw=2.2, label=f"depth Z = {Z} m")
    axs[0].set(xlabel="time since rain started (days)", ylabel="ψ (m)", title="Lagaataar barish: paani ki 'lehar' neeche jaati hai")
    axs[0].legend()
    psi = [float(transient_head_multipulse(2.0, x, [0, 1.0], [0.12, 0.0], 4.32, 0.864, 35)) for x in t]
    axs[1].plot(t, psi, color=C["brand"], lw=2.4, label="1 din ki barish, phir ruk gayi")
    axs[1].axvspan(0, 1, color=C["blue"], alpha=0.08); axs[1].text(0.5, max(psi) * 0.15, "barish", color=C["blue"], ha="center")
    axs[1].set(xlabel="time (days)", ylabel="ψ at Z = 2 m (m)", title="Barish rukne ke baad bhi peak der se aata hai")
    axs[1].legend()
    save(fig, PHYS / "02_iverson_pressure_head.png", "ws1b_geophys/iverson.py: D0=4.32 m²/day, K_z=0.864 m/day (1e-5 m/s), I=0.12 m/day (5 mm/h), β=35°. Superposition for the pulse.")


def fig_caine():
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    D = np.logspace(-0.3, 3, 200)
    ax.loglog(D, caine_threshold(D, 14, 0.39), color=C["brand"], lw=2.5, label="Caine line  I = 14·D^(−0.39)")
    ax.fill_between(D, caine_threshold(D, 14, 0.39), 200, color=C["red"], alpha=0.06)
    ax.text(2, 60, "line ke UPAR: landslide ka khatra", color=C["red"]); ax.text(30, 0.35, "line ke NEECHE: aam taur par safe", color=C["teal"])
    for (d, i, lab) in ((24, 5, "120 mm in 24 h (ratio 1.23)"), (72, 300 / 72, "300 mm in 3 days (1.58)"), (216, 1.03, "1 mm/h for 9 days (0.60)")):
        ax.scatter([d], [i], s=48, color=C["ink"], zorder=3); ax.annotate(lab, (d, i), textcoords="offset points", xytext=(6, 6), fontsize=9)
    ax.set(xlabel="Duration D (hours)", ylabel="Mean intensity I (mm/h)", title="Caine rainfall intensity–duration threshold", ylim=(0.2, 200))
    ax.legend(loc="lower left")
    save(fig, PHYS / "03_caine_threshold.png", "Global coefficients (a=14, b=0.39) from the repo; they must be re-fitted locally. OUR RESULT: zero-fit AUC 0.758 on 184 Indian events.")


def fig_fukuzono():
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    t = np.array([0, 2, 4, 6, 8, 10.]); rng = np.random.default_rng(0)
    v = 1 / (10 - 0.5 * t) * np.exp(rng.normal(0, 0.05, len(t)))
    f = inverse_velocity_fit(t, v, recency_halflife=4)
    tt = np.linspace(0, f.t_failure_high + 1, 100)
    ax.scatter(t, 1 / v, color=C["ink"], zorder=3, label="measured 1/velocity (synthetic creep)")
    ax.plot(tt, f.slope * tt - f.slope * f.t_failure, color=C["brand"], lw=2.2, label="weighted straight-line fit")
    ax.axvspan(f.t_failure_low, f.t_failure_high, color=C["red"], alpha=0.12, label=f"failure time {f.t_failure:.1f} h (95% interval {f.t_failure_low:.1f}–{f.t_failure_high:.1f})")
    ax.axhline(0, color=C["ink3"], lw=1)
    ax.set(xlabel="time (h)", ylabel="1 / velocity", title="Fukuzono: 1/v seedhi line me zero ki taraf → failure time", ylim=(-0.5, 11))
    ax.legend(loc="upper right", fontsize=9)
    save(fig, PHYS / "04_fukuzono_inverse_velocity.png", "ws1b_geophys/fukuzono.py inverse_velocity_fit (recency half-life 4 h, delta-method interval). No real creep data in the repo yet.")


def fig_fire():
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.0))
    Q = np.logspace(1.5, 4.8, 200)
    for D, col in ((0.5, C["brand2"]), (3, C["brand"]), (6, C["violet"])):
        L = [flame_height_heskestad(q, D) for q in Q]
        axs[0].semilogx(Q, np.maximum(L, 0), color=col, lw=2.2, label=f"base D = {D} m")
    axs[0].set(xlabel="heat release Q (kW)", ylabel="flame height L (m)", title="Heskestad: L = 0.235·Q^0.4 − 1.02·D"); axs[0].legend()
    U = np.linspace(0.3, 12, 300)
    for Qc, col in ((300, C["teal"]), (1500, C["brand"]), (6000, C["violet"])):
        axs[1].semilogy(U, [byram_convection_number(Qc, u) for u in U], color=col, lw=2.2, label=f"Q_c = {Qc} kW/m")
    axs[1].axhline(2, color=C["green"], ls="--", lw=1.2); axs[1].text(11.8, 2.4, "N_c = 2: plume-dominated above", ha="right", color=C["green"], fontsize=8.5)
    axs[1].axhline(1, color=C["red"], ls="--", lw=1.2); axs[1].text(11.8, 0.7, "N_c < 1: wind-dominated", ha="right", color=C["red"], fontsize=8.5)
    axs[1].set(xlabel="wind U (m/s)", ylabel="Byram N_c", title="Byram: hawa jeetegi ya aag ka plume?", ylim=(1e-3, 1e4)); axs[1].legend(loc="lower left")
    D = np.linspace(0.2, 8, 300)
    axs[2].plot(D, [strouhal_puffing_frequency(d) for d in D], color=C["brand"], lw=2.2, label="true puffing f = 1.5/√D")
    axs[2].plot(D, [aliased_frequency(strouhal_puffing_frequency(d), 2.0) for d in D], color=C["violet"], lw=2, ls="--", label="what a 2 fps camera sees")
    axs[2].set(xlabel="fire base D (m)", ylabel="frequency (Hz)", title="Strouhal flicker + camera aliasing"); axs[2].legend()
    save(fig, PHYS / "05_fire_physics.png", "ws1a_firephys/established_ef.py and novel_nd.aliased_frequency. Coefficients [coeff-verify]. Note: Q_c=1500 kW/m at 9 m/s gives N_c=0.11, so the gate lowers consistency for a real wind-driven fire.")


def fig_plume():
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    z = np.linspace(2, 40, 200)
    for Qc, col in ((200, C["teal"]), (500, C["brand"]), (2000, C["violet"])):
        ax.plot(z, [plume_centerline_dT(Qc, x) for x in z], color=col, lw=2.2, label=f"Q_c = {Qc} kW")
    ax.set_yscale("log"); ax.set(xlabel="height above fire z (m)", ylabel="excess temperature ΔT (K)", title="Plume: height dugni → ΔT ~3.2× kam")
    ax.legend()
    save(fig, PHYS / "06_plume_temperature.png", "plume_centerline_dT: ΔT = 9.1·(T/(g c_p² ρ²))^(1/3)·Q_c^(2/3)·z^(−5/3) ≈ 25·Q_c^(2/3)·z^(−5/3) at 293 K.")


def fig_cost_loss():
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.0))
    p = np.linspace(0, 0.3, 300); CFA, CM = 5, 100
    axs[0].plot(p, p * CM, color=C["red"], lw=2.2, label="HOLD: expected cost = p·C_miss")
    axs[0].plot(p, (1 - p) * CFA, color=C["blue"], lw=2.2, label="ALARM: expected cost = (1−p)·C_FA")
    ps = CFA / (CFA + CM)
    axs[0].axvline(ps, color=C["gold"], ls="--"); axs[0].text(ps + 0.004, 16, f"p* = 5/105 = {ps:.3f}", color=C["gold"])
    axs[0].set(xlabel="probability of a real fire p", ylabel="expected cost per decision", title="Cost-loss: alarm kab sasta hai?", ylim=(0, 20)); axs[0].legend()
    praw = np.linspace(0.001, 0.999, 400); PI = 1892 / 3410
    for tgt, col in ((PI, C["ink3"]), (0.1, C["brand"]), (0.01, C["violet"])):
        a = praw * tgt / PI; b = (1 - praw) * (1 - tgt) / (1 - PI)
        axs[1].plot(praw, a / (a + b), color=col, lw=2.2, label=f"deployment base rate {tgt:.3f}" + (" (no change)" if tgt == PI else ""))
    axs[1].axhline(ps, color=C["gold"], ls="--"); axs[1].set(xlabel="model probability (calibrated on 55% fire images)", ylabel="probability after prior shift",
                                                           title="Prior shift: rare-event duniya me probability"); axs[1].legend()
    save(fig, PHYS / "07_cost_loss_and_prior_shift.png", "Left: decision.py cut point. Right: PROPOSED Bayes prior-shift correction (Saerens et al. 2002), not in the repo yet.")


def fig_lora():
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.0))
    sfs = [7, 8, 9, 10, 11, 12]
    for terr, col in (("hill_forest", C["brand"]), ("valley_nlos", C["violet"])):
        axs[0].plot(sfs, [lm.lora_range_km(s, terr) for s in sfs], "o-", color=col, lw=2.2, label=terr.replace("_", " "))
    axs[0].set(xlabel="spreading factor SF", ylabel="planned range (km)", title="LoRa: SF badhao → range badhti hai")
    axs[0].legend()
    ax2 = axs[1]
    ax2.bar([str(s) for s in sfs], [lm.lora_airtime_s(24, s) * 1000 for s in sfs], color=C["teal"])
    ax2.set(xlabel="spreading factor SF", ylabel="time on air for 24 bytes (ms)", title="…par har message ka airtime bhi badhta hai")
    save(fig, PHYS / "08_lora_range_airtime.png", "ws3_alert/last_mile.py: SX1276 sensitivity, 30 dBm, 2+2 dBi, 15 dB fade margin, log-distance exponents 3.0 / 3.6 (ASSUMPTION).")


def _dem_profile(lon0, lat0, lon1, lat1, n=200, z=12):
    from PIL import Image
    cache = {}
    def elev(lon, lat):
        N = 2 ** z; fx = (lon + 180) / 360 * N; r = math.radians(lat)
        fy = (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * N
        tx, ty = int(fx), int(fy)
        key = (tx, ty)
        if key not in cache:
            p = ROOT / f"public/tiles/terrarium/{z}/{tx}/{ty}.png"
            a = np.asarray(Image.open(p).convert("RGB"), float)
            cache[key] = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
        G = cache[key]; i = min(255, int((fx - tx) * 256)); j = min(255, int((fy - ty) * 256))
        return G[j, i]
    f = np.linspace(0, 1, n)
    return f, np.array([elev(lon0 + k * (lon1 - lon0), lat0 + k * (lat1 - lat0)) for k in f])


def fig_fresnel():
    b = math.radians(52); ox, oy = 79.315, 30.398
    def ll(x, y):
        e = x * math.sin(b) - y * math.cos(b); nn = x * math.cos(b) + y * math.sin(b)
        return ox + e * 1000 / (111320 * math.cos(math.radians(oy))), oy + nn * 1000 / 110540
    a, v = ll(0, 0), ll(11.9, 3.1)   # GW-HQ to village V06 of the repo demo valley (synthetic positions)
    try:
        f, g = _dem_profile(*a, *v)
    except Exception as e:  # noqa: BLE001
        print("   fresnel: DEM tiles missing", e); return
    D = math.hypot((v[0] - a[0]) * 111320 * math.cos(math.radians(oy)), (v[1] - a[1]) * 110540)
    d = f * D; lam = 299.792458 / 866
    h0, h1 = g[0] + 15, g[-1] + 3
    los = h0 + f * (h1 - h0); r1 = np.sqrt(lam * d * (D - d) / max(D, 1)); bulge = d * (D - d) / (2 * 4 / 3 * 6371000)
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.fill_between(d / 1000, g.min() - 200, g + bulge, color="#E7D3BB", label="real terrain (Copernicus/SRTM via AWS tiles) + earth bulge")
    ax.plot(d / 1000, los, color=C["teal"], lw=2, label="radio line of sight (gateway 15 m mast → village 3 m)")
    ax.fill_between(d / 1000, los - 0.6 * r1, los + 0.6 * r1, color=C["teal"], alpha=0.15, label="60% of first Fresnel zone (must be clear)")
    blocked = (g + bulge) > los - 0.6 * r1
    if blocked.any():
        ax.scatter(d[blocked] / 1000, (g + bulge)[blocked], s=6, color=C["red"], label="terrain blocks the link here")
    ax.set(xlabel="distance along the link (km)", ylabel="elevation (m)", title=f"Chamoli: gateway → village link, {D/1000:.1f} km — pahad beech me aata hai")
    ax.legend(loc="upper left", fontsize=8.5)
    save(fig, PHYS / "09_fresnel_real_terrain.png", "Synthetic node positions of the repo demo valley laid on REAL Chamoli terrain (cached tiles). 866 MHz, λ = 0.346 m. This is why 47 of 55 candidate links are blocked in the console.")


def fig_noisy_or():
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    p1 = np.linspace(0, 1, 100)
    for p2, col in ((0.0, C["ink3"]), (0.3, C["brand2"]), (0.6, C["brand"]), (0.9, C["violet"])):
        ax.plot(p1, 1 - (1 - p1) * (1 - p2), color=col, lw=2.2, label=f"second signal p₂ = {p2}")
    ax.set(xlabel="first physics signal p₁", ylabel="combined p_phys", title="Noisy-OR: ek bhi signal bole to risk kabhi kam nahi hota"); ax.legend()
    save(fig, PHYS / "10_noisy_or.png", "ws1b_geophys/gate.py: p_phys = 1 − Π(1 − p_i). Monotone: adding evidence never lowers the warning.")


# ============================================================================ measured results
def _oof(p):
    d = np.load(p, allow_pickle=True)
    return d


def roc(p, y):
    o = np.argsort(-p); ys = y[o]; tp = np.cumsum(ys) / ys.sum(); fp = np.cumsum(1 - ys) / (1 - ys).sum()
    return np.r_[0, fp], np.r_[0, tp]


def fig_results():
    I = RSD / "fire_meta/inputs"
    fire, zs, cp = (_oof(I / f) for f in ("fire_s0_oof.npz", "zeroshot_s0_oof.npz", "clip_probe_s0_oof.npz"))
    stack = _oof(RSD / "fire_meta/fire_meta_fusion_s0_oof.npz")
    y = fire["y"].astype(int)
    series = [("fire CNN (ours)", fire, C["ink3"]), ("CLIP zero-shot", zs, C["blue"]), ("CLIP probe", cp, C["brand"]), ("stack (meta-fusion)", stack, C["violet"])]
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.4))
    for name, d, col in series:
        p = np.where(np.isnan(d["prob_cal"]), d["prob"], d["prob_cal"]); fx, ty = roc(p, d["y"].astype(int))
        axs[0].plot(fx, ty, color=col, lw=2.2, label=f"{name}  AUC {discrimination(p, d['y'])['roc_auc']:.3f}")
    axs[0].plot([0, 1], [0, 1], color=C["line"], ls="--"); axs[0].set(xlabel="false-alarm rate", ylabel="detection rate", title="Out-of-fold: 3410 images")
    axs[0].legend(loc="lower right", fontsize=9)
    for name, d, col in series:
        if "test_prob" not in d.files:
            continue
        p = d["test_prob_cal"] if "test_prob_cal" in d.files else d["test_prob"]; fx, ty = roc(p, d["test_y"].astype(int))
        axs[1].plot(fx, ty, color=col, lw=2.2, label=f"{name}  AUC {discrimination(p, d['test_y'])['roc_auc']:.3f}")
    axs[1].plot([0, 1], [0, 1], color=C["line"], ls="--"); axs[1].set(xlabel="false-alarm rate", ylabel="detection rate", title="Held-out: new dataset, 1023 images")
    axs[1].legend(loc="lower right", fontsize=9)
    save(fig, RES / "R1_fire_roc_oof_and_heldout.png", "OUR RESULT on the prototype pack. Stack = logistic on the same images (REAL pairing). Held-out AUC near 1 means that set is easy, not that the problem is solved.")

    # reliability (calibration)
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    for name, d, col in series:
        p = np.where(np.isnan(d["prob_cal"]), d["prob"], d["prob_cal"]); yy = d["y"].astype(int)
        bins = np.linspace(0, 1, 11); k = np.clip(np.digitize(p, bins) - 1, 0, 9)
        xs = [p[k == i].mean() for i in range(10) if (k == i).sum() > 20]; ys = [yy[k == i].mean() for i in range(10) if (k == i).sum() > 20]
        ax.plot(xs, ys, "o-", color=col, lw=1.8, ms=4, label=name)
    ax.plot([0, 1], [0, 1], color=C["line"], ls="--", label="perfect calibration")
    ax.set(xlabel="predicted probability", ylabel="observed fire fraction", title="Calibration: model jo kehta hai, kya utna hi hota hai?"); ax.legend(fontsize=9)
    save(fig, RES / "R2_calibration.png", "Cross-fit temperature-calibrated OOF probabilities, 10 bins (bins with ≤20 images hidden).")

    # alert flood vs deployment base rate (real rows)
    p = np.where(np.isnan(stack["prob_cal"]), stack["prob"], stack["prob_cal"]); PI = y.mean()
    rates = np.logspace(-3, math.log10(PI), 60); fa, rec = [], []
    for t in rates:
        a = p * t / PI; b = (1 - p) * (1 - t) / (1 - PI); q = a / (a + b)
        fa.append((q[y == 0] >= 4 * 5 / 105).mean()); rec.append((q[y == 1] >= 4 * 5 / 105).mean())
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.semilogx(rates, fa, color=C["red"], lw=2.4, label="false-alarm rate (non-fire images)")
    ax.semilogx(rates, rec, color=C["teal"], lw=2.4, label="detection rate (fire images)")
    ax.axvline(PI, color=C["ink3"], ls=":"); ax.text(PI, 0.5, " repo default\n (55% prior)", color=C["ink3"], fontsize=9)
    ax.set(xlabel="deployment base rate used for prior-shift (log scale)", ylabel="rate at WARNING cut (4·p*)",
           title="Base-rate correction: false alarms girte hain, detection bhi")
    ax.legend(loc="center left")
    save(fig, RES / "R3_alert_flood_vs_base_rate.png", "Real per-image stack probabilities (OOF). PROPOSED correction, not in the repo yet. Trade-off: at 1% base rate false alarms ~0 but per-image detection ~0.6; a fire is seen over many frames, so incident detection stays high in the console simulation.")

    # landslide
    gf = [json.load(open(f)) for f in sorted(glob.glob(str(RSD / "geo_fusion/geo_fusion_s*_report.json")))]
    if gf:
        rules = ["single: caine", "single: dfs", "single: geo_gate", "single: rain", "stacked logistic (rain+physics)", "FM-1 (calibrated)"]
        labels = ["Caine (zero training)", "ΔFS (zero training)", "geo gate", "rain logistic", "stack rain+physics", "FM-1 fusion"]
        m = [np.mean([g["rules"][r]["roc_auc"] for g in gf]) for r in rules]; s = [np.std([g["rules"][r]["roc_auc"] for g in gf]) for r in rules]
        fig, ax = plt.subplots(figsize=(8, 4.0))
        cols = [C["blue"], C["blue"], C["blue"], C["ink3"], C["violet"], C["brand"]]
        ax.barh(labels, m, xerr=s, color=cols); ax.set_xlim(0.6, 0.82); ax.invert_yaxis()
        for i, v in enumerate(m):
            ax.text(v + 0.003, i, f"{v:.3f}", va="center", fontsize=9)
        pinn = json.load(open(RSD / "geo_pinn/geo_pinn_s0_report.json")).get("oof_roc_auc")
        if pinn:
            ax.axvline(pinn, color=C["red"], ls="--"); ax.text(pinn + 0.002, 5.4, f"Geo-PINN {pinn:.3f}", color=C["red"], fontsize=9)
        ax.set(xlabel="ROC-AUC (spatial block CV, 736 rows, 184 real events)", title="Landslide: physics bina training ke kitna pakadti hai")
        save(fig, RES / "R4_landslide_auc.png", "OUR RESULT, NASA Global Landslide Catalog (India) + NASA POWER rain. Blue = physics with no fitting. Mean ± sd over 3 seeds.")

    # RL held-out
    R = [json.load(open(f)) for f in sorted(glob.glob(str(RSD / "offline_rl_heldout/*_report.json")))]
    if R:
        keys = [("cql", "learned RL (CQL)"), ("rule", "fixed rule"), ("rule_tuned", "tuned rule"), ("always_alarm", "always alarm")]
        m = [np.mean([r["policies"][k]["reward_per_row"] for r in R]) for k, _ in keys]
        fig, ax = plt.subplots(figsize=(7, 3.8))
        ax.bar([l for _, l in keys], m, color=[C["violet"], C["ink3"], C["teal"], C["red"]])
        for i, v in enumerate(m):
            ax.text(i, v - 0.08, f"{v:.2f}", ha="center", color="white", fontsize=10, fontweight="bold")
        ax.set(ylabel="reward per image (higher is better)", title="RL ko tuned rule se behtar hona chahiye tha — nahi hua")
        save(fig, RES / "R5_rl_heldout.png", "OUR RESULT: block-held-out folds, true reward from labels (C_FA 5, C_miss 100), 3 seeds. Gate kept the rule: deploy 0/3.")

    # deepfake generalisation gap (from master scorecard)
    m = json.load(open(RSD / "master_merged/master.json"))["scorecard"]
    rows = {r["expert"]: r for r in m}
    pairs = [(e, rows[e]["value"]) for e in ("fire_cnn", "zeroshot", "clip_probe", "deepfake") if e in rows and rows[e]["value"] and "/" in rows[e]["value"]]
    if pairs:
        fig, ax = plt.subplots(figsize=(7.2, 3.8))
        x = np.arange(len(pairs)); oof = [float(v.split("/")[0]) for _, v in pairs]; ho = [float(v.split("/")[1]) for _, v in pairs]
        ax.bar(x - 0.18, oof, 0.36, color=C["brand"], label="out-of-fold (same source)"); ax.bar(x + 0.18, ho, 0.36, color=C["blue"], label="held-out (new source)")
        ax.set_xticks(x, [p for p, _ in pairs]); ax.set_ylim(0.3, 1.05); ax.axhline(0.5, color=C["ink3"], ls=":")
        ax.text(len(pairs) - 1, 0.47, "0.5 = coin flip", ha="center", fontsize=8.5, color=C["ink3"])
        ax.set(ylabel="ROC-AUC", title="Naye source par kaun tikta hai? Deepfake nahi tika"); ax.legend(loc="lower left")
        save(fig, RES / "R6_generalisation_gap.png", "OUR RESULT. Deepfake: 0.961 on CIFAKE folds, 0.450 on unseen generators → kept as a low-trust down-weighter only.")


# ============================================================================ cross-modal + stress (X run)
def _reports(srcs):
    """(name, json) of every *_report.json inside the given zips and/or folders."""
    for src in srcs:
        if os.path.isdir(src):
            for f in glob.glob(os.path.join(src, "**", "*_report.json"), recursive=True):
                yield os.path.relpath(f, src).replace(os.sep, "/"), json.load(open(f))
        else:
            z = zipfile.ZipFile(src)
            for n in z.namelist():
                if n.endswith("_report.json"):
                    yield n, json.loads(z.read(n))


def fig_x(srcs):
    srcs = [srcs] if isinstance(srcs, (str, Path)) else list(srcs)
    seen, cm, st = set(), [], []
    for n, r in _reports(srcs):
        key = (os.path.basename(n), r.get("run_id"))      # X re-ships nothing twice, but X and S may both carry stress reports
        if key in seen:
            continue
        seen.add(key)
        if "crossmodal_s" in n:
            cm.append(r)
        elif "/stress_s" in "/" + n:
            st.append(r)
    if cm:
        streams = list(cm[0]["video"])
        J = [np.mean([r["video"][s]["detect_validated"] - r["video"][s]["fa_video_validated"] for r in cm]) for s in streams]
        fig, ax = plt.subplots(figsize=(8, 3.8))
        ax.bar(streams, J, color=[C["violet"] if s == "stack" else C["brand"] if s == "clip_probe" else C["ink3"] for s in streams])
        ax.set(ylabel="detection − false alarm (videos, validated)", title="FireSense videos: kaunsa stream best? (temporal validator ke baad)")
        save(fig, RES / "R7_crossmodal_video.png", f"OUR RESULT, 49 FireSense videos (small n), mean over {len(cm)} seed(s).")
        sets = sorted({k for r in cm for k in r["stress"]})
        if sets:
            fig, ax = plt.subplots(figsize=(9, 4))
            w = 0.8 / len(streams)
            for i, s in enumerate(streams):
                ax.bar(np.arange(len(sets)) + i * w, [np.mean([r["stress"][k]["streams"][s]["fa_rate_at_thr"] or 0 for r in cm if k in r["stress"]]) for k in sets], w, label=s)
            ax.set_xticks(np.arange(len(sets)) + 0.4 - w / 2, sets, rotation=10); ax.set(ylabel="false-alarm rate at 0.5", title="Confusers par false alarms (har stream)")
            ax.legend(fontsize=8, ncol=3)
            save(fig, RES / "R8_crossmodal_confusers.png", "OUR RESULT: per-image false alarms on confuser sets (all negatives).")
    if st:
        folds = [f for r in st for f in r["folds"]]
        hs = sorted({f["heldout_confuser"] for f in folds})
        fig, ax = plt.subplots(figsize=(9, 4))
        for i, (mk, lab, col) in enumerate((("probe_base", "probe (fire only)", C["ink3"]), ("probe_conf", "probe + hard negatives", C["brand"]),
                                            ("stack_base", "stack", C["blue"]), ("stack_conf", "stack + hard negatives", C["violet"]))):
            ax.bar(np.arange(len(hs)) + i * 0.2, [np.mean([f["models"][mk]["fa_thr90"] for f in folds if f["heldout_confuser"] == h]) for h in hs], 0.2, label=lab, color=col)
        ax.set_xticks(np.arange(len(hs)) + 0.3, [h.replace("stress_", "unseen: ") for h in hs]); ax.set(ylabel="false alarms at equal recall 0.90",
                                                                                                   title="Hard-negative training: unseen confuser par false alarms")
        ax.legend(fontsize=8.5, ncol=2)
        save(fig, RES / "R9_stress_retrain.png", f"OUR RESULT, leave-one-confuser-set-out, {len(st)} seed(s). Admitted only if FA drops with CI AND DeepFire AUC drop ≤ 0.01.")


def main():
    global RSD, RES, PHYS
    ap = argparse.ArgumentParser()
    ap.add_argument("--x-zip", nargs="*", default=[], help="X / S run outputs (zips or out/ folders) for cross-modal + stress figures")
    ap.add_argument("--results", default=None, help="results tree to read (default TRINETRA/results)")
    ap.add_argument("--fig-out", default=None, help="where result figures go (default TRINETRA/results/figures)")
    ap.add_argument("--phys-out", default=None, help="where physics figures go (default PHYSICS_FROM_ZERO/fig)")
    a = ap.parse_args()
    RSD = Path(a.results).resolve() if a.results else RSD
    RES = Path(a.fig_out).resolve() if a.fig_out else RES
    PHYS = Path(a.phys_out).resolve() if a.phys_out else PHYS
    failed = []
    def run(f, *args):
        try:
            f(*args)
        except Exception as e:                               # one missing input (e.g. DEM tiles) must not stop the rest
            failed.append(f.__name__); print(f"  [skip] {f.__name__}: {type(e).__name__}: {e}")
    print("physics figures:")
    for f in (fig_fs, fig_iverson, fig_caine, fig_fukuzono, fig_fire, fig_plume, fig_cost_loss, fig_lora, fig_fresnel, fig_noisy_or):
        run(f)
    print("result figures:"); run(fig_results)
    if a.x_zip:
        print("cross-modal / stress figures:"); run(fig_x, a.x_zip)
    print("skipped:", failed or "none")


if __name__ == "__main__":
    main()
