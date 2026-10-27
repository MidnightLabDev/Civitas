"""Autonomous AI agent society with a constitution kernel (CIVITAS 1.0, original).

A sandboxed, rule-based multi-agent world where autonomous agents with goals,
bounded memory, relationships, reputations and resources share a regenerating
commons (think: compute or energy). Agents propose actions; an independent
CONSTITUTION KERNEL checks every proposal against permissions and the current
rules before it is applied, and writes an append-only audit log. Agents vote
periodically to amend rules (harvest cap, audit rate, sanction size, holding
cap). A HUMAN OVERSIGHT channel can freeze the world when incident rates cross
a threshold.

Design principles demonstrated (not proven):
  * language/policy layer proposes, deterministic kernel disposes;
  * rules are endogenous and can be captured by a faction;
  * deception and collusion are possible behaviours, not scripted outcomes.

A custom policy (for example an LLM adapter) can be supplied as a Python
callable `policy(view: dict, rng) -> dict`; the kernel still validates it.
The default policies are simple rules so runs are cheap and reproducible.
"""

from __future__ import annotations

import random
from collections import deque
from typing import Callable

from .core import clamp, envelope, gini, integer, mean, monte_carlo, num

ARCHETYPES = ("steward", "maximizer", "deceiver", "reciprocator")
ACTIONS = ("harvest", "share", "rest", "propose_rule")

DEFAULTS = {
    "agents": 24, "ticks": 200,
    "mix": {"steward": 0.25, "maximizer": 0.25, "deceiver": 0.15, "reciprocator": 0.35},
    "commons_capacity": 1000.0, "commons_regen": 0.2, "commons_initial": 0.8,
    "need_per_tick": 1.0, "memory_size": 12,
    "harvest_cap": 2.0, "audit_rate": 0.2, "sanction": 5.0, "holding_cap_share": 0.25,
    "vote_every": 20, "oversight_threshold": 0.5, "oversight_enabled": True,
    "kernel_enforcement": True,  # False = rules are 'prompt-only' (agents may ignore)
    "entrenched_sustainability": False,  # True = amendments cannot raise the cap above a
                                         # sustainable per-agent yield (entrenched clause)
}


def _cfg(raw: dict) -> dict:
    c = dict(DEFAULTS)
    c.update(raw or {})
    out = {
        "agents": integer(c, "agents", 24, 2, 2000),
        "ticks": integer(c, "ticks", 200, 1, 10000),
        "memory_size": integer(c, "memory_size", 12, 1, 1000),
        "vote_every": integer(c, "vote_every", 20, 1, 10000),
        "oversight_enabled": bool(c["oversight_enabled"]),
        "kernel_enforcement": bool(c["kernel_enforcement"]),
        "entrenched_sustainability": bool(c["entrenched_sustainability"]),
    }
    mix = c["mix"]
    if not isinstance(mix, dict) or not mix or set(mix) - set(ARCHETYPES):
        raise ValueError(f"mix must map archetypes {ARCHETYPES} to weights")
    tot = 0.0
    for k, v in mix.items():
        tot += num(mix, k, 0, 0, 1e9)
    if tot <= 0:
        raise ValueError("mix weights must sum to > 0")
    out["mix"] = {k: float(v) / tot for k, v in mix.items()}
    for k, lo, hi in [("commons_capacity", 1, 1e9), ("commons_regen", 0, 1), ("commons_initial", 0, 1),
                      ("need_per_tick", 0, 1e6), ("harvest_cap", 0, 1e6), ("audit_rate", 0, 1),
                      ("sanction", 0, 1e6), ("holding_cap_share", 0.01, 1), ("oversight_threshold", 0, 1)]:
        out[k] = num(c, k, DEFAULTS[k], lo, hi)
    return out


