"""ws7_iot.lora_codec — compact binary LoRa frame codec (M7, offline uplink path).

COMPONENT_DESIGN.md §3.1. Target <=51 B payload on IN865-867. Fields are bit/scale-quantized and packed
with struct. Node id is carried as a 6-char ASCII tail-id. Round-trips within quantization tolerance.
Does NOT include the signature (that rides in the application layer / separate field) to keep the on-air
frame tiny; integrity for the demo uses the SensorReading HMAC at the app layer.
"""
from __future__ import annotations

import struct

# layout (big-endian):
#   6s  node tail-id (ascii, space-padded)
#   H   seq (uint16)
#   h   tilt0 centi-deg (int16, 0.01 deg)
#   h   tilt1 centi-deg
#   h   tilt_rate milli-deg/s (int16, 0.001 dps)
#   B   soil0 (uint8, 0..200 => 0..1.00 vwc, scale 0.005)
#   B   soil1
#   H   piezo (uint16, 0.1 kPa)
#   H   rain_15m (uint16, 0.1 mm)
#   h   temp (int16, 0.01 C)
#   H   batt_mV (uint16)
#   B   edge flag (0 NONE,1 WATCH,2 LOCAL_SIREN)
_FMT = ">6sHhhhBBHHhHB"
FRAME_LEN = struct.calcsize(_FMT)   # == 25 bytes (<=51 OK)

_EDGE = {"NONE": 0, "WATCH": 1, "LOCAL_SIREN": 2}
_EDGE_INV = {v: k for k, v in _EDGE.items()}


def encode_frame(node_id: str, seq: int, readings: dict, batt_mV: int, edge_level: str = "NONE") -> bytes:
    tail = node_id[-6:].rjust(6).encode("ascii")[:6]
    tilt = readings.get("tilt_deg", [0.0, 0.0])
    soil = readings.get("soil_vwc", [0.0, 0.0])
    return struct.pack(
        _FMT, tail, seq & 0xFFFF,
        int(round(tilt[0] * 100)), int(round(tilt[1] * 100)),
        int(round(readings.get("tilt_rate_dps", 0.0) * 1000)),
        int(round(soil[0] / 0.005)), int(round(soil[1] / 0.005)),
        int(round(readings.get("piezo_kPa", 0.0) * 10)) & 0xFFFF,
        int(round(readings.get("rain_mm_15m", 0.0) * 10)) & 0xFFFF,
        int(round(readings.get("temp_C", 0.0) * 100)),
        int(batt_mV) & 0xFFFF, _EDGE.get(edge_level, 0),
    )


def decode_frame(buf: bytes) -> dict:
    (tail, seq, t0, t1, tr, s0, s1, piezo, rain, temp, batt, edge) = struct.unpack(_FMT, buf)
    return {
        "node_tail": tail.decode("ascii").strip(),
        "seq": seq,
        "readings": {
            "tilt_deg": [t0 / 100.0, t1 / 100.0],
            "tilt_rate_dps": tr / 1000.0,
            "soil_vwc": [s0 * 0.005, s1 * 0.005],
            "piezo_kPa": piezo / 10.0,
            "rain_mm_15m": rain / 10.0,
            "temp_C": temp / 100.0,
        },
        "batt_mV": batt,
        "edge_level": _EDGE_INV.get(edge, "NONE"),
    }
