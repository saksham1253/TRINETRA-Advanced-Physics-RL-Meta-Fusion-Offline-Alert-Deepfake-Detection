import math
import unittest

from trinetra.ws3_alert.last_mile import (Conditions, Node, Params, Village, demo_valley, fspl_db, greedy_upgrades,
                                          lora_airtime_s, lora_range_km, plan, single_points_of_failure, siren_radius_m, summary)


class TestLastMile(unittest.TestCase):
    def test_airtime_matches_semtech_reference(self):
        # Semtech calculator reference values: SF7/BW125/CR4/5, 10-byte payload, 8 preamble ≈ 41.2 ms; SF12 ≈ 991 ms
        self.assertAlmostEqual(lora_airtime_s(10, 7) * 1000, 41.2, delta=0.5)
        self.assertAlmostEqual(lora_airtime_s(10, 12) * 1000, 991.2, delta=2.0)

    def test_fspl_and_range_monotone(self):
        self.assertAlmostEqual(fspl_db(1000, 866), 91.19, delta=0.05)
        self.assertGreater(lora_range_km(12, "ridge_los"), lora_range_km(7, "ridge_los"))
        self.assertGreater(lora_range_km(10, "ridge_los"), lora_range_km(10, "valley_nlos"))
        self.assertGreater(lora_range_km(10, "hill_forest"), 0.1)     # far beyond Bluetooth's ~0.1 km

    def test_siren_radius_physics(self):
        r = siren_radius_m()
        self.assertTrue(400 < r < 3000)
        self.assertGreater(siren_radius_m(l_ref_db=126), r)            # louder siren covers more

    def test_internet_and_cell_down_still_reaches_most(self):
        V, N = demo_valley(); p = Params()
        res = plan(V, N, Conditions(internet=False, cell=False, grid_power=False), p)
        s = summary(res, p.deadline_min)
        self.assertGreater(s["share_population_by_deadline"], 0.5)
        self.assertTrue(all(r.minutes is not None for r in res))       # runner fallback reaches everyone eventually

    def test_spof_and_greedy(self):
        V, N = demo_valley(); p = Params()
        spof = single_points_of_failure(V, N, Conditions(), p)
        self.assertIn("GW-HQ", spof)                                    # the only gateway is a single point of failure
        picks = greedy_upgrades(V, N, Conditions(), p, k=2)
        self.assertTrue(all(x["population_gained"] > 0 for x in picks))

    def test_no_channels_means_runner_only(self):
        V = [Village("A", 0, 0, 100), Village("B", 5, 0, 100)]
        N = [Node("GW", 0, 0, "gateway")]
        res = {r.id: r for r in plan(V, N, Conditions(satellite=False), Params())}
        self.assertTrue(res["B"].channel.startswith("runner"))
        self.assertAlmostEqual(res["B"].minutes, 5 / 2.5 * 60, delta=1e-6)


if __name__ == "__main__":
    unittest.main()
