"""Forecasting and evidence tools (CIVITAS 1.0).

* Reference-class base rates with a Beta posterior (Jeffreys prior by default).
* Bayesian updating in odds form from stated likelihood ratios, with a log of
  each update (so the reasoning chain is auditable).
* Pooling several probability judgements: linear and logit (geometric-odds)
  pooling with optional extremizing (cf. Satopaa et al. 2014).
* Proper scoring: Brier score, log score, Murphy decomposition, calibration
  table. Only for RESOLVED real questions.
* Append-only forecast ledger (JSONL) with resolution and scoring.
* Analysis of Competing Hypotheses (ACH) consistency matrix (Heuer style):
  ranks hypotheses by weighted INCONSISTENCY, not by confirming evidence.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path


# ------------------------------- base rates --------------------------------- #

def _betacf(a, b, x, itmax=200, eps=3e-14):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c if abs(1 + aa / c) > 1e-300 else 1e-300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c if abs(1 + aa / c) > 1e-300 else 1e-300
        de = d * c
        h *= de
        if abs(de - 1) < eps:
            break
    return h


def beta_cdf(x: float, a: float, b: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1 - front * _betacf(b, a, 1 - x) / b


def beta_ppf(q: float, a: float, b: float) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if beta_cdf(mid, a, b) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def base_rate(successes: int, trials: int, prior=(0.5, 0.5)) -> dict:
    """Posterior for an event frequency from a reference class (k of n cases)."""
    if trials < 0 or not 0 <= successes <= trials:
        raise ValueError("need 0 <= successes <= trials")
    a, b = prior[0] + successes, prior[1] + trials - successes
    return {"k": successes, "n": trials, "prior": list(prior), "posterior_mean": a / (a + b),
            "interval_90": [beta_ppf(0.05, a, b), beta_ppf(0.95, a, b)],
            "note": ("Interval reflects sampling uncertainty within the chosen reference class only; "
                     "the choice of reference class is usually the larger uncertainty.")}


# ------------------------------ Bayesian updates ----------------------------- #

def logit(p: float) -> float:
    p = min(1 - 1e-12, max(1e-12, p))
    return math.log(p / (1 - p))


def inv_logit(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def bayes_update(prior: float, evidence: list[dict]) -> dict:
    """evidence: [{"label": str, "likelihood_ratio": float}] where LR = P(E|H)/P(E|not H).
    Assumes conditional independence of evidence items given H (flagged in output)."""
    if not 0 < prior < 1:
        raise ValueError("prior must be strictly between 0 and 1")
    steps = []
    lo = logit(prior)
    for e in evidence:
        lr = float(e["likelihood_ratio"])
        if lr <= 0:
            raise ValueError("likelihood ratios must be positive")
        lo += math.log(lr)
        steps.append({"label": e.get("label", ""), "likelihood_ratio": lr, "posterior": inv_logit(lo)})
    return {"prior": prior, "posterior": inv_logit(lo), "steps": steps,
            "warning": "Assumes evidence items are independent given the hypothesis; correlated evidence double counts."}


def pool(probs: list[float], weights: list[float] | None = None, method: str = "logit",
         extremize: float = 1.0) -> float:
    if not probs:
        raise ValueError("no probabilities to pool")
    w = weights or [1.0] * len(probs)
    s = sum(w)
    if method == "linear":
        return sum(p * x for p, x in zip(probs, w)) / s
    if method != "logit":
        raise ValueError("method must be linear or logit")
    return inv_logit(extremize * sum(logit(p) * x for p, x in zip(probs, w)) / s)


# ------------------------------- scoring ------------------------------------ #

def brier(p: float, y: int) -> float:
    return (p - y) ** 2


def log_score(p: float, y: int) -> float:
    p = min(1 - 1e-12, max(1e-12, p))
    return -math.log(p if y else 1 - p)


def calibration(forecasts: list[tuple[float, int]], bins: int = 10) -> dict:
    """Calibration table and Murphy decomposition: BS = reliability - resolution + uncertainty."""
    if not forecasts:
        raise ValueError("no resolved forecasts")
    n = len(forecasts)
    base = sum(y for _, y in forecasts) / n
    table, rel, res = [], 0.0, 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        inside = [(p, y) for p, y in forecasts if (lo <= p < hi) or (b == bins - 1 and p == 1.0)]
        if not inside:
            continue
        mp = sum(p for p, _ in inside) / len(inside)
        fy = sum(y for _, y in inside) / len(inside)
        rel += len(inside) * (mp - fy) ** 2
        res += len(inside) * (fy - base) ** 2
        table.append({"bin": [lo, hi], "n": len(inside), "mean_forecast": mp, "observed_rate": fy})
    bs = sum(brier(p, y) for p, y in forecasts) / n
    return {"n": n, "brier": bs, "log_score": sum(log_score(p, y) for p, y in forecasts) / n,
            "reliability": rel / n, "resolution": res / n, "uncertainty": base * (1 - base),
            "climatology_brier": base * (1 - base), "table": table,
            "caution": "Fewer than ~50 resolved forecasts cannot establish calibration." if n < 50 else ""}


# ------------------------------ forecast ledger ------------------------------ #

class Ledger:
    """Append-only JSONL forecast log. Records are never rewritten; updates and
    resolutions are new lines that reference the question id."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def _append(self, rec: dict) -> dict:
        rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **rec}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        return rec

    def forecast(self, qid: str, question: str, p: float, resolution_criteria: str,
                 resolve_by: str, rationale: str = "") -> dict:
        if not 0 <= p <= 1:
            raise ValueError("p must be in [0,1]")
        return self._append({"type": "forecast", "qid": qid, "question": question, "p": p,
                             "resolution_criteria": resolution_criteria, "resolve_by": resolve_by,
                             "rationale": rationale})

    def resolve(self, qid: str, outcome: int, source: str) -> dict:
        if outcome not in (0, 1):
            raise ValueError("outcome must be 0 or 1")
        return self._append({"type": "resolution", "qid": qid, "outcome": outcome, "source": source})

    def records(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [json.loads(l) for l in self.path.read_text(encoding="utf-8").splitlines() if l.strip()]

    def score(self) -> dict:
        recs = self.records()
        latest, outcomes = {}, {}
        for r in recs:
            if r["type"] == "forecast":
                latest[r["qid"]] = r["p"]   # last forecast before resolution counts
            elif r["type"] == "resolution":
                outcomes[r["qid"]] = r["outcome"]
        pairs = [(latest[q], outcomes[q]) for q in outcomes if q in latest]
        if not pairs:
            return {"resolved": 0, "message": "No resolved questions yet; nothing can be scored."}
        return {"resolved": len(pairs), **calibration(pairs)}


# ---------------------------------- ACH ------------------------------------- #

ACH_SCALE = {"CC": 2, "C": 1, "N": 0, "I": -1, "II": -2}


def ach(hypotheses: list[str], evidence: list[dict]) -> dict:
    """evidence: [{"item": str, "weight": float (credibility x relevance, 0..1+),
                   "ratings": {hypothesis: "CC"|"C"|"N"|"I"|"II"}}]
    Score = weighted sum of inconsistencies (lower = less refuted). Also flags
    non-diagnostic evidence (same rating across all hypotheses)."""
    scores = {h: 0.0 for h in hypotheses}
    support = {h: 0.0 for h in hypotheses}
    nondiag = []
    for e in evidence:
        w = float(e.get("weight", 1.0))
        vals = []
        for h in hypotheses:
            r = e["ratings"].get(h, "N")
            if r not in ACH_SCALE:
                raise ValueError(f"rating {r!r} not in {list(ACH_SCALE)}")
            v = ACH_SCALE[r]
            vals.append(v)
            if v < 0:
                scores[h] += w * v
            else:
                support[h] += w * v
        if len(set(vals)) == 1:
            nondiag.append(e["item"])
    ranking = sorted(hypotheses, key=lambda h: scores[h], reverse=True)
    return {"inconsistency_scores": scores, "consistency_scores": support, "ranking_least_refuted_first": ranking,
            "non_diagnostic_evidence": nondiag,
            "note": "ACH ranks by what evidence argues AGAINST each hypothesis. It structures judgement; it does not compute truth."}
