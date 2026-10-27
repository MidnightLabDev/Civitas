"""Technology / behaviour diffusion models (CIVITAS 1.0).

1. Bass (1969) aggregate diffusion with closed-form solution, plus a fitting
   helper (grid search least squares, stdlib only) for observed adoption series.
2. Network threshold cascades (Granovetter 1978; Watts 2002): each agent adopts
   when the share of adopting neighbours reaches its personal threshold.
   Supports heterogeneous thresholds, seeding strategies and a 'backlash'
   share that never adopts (resistance).
"""

from __future__ import annotations

import math
import random

from .core import envelope, integer, make_graph, mean, num, summarize


# ---------------------------- Bass model ------------------------------------ #

def bass_cumulative(t: float, p: float, q: float, m: float = 1.0) -> float:
    """Closed-form cumulative adopters F(t)*m of the Bass model."""
    if p <= 0:
        return 0.0
    e = math.exp(-(p + q) * t)
    return m * (1 - e) / (1 + (q / p) * e)


def bass_peak_time(p: float, q: float) -> float | None:
    """Time of peak adoption rate; exists only when q > p."""
    if q <= p or p <= 0:
        return None
    return math.log(q / p) / (p + q)


def bass_series(p: float, q: float, m: float, periods: int) -> list[dict]:
    out = []
    prev = 0.0
    for t in range(periods + 1):
        cum = bass_cumulative(t, p, q, m)
        out.append({"t": t, "cumulative": cum, "new": cum - prev})
        prev = cum
    return out


def fit_bass(cumulative: list[float], m_grid: list[float] | None = None) -> dict:
    """Least-squares fit of (p, q, m) to an observed cumulative adoption series
    (t = 0, 1, 2 ...). Coarse-to-fine grid search; returns the fit and its SSE.
    Warning: early-stage series identify m very poorly (see Bass-model literature)."""
    if len(cumulative) < 4:
        raise ValueError("need at least 4 observations to fit Bass")
    obs_max = max(cumulative)
    m_grid = m_grid or [obs_max * k for k in (1.05, 1.25, 1.5, 2, 3, 5)]
    best = None
    for m in m_grid:
        for p in [10 ** (-4 + i * 0.1) for i in range(31)]:      # 1e-4 .. 1e-1
            for q in [0.02 * i for i in range(1, 51)]:             # 0.02 .. 1.0
                sse = sum((bass_cumulative(t, p, q, m) - y) ** 2 for t, y in enumerate(cumulative))
                if best is None or sse < best[0]:
                    best = (sse, p, q, m)
    sse, p, q, m = best
    # local refinement
    for _ in range(3):
        for dp in (0.8, 0.9, 1.1, 1.25):
            for dq in (0.9, 0.95, 1.05, 1.1):
                for dm in (0.95, 1.0, 1.05):
                    pp, qq, mm = p * dp, q * dq, max(obs_max, m * dm)
                    s = sum((bass_cumulative(t, pp, qq, mm) - y) ** 2 for t, y in enumerate(cumulative))
                    if s < sse:
                        sse, p, q, m = s, pp, qq, mm
    upper_hit = m >= max(m_grid) * 0.99
    return {"p": p, "q": q, "m": m, "sse": sse, "peak_time": bass_peak_time(p, q),
            "warning": ("Market size m hit the top of the search grid; the series is too early to identify m."
                        if upper_hit else "Fit is descriptive; parameters drift as more data arrive.")}


# ------------------------- Network threshold cascade ------------------------- #

DEFAULTS = {"agents": 500, "graph": "random", "degree": 6, "rewire": 0.1,
            "threshold_mean": 0.25, "threshold_sd": 0.1, "seed_share": 0.02,
            "seeding": "random", "resisters": 0.0, "max_steps": 200}


