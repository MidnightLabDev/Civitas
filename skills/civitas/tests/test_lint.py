"""Tests for the CIVITAS 1.0 response linter."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lint_response import lint  # noqa: E402


class LintTests(unittest.TestCase):
    def test_bad_answer_flagged(self):
        bad = ("Our simulation proves that the empire will inevitably fall. There is an 82% chance of collapse "
               "by 2040 (Smith et al., 2031).")
        res = lint(bad)
        codes = {f["code"] for f in res["findings"]}
        self.assertIn("CERTAINTY", codes)
        self.assertIn("UNSOURCED_PROBABILITY", codes)
        self.assertIn("FUTURE_CITATION", codes)
        self.assertFalse(res["pass"])

    def test_good_answer_passes(self):
        good = ("In this model [E3], under its assumptions, the simulation shows fewer crises when growth slows "
                "(10 seeds, 42-51). From a reference class of 3 cases in 20, the base rate is about 15% [E2].")
        res = lint(good)
        self.assertTrue(res["pass"], res["findings"])

    def test_model_as_reality(self):
        res = lint("The simulation shows universal basic income increases trust.")
        self.assertIn("MODEL_AS_REALITY", {f["code"] for f in res["findings"]})

    def test_long_quote(self):
        res = lint('"' + "word " * 60 + '"')
        self.assertIn("LONG_QUOTE", {f["code"] for f in res["findings"]})


if __name__ == "__main__":
    unittest.main()
