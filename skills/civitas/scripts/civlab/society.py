"""Networked population model: cooperation, institutions, inequality, legitimacy.

CIVITAS 1.0 original agent-based model (stdlib only).

Mechanisms are taken from well-studied stylised models, combined in an
original implementation:
  * neighbourhood public-goods game on a social network (spatial / network
    reciprocity; e.g. Santos, Santos & Pacheco 2008 style settings),
  * costly peer punishment (cf. Fehr & Gaechter 2000 laboratory results),
  * an optional central sanctioning institution funded by taxes, whose
    effectiveness depends on legitimacy and is eroded by corruption,
  * payoff-biased social learning (Fermi imitation rule) with in-group bias
    and mutation (cultural evolution),
  * subsistence costs, exit of ruined agents and replacement (demography),
  * scarcity shocks that temporarily cut the productivity of the commons.

All quantities are synthetic units. A wealth ledger is checked every round.
"""

from __future__ import annotations

import math
import random

from .core import (clamp, envelope, gini, integer, make_graph, mean, monte_carlo, num,
                   paired_delta)

C, D, P = "C", "D", "P"  # cooperator, defector, punishing cooperator

DEFAULTS = {
    "agents": 200, "rounds": 150, "groups": 2,
    "graph": "small_world", "degree": 6, "rewire": 0.1,
    "init_cooperators": 0.4, "init_punishers": 0.1,
    "contribution": 1.0, "multiplier": 4.5,
    "punish_cost": 0.3, "punish_fine": 1.0,
    "governance": "peer",          # none | peer | central | polycentric
    "tax_rate": 0.05, "monitoring_efficiency": 8.0, "central_fine": 3.0, "corruption": 0.1,
    "selection_strength": 1.0, "mutation": 0.01, "ingroup_bias": 0.5,
    "subsistence": 0.8, "initial_wealth": 5.0, "replacement": True,
    "shock_probability": 0.03, "shock_severity": 0.5, "shock_duration": 5,
}
GOVERNANCE = {"none", "peer", "central", "polycentric"}


def _cfg(raw: dict) -> dict:
    c = dict(DEFAULTS)
    c.update(raw or {})
    out = {
        "agents": integer(c, "agents", 200, 10, 5000),
        "rounds": integer(c, "rounds", 150, 1, 5000),
        "groups": integer(c, "groups", 2, 1, 20),
        "degree": integer(c, "degree", 6, 2, 50),
        "shock_duration": integer(c, "shock_duration", 5, 1, 100),
        "graph": c["graph"], "governance": c["governance"],
        "replacement": bool(c["replacement"]),
    }
    if out["governance"] not in GOVERNANCE:
        raise ValueError(f"governance must be one of {sorted(GOVERNANCE)}")
    if out["graph"] not in {"small_world", "random", "scale_free", "lattice"}:
        raise ValueError("graph must be small_world, random, scale_free or lattice")
    for k, lo, hi in [("rewire", 0, 1), ("init_cooperators", 0, 1), ("init_punishers", 0, 1),
                      ("contribution", 0, 100), ("multiplier", 0, 50), ("punish_cost", 0, 10),
                      ("punish_fine", 0, 50), ("tax_rate", 0, 0.5), ("monitoring_efficiency", 0, 100),
                      ("central_fine", 0, 50), ("corruption", 0, 1), ("selection_strength", 0, 50),
                      ("mutation", 0, 0.5), ("ingroup_bias", 0, 1), ("subsistence", 0, 50),
                      ("initial_wealth", 0, 1e6), ("shock_probability", 0, 1),
                      ("shock_severity", 0, 1)]:
        out[k] = num(c, k, DEFAULTS[k], lo, hi)
    if out["init_cooperators"] + out["init_punishers"] > 1:
        raise ValueError("init_cooperators + init_punishers must be <= 1")
    return out


def _random_strategy(rng: random.Random, c: dict) -> str:
    u = rng.random()
    if u < c["init_punishers"]:
        return P
    if u < c["init_punishers"] + c["init_cooperators"]:
        return C
    return D