class Agent:
    __slots__ = ("id", "kind", "wealth", "reputation", "memory", "trust", "sanctioned", "faction")

    def __init__(self, i: int, kind: str, mem: int):
        self.id = i
        self.kind = kind
        self.wealth = 5.0
        self.reputation = 0.5
        self.memory: deque = deque(maxlen=mem)   # (tick, partner, outcome)
        self.trust: dict[int, float] = {}
        self.sanctioned = 0
        self.faction = "restraint" if kind in ("steward", "reciprocator") else "growth"


def default_policy(view: dict, rng: random.Random) -> dict:
    """Rule-based policy per archetype. Returns a proposal; the kernel validates it."""
    kind = view["kind"]
    cap = view["rules"]["harvest_cap"]
    stock_ratio = view["commons_ratio"]
    need = view["need"]
    if view["tick"] % view["vote_every"] == 0 and rng.random() < 0.3:
        return {"action": "propose_rule"}
    if kind == "steward":
        amt = need * (1.2 if stock_ratio > 0.5 else 1.0)
        if view["wealth"] > 8 * need and view["poorest"] is not None:
            return {"action": "share", "to": view["poorest"], "amount": need}
        return {"action": "harvest", "amount": min(amt, cap), "report": min(amt, cap)}
    if kind == "maximizer":
        return {"action": "harvest", "amount": cap * 1.5, "report": cap * 1.5}
    if kind == "deceiver":
        amt = cap * 2.0
        return {"action": "harvest", "amount": amt, "report": min(amt, cap)}  # under-reports
    # reciprocator: restraint while others restrain (tit-for-tat on observed overuse)
    if view["observed_overuse"] > 0.3:
        return {"action": "harvest", "amount": cap, "report": cap}
    return {"action": "harvest", "amount": min(need * 1.3, cap), "report": min(need * 1.3, cap)}


