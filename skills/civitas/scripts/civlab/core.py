"""CIVITAS 1.0 civlab core utilities (stdlib only).

Shared statistics, graph generators, validation helpers and the result envelope
that every civlab model returns. The envelope carries an explicit epistemic
status so that no output can be mistaken for an empirical prediction.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
from typing import Any, Callable, Iterable, Sequence

VERSION = "1.0"

EPISTEMIC_LEVELS = (
    "established",        # E1 established scientific knowledge
    "evidence_estimate",  # E2 evidence supported estimate
    "model_projection",   # E3 model dependent projection
    "exploratory",        # E4 exploratory scenario
    "fiction",            # E5 fictional simulation / synthetic
    "speculation",        # E6 unsupported speculation
)


# --------------------------------------------------------------------------- #
# Validation helpers
# --------------------------------------------------------------------------- #

def num(cfg: dict, key: str, default: float, lo: float, hi: float) -> float:
    """Read a bounded finite number from a config dict."""
    v = cfg.get(key, default)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(f"{key}: expected a number, got {v!r}")
    v = float(v)
    if not math.isfinite(v) or not lo <= v <= hi:
        raise ValueError(f"{key}: expected a finite number in [{lo}, {hi}], got {v}")
    return v


def integer(cfg: dict, key: str, default: int, lo: int, hi: int) -> int:
    v = cfg.get(key, default)
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(f"{key}: expected an integer, got {v!r}")
    if not lo <= v <= hi:
        raise ValueError(f"{key}: expected an integer in [{lo}, {hi}], got {v}")
    return v


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else hi if x > hi else x


# --------------------------------------------------------------------------- #
# Statistics
# --------------------------------------------------------------------------- #

def mean(xs: Sequence[float]) -> float:
    return statistics.fmean(xs) if xs else float("nan")


def sd(xs: Sequence[float]) -> float:
    return statistics.stdev(xs) if len(xs) > 1 else 0.0


def quantile(xs: Sequence[float], q: float) -> float:
    """Linear interpolation quantile (type 7, same as numpy default)."""
    if not xs:
        return float("nan")
    s = sorted(xs)
    pos = (len(s) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return s[int(pos)]
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def gini(xs: Sequence[float]) -> float:
    """Gini coefficient of non-negative values (0 = equal, ->1 = concentrated)."""
    vals = sorted(max(0.0, float(x)) for x in xs)
    n = len(vals)
    total = sum(vals)
    if n == 0 or total <= 0:
        return 0.0
    cum = sum((i + 1) * v for i, v in enumerate(vals))
    return (2.0 * cum) / (n * total) - (n + 1.0) / n


def autocorr_lag1(xs: Sequence[float]) -> float:
    n = len(xs)
    if n < 3:
        return float("nan")
    m = mean(xs)
    num_ = sum((xs[i] - m) * (xs[i + 1] - m) for i in range(n - 1))
    den = sum((x - m) ** 2 for x in xs)
    return num_ / den if den > 0 else 0.0


def kendall_tau(xs: Sequence[float]) -> float:
    """Kendall rank correlation of a series against time (tau-a, ties count 0)."""
    n = len(xs)
    if n < 2:
        return float("nan")
    conc = disc = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            d = xs[j] - xs[i]
            if d > 0:
                conc += 1
            elif d < 0:
                disc += 1
    return (conc - disc) / (n * (n - 1) / 2)


def summarize(values: Sequence[float]) -> dict[str, float | None]:
    vals = [v for v in values if v is not None and math.isfinite(v)]
    if not vals:
        return {"n": 0, "mean": None, "sd": None, "p05": None, "p50": None, "p95": None,
                "min": None, "max": None}
    return {"n": len(vals), "mean": mean(vals), "sd": sd(vals),
            "p05": quantile(vals, 0.05), "p50": quantile(vals, 0.5), "p95": quantile(vals, 0.95),
            "min": min(vals), "max": max(vals)}


def paired_delta(a: Sequence[float], b: Sequence[float]) -> dict[str, Any]:
    """Summary of b - a for seed-matched runs, with a normal-approximation 95% interval
    of the mean difference across seeds (describes Monte Carlo noise only)."""
    if len(a) != len(b) or not a:
        raise ValueError("paired_delta needs equal-length non-empty sequences")
    d = [y - x for x, y in zip(a, b)]
    m = mean(d)
    se = sd(d) / math.sqrt(len(d)) if len(d) > 1 else 0.0
    return {"mean_delta": m, "mc_ci95": [m - 1.96 * se, m + 1.96 * se],
            "share_positive": sum(x > 0 for x in d) / len(d), "n_pairs": len(d),
            "note": "Interval reflects simulation noise across seeds, not real-world uncertainty."}


# --------------------------------------------------------------------------- #
# Graphs (adjacency lists of ints)
# --------------------------------------------------------------------------- #

def ring_lattice(n: int, k: int) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    half = max(1, k // 2)
    for i in range(n):
        for j in range(1, half + 1):
            a, b = i, (i + j) % n
            if a != b:
                adj[a].add(b)
                adj[b].add(a)
    return adj


def watts_strogatz(n: int, k: int, p: float, rng: random.Random) -> list[set[int]]:
    """Small-world graph (Watts & Strogatz 1998): ring lattice with rewiring prob p."""
    if n < 3:
        return [set(j for j in range(n) if j != i) for i in range(n)]
    adj = ring_lattice(n, min(k, n - 1))
    half = max(1, min(k, n - 1) // 2)
    for i in range(n):
        for j in range(1, half + 1):
            t = (i + j) % n
            if t in adj[i] and rng.random() < p:
                choices = [c for c in range(n) if c != i and c not in adj[i]]
                if not choices:
                    continue
                new = rng.choice(choices)
                adj[i].discard(t)
                adj[t].discard(i)
                adj[i].add(new)
                adj[new].add(i)
    return adj


def erdos_renyi(n: int, mean_degree: float, rng: random.Random) -> list[set[int]]:
    p = min(1.0, mean_degree / max(1, n - 1))
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def barabasi_albert(n: int, m: int, rng: random.Random) -> list[set[int]]:
    """Preferential attachment graph; heavy-tailed degree distribution."""
    m = max(1, min(m, n - 1))
    adj = [set() for _ in range(n)]
    for i in range(m + 1):
        for j in range(i + 1, m + 1):
            adj[i].add(j)
            adj[j].add(i)
    targets_pool = [i for i in range(m + 1) for _ in range(m)]
    for new in range(m + 1, n):
        chosen: set[int] = set()
        while len(chosen) < m:
            chosen.add(rng.choice(targets_pool))
        for t in chosen:
            adj[new].add(t)
            adj[t].add(new)
            targets_pool.extend([new, t])
    return adj


def make_graph(kind: str, n: int, rng: random.Random, k: int = 4, p: float = 0.1) -> list[set[int]]:
    if kind == "small_world":
        return watts_strogatz(n, k, p, rng)
    if kind == "random":
        return erdos_renyi(n, k, rng)
    if kind == "scale_free":
        return barabasi_albert(n, max(1, k // 2), rng)
    if kind == "lattice":
        return ring_lattice(n, k)
    raise ValueError(f"unknown graph kind {kind!r}; use small_world, random, scale_free, lattice")


def components(adj: Sequence[Iterable[int]], alive: Sequence[bool] | None = None) -> list[list[int]]:
    n = len(adj)
    alive = alive if alive is not None else [True] * n
    seen = [False] * n
    out = []
    for s in range(n):
        if seen[s] or not alive[s]:
            continue
        stack, comp = [s], []
        seen[s] = True
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if alive[v] and not seen[v]:
                    seen[v] = True
                    stack.append(v)
        out.append(comp)
    return out


# --------------------------------------------------------------------------- #
# Runs and envelopes
# --------------------------------------------------------------------------- #

def config_hash(cfg: Any) -> str:
    return hashlib.sha256(json.dumps(cfg, sort_keys=True, default=str).encode()).hexdigest()


def envelope(model: str, cfg: dict, assumptions: list[str], limitations: list[str],
             body: dict, epistemic: str = "fiction") -> dict:
    if epistemic not in EPISTEMIC_LEVELS:
        raise ValueError(f"bad epistemic level {epistemic}")
    return {
        "civitas_version": VERSION,
        "model": model,
        "epistemic_status": epistemic,
        "warning": ("Output describes the behaviour of a stylized model under its stated "
                    "assumptions. It is not an empirical forecast of any real society."),
        "config_sha256": config_hash(cfg),
        "configuration": cfg,
        "assumptions": assumptions,
        "limitations": limitations,
        **body,
    }


def monte_carlo(run_fn: Callable[[dict, int], dict], cfg: dict, seeds: Sequence[int],
                metrics: Sequence[str]) -> dict:
    """Run a model over seeds, return per-run metrics plus distribution summaries."""
    runs = [run_fn(cfg, s) for s in seeds]
    summary = {m: summarize([r["metrics"][m] for r in runs]) for m in metrics}
    return {"seeds": list(seeds), "summary": summary,
            "per_run": [{"seed": r["seed"], **r["metrics"]} for r in runs], "_runs": runs}
