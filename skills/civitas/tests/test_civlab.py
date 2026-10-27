"""CIVITAS 1.0 civlab test suite (stdlib unittest). Run from the skill root:
    python -m unittest discover -s tests -v

Tests check (a) implementation correctness against known analytic results,
(b) reproducibility and invariants, (c) input validation, and (d) qualitative
behaviours each model is documented to exhibit. (d) are statements about the
MODELS, not about the real world.
"""

import json
import math
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from civlab import (aisociety, cascade, cld, core, diffusion, ews, forecast,  # noqa: E402
                    knowledge, polity, sdt, sensitivity, society)


class CoreTests(unittest.TestCase):
    def test_gini_known_values(self):
        self.assertAlmostEqual(core.gini([1, 1, 1, 1]), 0.0)
        self.assertAlmostEqual(core.gini([0, 0, 0, 1]), 0.75)

    def test_quantile_matches_type7(self):
        self.assertAlmostEqual(core.quantile([1, 2, 3, 4], 0.5), 2.5)
        self.assertAlmostEqual(core.quantile([1, 2, 3, 4, 5], 0.25), 2.0)

    def test_kendall_and_autocorr(self):
        self.assertAlmostEqual(core.kendall_tau([1, 2, 3, 4, 5]), 1.0)
        self.assertAlmostEqual(core.kendall_tau([5, 4, 3, 2, 1]), -1.0)
        rng = random.Random(0)
        x = [0.0]
        for _ in range(4000):
            x.append(0.8 * x[-1] + rng.gauss(0, 1))
        self.assertAlmostEqual(core.autocorr_lag1(x), 0.8, delta=0.05)

    def test_graphs_are_symmetric_and_sized(self):
        rng = random.Random(1)
        for kind in ("small_world", "random", "scale_free", "lattice"):
            g = core.make_graph(kind, 100, rng, 4, 0.1)
            self.assertEqual(len(g), 100)
            for i, nb in enumerate(g):
                self.assertNotIn(i, nb)
                for j in nb:
                    self.assertIn(i, g[j])

    def test_paired_delta(self):
        d = core.paired_delta([1, 2, 3], [2, 3, 4])
        self.assertAlmostEqual(d["mean_delta"], 1.0)
        self.assertEqual(d["share_positive"], 1.0)

    def test_envelope_rejects_bad_epistemic(self):
        with self.assertRaises(ValueError):
            core.envelope("x", {}, [], [], {}, epistemic="certain")