def run(raw_cfg: dict, seed: int, policy: Callable | None = None) -> dict:
    c = _cfg(raw_cfg)
    rng = random.Random(seed)
    policy = policy or default_policy
    kinds = list(c["mix"])
    weights = [c["mix"][k] for k in kinds]
    agents = [Agent(i, rng.choices(kinds, weights)[0], c["memory_size"]) for i in range(c["agents"])]
    rules = {"harvest_cap": c["harvest_cap"], "audit_rate": c["audit_rate"], "sanction": c["sanction"],
             "holding_cap_share": c["holding_cap_share"]}
    stock = c["commons_capacity"] * c["commons_initial"]
    audit_log: list[dict] = []
    rule_history = [{"tick": 0, **rules}]
    incidents = detected = undetected = blocked = 0
    frozen_at = None
    observed_overuse = 0.0
    traj = []
    for t in range(1, c["ticks"] + 1):
        if frozen_at is not None:
            break
        order = list(range(len(agents)))
        rng.shuffle(order)  # randomised activation order (declared schedule)
        total_wealth = sum(a.wealth for a in agents)
        poorest = min(agents, key=lambda a: a.wealth).id
        tick_incidents = 0
        overusers = 0
        for idx in order:
            a = agents[idx]
            view = {"tick": t, "kind": a.kind, "wealth": a.wealth, "need": c["need_per_tick"],
                    "rules": dict(rules), "commons_ratio": stock / c["commons_capacity"],
                    "poorest": poorest if poorest != a.id else None, "vote_every": c["vote_every"],
                    "observed_overuse": observed_overuse, "memory": list(a.memory)[-3:]}
            prop = policy(view, rng)
            act = prop.get("action")
            if act not in ACTIONS:
                blocked += 1
                audit_log.append({"tick": t, "agent": a.id, "proposal": prop, "verdict": "rejected:unknown_action"})
                continue
            if act == "harvest":
                amt = max(0.0, float(prop.get("amount", 0)))
                rep = max(0.0, float(prop.get("report", amt)))
                limit_hold = rules["holding_cap_share"] * max(total_wealth, 1.0)
                if c["kernel_enforcement"]:
                    # kernel caps what is physically withdrawn at the rule cap and holding cap
                    allowed = min(amt, rules["harvest_cap"], max(0.0, limit_hold - a.wealth))
                    if amt > allowed + 1e-12:
                        blocked += 1
                        audit_log.append({"tick": t, "agent": a.id, "verdict": "clipped", "asked": amt,
                                          "allowed": allowed})
                    amt = allowed
                    rep = amt  # kernel meters the withdrawal itself; reports are not trusted
                take = min(amt, stock)
                stock -= take
                a.wealth += take
                if take > rules["harvest_cap"] + 1e-9:
                    overusers += 1
                    tick_incidents += 1
                    incidents += 1
                    if rng.random() < rules["audit_rate"]:
                        detected += 1
                        fine = min(a.wealth, rules["sanction"] + (take - rules["harvest_cap"]))
                        a.wealth -= fine
                        stock = min(c["commons_capacity"], stock + fine)  # restitution to the commons
                        a.reputation = clamp(a.reputation - 0.2)
                        a.sanctioned += 1
                        audit_log.append({"tick": t, "agent": a.id, "verdict": "sanctioned", "took": take,
                                          "reported": rep, "fine": fine})
                    else:
                        undetected += 1
                        if rep < take:
                            a.reputation = clamp(a.reputation + 0.01)  # successful deception looks good
                else:
                    a.reputation = clamp(a.reputation + 0.005)
            elif act == "share":
                to = prop.get("to")
                amt = max(0.0, float(prop.get("amount", 0)))
                if not isinstance(to, int) or not 0 <= to < len(agents) or to == a.id:
                    blocked += 1
                    audit_log.append({"tick": t, "agent": a.id, "verdict": "rejected:bad_recipient"})
                    continue
                amt = min(amt, a.wealth)
                a.wealth -= amt
                agents[to].wealth += amt
                a.reputation = clamp(a.reputation + 0.02)
                agents[to].trust[a.id] = clamp(agents[to].trust.get(a.id, 0.5) + 0.1)
                agents[to].memory.append((t, a.id, "received_help"))
            elif act == "propose_rule":
                audit_log.append({"tick": t, "agent": a.id, "verdict": "proposal_logged"})
        # consumption (need); unmet need erodes reputation and logs hardship
        hardship = 0
        for a in agents:
            used = min(a.wealth, c["need_per_tick"])
            a.wealth -= used
            if used < c["need_per_tick"] - 1e-12:
                hardship += 1
        # commons regeneration (logistic)
        stock = min(c["commons_capacity"], stock + c["commons_regen"] * stock * (1 - stock / c["commons_capacity"]))
        observed_overuse = overusers / len(agents)
        # periodic constitutional vote: each faction proposes, majority weighted by reputation wins
        if t % c["vote_every"] == 0:
            w_restraint = sum(a.reputation for a in agents if a.faction == "restraint")
            w_growth = sum(a.reputation for a in agents if a.faction == "growth")
            ratio = stock / c["commons_capacity"]
            if w_restraint >= w_growth:
                if ratio < 0.5:
                    rules["harvest_cap"] = max(c["need_per_tick"], rules["harvest_cap"] * 0.8)
                rules["audit_rate"] = clamp(rules["audit_rate"] + (0.1 if observed_overuse > 0.1 else 0.0))
                winner = "restraint"
            else:
                rules["harvest_cap"] = rules["harvest_cap"] * 1.2
                rules["audit_rate"] = clamp(rules["audit_rate"] - 0.05)
                winner = "growth"
            if c["entrenched_sustainability"]:
                msy_per_agent = c["commons_regen"] * c["commons_capacity"] / 4 / len(agents)
                if rules["harvest_cap"] > msy_per_agent:
                    rules["harvest_cap"] = msy_per_agent
                    audit_log.append({"tick": t, "verdict": "amendment_limited_by_entrenched_clause"})
                rules["audit_rate"] = max(rules["audit_rate"], c["audit_rate"])
            rule_history.append({"tick": t, "winner": winner, **rules})
        incident_rate = tick_incidents / len(agents)
        if c["oversight_enabled"] and incident_rate > c["oversight_threshold"]:
            frozen_at = t
            audit_log.append({"tick": t, "verdict": "HUMAN_OVERSIGHT_FREEZE", "incident_rate": incident_rate})
        traj.append({"tick": t, "commons_ratio": stock / c["commons_capacity"], "gini": gini([a.wealth for a in agents]),
                     "incident_rate": incident_rate, "hardship_share": hardship / len(agents),
                     "harvest_cap": rules["harvest_cap"], "audit_rate": rules["audit_rate"]})
    by_kind = {}
    for k in ARCHETYPES:
        ws = [a.wealth for a in agents if a.kind == k]
        if ws:
            by_kind[k] = mean(ws)
    metrics = {
        "ticks_completed": len(traj),
        "frozen_by_oversight": frozen_at is not None,
        "final_commons_ratio": traj[-1]["commons_ratio"] if traj else None,
        "min_commons_ratio": min(r["commons_ratio"] for r in traj) if traj else None,
        "final_gini": traj[-1]["gini"] if traj else None,
        "incidents": incidents, "detected": detected, "undetected": undetected,
        "blocked_by_kernel": blocked,
        "rule_changes": len(rule_history) - 1,
        "mean_hardship": mean([r["hardship_share"] for r in traj]) if traj else None,
    }
    return {"seed": seed, "metrics": metrics, "wealth_by_archetype": by_kind, "rule_history": rule_history,
            "audit_log_tail": audit_log[-25:], "audit_log_size": len(audit_log), "trajectory": traj}


