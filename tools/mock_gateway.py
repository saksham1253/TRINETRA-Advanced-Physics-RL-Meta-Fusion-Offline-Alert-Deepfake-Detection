"""TRINETRA mock inference gateway (stdlib only): streams LIVE events that are decided by the REPO'S OWN PYTHON CODE.

Every event = one real out-of-fold image score triple (fire_cnn, CLIP zero-shot, CLIP probe) from the evidence bank
(src/console/data/evidence_bank.json), fused with trinetra.ws5_fusion_rl.fusion_models.fuse and decided with
trinetra.ws5_fusion_rl.decision.decide, at a SYNTHETIC camera location. So LIVE mode exercises the real Python decision path;
the camera feed itself is a replay of real model outputs, not a camera.

Endpoints (CORS open, for the local console only):
  GET  /health             -> {"ok": true, "model": {...}}
  GET  /params             -> adjustable-at-inference parameters + those that require retraining
  POST /params  {id: val}  -> applies inference-time parameters, returns the recomputed last event per source
  GET  /stream             -> Server-Sent Events, one event per source per tick (live_event.schema.json)
Run:   python3 tools/mock_gateway.py --port 8765
Record a replay file:  python3 tools/mock_gateway.py --record 240 --out public/replay/session_demo.jsonl
"""
import argparse, json, math, random, sys, threading, time
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "TRINETRA/trinetra/src"))
from trinetra.common.config import Config                                     # noqa: E402
from trinetra.common.types import ExpertOutput                                # noqa: E402
from trinetra.ws5_fusion_rl.adapters import deep_expert                       # noqa: E402
from trinetra.ws5_fusion_rl.decision import decide                            # noqa: E402
from trinetra.ws5_fusion_rl.fusion_models import fuse                         # noqa: E402

BANK = json.load(open(Path(__file__).resolve().parents[1] / "src/console/data/evidence_bank.json"))
COL = {c: i for i, c in enumerate(BANK["columns"])}
POS = [r for r in BANK["rows"] if r[0] == 1]
NEG = [r for r in BANK["rows"] if r[0] == 0]
PI = BANK["n_pos"] / BANK["n"]
SOURCES = [  # synthetic camera positions inside the demo regions
    ("CAM-UK-01", 30.420, 79.470, 20), ("CAM-UK-02", 30.470, 79.520, None), ("CAM-KL-01", 11.680, 76.080, 60),
    ("CAM-MP-01", 22.280, 80.620, None), ("CAM-PB-01", 30.310, 75.970, 120), ("CAM-GJ-01", 20.370, 72.930, None),
]
ADJUSTABLE = {"fusion.model": "FM-1", "fusion.tau": 0.5, "fusion.lambda": 0.3, "cost.C_FA": 5.0, "cost.C_miss": 100.0,
              "dec.uncertain": 0.6, "fusion.prior": PI}
RETRAIN = ["fire.*", "geo.*", "sur.*", "trust.* (reliability caps are policy, change in adapters.py)", "cctv.* (edge firmware)", "lora.*"]
STATE = {"params": dict(ADJUSTABLE), "tick": 0, "last": {}}
LOCK = threading.Lock()


def h2(p):
    p = min(max(p, 1e-6), 1 - 1e-6)
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def shift(p, target):
    if abs(target - PI) < 1e-9:
        return p
    a, b = p * target / PI, (1 - p) * (1 - target) / (1 - PI)
    return a / (a + b)