class SocietyTests(unittest.TestCase):
    CFG = {"agents": 120, "rounds": 80}

    def test_reproducible(self):
        self.assertEqual(society.run(self.CFG, 7)["metrics"], society.run(self.CFG, 7)["metrics"])

    def test_ledger_and_bounds(self):
        r = society.run({**self.CFG, "governance": "polycentric"}, 3)
        for row in r["trajectory"]:
            self.assertLess(abs(row["ledger_error"]), 1e-6)
            self.assertTrue(0 <= row["cooperation"] <= 1)
            self.assertTrue(0 <= row["gini"] <= 1)
            self.assertTrue(0 <= row["legitimacy"] <= 1)

    def test_peer_punishment_raises_cooperation_in_model(self):
        none = society.execute({**self.CFG, "governance": "none"}, runs=6)
        peer = society.execute({**self.CFG, "governance": "peer"}, runs=6)
        self.assertGreater(peer["baseline"]["summary"]["tail_mean_cooperation"]["mean"],
                           none["baseline"]["summary"]["tail_mean_cooperation"]["mean"] + 0.2)

    def test_corruption_tipping_in_model(self):
        clean = society.execute({**self.CFG, "governance": "central", "corruption": 0.0}, runs=5)
        corrupt = society.execute({**self.CFG, "governance": "central", "corruption": 0.5}, runs=5)
        self.assertGreater(clean["baseline"]["summary"]["final_legitimacy"]["mean"],
                           corrupt["baseline"]["summary"]["final_legitimacy"]["mean"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            society.run({"governance": "anarchy"}, 1)
        with self.assertRaises(ValueError):
            society.run({"init_cooperators": 0.8, "init_punishers": 0.5}, 1)

    def test_compare_uses_matched_seeds(self):
        out = society.execute(self.CFG, runs=3, compare={"governance": "none"})
        self.assertEqual(out["baseline"]["seeds"], out["comparison"]["alternative"]["seeds"])
        self.assertEqual(out["epistemic_status"], "fiction")


class AISocietyTests(unittest.TestCase):
    CAPTURE = {"oversight_enabled": False,
               "mix": {"steward": 0.15, "maximizer": 0.35, "deceiver": 0.25, "reciprocator": 0.25}}

    def test_reproducible(self):
        self.assertEqual(aisociety.run({}, 5)["metrics"], aisociety.run({}, 5)["metrics"])

    def test_kernel_blocks_all_overuse(self):
        r = aisociety.run({"kernel_enforcement": True}, 2)
        self.assertEqual(r["metrics"]["incidents"], 0)
        self.assertGreater(r["metrics"]["blocked_by_kernel"], 0)

    def test_prompt_only_rules_allow_incidents(self):
        r = aisociety.run({"kernel_enforcement": False, "oversight_enabled": False}, 2)
        self.assertGreater(r["metrics"]["incidents"], 0)

    def test_oversight_freezes(self):
        r = aisociety.run({"kernel_enforcement": False, "oversight_threshold": 0.1}, 2)
        self.assertTrue(r["metrics"]["frozen_by_oversight"])
        self.assertLess(r["metrics"]["ticks_completed"], 200)

    def test_entrenched_clause_protects_commons_under_capture(self):
        a = aisociety.execute(self.CAPTURE, runs=6)
        b = aisociety.execute({**self.CAPTURE, "entrenched_sustainability": True}, runs=6)
        self.assertGreater(b["baseline"]["summary"]["final_commons_ratio"]["mean"],
                           a["baseline"]["summary"]["final_commons_ratio"]["mean"] + 0.2)

    def test_custom_policy_is_validated(self):
        def rogue(view, rng):
            return {"action": "delete_world"}
        r = aisociety.run({"ticks": 5}, 1, policy=rogue)
        self.assertEqual(r["metrics"]["blocked_by_kernel"], 5 * 24)

    def test_commons_bounded(self):
        r = aisociety.run({}, 9)
        for row in r["trajectory"]:
            self.assertTrue(0 <= row["commons_ratio"] <= 1 + 1e-9)


class SDTTests(unittest.TestCase):
    def test_reproducible_and_bounded(self):
        a = sdt.run({"years": 300}, 4)
        self.assertEqual(a["metrics"], sdt.run({"years": 300}, 4)["metrics"])
        for row in a["trajectory"]:
            self.assertTrue(0 < row["elite_share"] <= 0.5)
            self.assertGreater(row["wage"], 0)
            self.assertGreaterEqual(row["debt_ratio"], 0)

    def test_integrative_phase_precedes_first_crisis(self):
        firsts = [sdt.run({}, s)["crises"][0]["start_year"] for s in range(10) if sdt.run({}, s)["crises"]]
        self.assertGreater(min(firsts), 30)

    def test_slower_population_growth_fewer_crises_in_model(self):
        fast = sdt.execute({"pop_growth": 0.015}, runs=20)
        slow = sdt.execute({"pop_growth": 0.005}, runs=20)
        self.assertLess(slow["monte_carlo"]["summary"]["crisis_count"]["mean"],
                        fast["monte_carlo"]["summary"]["crisis_count"]["mean"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            sdt.run({"tax_rate": 2}, 1)


class PolityTests(unittest.TestCase):
    def test_reproducible_and_conserves_cells(self):
        cfg = {"width": 12, "height": 12, "ticks": 60, "initial_polities": 6}
        a = polity.run(cfg, 3)
        self.assertEqual(a["metrics"], polity.run(cfg, 3)["metrics"])
        for row in a["trajectory"]:
            self.assertTrue(0 <= row["largest_share"] <= 1)
            self.assertTrue(0 <= row["stateless_share"] <= 1)
            self.assertTrue(0 < row["hhi"] <= 1 or row["polities"] == 0)

    def test_empires_rise_and_fragment(self):
        r = polity.run({"width": 16, "height": 16, "ticks": 200}, 1)
        self.assertGreater(r["metrics"]["peak_largest_share"], 0.2)
        self.assertGreater(r["metrics"]["collapses"], 0)


class DiffusionTests(unittest.TestCase):
    def test_bass_closed_form_properties(self):
        p, q = 0.03, 0.38
        self.assertAlmostEqual(diffusion.bass_cumulative(0, p, q), 0.0)
        self.assertAlmostEqual(diffusion.bass_cumulative(1000, p, q), 1.0, places=6)
        tp = diffusion.bass_peak_time(p, q)
        # cumulative adoption at peak is (q - p) / (2q)
        self.assertAlmostEqual(diffusion.bass_cumulative(tp, p, q), (q - p) / (2 * q), places=6)
        self.assertIsNone(diffusion.bass_peak_time(0.5, 0.1))

    def test_bass_fit_recovers_parameters(self):
        obs = [diffusion.bass_cumulative(t, 0.02, 0.5, 100) for t in range(15)]
        fit = diffusion.fit_bass(obs)
        self.assertAlmostEqual(fit["q"], 0.5, delta=0.08)
        self.assertAlmostEqual(fit["m"], 100, delta=10)

    def test_threshold_cascade_phase_change(self):
        low = diffusion.execute({"threshold_mean": 0.12, "agents": 300}, runs=5)
        high = diffusion.execute({"threshold_mean": 0.4, "agents": 300}, runs=5)
        self.assertGreater(low["summary"]["final_adoption"]["mean"], 0.9)
        self.assertLess(high["summary"]["final_adoption"]["mean"], 0.2)

    def test_resisters_never_adopt(self):
        r = diffusion.cascade_run({"agents": 200, "threshold_mean": 0.0, "threshold_sd": 0.0,
                                   "resisters": 0.3}, 1)
        self.assertLess(r["metrics"]["final_adoption"], 0.8)


class CascadeTests(unittest.TestCase):
    def test_tolerance_reduces_failure(self):
        lo = cascade.execute({"tolerance": 0.1}, runs=5)
        hi = cascade.execute({"tolerance": 1.0}, runs=5)
        self.assertGreater(hi["summary"]["surviving_share"]["mean"], lo["summary"]["surviving_share"]["mean"])

    def test_targeted_worse_than_random_on_scale_free(self):
        r = cascade.execute({"tolerance": 0.5, "attack": "random"}, runs=8)
        t = cascade.execute({"tolerance": 0.5, "attack": "targeted"}, runs=8)
        self.assertGreater(r["summary"]["surviving_share"]["mean"], t["summary"]["surviving_share"]["mean"])

    def test_interdependence_never_helps(self):
        for s in range(3):
            a = cascade.run({"tolerance": 0.5}, s)["metrics"]["surviving_share"]
            b = cascade.run({"tolerance": 0.5, "interdependent": True}, s)["metrics"]["surviving_share"]
            self.assertLessEqual(b, a + 1e-12)


class EWSTests(unittest.TestCase):
    def test_indicators_rise_when_approaching_transition(self):
        taus = [ews.analyze(ews.synthetic_fold(300, s, True), surrogates=19, seed=s) for s in range(3)]
        self.assertTrue(all(t["kendall_tau_ac1"] > 0 for t in taus))

    def test_no_signal_in_stationary_null(self):
        for s in range(3):
            res = ews.analyze(ews.synthetic_fold(300, s, False), surrogates=19, seed=s)
            self.assertEqual(res["signal"], "no_robust_signal")

    def test_short_series_rejected(self):
        with self.assertRaises(ValueError):
            ews.analyze([1, 2, 3])


class KnowledgeTests(unittest.TestCase):
    def test_henrich_threshold_analytic(self):
        a, b = 7.0, 1.0
        nstar = knowledge.henrich_critical_population(a, b)
        self.assertAlmostEqual(knowledge.henrich_expected_change(nstar, a, b), 0.0, places=9)
        self.assertLess(knowledge.henrich_expected_change(nstar / 5, a, b), 0)
        self.assertGreater(knowledge.henrich_expected_change(nstar * 5, a, b), 0)

    def test_stochastic_matches_analytic_sign(self):
        rng = random.Random(0)
        small = knowledge.simulate_tacit(60, 7, 1, 30, rng)
        big = knowledge.simulate_tacit(3000, 7, 1, 30, rng)
        self.assertLess(small[-1], small[0])
        self.assertGreater(big[-1], big[0])

    def test_redundancy_and_format_risk(self):
        rng = random.Random(1)
        one = knowledge.simulate_archive(100, 1, 0.02, 0.3, 200, 1, 0.0, rng)["final_survival"]
        five = knowledge.simulate_archive(100, 5, 0.02, 0.3, 200, 1, 0.0, rng)["final_survival"]
        self.assertGreater(five, one)
        mono = knowledge.simulate_archive(100, 4, 0.0, 0.3, 200, 1, 0.02, random.Random(2))["final_survival"]
        multi = knowledge.simulate_archive(100, 4, 0.0, 0.3, 200, 4, 0.02, random.Random(2))["final_survival"]
        self.assertGreaterEqual(multi, mono)


class ForecastTests(unittest.TestCase):
    def test_scores(self):
        self.assertAlmostEqual(forecast.brier(0.7, 1), 0.09)
        self.assertAlmostEqual(forecast.log_score(0.5, 0), math.log(2))

    def test_murphy_decomposition_identity(self):
        rng = random.Random(3)
        fc = [(rng.randrange(10) / 10 + 0.05, int(rng.random() < 0.4)) for _ in range(300)]
        cal = forecast.calibration(fc)
        # identity holds exactly when forecasts within a bin are identical (rounded to bin centres)
        self.assertAlmostEqual(cal["brier"], cal["reliability"] - cal["resolution"] + cal["uncertainty"], places=6)

    def test_base_rate_beta(self):
        br = forecast.base_rate(3, 20)
        self.assertAlmostEqual(br["posterior_mean"], 3.5 / 21)
        lo, hi = br["interval_90"]
        self.assertTrue(lo < br["posterior_mean"] < hi)
        self.assertAlmostEqual(forecast.beta_cdf(0.5, 2, 2), 0.5, places=6)

    def test_bayes_odds_form(self):
        r = forecast.bayes_update(0.5, [{"label": "x", "likelihood_ratio": 3}])
        self.assertAlmostEqual(r["posterior"], 0.75)

    def test_pool(self):
        self.assertAlmostEqual(forecast.pool([0.2, 0.8], method="linear"), 0.5)
        self.assertAlmostEqual(forecast.pool([0.2, 0.8]), 0.5)
        self.assertGreater(forecast.pool([0.7, 0.7], extremize=2), 0.7)

    def test_ledger_append_only_scoring(self):
        with tempfile.TemporaryDirectory() as d:
            L = forecast.Ledger(Path(d) / "f.jsonl")
            self.assertEqual(L.score()["resolved"], 0)
            L.forecast("q1", "Will X happen by 2027-01-01?", 0.3, "Official stats", "2027-01-01")
            L.forecast("q1", "Will X happen by 2027-01-01?", 0.6, "Official stats", "2027-01-01")
            L.resolve("q1", 1, "stats office bulletin")
            s = L.score()
            self.assertEqual(s["resolved"], 1)
            self.assertAlmostEqual(s["brier"], 0.16)
            self.assertEqual(len(L.records()), 3)

    def test_ach(self):
        spec = json.loads((ROOT / "examples" / "ach_example.json").read_text())
        r = forecast.ach(spec["hypotheses"], spec["evidence"])
        self.assertEqual(r["ranking_least_refuted_first"][0], "speculative hoarding")
        self.assertIn("Bread is expensive", r["non_diagnostic_evidence"])


class CLDTests(unittest.TestCase):
    def test_loop_polarity(self):
        res = cld.analyze([
            {"from": "a", "to": "b", "sign": "+"}, {"from": "b", "to": "a", "sign": "+"},
            {"from": "a", "to": "c", "sign": "+", "delay": True}, {"from": "c", "to": "a", "sign": "-"}])
        types = sorted(l["type"] for l in res["loops"])
        self.assertEqual(types, ["balancing", "reinforcing"])
        self.assertTrue(any(l["has_delay"] for l in res["loops"]))

    def test_missing_balancing_warns(self):
        res = cld.analyze([{"from": "a", "to": "b", "sign": "+"}, {"from": "b", "to": "a", "sign": "+"}])
        self.assertTrue(res["warnings"])

    def test_example_file(self):
        spec = json.loads((ROOT / "examples" / "cld_platform.json").read_text())
        res = cld.analyze(spec["edges"])
        self.assertEqual(res["reinforcing"], 1)
        self.assertEqual(res["balancing"], 2)


class SensitivityTests(unittest.TestCase):
    def test_morris_identifies_dominant_parameter(self):
        def toy(cfg, seed):
            return {"metrics": {"y": 10 * cfg["a"] + 0.1 * cfg["b"]}}
        res = sensitivity.morris(toy, {"a": 0.5, "b": 0.5}, {"a": (0, 1), "b": (0, 1)}, "y", trajectories=6)
        self.assertEqual(res["ranking_by_mu_star"][0], "a")
        self.assertAlmostEqual(res["effects"]["a"]["mu_star"], 10, places=6)

    def test_lhs_stratified(self):
        pts = sensitivity.latin_hypercube({"x": (0, 1)}, 10, seed=1)
        bins = sorted(int(p["x"] * 10) for p in pts)
        self.assertEqual(bins, list(range(10)))

    def test_robust_choice_regret(self):
        def toy(cfg, seed):
            return {"metrics": {"y": cfg["x"] * cfg["k"] * 0.8 + (1 - cfg["x"]) * 0.5}}
        res = sensitivity.robust_choice(toy, {"x": 0}, {"safe": {"x": 0}, "bold": {"x": 1}},
                                        {"k": (0, 1)}, "y", futures=20)
        self.assertEqual(res["minimax_regret_choice"], "safe")


class CLITests(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / "civitas.py"), *args],
                              capture_output=True, text=True, cwd=ROOT, timeout=300)

    def test_list_and_run(self):
        self.assertEqual(self._run("list").returncode, 0)
        r = self._run("run", "society", "--config", "examples/society_commons.json", "--runs", "2",
                      "--set", "rounds=20")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("epistemic_status", r.stdout)

    def test_compare_and_errors(self):
        r = self._run("compare", "aisociety", "--set", "ticks=30", "--alt", "kernel_enforcement=false", "--runs", "2")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("paired_deltas_alt_minus_base", r.stdout)
        bad = self._run("run", "society", "--set", "governance=anarchy", "--runs", "1")
        self.assertEqual(bad.returncode, 2)

    def test_legacy_simulator_still_runs(self):
        r = subprocess.run([sys.executable, "scripts/civitas_sim.py", "--config",
                            "examples/civilization_scenario.json", "--runs", "3", "--compare"],
                           capture_output=True, text=True, cwd=ROOT, timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
