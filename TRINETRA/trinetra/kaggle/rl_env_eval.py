"""RL on the physics-based landslide ENVIRONMENT (ws5_fusion_rl/env_landslide.py), with REAL rainfall seasons.

Steps: (1) build monsoon seasons from the NASA POWER cache written by data_adapters/build_geo.py; (2) fit the hazard
slope beta from the REAL case-control table (logistic of label on dFS_backcalc; case-control leaves the slope consistent,
only the intercept is biased) and set the intercept alpha so a HOLD-forever slope fails with --season-fail probability
(ASSUMPTION); (3) evaluate baselines ONLINE; (4) log eps-rule transitions (also saved for kaggle/train_offline_rl.py);
(5) train CQL (gamma>0) and evaluate it ONLINE with the repo shield; compare its OPE estimate with the true online value.
Run (CPU ok, ~5-15 min): python kaggle/rl_env_eval.py --events geo/geo_events.csv --power-cache power_cache --out out/rl_env
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from trinetra.ws5_fusion_rl.env_landslide import (EnvConfig, LandslideAlertEnv, rollout, log_transitions,  # noqa: E402
                                                  physics_rule_policy, caine_rule_policy, bayes_action)
from trinetra.ws5_fusion_rl.shield import ShieldSignals, shield_floor                                        # noqa: E402
from trinetra.ws5_fusion_rl.rl import wis_value                                                              # noqa: E402
from trinetra.common.types import Level                                                                     # noqa: E402


def seasons_from_cache(cache: str, memory=30, horizon=122):
    out = []
    for f in sorted(glob.glob(os.path.join(cache, "power_*.json"))):
        ser = json.load(open(f))
        for y in range(2007, 2017):
            start = np.datetime64(f"{y}-06-01") - np.timedelta64(memory, "D")
            days = [str(start + np.timedelta64(i, "D")).replace("-", "") for i in range(memory + horizon)]
            v = np.array([ser.get(d) if ser.get(d) is not None else np.nan for d in days], float)
            if np.isnan(v).mean() < 0.05:
                out.append(np.nan_to_num(v, nan=0.0))
    return out


def fit_logit_1d(x, y, iters=50):
    w = np.zeros(2); X = np.c_[np.ones_like(x), x]
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w)); W = p * (1 - p) + 1e-9
        w += np.linalg.solve(X.T @ (X * W[:, None]) + 1e-6 * np.eye(2), X.T @ (y - p))
    return w


def calibrate_alpha(env, seasons, target):
    fs_paths = []
    for s in seasons:
        fs_paths.append(np.array([env.fs_from_rain(s[env.cfg.memory_days + t - env.cfg.memory_days + 1: env.cfg.memory_days + t + 1])[0]
                                  for t in range(env.cfg.horizon)]))
    lo, hi = -30.0, 5.0
    for _ in range(60):
        mid = (lo + hi) / 2; env.cfg.alpha = mid
        pf = np.mean([1 - np.prod([1 - env.hazard(f) for f in path]) for path in fs_paths])
        lo, hi = (mid, hi) if pf < target else (lo, mid)
    return env.cfg.alpha, float(pf)


def main(argv=None):
    import pandas as pd
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", required=True); ap.add_argument("--power-cache", required=True)
    ap.add_argument("--out", default="out/rl_env"); ap.add_argument("--season-fail", type=float, default=0.3)
    ap.add_argument("--episodes", type=int, default=300); ap.add_argument("--log-episodes", type=int, default=400)
    ap.add_argument("--eps", type=float, default=0.3); ap.add_argument("--gamma", type=float, default=0.95)
    ap.add_argument("--epochs", type=int, default=30); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-torch", action="store_true")
    ap.add_argument("--C-miss", type=float, default=None, help="override configs C_miss (sensitivity: value of warning vs cost ratio)")
    ap.add_argument("--C-FA", type=float, default=None)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    ev = pd.read_csv(a.events)
    seasons = seasons_from_cache(a.power_cache)
    if not seasons:
        raise SystemExit("no seasons in POWER cache; run data_adapters/build_geo.py first")
    beta = float(np.nanmedian(ev.slope_p90_deg))
    cfg = EnvConfig(beta_deg=beta, seasons=seasons)
    if a.C_miss is not None:
        cfg.C_miss = a.C_miss
    if a.C_FA is not None:
        cfg.C_FA = a.C_FA
    env = LandslideAlertEnv(cfg, seed=a.seed)
    # dFS = FS_dry - FS_wet = du * tan(phi) / (gamma z sin(b) cos(b)) does NOT depend on c', so the `dfs` column from
    # build_geo equals the env's fs_dry - fs regardless of the back-analysed cohesion (bug B-24: 1.2 - fs_backcalc is
    # wrong on gentle slopes where c' clips at 0 and FS_dry >> 1.2).
    x = ev.dfs.values.astype(float); m = np.isfinite(x)
    w = fit_logit_1d(x[m], ev.label.values[m].astype(float)); env.cfg.beta_h = float(max(w[1], 1.0))
    rep_fit = {"logit_intercept_case_control": float(w[0]), "logit_slope_dfs": float(w[1]), "n_fit": int(m.sum())}
    alpha, pf = calibrate_alpha(env, seasons, a.season_fail)
    rep = {"name": "rl_env", "seed": a.seed, "n_seasons": len(seasons), "slope_deg": beta, "c_backcalc_kpa": env.c_bc,
           "hazard_beta_fitted_on_real_events": env.cfg.beta_h, "hazard_fit": rep_fit, "hazard_alpha": alpha, "season_fail_target": a.season_fail,
           "season_fail_achieved_hold": pf, "C_FA": env.cfg.C_FA, "C_miss": env.cfg.C_miss, "policies": {}}
    pol = {"always_hold": lambda o: 0, "always_alarm": lambda o: 2, "caine_rule": caine_rule_policy,
           "physics_rule": lambda o: physics_rule_policy(o, env=env)}
    oracle_env = env
    pol["oracle_true_hazard"] = lambda o: bayes_action(oracle_env.hazard(oracle_env._fs_true), oracle_env.cfg)  # upper bound (sees true FS)
    for k, p in pol.items():
        rep["policies"][k] = rollout(env, p, a.episodes, seed=a.seed + 1)
        print(f"[rl-env] {k:20s} return {rep['policies'][k]['return_mean']:8.2f} miss_rate {rep['policies'][k]['miss_rate']} alarm_days {rep['policies'][k]['alarm_days_per_season']:.1f} watch_days {rep['policies'][k]['watch_days_per_season']:.1f}")
    logs = log_transitions(env, pol["physics_rule"], a.log_episodes, a.eps, seed=a.seed)
    np.savez_compressed(os.path.join(a.out, "env_logs.npz"), **logs)
    rep["logged_transitions"] = int(len(logs["a"]))
    if not a.no_torch:
        try:
            import torch
            from trinetra.deep.offline_rl import CQLPolicy, CQLConfig
            torch.manual_seed(a.seed)
            S = torch.tensor(logs["s"]); A_ = torch.tensor(logs["a"]); R = torch.tensor(logs["r"]) / env.cfg.C_miss
            S2 = torch.tensor(logs["s_next"]); D = torch.tensor(logs["done"])
            cql = CQLPolicy(CQLConfig(state_dim=S.shape[1], n_actions=3, gamma=a.gamma))
            opt = torch.optim.AdamW(cql.online.parameters(), lr=3e-4, weight_decay=1e-4)
            n = len(S)
            for _ in range(a.epochs):
                perm = torch.randperm(n)
                for i in range(0, n, 512):
                    b = perm[i:i + 512]
                    opt.zero_grad(); loss = cql.cql_loss(S[b], A_[b], R[b], S2[b], D[b])["loss"]; loss.backward()
                    torch.nn.utils.clip_grad_norm_(cql.online.parameters(), 1.0); opt.step(); cql.polyak_update()
            cql.eval()

            def learned(o):
                with torch.no_grad():
                    return int(cql.online(torch.tensor(o)[None]).argmax(1))

            def shielded(o):
                act = learned(o)
                floor = shield_floor(ShieldSignals(FS=float(o[5]), rain_24h_mm=float(math.expm1(o[0])))).floor
                return max(act, 2 if floor >= Level.ORANGE else (1 if floor >= Level.YELLOW else 0))
            for k, p in (("cql_learned", learned), ("cql_learned_shielded", shielded)):
                rep["policies"][k] = rollout(env, p, a.episodes, seed=a.seed + 1)
                print(f"[rl-env] {k:20s} return {rep['policies'][k]['return_mean']:8.2f} miss_rate {rep['policies'][k]['miss_rate']} alarm_days {rep['policies'][k]['alarm_days_per_season']:.1f}")
            with torch.no_grad():
                greedy = cql.online(S).argmax(1).numpy()
            tp = (greedy == logs["a"]).astype(float)
            # per-step WIS of immediate reward (one-step OPE proxy) vs the logging policy, to show OPE vs truth gap
            v_l, ess = wis_value(logs["behavior_prob"], tp, logs["r"])
            v_b, _ = wis_value(logs["behavior_prob"], np.ones_like(tp), logs["r"])
            rep["ope_one_step_proxy"] = {"learned": v_l, "logging": v_b, "ess": ess,
                                         "note": "per-step WIS proxy; compare with ONLINE returns above (ground truth in sim)"}
        except ImportError:
            rep["cql"] = "torch not installed"
    best_rule = max(("caine_rule", "physics_rule", "always_hold"), key=lambda k: rep["policies"][k]["return_mean"])
    rep["best_rule"] = best_rule
    if "cql_learned_shielded" in rep["policies"]:
        # BUGFIX (B-25): deploy only if the PAIRED per-episode gain (same seeds -> same rain + failure draws) has a 95% lower
        # bound > 0; a raw mean comparison admitted a +0.01 noise-level gain.
        d = np.asarray(rep["policies"]["cql_learned_shielded"]["returns"]) - np.asarray(rep["policies"][best_rule]["returns"])
        lcb = float(d.mean() - 1.96 * d.std(ddof=1) / np.sqrt(len(d)))
        rep["gain_vs_rule_mean"] = float(d.mean()); rep["gain_vs_rule_lcb95"] = lcb
        rep["deploy_learned"] = bool(lcb > 0)
    for v in rep["policies"].values():
        v.pop("returns", None)
    rep["note"] = ("ONLINE returns in a physics simulator with REAL rainfall; hazard intercept is an ASSUMPTION (season-fail). "
                   "Simulator results are not field results.")
    tag = f"rl_env_cmiss{int(env.cfg.C_miss)}" if a.C_miss is not None else "rl_env"
    rep["name"] = tag
    json.dump(rep, open(os.path.join(a.out, f"{tag}_s{a.seed}_report.json"), "w"), indent=2)
    print(json.dumps({k: v for k, v in rep.items() if k != "policies"}, indent=2))


if __name__ == "__main__":
    main()