def event(src, tick, row, active, mode="LIVE"):
    P = STATE["params"]
    cfg = Config(); cfg.data["fusion"]["model"] = "GMF" if P["fusion.model"] == "GMF" else "FM-1"
    cfg.data["fusion"]["operator"]["pharaoh"] = P["fusion.model"] == "PHARAOH"
    cfg.data["fusion"]["tau"] = float(P["fusion.tau"]); cfg.data["fusion"]["lambda"] = float(P["fusion.lambda"])
    cfg.data["cost"] = {"C_FA": float(P["cost.C_FA"]), "C_miss": float(P["cost.C_miss"])}
    names = [("fire_cnn", "cal_fire_cnn"), ("zeroshot", "cal_zeroshot"), ("clip_probe", "cal_clip_probe")]
    ps = {n: shift(row[COL[c]], float(P["fusion.prior"])) for n, c in names}
    ex = [deep_expert(n, p, uncertainty=0.5 * h2(p)) for n, p in ps.items()]
    f = fuse(ex, cfg)
    d = decide(ex, None, cfg, uncertain_threshold=float(P["dec.uncertain"]))
    sid, lat, lon, start = src
    t = datetime(2026, 11, 1, 6, 0, tzinfo=timezone.utc) + timedelta(seconds=30 * tick)
    return {"schema_version": "1.0", "mode": mode,
            "model": {"name": "trinetra-fire-stack", "version": "prototype-v1", "run_id": BANK["run_ids"]["fire_cnn"],
                      "checkpoint_hash": None, "trained_on": "prototype-v1 D-Fire subset (OOF)"},
            "source_id": sid, "location": {"lat": lat, "lon": lon, "elevation": None, "accuracy_m": 50, "location_origin": "SYNTHETIC"},
            "timestamp_utc": t.isoformat().replace("+00:00", "Z"),
            "modules": [{"id": n, "status": "IMPLEMENTED", "score": round(p, 4), "uncertainty": round(0.5 * h2(p), 4), "validity_flag": True,
                         "origin": "REPLAYED" if mode == "REPLAY" else "LIVE", "parameters_used": {"prior": P["fusion.prior"]}} for n, p in ps.items()]
                       + [{"id": "satellite", "status": "PLANNED", "score": None, "uncertainty": None, "origin": "SIMULATED"},
                          {"id": "iot", "status": "PLANNED", "score": None, "uncertainty": None, "origin": "SIMULATED"}],
            "physics": [],
            "fusion": {"technique": f.model, "inputs": [n for n, _ in names], "weights": [], "calibrated_probability": round(f.p, 5),
                       "uncertainty": round(f.u_star, 4), "abstained": bool(d.uncertain), "reason": "U* above threshold" if d.uncertain else None,
                       "cost_ratio": float(P["cost.C_miss"]) / float(P["cost.C_FA"]), "threshold": round(cfg.p_star, 5)},
            "decision": {"tier": d.level.name, "requires_approval": True, "explanation_template_id": "tier_v1",
                         "explanation_values": {"risk": round(d.risk, 4), "p_star": round(cfg.p_star, 4), "reliability": d.conformal.reliability.value}},
            "network": {"internet": True, "cellular": True, "lora": True},
            "ground_truth": {"hazard_active": active, "note": "label of the real image row; camera location synthetic"},
            "notes": "decided by the repo Python fuse()/decide() on a real out-of-fold image score"}


def tick_events(mode="LIVE", rng=random.Random(7)):
    with LOCK:
        k = STATE["tick"]; STATE["tick"] += 1
        out = []
        for src in SOURCES:
            active = src[3] is not None and k * 0.5 >= src[3]
            row = rng.choice(POS if active else NEG)
            e = event(src, k, row, active, mode); STATE["last"][src[0]] = (src, k, row, active); out.append(e)
        return out


class H(BaseHTTPRequestHandler):
    def _h(self, code=200, ctype="application/json"):
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "content-type, authorization"); self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def log_message(self, *a):
        pass

    def do_OPTIONS(self):
        self._h(204)

    def do_GET(self):
        if self.path.startswith("/health"):
            self._h(); self.wfile.write(json.dumps({"ok": True, "model": {"name": "trinetra-fire-stack", "run_id": BANK["run_ids"]["fire_cnn"]}}).encode())
        elif self.path.startswith("/params"):
            self._h(); self.wfile.write(json.dumps({"adjustable": STATE["params"], "requires_retraining": RETRAIN}).encode())
        elif self.path.startswith("/stream"):
            self._h(ctype="text/event-stream"); self.wfile.flush()
            try:
                while True:
                    for e in tick_events():
                        self.wfile.write(f"data: {json.dumps(e)}\n\n".encode())
                    self.wfile.flush(); time.sleep(1.0)
            except (BrokenPipeError, ConnectionResetError):
                return
        else:
            self._h(404); self.wfile.write(b"{}")

    def do_POST(self):
        if not self.path.startswith("/params"):
            self._h(404); return
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        bad = [k for k in body if k not in ADJUSTABLE]
        with LOCK:
            for k, v in body.items():
                if k in ADJUSTABLE:
                    STATE["params"][k] = v
            recomputed = [event(*STATE["last"][s]) for s in STATE["last"]]
        self._h(); self.wfile.write(json.dumps({"applied": {k: v for k, v in body.items() if k in ADJUSTABLE}, "rejected_requires_retraining": bad,
                                                "recomputed": recomputed}).encode())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--record", type=int, default=0, help="write N ticks to --out as REPLAY events and exit")
    ap.add_argument("--out", default="public/replay/session_demo.jsonl")
    a = ap.parse_args()
    if a.record:
        with open(a.out, "w") as f:
            for _ in range(a.record):
                for e in tick_events("REPLAY"):
                    f.write(json.dumps(e) + "\n")
        print("recorded", a.record * len(SOURCES), "events ->", a.out); return
    print(f"TRINETRA mock gateway on http://localhost:{a.port}  (stream: /stream, params: /params)")
    ThreadingHTTPServer(("0.0.0.0", a.port), H).serve_forever()


if __name__ == "__main__":
    main()
