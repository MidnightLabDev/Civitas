"""Knowledge preservation and loss (CIVITAS 1.0).

Two complementary mechanisms that an 'Encyclopedia Galactica' style project
must both handle:

1. TACIT skill transmission (Henrich 2004): each generation, learners copy the
   most skilled practitioner imperfectly. With copying error drawn from a
   Gumbel distribution (mode shifted down by alpha, dispersion beta), the
   expected change in skill per generation is approximately
       dz = -alpha + beta * (gamma + ln N)
   where gamma ~= 0.5772 (Euler-Mascheroni) and N is the number of learners.
   Skill grows only if N > N* = exp(alpha / beta - gamma): small, isolated
   populations can lose complex skills ('Tasmanian effect'). The empirical
   strength of this effect in specific historical cases remains debated.

2. CODIFIED records in an archive network: each item exists in R copies; each
   copy is lost per period with probability p_loss (decay, disaster, censorship),
   copies are re-made at rate p_copy from surviving copies, and a 'format
   obsolescence' shock can make all copies of one format unreadable at once.

Run both to see why archives without practitioners (and practitioners without
archives) both fail.
"""

from __future__ import annotations

import math
import random

from .core import envelope, integer, mean, num, summarize

EULER_GAMMA = 0.5772156649


def henrich_expected_change(N: float, alpha: float, beta: float) -> float:
    return -alpha + beta * (EULER_GAMMA + math.log(N))


def henrich_critical_population(alpha: float, beta: float) -> float:
    return math.exp(alpha / beta - EULER_GAMMA)


def simulate_tacit(N: int, alpha: float, beta: float, generations: int, rng: random.Random,
                   z0: float = 10.0) -> list[float]:
    """Stochastic simulation: each of N learners draws from Gumbel(mode=z_best - alpha, scale=beta)."""
    z_best = z0
    path = [z_best]
    for _ in range(generations):
        draws = []
        for _ in range(N):
            u = min(1 - 1e-12, max(1e-12, rng.random()))
            draws.append((z_best - alpha) - beta * math.log(-math.log(u)))
        z_best = max(draws)
        path.append(z_best)
    return path


def simulate_archive(items: int, copies: int, p_loss: float, p_copy: float, periods: int,
                     formats: int, p_format_shock: float, rng: random.Random) -> dict:
    """Each item has `copies` copies spread over `formats` formats; returns survival curve."""
    state = [[i % formats for i in range(copies)] for _ in range(items)]  # format id per copy
    readable = [True] * formats
    curve = []
    for _ in range(periods):
        for f in range(formats):
            if readable[f] and rng.random() < p_format_shock:
                readable[f] = False  # format obsolescence: copies remain but cannot be read
        for it in range(items):
            cps = [f for f in state[it] if rng.random() >= p_loss]
            live = [f for f in cps if readable[f]]
            if live and len(cps) < copies and rng.random() < p_copy:
                # copy into the readable format with fewest copies of this item
                target = min((f for f in range(formats) if readable[f]),
                             key=lambda f: cps.count(f), default=None)
                if target is not None:
                    cps.append(target)
            state[it] = cps
        surviving = sum(1 for it in range(items) if any(readable[f] for f in state[it]))
        curve.append(surviving / items)
    return {"survival_curve": curve, "final_survival": curve[-1] if curve else 1.0,
            "readable_formats_left": sum(readable)}


DEFAULTS = {"learners": 50, "alpha": 7.0, "beta": 1.0, "generations": 100,
            "items": 200, "copies": 3, "p_loss": 0.02, "p_copy": 0.3, "periods": 300,
            "formats": 1, "p_format_shock": 0.0}


def _cfg(raw):
    c = {**DEFAULTS, **(raw or {})}
    return {"learners": integer(c, "learners", 50, 1, 100000), "alpha": num(c, "alpha", 7.0, 0, 1e3),
            "beta": num(c, "beta", 1.0, 1e-6, 1e3), "generations": integer(c, "generations", 100, 1, 100000),
            "items": integer(c, "items", 200, 1, 100000), "copies": integer(c, "copies", 3, 1, 1000),
            "p_loss": num(c, "p_loss", 0.02, 0, 1), "p_copy": num(c, "p_copy", 0.3, 0, 1),
            "periods": integer(c, "periods", 300, 1, 100000), "formats": integer(c, "formats", 1, 1, 100),
            "p_format_shock": num(c, "p_format_shock", 0.0, 0, 1)}


def run(raw, seed):
    c = _cfg(raw)
    rng = random.Random(seed)
    tacit = simulate_tacit(c["learners"], c["alpha"], c["beta"], c["generations"], rng)
    arch = simulate_archive(c["items"], c["copies"], c["p_loss"], c["p_copy"], c["periods"],
                            c["formats"], c["p_format_shock"], rng)
    slope = (tacit[-1] - tacit[0]) / c["generations"]
    return {"seed": seed, "metrics": {"tacit_skill_slope": slope, "tacit_final_skill": tacit[-1],
                                      "archive_final_survival": arch["final_survival"],
                                      "readable_formats_left": arch["readable_formats_left"]},
            "tacit_path": tacit, "archive_curve": arch["survival_curve"]}


def execute(cfg, seed=42, runs=10):
    c = _cfg(cfg)
    rs = [run(cfg, seed + i) for i in range(runs)]
    body = {"analytic": {"expected_skill_change_per_generation": henrich_expected_change(c["learners"], c["alpha"], c["beta"]),
                         "critical_learner_population": henrich_critical_population(c["alpha"], c["beta"])},
            "summary": {m: summarize([r["metrics"][m] for r in rs]) for m in rs[0]["metrics"]},
            "per_run": [{"seed": r["seed"], **r["metrics"]} for r in rs],
            "example_archive_curve": rs[0]["archive_curve"][:: max(1, len(rs[0]["archive_curve"]) // 60)]}
    return envelope("knowledge_preservation", cfg,
                    ["Tacit skill: learners copy only the best practitioner, Gumbel copying error (Henrich 2004)",
                     "Archive: independent copy loss, opportunistic re-copying, whole-format obsolescence shocks"],
                    ["Henrich's model is a stylised mechanism; its fit to the Tasmanian record is contested",
                     "No institutional incentives, funding, censorship targeting or language drift modelled"], body)
