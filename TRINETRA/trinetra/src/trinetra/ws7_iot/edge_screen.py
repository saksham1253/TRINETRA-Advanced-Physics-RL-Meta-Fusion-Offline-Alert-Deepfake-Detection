"""ws7_iot.edge_screen — Tier-0 node-local pre-screen (M7, offline autonomy within strict bounds).

The node may raise its OWN co-located siren (LOCAL_SIREN) under a HARD physical rule, with NO network and
NO model (constraint C1). It may NEVER issue a public/network alert autonomously (Rule 19) — that stays
human-gated at the gateway. This function returns only an edge level + the rule that fired.
"""
from __future__ import annotations


def node_local_edge_flag(readings: dict,
                         tilt_rate_siren: float = 5.0,     # deg/s? no -> deg/day proxy; see note
                         tilt_rate_watch: float = 2.0,
                         rain_15m_watch: float = 20.0) -> dict:
    """Deterministic Tier-0 screen. Returns {'level','rule'}.

    LOCAL_SIREN requires BOTH fast tilt-rate AND heavy recent rain (two independent physical cues) so a
    single noisy sensor cannot fire the local siren. Thresholds are illustrative and must be field-tuned.
    """
    tr = float(readings.get("tilt_rate_dps", 0.0))
    rain = float(readings.get("rain_mm_15m", 0.0))

    if tr >= tilt_rate_siren and rain >= rain_15m_watch:
        return {"level": "LOCAL_SIREN", "rule": "tilt_rate>=siren AND rain>=watch (two cues)"}
    if tr >= tilt_rate_watch or rain >= rain_15m_watch:
        return {"level": "WATCH", "rule": "single elevated cue"}
    return {"level": "NONE", "rule": None}
