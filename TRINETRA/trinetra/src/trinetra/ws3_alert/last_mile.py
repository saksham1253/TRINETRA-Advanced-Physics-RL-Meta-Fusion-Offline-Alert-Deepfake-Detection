"""ws3_alert.last_mile — offline LAST-MILE alert planner (stdlib only).

Problem: when the internet and mobile towers are down, Bluetooth (≈10–100 m) cannot reach scattered hill villages.
This module answers, for every village: *how many minutes until people hear the warning, through which channel, and what
breaks if one relay or siren fails?* It combines independent channels and keeps the earliest one:

  1. LoRa mesh  gateway → ridge relays → village "pager" (buzzer + light + Hindi text), km-scale hops at 865–867 MHz;
  2. sirens     triggered over the same mesh; audible radius from a spherical-spreading + excess-attenuation model;
  3. satellite  short-message receivers (e.g. GAGAN/NavIC messaging, INCOIS GEMINI-type) — works with no ground network;
  4. cell broadcast / FM / community radio — only if towers or stations are up;
  5. human relay  a runner (Aapda Mitra / volunteer) from the nearest already-warned place.

Physics and parameter sources (planning values; field calibration is required):
  * LoRa time-on-air: Semtech SX1272/76 formula (AN1200.13). Sensitivity by SF from the SX1276 datasheet (BW 125 kHz).
  * Link budget: log-distance path loss PL(d) = FSPL(1 m) + 10·n·log10(d / 1 m); exponent n by terrain class is an
    ASSUMPTION (LOS ridge 2.2, hill-forest 3.0, deep valley NLOS 3.6) and must be fitted from a site survey.
  * India 865–867 MHz is licence-exempt (WPC GSR 1048(E), 2005: ≤ 1 W transmit, ≤ 4 W EIRP); default Tx 30 dBm = E32-900T30D.
  * Siren: L(r) = L_ref − 20·log10(r / r_ref) − α·(r − r_ref); default 120 dB at 30 m, α = 1 dB / 100 m (hills, ASSUMPTION),
    alerting contour 70 dB (common outdoor warning-siren design contour).
No hardware is driven here; outputs are plans and coverage numbers for a human planner.
"""
from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field

# --------------------------------------------------------------------------------------------- LoRa radio
SX1276_SENS_DBM = {7: -123.0, 8: -126.0, 9: -129.0, 10: -132.0, 11: -134.5, 12: -137.0}   # BW 125 kHz, datasheet
TERRAIN_N = {"ridge_los": 2.2, "hill_forest": 3.0, "valley_nlos": 3.6}                    # path-loss exponent (ASSUMPTION)


