"""Infrastructure / institutional failure cascades (CIVITAS 1.0).

Load-redistribution cascade in the spirit of Motter & Lai (2002): each node
carries load (here: its betweenness proxy = degree-based load, cheap and
transparent) and has capacity (1 + tolerance) x initial load. When nodes fail,
the load they carried is redistributed to surviving neighbours; overloaded
nodes fail in turn. Optional interdependence (Buldyrev et al. 2010 flavour):
nodes in layer B fail when their partner in layer A fails.

Use it to compare redundancy, tolerance margins and attack/failure modes for a
networked system (power, supply chains, payment rails, institutions that
depend on each other). Not an engineering-grade power-flow model.
"""

from __future__ import annotations

import random

from .core import components, envelope, integer, make_graph, mean, num, summarize

DEFAULTS = {"nodes": 300, "graph": "scale_free", "degree": 4, "rewire": 0.1,
            "tolerance": 0.3, "initial_failures": 3, "attack": "random",
            "interdependent": False}


def _cfg(raw):
    c = {**DEFAULTS, **(raw or {})}
    if c["attack"] not in {"random", "targeted"}:
        raise ValueError("attack must be random or targeted")
    return {"nodes": integer(c, "nodes", 300, 10, 50000), "graph": c["graph"],
            "degree": integer(c, "degree", 4, 1, 100), "rewire": num(c, "rewire", 0.1, 0, 1),
            "tolerance": num(c, "tolerance", 0.3, 0, 100),
            "initial_failures": integer(c, "initial_failures", 3, 1, 50000),
            "attack": c["attack"], "interdependent": bool(c["interdependent"])}


def _cascade(adj, load, cap, alive, initial):
    for i in initial:
        alive[i] = False
    queue = list(initial)
    rounds = 0
    while queue:
        rounds += 1
        nxt = []
        for f in queue:
            nbrs = [v for v in adj[f] if alive[v]]
            if nbrs:
                share = load[f] / len(nbrs)
                for v in nbrs:
                    load[v] += share
            load[f] = 0.0
        for v in range(len(adj)):
            if alive[v] and load[v] > cap[v] + 1e-12:
                alive[v] = False
                nxt.append(v)
        queue = nxt
    return rounds


def run(raw, seed):
    c = _cfg(raw)
    rng = random.Random(seed)
    n = c["nodes"]
    adj = [sorted(s) for s in make_graph(c["graph"], n, rng, c["degree"], c["rewire"])]
    load = [float(len(a)) + 1.0 for a in adj]
    cap = [(1 + c["tolerance"]) * x for x in load]
    alive = [True] * n
    k = min(n, c["initial_failures"])
    initial = (sorted(range(n), key=lambda i: len(adj[i]), reverse=True)[:k]
               if c["attack"] == "targeted" else rng.sample(range(n), k))
    rounds = _cascade(adj, load, cap, alive, initial)
    if c["interdependent"]:
        # layer B: independent random graph of same size, node i depends on A-node perm[i]
        adj_b = [sorted(s) for s in make_graph("random", n, rng, c["degree"], 0)]
        perm = list(range(n))
        rng.shuffle(perm)
        alive_b = [alive[perm[i]] for i in range(n)]
        changed = True
        while changed:
            changed = False
            giant_b = max(components(adj_b, alive_b), key=len, default=[])
            gb = set(giant_b)
            for i in range(n):
                if alive_b[i] and i not in gb:
                    alive_b[i] = False
                    changed = True
            for i in range(n):
                if not alive_b[i] and alive[perm[i]]:
                    alive[perm[i]] = False
                    changed = True
            giant_a = set(max(components(adj, alive), key=len, default=[]))
            for i in range(n):
                if alive[i] and i not in giant_a:
                    alive[i] = False
                    changed = True
            for i in range(n):
                if alive_b[i] and not alive[perm[i]]:
                    alive_b[i] = False
                    changed = True
    giant = max(components(adj, alive), key=len, default=[])
    metrics = {"surviving_share": sum(alive) / n, "giant_component_share": len(giant) / n,
               "cascade_rounds": rounds, "failed_share": 1 - sum(alive) / n}
    return {"seed": seed, "metrics": metrics}


def execute(cfg, seed=42, runs=20):
    _cfg(cfg)
    rs = [run(cfg, seed + i) for i in range(runs)]
    body = {"summary": {m: summarize([r["metrics"][m] for r in rs]) for m in rs[0]["metrics"]},
            "per_run": [{"seed": r["seed"], **r["metrics"]} for r in rs]}
    return envelope("failure_cascade", cfg,
                    ["Node load = degree + 1 (proxy for flow); capacity = (1 + tolerance) x initial load",
                     "Failed node's load is shared equally among surviving neighbours",
                     "Interdependent mode: a node survives only if its partner survives and it is in its layer's giant component"],
                    ["Proxy loads, not physical flows; real grids need power-flow models",
                     "Assumes instant redistribution and no repair or islanding control"], body)
