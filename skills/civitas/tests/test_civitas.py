"""Executable CIVITAS 1.0 tests; stdlib only."""

import copy
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from civitas_sim import execute, one_run, step, validate  # noqa: E402


class CivicModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / "examples" / "civilization_scenario.json").read_text())

    def test_valid_scenario(self):
        self.assertEqual(validate(self.config)["ticks"], 30)

    def test_identical_seed_repeats(self):
        first = one_run(self.config, 42)
        second = one_run(self.config, 42)
        self.assertEqual(first, second)

    def test_different_seeds_change_shocks(self):
        a = one_run(self.config, 42)
        b = one_run(self.config, 99)
        self.assertNotEqual([t["shocks"] for t in a["trajectory"]],
                            [t["shocks"] for t in b["trajectory"]])

    def test_conservation_and_bounded_variables(self):
        run = one_run(self.config, 1)
        for record in run["trajectory"]:
            for error in record["resource_ledger_error"].values():
                self.assertLess(abs(error), 1e-7)
            self.assertGreaterEqual(record["total_food"], 0)
            self.assertGreaterEqual(record["total_energy"], 0)
        for s in run["final_societies"]:
            self.assertGreater(s["population"], 0)
            self.assertGreaterEqual(s["food"], -1e-8)
            self.assertGreaterEqual(s["energy"], -1e-8)
            for f in ("trust", "knowledge", "legitimacy"):
                self.assertTrue(0 <= s[f] <= 1)

    def test_comparison_uses_matched_seeds(self):
        result = execute(self.config, seed=10, runs=3, compare=True)
        a = result["baseline"]["runs"]
        b = result["comparison"]["alternative"]["runs"]
        self.assertEqual([x["seed"] for x in a], [x["seed"] for x in b])
        self.assertEqual([x["seed"] for x in a], [10, 11, 12])
        self.assertTrue(result["comparison"]["same_seed_pairs"])

    def test_comparison_is_not_fabricated(self):
        result = execute(self.config, seed=42, runs=10, compare=True)
        a = result["baseline"]["summary"]["food_shortfall_total"]["mean"]
        b = result["comparison"]["alternative"]["summary"]["food_shortfall_total"]["mean"]
        self.assertGreaterEqual(b, a)

    def test_invalid_inputs_rejected(self):
        cfg = copy.deepcopy(self.config)
        cfg["parameters"]["resource_shock_probability"] = -0.01
        with self.assertRaises(ValueError):
            validate(cfg)
        cfg = copy.deepcopy(self.config)
        cfg["societies"][1]["id"] = cfg["societies"][0]["id"]
        with self.assertRaises(ValueError):
            validate(cfg)
        with self.assertRaises(ValueError):
            execute(self.config, runs=0)

    def test_minimal_one_society(self):
        cfg = copy.deepcopy(self.config)
        cfg["societies"] = cfg["societies"][:1]
        out = execute(cfg, seed=42, runs=1)
        self.assertTrue(math.isfinite(out["baseline"]["runs"][0]["metrics"]["total_population"]))


if __name__ == "__main__":
    unittest.main()
