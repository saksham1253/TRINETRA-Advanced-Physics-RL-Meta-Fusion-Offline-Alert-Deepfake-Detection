"""IoT node tests (M7, gate G5): LoRa codec round-trip, signing, replay, edge screen."""
import unittest

from trinetra.ws7_iot import (
    encode_frame, decode_frame, FRAME_LEN,
    SensorReading, sign_reading, verify_reading, validate_reading, ReplayGuard, node_local_edge_flag,
)


class TestLoRaCodec(unittest.TestCase):
    def test_frame_within_budget(self):
        self.assertLessEqual(FRAME_LEN, 51)

    def test_roundtrip(self):
        readings = {"tilt_deg": [1.23, -0.45], "tilt_rate_dps": 0.08, "soil_vwc": [0.31, 0.28],
                    "piezo_kPa": 42.1, "rain_mm_15m": 6.4, "temp_C": 14.2}
        buf = encode_frame("SS-UK-00123", seq=10492, readings=readings, batt_mV=3920, edge_level="WATCH")
        self.assertEqual(len(buf), FRAME_LEN)
        d = decode_frame(buf)
        self.assertEqual(d["seq"], 10492)
        self.assertEqual(d["edge_level"], "WATCH")
        self.assertAlmostEqual(d["readings"]["tilt_deg"][0], 1.23, places=2)
        self.assertAlmostEqual(d["readings"]["rain_mm_15m"], 6.4, places=1)
        self.assertAlmostEqual(d["readings"]["temp_C"], 14.2, places=2)


class TestAuthReplay(unittest.TestCase):
    def _reading(self, seq=1):
        return SensorReading(node_id="SS-UK-00123", zone_id="UK-CHX-07", t="2026-10-10T08:46:00Z",
                             seq=seq, batt_mV=3900,
                             readings={"tilt_deg": [1.0, 0.0], "tilt_rate_dps": 0.0,
                                       "soil_vwc": [0.3, 0.3], "rain_mm_15m": 1.0, "temp_C": 12.0})

    def test_sign_verify(self):
        key = b"node-key-123"
        r = sign_reading(self._reading(), key)
        self.assertTrue(verify_reading(r, key))

    def test_tamper_detected(self):
        key = b"node-key-123"
        r = sign_reading(self._reading(), key)
        r.readings["tilt_deg"] = [9.0, 9.0]            # tamper after signing
        self.assertFalse(verify_reading(r, key))

    def test_replay_rejected(self):
        g = ReplayGuard()
        self.assertTrue(g.accept("n1", 5))
        self.assertFalse(g.accept("n1", 5))            # replay
        self.assertFalse(g.accept("n1", 3))            # older
        self.assertTrue(g.accept("n1", 6))

    def test_validation(self):
        self.assertEqual(validate_reading(self._reading()), [])
        bad = self._reading(); bad.batt_mV = 9999
        self.assertTrue(any("batt_mV" in p for p in validate_reading(bad)))


class TestEdgeScreen(unittest.TestCase):
    def test_two_cues_local_siren(self):
        f = node_local_edge_flag({"tilt_rate_dps": 6.0, "rain_mm_15m": 25.0})
        self.assertEqual(f["level"], "LOCAL_SIREN")

    def test_single_cue_watch(self):
        f = node_local_edge_flag({"tilt_rate_dps": 6.0, "rain_mm_15m": 0.0})
        self.assertEqual(f["level"], "WATCH")

    def test_quiet_none(self):
        f = node_local_edge_flag({"tilt_rate_dps": 0.1, "rain_mm_15m": 0.0})
        self.assertEqual(f["level"], "NONE")


if __name__ == "__main__":
    unittest.main()