def _cfg(raw: dict) -> dict:
    c = {**DEFAULTS, **(raw or {})}
    if c["seeding"] not in {"random", "hubs", "cluster"}:
        raise ValueError("seeding must be random, hubs or cluster")
    return {"agents": integer(c, "agents", 500, 10, 100000), "graph": c["graph"],
            "degree": integer(c, "degree", 6, 1, 200), "rewire": num(c, "rewire", 0.1, 0, 1),
            "threshold_mean": num(c, "threshold_mean", 0.25, 0, 1),
            "threshold_sd": num(c, "threshold_sd", 0.1, 0, 1),
            "seed_share": num(c, "seed_share", 0.02, 0, 1), "seeding": c["seeding"],
            "resisters": num(c, "resisters", 0.0, 0, 1),
            "max_steps": integer(c, "max_steps", 200, 1, 100000)}


def cascade_run(raw: dict, seed: int) -> dict:
    c = _cfg(raw)
    rng = random.Random(seed)
    n = c["agents"]
    adj = [sorted(s) for s in make_graph(c["graph"], n, rng, c["degree"], c["rewire"])]
    thr = [min(1.0, max(0.0, rng.gauss(c["threshold_mean"], c["threshold_sd"]))) for _ in range(n)]
    resist = [rng.random() < c["resisters"] for _ in range(n)]
    k = max(1, round(c["seed_share"] * n))
    if c["seeding"] == "hubs":
        seeds = sorted(range(n), key=lambda i: len(adj[i]), reverse=True)[:k]
    elif c["seeding"] == "cluster":
        start = rng.randrange(n)
        seeds, frontier, seen = [], [start], {start}
        while frontier and len(seeds) < k:
            u = frontier.pop(0)
            seeds.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    frontier.append(v)
    else:
        seeds = rng.sample(range(n), k)
    adopted = [False] * n
    for s in seeds:
        adopted[s] = True
    curve = [sum(adopted) / n]
    for _ in range(c["max_steps"]):
        new = adopted[:]
        changed = False
        for i in range(n):
            if adopted[i] or resist[i] or not adj[i]:
                continue
            frac = sum(adopted[j] for j in adj[i]) / len(adj[i])
            if frac >= thr[i]:
                new[i] = True
                changed = True
        adopted = new
        curve.append(sum(adopted) / n)
        if not changed:
            break
    final = curve[-1]
    return {"seed": seed, "metrics": {"final_adoption": final, "steps": len(curve) - 1,
                                      "global_cascade": final > 0.5}, "curve": curve}


def execute(cfg: dict, seed: int = 42, runs: int = 20) -> dict:
    mode = cfg.get("mode", "cascade")
    if mode == "bass":
        p = num(cfg, "p", 0.03, 0, 1)
        q = num(cfg, "q", 0.38, 0, 5)
        m = num(cfg, "m", 1.0, 0, 1e12)
        periods = integer(cfg, "periods", 30, 1, 10000)
        body = {"series": bass_series(p, q, m, periods), "peak_time": bass_peak_time(p, q)}
        if "observed_cumulative" in cfg:
            body["fit"] = fit_bass([float(x) for x in cfg["observed_cumulative"]])
        return envelope("bass_diffusion", cfg,
                        ["Homogeneous, fully mixed population", "Fixed market potential m",
                         "Constant innovation p and imitation q"],
                        ["No supply limits, prices, competing technologies or repeat purchase",
                         "Early-stage fits identify m poorly"], body, epistemic="model_projection")
    sub = {k: v for k, v in cfg.items() if k != "mode"}
    runs_ = [cascade_run(sub, seed + i) for i in range(runs)]
    finals = [r["metrics"]["final_adoption"] for r in runs_]
    body = {"summary": {"final_adoption": summarize(finals),
                        "global_cascade_share": mean([r["metrics"]["global_cascade"] for r in runs_])},
            "per_run": [{"seed": r["seed"], **r["metrics"]} for r in runs_],
            "example_curve": runs_[0]["curve"]}
    return envelope("threshold_cascade", sub,
                    ["Agents adopt irreversibly once neighbour adoption share >= personal threshold",
                     "Thresholds ~ Normal(mean, sd) clipped to [0,1]; resisters never adopt",
                     "Static network; synchronous updating"],
                    ["Real adoption also depends on price, access, media and changing thresholds",
                     "Cascade size is famously bimodal and seed-sensitive: report the distribution, not the mean"],
                    body)
