#!/usr/bin/env python3
"""CIVITAS 1.0 unified command line for the civlab model suite (stdlib only).

Usage (run from the skill root folder):
  python scripts/civitas.py list
  python scripts/civitas.py run society --config examples/society_commons.json --runs 10 --seed 42
  python scripts/civitas.py run society --set governance=central --set corruption=0.4 --runs 10
  python scripts/civitas.py compare society --set governance=none --alt governance=peer --runs 10
  python scripts/civitas.py sensitivity society --metric tail_mean_cooperation \
        --range multiplier=2.5:5.5 --range punish_fine=0:2 --method morris
  python scripts/civitas.py robust aisociety --metric final_commons_ratio \
        --policy open= --policy entrenched=entrenched_sustainability=true \
        --uncertain commons_regen=0.1:0.3
  python scripts/civitas.py ews --csv data.csv --column value
  python scripts/civitas.py cld --config examples/cld_platform.json
  python scripts/civitas.py baserate --k 3 --n 20
  python scripts/civitas.py bayes --prior 0.2 --lr "signal A=3" --lr "signal B=0.5"
  python scripts/civitas.py ach --config examples/ach_example.json

Every result is JSON with an 'epistemic_status' and 'warning'. Full results go
to --output; stdout gets a compact summary so it fits in a model's context.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from civlab import (aisociety, cascade, cld, diffusion, ews, forecast, knowledge,  # noqa: E402
                    polity, sdt, sensitivity, society)
from civlab.core import paired_delta  # noqa: E402

MODELS = {
    "society": (society, "Networked population: cooperation, punishment, institutions, legitimacy, inequality"),
    "aisociety": (aisociety, "Autonomous AI agent society with constitution kernel, votes, audits, oversight"),
    "sdt": (sdt, "Structural-demographic stress (elite overproduction, wages, fiscal distress, PSI)"),
    "polity": (polity, "Multi-polity civilization: expansion, alliances, solidarity, fragmentation"),
    "diffusion": (diffusion, "Technology/behaviour diffusion: Bass curve or network threshold cascades"),
    "cascade": (cascade, "Infrastructure/institutional failure cascades, optional interdependence"),
    "knowledge": (knowledge, "Knowledge preservation: tacit skill (Henrich) + archive redundancy"),
    "ews": (ews, "Early-warning signals of critical transitions in a time series"),
}
RUNNABLE = {"society", "aisociety", "sdt", "polity", "diffusion", "cascade", "knowledge"}


def parse_value(v: str):
    low = v.lower()
    if low in ("true", "false"):
        return low == "true"
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    if v.startswith(("{", "[")):
        return json.loads(v)
    return v


def kv_list(items) -> dict:
    out = {}
    for it in items or []:
        if "=" not in it:
            raise ValueError(f"expected key=value, got {it!r}")
        k, v = it.split("=", 1)
        out[k.strip()] = parse_value(v.strip())
    return out


def load_cfg(path, sets) -> dict:
    cfg = json.loads(Path(path).read_text(encoding="utf-8")) if path else {}
    cfg = cfg.get("parameters", cfg) if isinstance(cfg, dict) else cfg
    cfg = {k: v for k, v in cfg.items() if not k.startswith("_")}
    cfg.update(kv_list(sets))
    return cfg


def compact(obj, depth=0):
    """Strip long arrays so stdout stays readable."""
    if isinstance(obj, dict):
        return {k: compact(v, depth + 1) for k, v in obj.items()
                if k not in ("per_run", "trajectory", "example_trajectory", "indicators", "series",
                             "example_curve", "configuration", "audit_log_tail", "trajectory_thinned",
                             "example_archive_curve", "curve")}
    if isinstance(obj, list) and len(obj) > 12:
        return obj[:6] + [f"... {len(obj) - 6} more"]
    if isinstance(obj, float):
        return round(obj, 5)
    if isinstance(obj, list):
        return [compact(x, depth + 1) for x in obj]
    return obj


def emit(result, output):
    if output:
        p = Path(output)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(result, indent=2, default=str, allow_nan=True) + "\n", encoding="utf-8")
    print(json.dumps(compact(result), indent=2, default=str))


def parse_ranges(items):
    out = {}
    for it in items or []:
        k, v = it.split("=", 1)
        lo, hi = v.split(":")
        out[k] = (float(lo), float(hi))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="CIVITAS 1.0 civlab command line")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    for name in ("run", "compare"):
        p = sub.add_parser(name)
        p.add_argument("model", choices=sorted(RUNNABLE))
        p.add_argument("--config")
        p.add_argument("--set", action="append", default=[])
        p.add_argument("--alt", action="append", default=[], help="compare: overrides for the alternative")
        p.add_argument("--runs", type=int, default=10)
        p.add_argument("--seed", type=int, default=42)
        p.add_argument("--output")
    p = sub.add_parser("sensitivity")
    p.add_argument("model", choices=sorted(RUNNABLE - {"diffusion", "knowledge"}))
    p.add_argument("--config")
    p.add_argument("--set", action="append", default=[])
    p.add_argument("--metric", required=True)
    p.add_argument("--range", action="append", required=True, help="param=lo:hi")
    p.add_argument("--method", choices=["oat", "morris"], default="morris")
    p.add_argument("--trajectories", type=int, default=8)
    p.add_argument("--output")
    p = sub.add_parser("robust")
    p.add_argument("model", choices=sorted(RUNNABLE - {"diffusion", "knowledge"}))
    p.add_argument("--config")
    p.add_argument("--set", action="append", default=[])
    p.add_argument("--metric", required=True)
    p.add_argument("--minimize", action="store_true")
    p.add_argument("--policy", action="append", required=True, help="name=k=v,k=v  (name= for baseline)")
    p.add_argument("--uncertain", action="append", required=True, help="param=lo:hi")
    p.add_argument("--futures", type=int, default=12)
    p.add_argument("--output")
    p = sub.add_parser("ews")
    p.add_argument("--csv")
    p.add_argument("--column")
    p.add_argument("--synthetic", choices=["approach", "null"])
    p.add_argument("--window-frac", type=float, default=0.5)
    p.add_argument("--bandwidth-frac", type=float, default=0.1)
    p.add_argument("--surrogates", type=int, default=100)
    p.add_argument("--output")
    p = sub.add_parser("cld")
    p.add_argument("--config", required=True)
    p.add_argument("--output")
    p = sub.add_parser("baserate")
    p.add_argument("--k", type=int, required=True)
    p.add_argument("--n", type=int, required=True)
    p = sub.add_parser("bayes")
    p.add_argument("--prior", type=float, required=True)
    p.add_argument("--lr", action="append", default=[], help="'label=ratio'")
    p = sub.add_parser("pool")
    p.add_argument("--p", type=float, action="append", required=True)
    p.add_argument("--method", choices=["logit", "linear"], default="logit")
    p.add_argument("--extremize", type=float, default=1.0)
    p = sub.add_parser("score")
    p.add_argument("--ledger", required=True)
    p = sub.add_parser("ach")
    p.add_argument("--config", required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "list":
            print(json.dumps({k: v[1] for k, v in MODELS.items()} |
                             {"cld": "Causal loop analyser", "baserate/bayes/pool/score/ach": "Forecasting and evidence tools",
                              "sensitivity/robust": "OAT, Morris screening, minimax-regret robust choice"}, indent=2))
            return 0
        if args.cmd == "run":
            mod = MODELS[args.model][0]
            emit(mod.execute(load_cfg(args.config, args.set), seed=args.seed, runs=args.runs), args.output)
            return 0
        if args.cmd == "compare":
            mod = MODELS[args.model][0]
            base = load_cfg(args.config, args.set)
            alt = {**base, **kv_list(args.alt)}
            if not args.alt:
                raise ValueError("compare needs at least one --alt key=value")
            r_a = mod.execute(base, seed=args.seed, runs=args.runs)
            r_b = mod.execute(alt, seed=args.seed, runs=args.runs)
            pa = _per_run(r_a)
            pb = _per_run(r_b)
            deltas = {}
            for m in pa[0]:
                if m == "seed":
                    continue
                xa = [r[m] for r in pa]
                xb = [r[m] for r in pb]
                if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in xa + xb):
                    deltas[m] = paired_delta(xa, xb)
            emit({"civitas_version": "1.0", "model": args.model, "epistemic_status": r_a["epistemic_status"],
                  "warning": r_a["warning"], "baseline_overrides": kv_list(args.set),
                  "alternative_overrides": kv_list(args.alt), "same_seeds": True, "n_runs": args.runs,
                  "paired_deltas_alt_minus_base": deltas, "assumptions": r_a["assumptions"],
                  "limitations": r_a["limitations"]}, args.output)
            return 0
        if args.cmd == "sensitivity":
            mod = MODELS[args.model][0]
            base = load_cfg(args.config, args.set)
            rng_ = parse_ranges(args.range)
            res = (sensitivity.morris(mod.run, base, rng_, args.metric, trajectories=args.trajectories)
                   if args.method == "morris" else sensitivity.one_at_a_time(mod.run, base, rng_, args.metric))
            emit({"civitas_version": "1.0", "model": args.model, "epistemic_status": "fiction", **res}, args.output)
            return 0
        if args.cmd == "robust":
            mod = MODELS[args.model][0]
            base = load_cfg(args.config, args.set)
            pols = {}
            for it in args.policy:
                name, _, rest = it.partition("=")
                pols[name] = kv_list([x for x in rest.split(",") if x])
            res = sensitivity.robust_choice(mod.run, base, pols, parse_ranges(args.uncertain), args.metric,
                                            maximize=not args.minimize, futures=args.futures)
            emit({"civitas_version": "1.0", "model": args.model, "epistemic_status": "fiction", **res}, args.output)
            return 0
        if args.cmd == "ews":
            cfg = {"window_frac": args.window_frac, "bandwidth_frac": args.bandwidth_frac,
                   "surrogates": args.surrogates}
            if args.csv:
                with open(args.csv, newline="", encoding="utf-8") as f:
                    rows = list(csv.DictReader(f))
                col = args.column or list(rows[0])[-1]
                cfg["series"] = [float(r[col]) for r in rows if r[col] not in ("", None)]
            else:
                cfg["approach"] = (args.synthetic or "approach") == "approach"
            emit(ews.execute(cfg), args.output)
            return 0
        if args.cmd == "cld":
            spec = json.loads(Path(args.config).read_text(encoding="utf-8"))
            res = cld.analyze(spec["edges"] if isinstance(spec, dict) else spec)
            emit({"civitas_version": "1.0", "epistemic_status": "model_projection", **res}, args.output)
            return 0
        if args.cmd == "baserate":
            print(json.dumps(forecast.base_rate(args.k, args.n), indent=2))
            return 0
        if args.cmd == "bayes":
            ev = []
            for it in args.lr:
                lab, _, val = it.rpartition("=")
                ev.append({"label": lab, "likelihood_ratio": float(val)})
            print(json.dumps(forecast.bayes_update(args.prior, ev), indent=2))
            return 0
        if args.cmd == "pool":
            print(json.dumps({"pooled": forecast.pool(args.p, method=args.method, extremize=args.extremize)}))
            return 0
        if args.cmd == "score":
            print(json.dumps(forecast.Ledger(args.ledger).score(), indent=2))
            return 0
        if args.cmd == "ach":
            spec = json.loads(Path(args.config).read_text(encoding="utf-8"))
            print(json.dumps(forecast.ach(spec["hypotheses"], spec["evidence"]), indent=2))
            return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError, AssertionError) as exc:
        print(f"CIVITAS error: {exc}", file=sys.stderr)
        return 2
    return 1


def _per_run(result):
    for key in ("baseline", "monte_carlo"):
        if key in result and "per_run" in result[key]:
            return result[key]["per_run"]
    if "per_run" in result:
        return result["per_run"]
    raise ValueError("model result has no per-run metrics to compare")


if __name__ == "__main__":
    sys.exit(main())
