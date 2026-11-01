"""ws5_fusion_rl.env_landslide — physics-based RL ENVIRONMENT for landslide alert decisions (numpy only).

Added 2026-10-31 (hackathon v2). The repo's RL was offline-only with no simulator; this environment gives
  (1) logged transitions for offline RL (CQL, gamma > 0, sequential), and
  (2) an ONLINE ground-truth evaluator: a learned policy's TRUE return can be measured, not only OPE-estimated.

Dynamics (one step = one monsoon day, Jun-Sep = 122 steps):
  forcing  : REAL daily rainfall seasons (NASA POWER PRECTOTCORR, cached by data_adapters/build_geo.py), resampled per episode
  physics  : Iverson (2000) multipulse transient head (ws1b_geophys.iverson) over the last 30 days -> pore pressure ->
             infinite-slope FS with BACK-ANALYSED c' (FS_dry = 1.2)                                   [Class A model]
  hazard   : P(failure today) = sigmoid(alpha + beta * dFS), dFS = FS_dry - FS_t  (alpha, beta: fitted / calibrated by
             kaggle/rl_env_eval.py from the REAL geo_events table + a target seasonal failure rate)  [Class B/ASSUMPTION]
  sensors  : rain gauge (multiplicative noise), piezometer head (additive noise + dropout), model FS estimate
Actions  : 0 HOLD, 1 WATCH, 2 ALARM (= evacuate / close road). Same ACTIONS as deep/offline_rl.py.
Reward   : alarm day -C_FA, watch day -c_watch*C_FA; failure while HOLD -C_miss, WATCH -watch_miss*C_miss, ALARM 0.
           C_FA, C_miss from configs/default.json (5, 100). Episode ends at failure or day 122.
Observation (8): [rain_1d, rain_3d, rain_15d, caine_ratio, piezo_head, fs_est, day_frac, prev_action] — scaled.
Gymnasium-style API (reset/step) without requiring gymnasium. Advisory only: the shield still applies at deployment.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from ..ws1b_geophys.caine import caine_exceedance
from ..ws1b_geophys.fs import factor_of_safety, pore_pressure_from_head
from ..ws1b_geophys.iverson import transient_head_multipulse

ACTIONS = ("HOLD", "WATCH", "ALARM")


@dataclass
class EnvConfig:
    beta_deg: float = 40.0
    phi: float = 32.0; gamma: float = 19.0; z: float = 2.0; K_z: float = 1e-5; D0: float = 5e-5; psi0: float = 0.0
    fs_dry_target: float = 1.2
    alpha: float = -8.0; beta_h: float = 50.0          # hazard logit; overwritten by calibration
    C_FA: float = 5.0; C_miss: float = 100.0; c_watch: float = 0.2; watch_miss: float = 0.5
    rain_noise: float = 0.15; piezo_noise: float = 0.05; piezo_dropout: float = 0.1
    horizon: int = 122; memory_days: int = 30
    seasons: list = field(default_factory=list)        # list of np.ndarray daily rain (mm), length >= horizon + memory


class LandslideAlertEnv:
    obs_dim = 8
    n_actions = 3

    def __init__(self, cfg: EnvConfig, seed: int = 0):
        if not cfg.seasons:
            raise ValueError("EnvConfig.seasons is empty: pass real rainfall seasons (see kaggle/rl_env_eval.py)")
        self.cfg = cfg
        self.rng = np.random.default_rng(seed)
        b, ph = math.radians(cfg.beta_deg), math.radians(cfg.phi)
        gz = cfg.gamma * cfg.z
        self.c_bc = max(0.0, cfg.fs_dry_target * gz * math.sin(b) * math.cos(b) - gz * math.cos(b) ** 2 * math.tan(ph))
        self.fs_dry = float(factor_of_safety(self.c_bc, cfg.phi, cfg.gamma, cfg.z, cfg.beta_deg, u_w=0.0))
        self._true_cache: dict = {}     # season index -> (fs, psi) per day (true physics is deterministic per season)

    # ---------------------------------------------------------------- physics
    def fs_from_rain(self, rain_mm: np.ndarray) -> tuple[float, float]:
        c = self.cfg
        r = np.nan_to_num(rain_mm[-c.memory_days:], nan=0.0)
        t = np.arange(len(r)) * 86400.0
        Iz = np.minimum(r / 1000.0 / 86400.0, c.K_z)
        psi = c.psi0 + float(transient_head_multipulse(c.z, len(r) * 86400.0, t, Iz, c.D0, c.K_z, c.beta_deg))
        psi = min(psi, c.z * math.cos(math.radians(c.beta_deg)) ** 2)
        fs = float(factor_of_safety(self.c_bc, c.phi, c.gamma, c.z, c.beta_deg, u_w=float(pore_pressure_from_head(max(psi, 0.0)))))
        return fs, psi

    def hazard(self, fs: float) -> float:
        return float(1.0 / (1.0 + math.exp(-(self.cfg.alpha + self.cfg.beta_h * (self.fs_dry - fs)))))

    # ---------------------------------------------------------------- API
    def reset(self, seed: int | None = None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.season_idx = int(self.rng.integers(len(self.cfg.seasons)))
        self.season = self.cfg.seasons[self.season_idx]
        self.t = 0; self.prev = 0; self.done = False
        return self._obs(), {}

    def _day_index(self):
        return self.cfg.memory_days + self.t

    def _obs(self):
        c = self.cfg; i = self._day_index()
        hist = self.season[i - c.memory_days + 1: i + 1]
        noisy = hist * np.clip(1 + c.rain_noise * self.rng.standard_normal(len(hist)), 0, None)
        key = (self.season_idx, self.t)
        if key not in self._true_cache:
            self._true_cache[key] = self.fs_from_rain(hist)
        fs, psi = self._true_cache[key]
        self._fs_true, self._psi_true = fs, psi
        dry = np.where(noisy[::-1] < 1.0)[0]
        D = 24.0 * max(1, int(dry[0]) if len(dry) else len(noisy))     # consecutive wet days ending today
        I = noisy[-int(D / 24):].sum() / D
        caine = float(caine_exceedance(max(I, 1e-6), D, 14.0, 0.39)[1])
        piezo = np.nan if self.rng.random() < c.piezo_dropout else psi + c.piezo_noise * self.rng.standard_normal()
        fs_est, _ = self.fs_from_rain(noisy)
        return np.array([np.log1p(noisy[-1]), np.log1p(noisy[-3:].sum()), np.log1p(noisy[-15:].sum()),
                         np.log(max(caine, 1e-3)), 0.0 if np.isnan(piezo) else piezo, fs_est,
                         self.t / c.horizon, self.prev / 2.0], np.float32)

    def step(self, action: int):
        c = self.cfg
        action = int(action)
        fail = self.rng.random() < self.hazard(self._fs_true)
        if fail:
            r = {0: -c.C_miss, 1: -c.watch_miss * c.C_miss, 2: 0.0}[action]
        else:
            r = {0: 0.0, 1: -c.c_watch * c.C_FA, 2: -c.C_FA}[action]
        self.prev = action; self.t += 1
        self.done = fail or self.t >= c.horizon
        info = {"failure": fail, "fs_true": self._fs_true, "hazard": self.hazard(self._fs_true)}
        obs = self._obs() if not self.done else np.zeros(self.obs_dim, np.float32)
        return obs, float(r), self.done, False, info


# -------------------------------------------------------------------- policies + evaluation
def bayes_action(h: float, cfg: EnvConfig) -> int:
    """Myopic Bayes-optimal action for daily failure probability h under the env costs (actions do not change the
    physics, so myopic = optimal per step): argmin {HOLD: h*C_miss, WATCH: (1-h)*c_watch*C_FA + h*watch_miss*C_miss,
    ALARM: (1-h)*C_FA}."""
    costs = (h * cfg.C_miss, (1 - h) * cfg.c_watch * cfg.C_FA + h * cfg.watch_miss * cfg.C_miss, (1 - h) * cfg.C_FA)
    return int(np.argmin(costs))


def physics_rule_policy(obs, p_star: float = 5.0 / 105.0, env: LandslideAlertEnv | None = None) -> int:
    """Rule baseline using ONLY the physics estimate: Bayes action on hazard(fs_est from NOISY rain)."""
    return bayes_action(env.hazard(float(obs[5])), env.cfg) if env is not None else 0


def caine_rule_policy(obs, ratio_watch: float = 0.5, ratio_alarm: float = 1.0) -> int:
    r = math.exp(float(obs[3]))
    return 0 if r < ratio_watch else (1 if r < ratio_alarm else 2)


def rollout(env: LandslideAlertEnv, policy, n_episodes: int = 200, seed: int = 0) -> dict:
    rets, fails, misses, alarm_days, watch_days, lead = [], 0, 0, [], [], []
    for e in range(n_episodes):
        obs, _ = env.reset(seed=seed + e); R = 0.0; ad = wd = 0; done = False; last_alarm = None
        while not done:
            a = policy(obs)
            if a == 2 and last_alarm is None:
                last_alarm = env.t
            obs, r, done, _, info = env.step(a); R += r; ad += a == 2; wd += a == 1
            if a != 2:
                last_alarm = None
            if info["failure"]:
                fails += 1; misses += a != 2
                lead.append(env.t - 1 - last_alarm if (a == 2 and last_alarm is not None) else -1)
        rets.append(R); alarm_days.append(ad); watch_days.append(wd)
    rets = np.asarray(rets)
    return {"return_mean": float(rets.mean()), "return_sd": float(rets.std()), "episodes": n_episodes, "returns": rets.tolist(),
            "failures": fails, "missed_failures": misses, "miss_rate": float(misses / fails) if fails else None,
            "alarm_days_per_season": float(np.mean(alarm_days)), "watch_days_per_season": float(np.mean(watch_days)),
            "mean_lead_days_when_caught": float(np.mean([x for x in lead if x >= 0])) if any(x >= 0 for x in lead) else None}


def log_transitions(env: LandslideAlertEnv, behavior, n_episodes: int, eps: float = 0.3, seed: int = 0) -> dict:
    """Epsilon-randomized behavior logs -> RLTransitionDataset keys. behavior_prob is the exact logging prob."""
    rng = np.random.default_rng(seed)
    S, A, R, S2, D, B = [], [], [], [], [], []
    for e in range(n_episodes):
        obs, _ = env.reset(seed=seed + 10_000 + e); done = False
        while not done:
            g = behavior(obs)
            a = int(rng.integers(3)) if rng.random() < eps else g
            b = (1 - eps + eps / 3) if a == g else eps / 3
            nobs, r, done, _, _ = env.step(a)
            S.append(obs); A.append(a); R.append(r); S2.append(nobs); D.append(float(done)); B.append(b)
            obs = nobs
    return {"s": np.asarray(S, np.float32), "a": np.asarray(A, np.int64), "r": np.asarray(R, np.float32),
            "s_next": np.asarray(S2, np.float32), "done": np.asarray(D, np.float32), "behavior_prob": np.asarray(B, np.float32)}
