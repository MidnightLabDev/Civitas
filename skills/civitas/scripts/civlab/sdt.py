"""Structural-demographic stress model (CIVITAS 1.0 original implementation).

Inspired by the structural-demographic theory (SDT) of Goldstone (1991) and
Turchin & Nefedov (2009), and by Goldstone's Political Stress Indicator
PSI = MMP x EMP x SFD (mass mobilisation potential x elite mobilisation
potential x state fiscal distress). The equations below are a deliberately
simple, ORIGINAL stylisation written for CIVITAS. They are not Turchin's
published model code, they are not fitted to any society, and their
parameters are illustrative.

What the model can show: whether, under its assumptions, population pressure,
an elite "wealth pump", and fiscal strain can generate recurring stress peaks,
and how interventions change the timing and size of those peaks.

What it cannot show: that any real country is "due" for a crisis.
"""

from __future__ import annotations

import math
import random

from .core import clamp, envelope, integer, mean, num, summarize

DEFAULTS = {
    "years": 600,
    "pop_growth": 0.015,          # intrinsic annual commoner growth rate
    "capacity_growth": 0.001,     # annual growth in carrying capacity (technology)
    "initial_pop_ratio": 0.35,    # N0 / K0
    "initial_elite_share": 0.01,
    "mobility_rate": 0.004,       # upward mobility into elite when wages fall (wealth pump)
    "elite_downward": 0.02,       # downward mobility when elite income per head falls
    "elite_tax": 0.0,             # policy: damps the wealth pump (0..1)
    "wage_support": 0.0,          # policy: raises effective wages floor (0..0.5)
    "tax_rate": 0.12,             # state revenue share of output
    "elite_patronage_cost": 3.0,  # state spending per elite share
    "public_cost": 0.08,          # state spending per unit population
    "fiscal_discipline": 0.0,     # policy: cuts spending growth (0..0.5)
    "crisis_base_hazard": 0.002,  # annual crisis hazard at PSI = 1
    "crisis_exponent": 3.0,       # hazard elasticity to PSI
    "crisis_mortality": 0.25,     # population lost in a crisis year
    "elite_culling": 0.40,        # elite share lost in a crisis year
    "debt_default": 0.8,          # share of debt repudiated in a crisis
    "crisis_duration": 15,        # years a crisis persists once triggered
}


def _cfg(raw: dict) -> dict:
    c = dict(DEFAULTS)
    c.update(raw or {})
    out = {
        "years": integer(c, "years", 600, 10, 5000),
        "crisis_duration": integer(c, "crisis_duration", 15, 1, 100),
    }
    bounds = {
        "pop_growth": (0, 0.1), "capacity_growth": (0, 0.05), "initial_pop_ratio": (0.01, 1.5),
        "initial_elite_share": (0.001, 0.5), "mobility_rate": (0, 0.1), "elite_downward": (0, 0.5),
        "elite_tax": (0, 1), "wage_support": (0, 0.5), "tax_rate": (0, 0.6),
        "elite_patronage_cost": (0, 50), "public_cost": (0, 1), "fiscal_discipline": (0, 0.5),
        "crisis_base_hazard": (0, 1), "crisis_exponent": (0, 6), "crisis_mortality": (0, 0.9),
        "elite_culling": (0, 0.9), "debt_default": (0, 1),
    }
    for k, (lo, hi) in bounds.items():
        out[k] = num(c, k, DEFAULTS[k], lo, hi)
    return out


