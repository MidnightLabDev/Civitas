"""Civilization formation, expansion, alliance and fragmentation (CIVITAS 1.0).

A spatial multi-polity model inspired by Turchin's 'metaethnic frontier'
theory of asabiyyah (collective solidarity; the term is Ibn Khaldun's) as
formalised in Turchin (2003, Historical Dynamics) - re-implemented here as an
original stylised CIVITAS model, not a reproduction of the published code.

Mechanisms:
  * each cell belongs to a polity (or is stateless); cell solidarity S grows
    logistically on frontiers (contact with other polities) and decays in the
    secure interior;
  * a polity's projected power at distance d from its capital is
    size x mean(S) x exp(-d / reach), so large empires overstretch;
  * border cells change hands when attacker power exceeds defender power by a
    margin; defenders may receive help from allies (alliances form against a
    neighbour much larger than oneself - balancing behaviour);
  * a polity whose mean solidarity falls below a threshold fragments into
    independent cells (institutional failure), which can later re-coalesce.

Outputs: number of polities, largest polity share, concentration (HHI),
collapse events and polity lifespans over time.
"""

from __future__ import annotations

import math
import random

from .core import envelope, integer, mean, monte_carlo, num

DEFAULTS = {"width": 24, "height": 24, "ticks": 300, "initial_polities": 12,
            "frontier_growth": 0.2, "interior_decay": 0.1, "reach": 4.0,
            "attack_margin": 0.1, "collapse_threshold": 0.1, "alliances": True,
            "alliance_ratio": 2.0, "ally_contribution": 0.5, "wrap": True}


def _cfg(raw):
    c = {**DEFAULTS, **(raw or {})}
    return {"width": integer(c, "width", 24, 4, 200), "height": integer(c, "height", 24, 4, 200),
            "ticks": integer(c, "ticks", 300, 1, 20000),
            "initial_polities": integer(c, "initial_polities", 12, 1, 5000),
            "frontier_growth": num(c, "frontier_growth", 0.2, 0, 2),
            "interior_decay": num(c, "interior_decay", 0.1, 0, 1),
            "reach": num(c, "reach", 4.0, 0.1, 1000), "attack_margin": num(c, "attack_margin", 0.1, 0, 100),
            "collapse_threshold": num(c, "collapse_threshold", 0.1, 0, 1),
            "alliances": bool(c["alliances"]), "alliance_ratio": num(c, "alliance_ratio", 2.0, 1, 100),
            "ally_contribution": num(c, "ally_contribution", 0.5, 0, 1), "wrap": bool(c["wrap"])}