def lora_airtime_s(payload_bytes: int, sf: int = 10, bw_hz: float = 125e3, cr: int = 1, preamble: int = 8,
                   explicit_header: bool = True, crc: bool = True) -> float:
    """Semtech LoRa time-on-air in seconds (AN1200.13). cr=1..4 means coding rate 4/5..4/8."""
    t_sym = (2 ** sf) / bw_hz
    de = 1 if (sf >= 11 and bw_hz <= 125e3) else 0          # low-data-rate optimisation
    ih = 0 if explicit_header else 1
    num = 8 * payload_bytes - 4 * sf + 28 + 16 * (1 if crc else 0) - 20 * ih
    n_payload = 8 + max(math.ceil(num / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (preamble + 4.25) * t_sym + n_payload * t_sym


def fspl_db(d_m: float, f_mhz: float = 866.0) -> float:
    """Free-space path loss in dB (d in metres, f in MHz)."""
    return 20 * math.log10(max(d_m, 1e-3) / 1000.0) + 20 * math.log10(f_mhz) + 32.44


def lora_range_km(sf: int = 10, terrain: str = "hill_forest", tx_dbm: float = 30.0, g_tx_dbi: float = 2.0,
                  g_rx_dbi: float = 2.0, cable_loss_db: float = 1.0, fade_margin_db: float = 15.0, f_mhz: float = 866.0) -> float:
    """Distance (km) at which received power meets sensitivity + fade margin under the log-distance model."""
    budget = tx_dbm + g_tx_dbi + g_rx_dbi - cable_loss_db - (SX1276_SENS_DBM[sf] + fade_margin_db)
    pl_1m = fspl_db(1.0, f_mhz)
    n = TERRAIN_N[terrain]
    return 10 ** ((budget - pl_1m) / (10 * n)) / 1000.0


# --------------------------------------------------------------------------------------------- siren acoustics
def siren_level_db(r_m: float, l_ref_db: float = 120.0, r_ref_m: float = 30.0, alpha_db_per_m: float = 0.01) -> float:
    r = max(r_m, r_ref_m)
    return l_ref_db - 20 * math.log10(r / r_ref_m) - alpha_db_per_m * (r - r_ref_m)


def siren_radius_m(l_ref_db: float = 120.0, r_ref_m: float = 30.0, alpha_db_per_m: float = 0.01, contour_db: float = 70.0) -> float:
    """Radius where the siren falls to the alerting contour (bisection; monotone decreasing level)."""
    lo, hi = r_ref_m, 50_000.0
    if siren_level_db(lo, l_ref_db, r_ref_m, alpha_db_per_m) <= contour_db:
        return lo
    for _ in range(80):
        mid = (lo + hi) / 2
        if siren_level_db(mid, l_ref_db, r_ref_m, alpha_db_per_m) > contour_db:
            lo = mid
        else:
            hi = mid
    return lo


# --------------------------------------------------------------------------------------------- scenario model
@dataclass
class Village:
    id: str
    x_km: float
    y_km: float
    population: int
    has_pager: bool = False             # LoRa receiver with buzzer/light/text (also acts as a relay when powered)
    has_satellite_rx: bool = False      # satellite short-message receiver
    cell_coverage: bool = True
    fm_coverage: bool = False


@dataclass
class Node:
    id: str
    x_km: float
    y_km: float
    kind: str                           # "gateway" | "relay" | "siren"
    terrain: str = "hill_forest"        # terrain class of links that touch this node
    battery_ok: bool = True


@dataclass
class Conditions:
    internet: bool = False
    cell: bool = False
    grid_power: bool = False
    fm: bool = False
    satellite: bool = True


@dataclass
class Params:
    sf: int = 10
    payload_bytes: int = 24             # compact alert frame (level, zone, code, timestamp, signature tail)
    hop_processing_s: float = 0.5
    deadline_min: float = 10.0
    runner_kmh: float = 2.5             # mountain trail walking speed (ASSUMPTION)
    cell_broadcast_min: float = 1.0
    fm_min: float = 3.0
    satellite_min: float = 3.0
    siren_contour_db: float = 70.0
    siren_alpha_db_per_m: float = 0.01
    max_hop_km: float = 30.0            # planning cap: Fresnel clearance / earth curvature / unproven long links


@dataclass
class VillageResult:
    id: str
    population: int
    minutes: float | None
    channel: str
    path: list[str] = field(default_factory=list)
    channels_available: int = 0


def _dist(a, b) -> float:
    return math.hypot(a.x_km - b.x_km, a.y_km - b.y_km)


def _mesh_times(villages, nodes, params: Params, cond: Conditions, disabled: set[str]):
    """Dijkstra over the LoRa mesh from powered gateways. Pagers relay too. Returns {id: (seconds, path)}."""
    hop_s = lora_airtime_s(params.payload_bytes, params.sf) * 2 + params.hop_processing_s   # airtime + listen-before-talk backoff
    pts = {n.id: n for n in nodes if n.id not in disabled and n.battery_ok and n.kind in ("gateway", "relay", "siren")}
    pts.update({v.id: v for v in villages if v.has_pager and v.id not in disabled})
    terr = {n.id: n.terrain for n in nodes}
    rng_cache = {t: min(lora_range_km(params.sf, t), params.max_hop_km) for t in TERRAIN_N}
    start = [n.id for n in nodes if n.kind == "gateway" and n.id in pts]
    best = {s: (0.0, [s]) for s in start}
    pq = [(0.0, s) for s in start]
    while pq:
        t, u = heapq.heappop(pq)
        if t > best[u][0]:
            continue
        if u in pts and isinstance(pts[u], Node) and pts[u].kind == "siren":
            continue                                   # sirens receive but do not rebroadcast
        for v, pv in pts.items():
            if v == u:
                continue
            tclass = min(terr.get(u, "hill_forest"), terr.get(v, "hill_forest"), key=lambda k: -TERRAIN_N[k])  # worse link wins
            if _dist(pts[u], pv) <= rng_cache[tclass]:
                nt = t + hop_s
                if v not in best or nt < best[v][0]:
                    best[v] = (nt, best[u][1] + [v]); heapq.heappush(pq, (nt, v))
    return best


def plan(villages: list[Village], nodes: list[Node], cond: Conditions | None = None, params: Params | None = None,
         disabled: set[str] | None = None) -> list[VillageResult]:
    cond = cond or Conditions(); params = params or Params(); disabled = disabled or set()
    mesh = _mesh_times(villages, nodes, params, cond, disabled)
    r_siren_km = siren_radius_m(alpha_db_per_m=params.siren_alpha_db_per_m, contour_db=params.siren_contour_db) / 1000.0
    out: dict[str, VillageResult] = {}
    for v in villages:
        opts = []
        if v.has_pager and v.id in mesh:
            opts.append((mesh[v.id][0] / 60.0, "LoRa pager", mesh[v.id][1]))
        for n in nodes:
            if n.kind == "siren" and n.id in mesh and _dist(n, v) <= r_siren_km:
                opts.append((mesh[n.id][0] / 60.0 + 0.1, f"siren {n.id}", mesh[n.id][1]))
        if cond.cell and v.cell_coverage:
            opts.append((params.cell_broadcast_min, "cell broadcast", []))
        if cond.fm and v.fm_coverage:
            opts.append((params.fm_min, "FM / community radio", []))
        if cond.satellite and v.has_satellite_rx:
            opts.append((params.satellite_min, "satellite message", []))
        opts.sort(key=lambda o: o[0])
        out[v.id] = VillageResult(v.id, v.population, opts[0][0] if opts else None, opts[0][1] if opts else "none",
                                  opts[0][2] if opts else [], len(opts))
    # human relay: a runner from the nearest warned village or powered mesh node (repeat until no improvement)
    sources = {n.id: (n, mesh[n.id][0] / 60.0) for n in nodes if n.id in mesh and n.kind != "siren"}
    for _ in range(len(villages)):
        changed = False
        warned = [(v, out[v.id].minutes) for v in villages if out[v.id].minutes is not None]
        for v in villages:
            cand = [(m + _dist(s, v) / params.runner_kmh * 60.0, s.id) for s, m in warned if s.id != v.id]
            cand += [(m + _dist(n, v) / params.runner_kmh * 60.0, n.id) for n, m in sources.values()]
            if not cand:
                continue
            t, via = min(cand)
            r = out[v.id]
            if r.minutes is None or t < r.minutes - 1e-9:
                r.minutes, r.channel, r.path = t, f"runner from {via}", [via, v.id]; changed = True
        if not changed:
            break
    return [out[v.id] for v in villages]


def mesh_unreachable(villages, nodes, cond=None, params=None, disabled=None) -> list[str]:
    """Relays / sirens the LoRa mesh cannot reach (e.g. a valley siren without line of sight to any relay)."""
    mesh = _mesh_times(villages, nodes, params or Params(), cond or Conditions(), disabled or set())
    return [n.id for n in nodes if n.id not in mesh and n.id not in (disabled or set())]


def summary(results: list[VillageResult], deadline_min: float) -> dict:
    pop = sum(r.population for r in results)
    ok = [r for r in results if r.minutes is not None and r.minutes <= deadline_min]
    return {"villages": len(results), "population": pop, "reached_by_deadline": len(ok),
            "population_by_deadline": sum(r.population for r in ok),
            "share_population_by_deadline": (sum(r.population for r in ok) / pop) if pop else 0.0,
            "late_or_unreached": [r.id for r in results if r.minutes is None or r.minutes > deadline_min]}


def single_points_of_failure(villages, nodes, cond=None, params=None) -> dict:
    """For each relay / siren / gateway: villages that miss the deadline only when THAT element fails."""
    params = params or Params()
    base = {r.id for r in plan(villages, nodes, cond, params) if r.minutes is not None and r.minutes <= params.deadline_min}
    spof = {}
    for n in nodes:
        res = plan(villages, nodes, cond, params, disabled={n.id})
        lost = sorted(base - {r.id for r in res if r.minutes is not None and r.minutes <= params.deadline_min})
        if lost:
            spof[n.id] = lost
    return spof


def greedy_upgrades(villages, nodes, cond=None, params=None, k: int = 3) -> list[dict]:
    """Pick up to k villages to receive a pager (receiver + relay) that most increase population reached by the deadline."""
    params = params or Params(); vs = [Village(**vars(v)) for v in villages]; picks = []
    for _ in range(k):
        base = summary(plan(vs, nodes, cond, params), params.deadline_min)["population_by_deadline"]
        best = None
        for i, v in enumerate(vs):
            if v.has_pager:
                continue
            trial = [Village(**vars(x)) for x in vs]; trial[i].has_pager = True
            gain = summary(plan(trial, nodes, cond, params), params.deadline_min)["population_by_deadline"] - base
            if gain > 0 and (best is None or gain > best[1]):
                best = (i, gain)
        if best is None:
            break
        vs[best[0]].has_pager = True
        picks.append({"village": vs[best[0]].id, "population_gained": best[1]})
    return picks


def demo_valley() -> tuple[list[Village], list[Node]]:
    """SYNTHETIC hill-valley layout (not a real map): 12 villages across ~25 km, one block-HQ gateway, ridge relays, sirens."""
    V = [Village("V01", 1.0, 0.5, 820, True, cell_coverage=True), Village("V02", 3.2, 1.8, 410, True), Village("V03", 5.5, 0.9, 260),
         Village("V04", 7.8, 2.6, 530, True), Village("V05", 9.6, 4.2, 190), Village("V06", 11.9, 3.1, 340, True, True),
         Village("V07", 14.4, 5.6, 120), Village("V08", 16.1, 3.9, 610, True), Village("V09", 18.7, 6.8, 90, False, True),
         Village("V10", 20.3, 4.4, 280, fm_coverage=True), Village("V11", 22.8, 7.9, 150, fm_coverage=True),
         Village("V12", 24.6, 5.2, 70, fm_coverage=True)]
    N = [Node("GW-HQ", 0.0, 0.0, "gateway", "ridge_los"), Node("R1-ridge", 6.5, 4.0, "relay", "ridge_los"),
         Node("R2-ridge", 15.0, 7.5, "relay", "ridge_los"), Node("S1", 5.4, 1.2, "siren", "hill_forest"),
         Node("S2", 16.0, 4.2, "siren", "hill_forest"), Node("S3", 21.0, 4.9, "siren", "valley_nlos")]
    return V, N