def run(raw_cfg: dict, seed: int) -> dict:
    c = _cfg(raw_cfg)
    rng = random.Random(seed)
    K = 1.0
    N = c["initial_pop_ratio"]
    E = c["initial_elite_share"]
    E0 = E
    D = 0.0
    crisis_left = 0
    crises = []
    W_init = clamp((K / (2 * N)) ** 0.8, 0.05, 3.0)
    Y_init = N * (K / N) ** 0.3
    base_income_pc = (1 - clamp(0.6 * W_init, 0.2, 0.9)) * Y_init / (E0 * N)
    traj = []
    for t in range(c["years"]):
        K *= 1 + c["capacity_growth"]
        # wages fall as labour supply approaches capacity (stylised elasticity 0.8)
        W = (K / (2 * N)) ** 0.8 if N > 0 else 2.0
        W = clamp(W + c["wage_support"] * max(0.0, 1 - W), 0.05, 3.0)
        Y = N * (K / N) ** 0.3                       # output, diminishing returns
        labour_share = clamp(0.6 * W, 0.2, 0.9)
        elite_income_pc = (1 - labour_share) * Y / max(E * N, 1e-9)
        eps = elite_income_pc / base_income_pc       # relative elite income (1 = founding level)

        # elite dynamics: wealth pump when wages < 1, downward mobility when eps < 1
        pump = c["mobility_rate"] * max(0.0, 1 - W) * (1 - c["elite_tax"])
        down = c["elite_downward"] * max(0.0, 1 - eps)
        E = clamp(E + pump * (1 - E) - down * E, 1e-4, 0.5)

        # state finances
        revenue = c["tax_rate"] * Y
        spend = (c["elite_patronage_cost"] * E + c["public_cost"]) * N * (1 - c["fiscal_discipline"])
        interest = 0.02 * D
        D = max(0.0, D + spend + interest - revenue)
        debt_ratio = D / max(Y, 1e-9)

        MMP = (1 / W) * (1.0 + max(0.0, N / K - 0.5))      # immiseration and crowding
        EMP = (E / E0) ** 0.5 * (1 / max(eps, 0.05)) ** 0.5  # elite overproduction and competition
        SFD = 1 + debt_ratio
        PSI = MMP * EMP * SFD / 3.0                          # scaled so a calm society sits near ~0.5-1

        in_crisis = crisis_left > 0
        if not in_crisis:
            hazard = clamp(c["crisis_base_hazard"] * PSI ** c["crisis_exponent"], 0, 0.95)
            if rng.random() < hazard:
                crisis_left = c["crisis_duration"]
                crises.append({"start_year": t, "psi_at_onset": PSI})
                D *= 1 - c["debt_default"]
                in_crisis = True
        births = c["pop_growth"] * N * (1 - N / K)
        if in_crisis:
            N = max(1e-4, N * (1 - c["crisis_mortality"] / c["crisis_duration"]) + 0.2 * births)
            E = max(1e-4, E * (1 - c["elite_culling"] / c["crisis_duration"]))
            crisis_left -= 1
        else:
            N = max(1e-4, N + births)
        traj.append({"year": t, "psi": PSI, "wage": W, "elite_share": E, "relative_elite_income": eps,
                     "debt_ratio": debt_ratio, "pop_to_capacity": N / K, "in_crisis": in_crisis})

    psi = [r["psi"] for r in traj]
    crisis_years = sum(r["in_crisis"] for r in traj)
    gaps = [b["start_year"] - a["start_year"] for a, b in zip(crises, crises[1:])]
    metrics = {
        "crisis_count": len(crises),
        "share_years_in_crisis": crisis_years / len(traj),
        "mean_years_between_crises": mean(gaps) if gaps else None,
        "peak_psi": max(psi),
        "mean_psi": mean(psi),
        "final_elite_share": traj[-1]["elite_share"],
        "min_wage": min(r["wage"] for r in traj),
    }
    return {"seed": seed, "metrics": metrics, "crises": crises, "trajectory": traj}


METRICS = ["crisis_count", "share_years_in_crisis", "mean_years_between_crises", "peak_psi",
           "mean_psi", "final_elite_share", "min_wage"]

ASSUMPTIONS = [
    "Single aggregated polity; commoners, elites and the state are the only actors.",
    "Wages are a fixed power function of population relative to carrying capacity (elasticity 0.8).",
    "Elite numbers grow through a wealth pump active only when wages fall below the founding level.",
    "State spending scales with elite share (patronage) and population; debt carries 2% interest.",
    "Crisis hazard is a power function of a PSI-like composite; crises kill commoners, cull elites and repudiate debt.",
    "No external war, climate, disease, trade or ideology enters except through parameters.",
]
LIMITATIONS = [
    "Original stylisation, not Turchin's or Goldstone's published code; parameters are not fitted.",
    "Cycle length is an artefact of chosen rates; do not read it as a real 'secular cycle' period.",
    "PSI here is a model composite; real PSI estimates use measured series (wages, elite counts, debt).",
    "Use for teaching, hypothesis generation and intervention comparison inside the model only.",
]


def execute(cfg: dict, seed: int = 42, runs: int = 20) -> dict:
    from .core import monte_carlo
    _cfg(cfg)  # validate early
    mc = monte_carlo(run, cfg, [seed + i for i in range(runs)], METRICS)
    example = mc.pop("_runs")[0]
    thin = example["trajectory"][::max(1, len(example["trajectory"]) // 120)]
    return envelope("sdt_stress", cfg, ASSUMPTIONS, LIMITATIONS,
                    {"monte_carlo": mc, "example_run": {"seed": example["seed"], "crises": example["crises"],
                                                        "trajectory_thinned": thin}})