def run(raw, seed):
    c = _cfg(raw)
    rng = random.Random(seed)
    W, H = c["width"], c["height"]
    n = W * H

    def nbrs(i):
        x, y = i % W, i // W
        out = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if c["wrap"]:
                nx %= W
                ny %= H
            elif not (0 <= nx < W and 0 <= ny < H):
                continue
            out.append(ny * W + nx)
        return out

    NB = [nbrs(i) for i in range(n)]

    def dist(a, b):
        ax, ay, bx, by = a % W, a // W, b % W, b // W
        dx, dy = abs(ax - bx), abs(ay - by)
        if c["wrap"]:
            dx, dy = min(dx, W - dx), min(dy, H - dy)
        return math.hypot(dx, dy)

    owner = [-1] * n
    S = [0.05] * n
    capitals, born = {}, {}
    next_id = 0
    for cell in rng.sample(range(n), min(n, c["initial_polities"])):
        owner[cell] = next_id
        S[cell] = 0.5
        capitals[next_id] = cell
        born[next_id] = 0
        next_id += 1
    lifespans, collapses, traj = [], 0, []
    for t in range(c["ticks"]):
        # 1. solidarity dynamics
        newS = S[:]
        for i in range(n):
            if owner[i] < 0:
                newS[i] = max(0.01, S[i] * 0.99)
                continue
            frontier = any(owner[j] != owner[i] for j in NB[i])
            if frontier:
                newS[i] = min(1.0, S[i] + c["frontier_growth"] * S[i] * (1 - S[i]))
            else:
                newS[i] = max(0.0, S[i] - c["interior_decay"] * S[i])
        S = newS
        cells_of = {}
        for i, o in enumerate(owner):
            if o >= 0:
                cells_of.setdefault(o, []).append(i)
        size = {p: len(cs) for p, cs in cells_of.items()}
        meanS = {p: mean([S[i] for i in cs]) for p, cs in cells_of.items()}

        def power(p, at):
            return size[p] * meanS[p] * math.exp(-dist(capitals[p], at) / c["reach"])

        # alliances: neighbours of a much larger polity support each other against it
        neighbours = {p: set() for p in cells_of}
        for i in range(n):
            if owner[i] >= 0:
                for j in NB[i]:
                    if owner[j] >= 0 and owner[j] != owner[i]:
                        neighbours[owner[i]].add(owner[j])
        # 2. border conflict (asynchronous, random order)
        order = list(range(n))
        rng.shuffle(order)
        for i in order:
            d = owner[i]
            for j in NB[i]:
                a = owner[j]
                if a < 0 or a == d or a not in size:
                    continue
                att = power(a, i)
                if d < 0:
                    dfn = S[i] * 0.5   # stateless cell resists weakly
                else:
                    if d not in size:
                        continue
                    dfn = power(d, i)
                    if c["alliances"]:
                        for ally in neighbours.get(d, ()):
                            if ally != a and ally in size and a in neighbours.get(ally, ()) \
                                    and size[a] > c["alliance_ratio"] * size[d]:
                                dfn += c["ally_contribution"] * power(ally, i)
                if att - dfn > c["attack_margin"] and rng.random() < 0.5:
                    if d >= 0:
                        size[d] -= 1
                        if size[d] <= 0:
                            lifespans.append(t - born[d])
                            del size[d]
                    owner[i] = a
                    size[a] = size.get(a, 0) + 1
                    S[i] = (S[i] + meanS[a]) / 2
                    break
        # 3. fragmentation of low-solidarity polities; capitals lost -> relocate
        cells_of = {}
        for i, o in enumerate(owner):
            if o >= 0:
                cells_of.setdefault(o, []).append(i)
        for p in list(capitals):
            if p not in cells_of:
                del capitals[p]
                continue
            if owner[capitals[p]] != p:
                capitals[p] = max(cells_of[p], key=lambda k: S[k])
            ms = mean([S[i] for i in cells_of[p]])
            if ms < c["collapse_threshold"] and len(cells_of[p]) > 1:
                collapses += 1
                lifespans.append(t - born[p])
                del capitals[p]
                for i in cells_of[p]:
                    if rng.random() < 0.3:      # some cells found new micro-polities
                        owner[i] = next_id
                        S[i] = max(S[i], 0.3)
                        capitals[next_id] = i
                        born[next_id] = t
                        next_id += 1
                    else:
                        owner[i] = -1
        sizes = {}
        for o in owner:
            if o >= 0:
                sizes[o] = sizes.get(o, 0) + 1
        tot = sum(sizes.values()) or 1
        traj.append({"tick": t, "polities": len(sizes), "largest_share": max(sizes.values(), default=0) / n,
                     "hhi": sum((v / tot) ** 2 for v in sizes.values()), "stateless_share": 1 - tot / n,
                     "mean_solidarity": mean([S[i] for i in range(n) if owner[i] >= 0]) if tot else 0.0})
    largest = [r["largest_share"] for r in traj]
    metrics = {"final_polities": traj[-1]["polities"], "peak_largest_share": max(largest),
               "final_largest_share": largest[-1], "mean_hhi": mean([r["hhi"] for r in traj]),
               "collapses": collapses, "mean_lifespan": mean(lifespans) if lifespans else None,
               "final_stateless_share": traj[-1]["stateless_share"]}
    return {"seed": seed, "metrics": metrics, "trajectory": traj}


METRICS = ["final_polities", "peak_largest_share", "final_largest_share", "mean_hhi", "collapses",
           "mean_lifespan", "final_stateless_share"]


def execute(cfg, seed=42, runs=8, compare=None):
    _cfg(cfg)
    seeds = [seed + i for i in range(runs)]
    base = monte_carlo(run, cfg, seeds, METRICS)
    ex = base.pop("_runs")[0]
    body = {"baseline": base, "example_trajectory": ex["trajectory"][:: max(1, len(ex["trajectory"]) // 60)]}
    if compare:
        alt = monte_carlo(run, {**cfg, **compare}, seeds, METRICS)
        alt.pop("_runs")
        body["comparison"] = {"changes": compare, "alternative": alt}
    return envelope("polity_dynamics", cfg,
                    ["Space is a grid; one polity per cell; power decays exponentially with distance from capital",
                     "Solidarity grows on frontiers and decays in interiors (metaethnic frontier hypothesis)",
                     "Conflict resolves by power margin; alliances balance against much larger neighbours",
                     "Polities whose mean solidarity falls below a threshold fragment"],
                    ["Geography, economy, ideology, disease, climate and technology are absent",
                     "The frontier hypothesis is one contested theory of state formation among several",
                     "Cycle lengths and empire sizes are parameter artefacts, not historical estimates"], body)
