"""Causal loop diagram analyser (CIVITAS 1.0).

Input: signed directed edges [{"from": A, "to": B, "sign": "+"|"-",
"delay": bool, "evidence": "established|estimate|assumed|speculative"}].

Output:
  * every elementary feedback cycle (Johnson-style DFS, bounded length),
    classified REINFORCING (even number of negative links) or BALANCING (odd),
  * loops containing delays (oscillation risk),
  * the weakest evidence on each loop (a loop is only as strong as its weakest link),
  * leverage candidates: variables on the most loops, and in/out degree,
  * a Mermaid diagram string for rendering.

A CLD is a hypothesis about structure, not a proof of causation.
"""

from __future__ import annotations

EVIDENCE_RANK = {"established": 3, "estimate": 2, "assumed": 1, "speculative": 0}


def _cycles(nodes, out, max_len):
    order = {n: i for i, n in enumerate(nodes)}
    found = []

    def dfs(start, v, path, visited):
        for w in out.get(v, []):
            if w == start and len(path) >= 1:
                found.append(path[:])
            elif w not in visited and order[w] > order[start] and len(path) < max_len:
                visited.add(w)
                path.append(w)
                dfs(start, w, path, visited)
                path.pop()
                visited.discard(w)

    for s in nodes:
        dfs(s, s, [s], {s})
    return found


def analyze(edges: list[dict], max_loop_length: int = 8) -> dict:
    if not edges:
        raise ValueError("no edges")
    emap = {}
    nodes = []
    out: dict[str, list[str]] = {}
    for e in edges:
        a, b, s = e["from"], e["to"], e.get("sign", "+")
        if s not in ("+", "-"):
            raise ValueError(f"sign must be + or -: {e}")
        ev = e.get("evidence", "assumed")
        if ev not in EVIDENCE_RANK:
            raise ValueError(f"evidence must be one of {list(EVIDENCE_RANK)}")
        for x in (a, b):
            if x not in out:
                out[x] = []
                nodes.append(x)
        out[a].append(b)
        emap[(a, b)] = {"sign": s, "delay": bool(e.get("delay", False)), "evidence": ev}
    loops = []
    for cyc in _cycles(nodes, out, max_loop_length):
        links = [(cyc[i], cyc[(i + 1) % len(cyc)]) for i in range(len(cyc))]
        neg = sum(emap[l]["sign"] == "-" for l in links)
        weakest = min((emap[l]["evidence"] for l in links), key=lambda x: EVIDENCE_RANK[x])
        loops.append({"variables": cyc, "type": "balancing" if neg % 2 else "reinforcing",
                      "length": len(cyc), "has_delay": any(emap[l]["delay"] for l in links),
                      "weakest_evidence": weakest})
    count = {n: 0 for n in nodes}
    for lp in loops:
        for v in lp["variables"]:
            count[v] += 1
    indeg = {n: 0 for n in nodes}
    for (a, b) in emap:
        indeg[b] += 1
    leverage = sorted(nodes, key=lambda n: (count[n], len(out[n]) + indeg[n]), reverse=True)
    mer = ["graph LR"]
    ids = {n: f"n{i}" for i, n in enumerate(nodes)}
    for (a, b), d in emap.items():
        lab = d["sign"] + (" ||" if d["delay"] else "")
        mer.append(f'  {ids[a]}["{a}"] -->|"{lab}"| {ids[b]}["{b}"]')
    warnings = []
    if not any(l["type"] == "balancing" for l in loops):
        warnings.append("No balancing loop: real systems hit limits; a constraint is probably missing.")
    if any(l["type"] == "reinforcing" and l["weakest_evidence"] in ("assumed", "speculative") for l in loops):
        warnings.append("At least one reinforcing loop rests on assumed/speculative links: treat runaway conclusions as hypotheses.")
    return {"n_variables": len(nodes), "n_links": len(emap), "loops": loops,
            "reinforcing": sum(l["type"] == "reinforcing" for l in loops),
            "balancing": sum(l["type"] == "balancing" for l in loops),
            "loop_participation": count, "leverage_candidates": leverage[:5],
            "warnings": warnings, "mermaid": "\n".join(mer)}
