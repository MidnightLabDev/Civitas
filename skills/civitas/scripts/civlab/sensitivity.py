"""Sensitivity analysis and robust decision tools for any civlab model (CIVITAS 1.0).

* one_at_a_time: vary each parameter across a range, others at baseline.
* morris: Morris (1991) elementary-effects screening with trajectories;
  reports mu* (mean absolute effect) and sigma (interaction / nonlinearity).
* latin_hypercube: space-filling sample for uncertainty propagation.
* robust_choice: compare policies across sampled futures with regret
  (minimax regret, as used in Robust Decision Making; Lempert et al. 2003).

Models are referenced by name and evaluated through their run(cfg, seed)
functions; the metric is averaged over a small set of seeds per point.
"""

from __future__ import annotations

import random
from typing import Callable

from .core import mean, sd


def _eval(run_fn: Callable, cfg: dict, metric: str, seeds: list[int]) -> float:
    vals = [run_fn(cfg, s)["metrics"][metric] for s in seeds]
    vals = [v for v in vals if v is not None]
    return mean(vals) if vals else float("nan")


def one_at_a_time(run_fn, base: dict, ranges: dict, metric: str, levels: int = 5,
                  seeds: list[int] | None = None) -> dict:
    seeds = seeds or [1, 2, 3]
    out = {}
    for k, (lo, hi) in ranges.items():
        pts = []
        for i in range(levels):
            v = lo + (hi - lo) * i / (levels - 1)
            if isinstance(base.get(k), int) and not isinstance(base.get(k), bool):
                v = int(round(v))
            pts.append({"value": v, metric: _eval(run_fn, {**base, k: v}, metric, seeds)})
        ys = [p[metric] for p in pts]
        out[k] = {"points": pts, "swing": max(ys) - min(ys)}
    ranking = sorted(out, key=lambda k: out[k]["swing"], reverse=True)
    return {"metric": metric, "results": out, "ranking_by_swing": ranking,
            "caution": "OAT misses interactions; use morris() before trusting a ranking."}


def morris(run_fn, base: dict, ranges: dict, metric: str, trajectories: int = 10, levels: int = 4,
           seed: int = 0, seeds: list[int] | None = None) -> dict:
    rng = random.Random(seed)
    seeds = seeds or [1, 2]
    keys = list(ranges)
    k = len(keys)
    delta = levels / (2 * (levels - 1))
    effects = {key: [] for key in keys}
    grid = [i / (levels - 1) for i in range(levels)]
    for _ in range(trajectories):
        x = [rng.choice([g for g in grid if g + delta <= 1 + 1e-9]) for _ in range(k)]
        order = list(range(k))
        rng.shuffle(order)

        def to_cfg(u):
            cfg = dict(base)
            for j, key in enumerate(keys):
                lo, hi = ranges[key]
                v = lo + (hi - lo) * u[j]
                if isinstance(base.get(key), int) and not isinstance(base.get(key), bool):
                    v = int(round(v))
                cfg[key] = v
            return cfg

        y_prev = _eval(run_fn, to_cfg(x), metric, seeds)
        for j in order:
            x2 = x[:]
            x2[j] = x[j] + delta
            y = _eval(run_fn, to_cfg(x2), metric, seeds)
            effects[keys[j]].append((y - y_prev) / delta)
            x, y_prev = x2, y
    res = {key: {"mu_star": mean([abs(e) for e in v]), "mu": mean(v), "sigma": sd(v), "n": len(v)}
           for key, v in effects.items()}
    return {"metric": metric, "effects": res,
            "ranking_by_mu_star": sorted(res, key=lambda q: res[q]["mu_star"], reverse=True),
            "reading": "High mu*: influential. High sigma relative to mu*: nonlinear or interacting."}


def latin_hypercube(ranges: dict, n: int, seed: int = 0) -> list[dict]:
    rng = random.Random(seed)
    cols = {}
    for key, (lo, hi) in ranges.items():
        cuts = [(i + rng.random()) / n for i in range(n)]
        rng.shuffle(cuts)
        cols[key] = [lo + (hi - lo) * c for c in cuts]
    return [{key: cols[key][i] for key in ranges} for i in range(n)]


def robust_choice(run_fn, base: dict, policies: dict[str, dict], uncertain: dict, metric: str,
                  maximize: bool = True, futures: int = 20, seed: int = 0,
                  seeds: list[int] | None = None) -> dict:
    """Evaluate each policy (dict of parameter overrides) in each sampled future
    (Latin hypercube over uncertain parameters). Regret = best-in-future minus policy."""
    seeds = seeds or [1, 2]
    worlds = latin_hypercube(uncertain, futures, seed)
    table = {p: [] for p in policies}
    for w in worlds:
        vals = {p: _eval(run_fn, {**base, **w, **ov}, metric, seeds) for p, ov in policies.items()}
        best = max(vals.values()) if maximize else min(vals.values())
        for p, v in vals.items():
            table[p].append({"value": v, "regret": (best - v) if maximize else (v - best)})
    summary = {p: {"mean": mean([r["value"] for r in rows]), "worst": (min if maximize else max)(r["value"] for r in rows),
                   "max_regret": max(r["regret"] for r in rows), "mean_regret": mean([r["regret"] for r in rows])}
               for p, rows in table.items()}
    return {"metric": metric, "maximize": maximize, "futures": futures, "summary": summary,
            "minimax_regret_choice": min(summary, key=lambda p: summary[p]["max_regret"]),
            "best_mean_choice": (max if maximize else min)(summary, key=lambda p: summary[p]["mean"]),
            "note": "Futures are samples of model parameters, not probabilities of real worlds."}
