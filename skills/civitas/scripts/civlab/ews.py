"""Early-warning signals of critical transitions (CIVITAS 1.0).

Implements generic indicators of 'critical slowing down' (Scheffer et al. 2009;
Dakos et al. 2012): rising variance and rising lag-1 autocorrelation in a
rolling window, summarised by Kendall's tau trend. Also includes a
surrogate-data significance test (shuffle / AR(1) surrogates) and a synthetic
generator of a system approaching a fold bifurcation, used to validate the
detector.

Caveats are part of the API output: these signals can be absent before real
transitions (noise-induced or fast-forcing transitions) and present without
one (false positives); they need long, evenly sampled, detrended series.
"""

from __future__ import annotations

import math
import random

from .core import autocorr_lag1, envelope, kendall_tau, mean, sd


def detrend(xs: list[float], bandwidth: int) -> list[float]:
    """Subtract a centred moving average (simple, transparent detrending)."""
    n = len(xs)
    out = []
    for i in range(n):
        lo, hi = max(0, i - bandwidth), min(n, i + bandwidth + 1)
        out.append(xs[i] - mean(xs[lo:hi]))
    return out


def rolling_indicators(xs: list[float], window: int) -> dict:
    var, ac = [], []
    for i in range(window, len(xs) + 1):
        w = xs[i - window:i]
        var.append(sd(w) ** 2)
        ac.append(autocorr_lag1(w))
    return {"variance": var, "ac1": ac}


def analyze(series: list[float], window_frac: float = 0.5, bandwidth_frac: float = 0.1,
            surrogates: int = 200, seed: int = 0) -> dict:
    n = len(series)
    if n < 30:
        raise ValueError("early-warning analysis needs at least 30 evenly spaced observations")
    window = max(10, int(n * window_frac))
    bw = max(2, int(n * bandwidth_frac))
    resid = detrend([float(x) for x in series], bw)
    ind = rolling_indicators(resid, window)
    tau_var = kendall_tau(ind["variance"])
    tau_ac = kendall_tau(ind["ac1"])
    # surrogate test: AR(1) surrogates with the same lag-1 autocorrelation and variance
    rng = random.Random(seed)
    phi = max(-0.99, min(0.99, autocorr_lag1(resid)))
    sigma = sd(resid) * math.sqrt(max(1e-9, 1 - phi ** 2))
    exceed_var = exceed_ac = 0
    for _ in range(surrogates):
        x = [0.0]
        for _ in range(n - 1):
            x.append(phi * x[-1] + rng.gauss(0, sigma))
        si = rolling_indicators(x, window)
        if kendall_tau(si["variance"]) >= tau_var:
            exceed_var += 1
        if kendall_tau(si["ac1"]) >= tau_ac:
            exceed_ac += 1
    p_var = (exceed_var + 1) / (surrogates + 1)
    p_ac = (exceed_ac + 1) / (surrogates + 1)
    warning = tau_var > 0 and tau_ac > 0 and p_var < 0.1 and p_ac < 0.1
    return {
        "n": n, "window": window, "detrend_bandwidth": bw,
        "kendall_tau_variance": tau_var, "kendall_tau_ac1": tau_ac,
        "surrogate_p_variance": p_var, "surrogate_p_ac1": p_ac,
        "signal": "rising_indicators" if warning else "no_robust_signal",
        "interpretation": ("Both variance and autocorrelation trend upward beyond AR(1) surrogates: consistent "
                           "with critical slowing down. This is a warning to investigate, not a forecast."
                           if warning else
                           "No robust joint upward trend. Absence of a signal does NOT rule out a transition."),
        "indicators": ind,
    }


def synthetic_fold(n: int = 400, seed: int = 1, approach: bool = True, noise: float = 0.05) -> list[float]:
    """Simulate dx = (r + x - x^3/3... ) style system: x relaxes to an equilibrium whose
    recovery rate shrinks linearly to near zero (approach=True) or stays constant."""
    rng = random.Random(seed)
    x, out = 0.0, []
    for t in range(n):
        k = 1.0 - 0.95 * (t / n) if approach else 1.0      # recovery rate
        x = x - 0.2 * k * x + rng.gauss(0, noise)
        out.append(x)
    return out


def execute(cfg: dict, seed: int = 0, runs: int = 1) -> dict:
    series = cfg.get("series")
    if series is None:
        series = synthetic_fold(int(cfg.get("n", 400)), seed, bool(cfg.get("approach", True)))
        src = "synthetic"
    else:
        src = "user_supplied"
    res = analyze(series, float(cfg.get("window_frac", 0.5)), float(cfg.get("bandwidth_frac", 0.1)),
                  int(cfg.get("surrogates", 200)), seed)
    res["indicators"] = {k: v[:: max(1, len(v) // 100)] for k, v in res["indicators"].items()}
    return envelope("early_warning_signals", {k: v for k, v in cfg.items() if k != "series"} | {"source": src},
                    ["Series is evenly sampled and long relative to the window",
                     "Transition, if any, is a slow approach to a local bifurcation (critical slowing down)"],
                    ["False negatives for noise-induced, fast or externally forced shifts",
                     "False positives from changing noise, sampling or measurement processes",
                     "Choice of window and detrending changes results: run a sensitivity check"],
                    {"result": res}, epistemic="evidence_estimate" if src == "user_supplied" else "fiction")