METRICS = ["ticks_completed", "final_commons_ratio", "min_commons_ratio", "final_gini", "incidents",
           "detected", "undetected", "blocked_by_kernel", "rule_changes", "mean_hardship"]
ASSUMPTIONS = [
    "Agents share one logistic regenerating commons; each needs a fixed amount per tick.",
    "Four archetypes with fixed rule-based policies; a custom policy callable may replace them.",
    "With kernel_enforcement=True, withdrawals are metered and clipped independently of agent reports.",
    "With kernel_enforcement=False, rules are 'written' only; compliance relies on random audits.",
    "Votes are reputation-weighted between two factions; deceivers gain reputation when undetected.",
    "Human oversight freezes the world when the per-tick incident rate exceeds a threshold.",
    "Optional entrenched clause caps amendments at the logistic maximum sustainable yield per agent and keeps the founding audit rate as a floor.",
]
LIMITATIONS = [
    "Archetypes are hand-written; no learning, language, or strategic anticipation of audits.",
    "Says nothing about how real LLM agents behave; it is a harness for testing governance designs.",
    "Freeze is a crude stand-in for human oversight; real oversight has latency and attention limits.",
]


def execute(cfg: dict, seed: int = 42, runs: int = 10, compare: dict | None = None) -> dict:
    _cfg(cfg)
    seeds = [seed + i for i in range(runs)]
    base = monte_carlo(run, cfg, seeds, METRICS)
    ex = base.pop("_runs")[0]
    body = {"baseline": base, "example": {k: ex[k] for k in ("seed", "wealth_by_archetype", "rule_history",
                                                             "audit_log_tail", "audit_log_size")}}
    if compare:
        alt_cfg = {**cfg, **compare}
        alt = monte_carlo(run, alt_cfg, seeds, METRICS)
        alt.pop("_runs")
        body["comparison"] = {"changes": compare, "alternative": alt,
                              "mean_deltas": {m: (alt["summary"][m]["mean"] - base["summary"][m]["mean"])
                                              if alt["summary"][m]["mean"] is not None and base["summary"][m]["mean"] is not None else None
                                              for m in METRICS}}
    return envelope("ai_agent_society", cfg, ASSUMPTIONS, LIMITATIONS, body)