def run(raw_cfg: dict, seed: int) -> dict:
    c = _cfg(raw_cfg)
    rng = random.Random(seed)
    n = c["agents"]
    adj = [sorted(s) for s in make_graph(c["graph"], n, rng, c["degree"], c["rewire"])]
    strat = [_random_strategy(rng, c) for _ in range(n)]
    group = [rng.randrange(c["groups"]) for _ in range(n)]
    wealth = [c["initial_wealth"]] * n
    legitimacy = 0.6
    shock_left = 0
    exits = 0
    traj = []
    peer = c["governance"] in {"peer", "polycentric"}
    central = c["governance"] in {"central", "polycentric"}
    for t in range(c["rounds"]):
        if shock_left == 0 and rng.random() < c["shock_probability"]:
            shock_left = c["shock_duration"]
        r_eff = c["multiplier"] * (1 - c["shock_severity"] if shock_left > 0 else 1)
        shock_left = max(0, shock_left - 1)

        before = sum(wealth)
        payoff = [0.0] * n
        created = destroyed = 0.0
        # 1. neighbourhood public goods games, one centred on each agent
        for i in range(n):
            members = [i] + adj[i]
            contributors = [j for j in members if strat[j] != D]
            # each cooperator splits its total contribution evenly across the games it joins
            gifts = [c["contribution"] / (len(adj[j]) + 1) for j in contributors]
            pot = sum(gifts)
            share = pot * r_eff / len(members)
            for j, gift in zip(contributors, gifts):
                payoff[j] -= gift
            for j in members:
                payoff[j] += share
            created += pot * r_eff - pot
        # 2. peer punishment: punishers fine defecting neighbours (both payments destroyed)
        if peer:
            for i in range(n):
                if strat[i] != P:
                    continue
                for j in adj[i]:
                    if strat[j] == D:
                        payoff[i] -= c["punish_cost"]
                        payoff[j] -= c["punish_fine"]
                        destroyed += c["punish_cost"] + c["punish_fine"]
        # 3. central institution: taxes fund monitoring; fines and corruption flow
        detected = 0
        budget = 0.0
        skim = 0.0
        if central:
            gains = [max(0.0, p) for p in payoff]
            for i in range(n):
                tax = gains[i] * c["tax_rate"]
                payoff[i] -= tax
                budget += tax
            skim = budget * c["corruption"]
            p_detect = clamp((budget - skim) * c["monitoring_efficiency"] / n) * legitimacy
            fines = 0.0
            for i in range(n):
                if strat[i] == D and rng.random() < p_detect:
                    payoff[i] -= c["central_fine"]
                    fines += c["central_fine"]
                    detected += 1
            # skim goes to the richest 5% (elite capture); rest of budget + fines is spent on
            # monitoring (consumed) -> destroyed from the ledger's point of view
            elite = sorted(range(n), key=lambda k: wealth[k], reverse=True)[:max(1, n // 20)]
            for k in elite:
                payoff[k] += skim / len(elite)
            destroyed += budget - skim + fines
        # 4. subsistence
        for i in range(n):
            payoff[i] -= c["subsistence"]
        destroyed += c["subsistence"] * n
        for i in range(n):
            wealth[i] += payoff[i]
        after = sum(wealth)
        ledger_err = after - (before + created - destroyed)
        if abs(ledger_err) > 1e-6 * max(1.0, abs(before)):
            raise AssertionError(f"wealth ledger broken at round {t}: {ledger_err}")

        # 5. demography: ruined agents exit and are replaced by newcomers with zero-ish wealth
        exited_now = 0
        for i in range(n):
            if wealth[i] < 0:
                exited_now += 1
                if c["replacement"]:
                    strat[i] = _random_strategy(rng, c)
                    wealth[i] = 0.0  # debt written off (ledger resets for this agent)
                    group[i] = rng.randrange(c["groups"])
        exits += exited_now

        # 6. cultural evolution: payoff-biased imitation with in-group bias, then mutation
        new = strat[:]
        for i in range(n):
            if not adj[i]:
                continue
            j = rng.choice(adj[i])
            same = group[i] == group[j]
            weight = 1.0 if same else 1.0 - c["ingroup_bias"]
            delta = payoff[j] - payoff[i]
            x = clamp(-c["selection_strength"] * delta, -50, 50)
            if rng.random() < weight / (1 + math.exp(x)):
                new[i] = strat[j]
            if rng.random() < c["mutation"]:
                new[i] = rng.choice((C, D, P))
        strat = new

        coop = sum(s != D for s in strat) / n
        g = gini(wealth)
        if central:
            # legitimacy relaxes toward a target set by performance, fairness and integrity
            target = clamp(0.3 + 0.6 * coop - 1.0 * c["corruption"] - 0.5 * max(0.0, g - 0.35)
                           - (0.15 if shock_left > 0 else 0.0))
            legitimacy = clamp(legitimacy + 0.1 * (target - legitimacy))
        traj.append({"round": t, "cooperation": coop, "punishers": sum(s == P for s in strat) / n,
                     "gini": g, "mean_wealth": mean(wealth), "legitimacy": legitimacy if central else None,
                     "detected_defectors": detected, "exits": exited_now, "shock": shock_left > 0,
                     "ledger_error": ledger_err})
    tail = traj[-max(1, len(traj) // 5):]
    between = _group_cooperation_gap(strat, group, c["groups"])
    metrics = {
        "final_cooperation": traj[-1]["cooperation"],
        "tail_mean_cooperation": mean([r["cooperation"] for r in tail]),
        "final_gini": traj[-1]["gini"],
        "final_mean_wealth": traj[-1]["mean_wealth"],
        "total_exits": exits,
        "final_legitimacy": traj[-1]["legitimacy"] if central else None,
        "group_cooperation_gap": between,
    }
    return {"seed": seed, "metrics": metrics, "trajectory": traj}


def _group_cooperation_gap(strat, group, g):
    rates = []
    for k in range(g):
        members = [s for s, gr in zip(strat, group) if gr == k]
        if members:
            rates.append(sum(s != D for s in members) / len(members))
    return max(rates) - min(rates) if len(rates) > 1 else 0.0


METRICS = ["final_cooperation", "tail_mean_cooperation", "final_gini", "final_mean_wealth",
           "total_exits", "final_legitimacy", "group_cooperation_gap"]
ASSUMPTIONS = [
    "Agents play repeated neighbourhood public-goods games on a fixed social network; a cooperator's per-round contribution is split across the games it joins.",
    "Strategies spread by payoff-biased imitation (Fermi rule), discounted across group lines.",
    "Peer punishment is costly to the punisher and the fine is destroyed, as in classic lab designs.",
    "A central institution detects defectors with probability rising in its net budget and legitimacy.",
    "Corruption diverts part of the budget to the wealthiest 5% (elite capture).",
    "Legitimacy relaxes toward a target that rises with cooperation and falls with corruption, inequality above 0.35 Gini and shocks (ad hoc rule).",
    "Ruined agents exit and are replaced by newcomers with random strategies.",
]
LIMITATIONS = [
    "Stylised: strategies are three discrete types; no language, norms internalisation, or reputation.",
    "Legitimacy dynamics are an illustrative rule, not an estimated relationship.",
    "Results depend strongly on multiplier, network and selection strength; always run sensitivity analysis.",
    "Cannot predict cooperation levels in any real community.",
]


def execute(cfg: dict, seed: int = 42, runs: int = 10, compare: dict | None = None) -> dict:
    _cfg(cfg)
    seeds = [seed + i for i in range(runs)]
    base = monte_carlo(run, cfg, seeds, METRICS)
    base_runs = base.pop("_runs")
    body = {"baseline": base,
            "example_trajectory": base_runs[0]["trajectory"][::max(1, len(base_runs[0]["trajectory"]) // 60)]}
    if compare:
        alt_cfg = {**cfg, **compare}
        _cfg(alt_cfg)
        alt = monte_carlo(run, alt_cfg, seeds, METRICS)
        alt.pop("_runs")
        deltas = {}
        for m in METRICS:
            a = [r[m] for r in base["per_run"]]
            b = [r[m] for r in alt["per_run"]]
            if all(v is not None for v in a + b):
                deltas[m] = paired_delta(a, b)
        body["comparison"] = {"changes": compare, "alternative": alt, "paired_deltas": deltas}
    return envelope("networked_society", cfg, ASSUMPTIONS, LIMITATIONS, body)
