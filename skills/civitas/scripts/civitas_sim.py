#!/usr/bin/env python3
"""CIVITAS 1.0: seeded fictional aggregate civilization teaching model.

This is NOT a fitted population model, psychohistory predictor, policy estimator,
individual agent simulation, or evidence for real social outcomes.

Run from the civitas folder:
    python scripts/civitas_sim.py --config examples/civilization_scenario.json --runs 25 --seed 42 --compare --output comparison.json
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


FLOAT_FIELDS = ("food", "energy", "knowledge", "trust", "legitimacy", "population", "production_factor")
PARAMS = {
    "food_production_per_person": (0, 50),
    "food_need_per_person": (0, 50),
    "energy_production_per_person": (0, 50),
    "energy_need_per_person": (0, 50),
    "resource_decay": (0, 1),
    "knowledge_gain": (0, 1),
    "population_growth": (0, 1),
    "shortage_population_loss": (0, 1),
    "resource_shock_probability": (0, 1),
    "resource_shock_fraction": (0, 1),
    "redistribution_rate": (0, 1),
    "reserve_fraction": (0, 10),
    "aid_trust_gain": (0, 1),
    "shortage_trust_loss": (0, 1),
}


def bounded(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return min(high, max(low, value))


def number(value: Any, name: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}: expected a number")
    x = float(value)
    if not math.isfinite(x) or not minimum <= x <= maximum:
        raise ValueError(f"{name}: expected finite number in [{minimum}, {maximum}]")
    return x


def validate(config: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a JSON object")
    if not isinstance(config.get("title"), str) or not config["title"].strip():
        raise ValueError("title must be nonempty text")
    ticks = config.get("ticks")
    if isinstance(ticks, bool) or not isinstance(ticks, int) or not 1 <= ticks <= 10000:
        raise ValueError("ticks must be an integer between 1 and 10000")
    societies = config.get("societies")
    if not isinstance(societies, list) or not 1 <= len(societies) <= 1000:
        raise ValueError("societies must contain between 1 and 1000 entries")
    ids: set[str] = set()
    for society in societies:
        if not isinstance(society, dict) or not isinstance(society.get("id"), str):
            raise ValueError("Each society must have a string id")
        name = society["id"]
        if not name or name in ids:
            raise ValueError(f"Society ids must be nonempty and unique: {name}")
        ids.add(name)
        for field in FLOAT_FIELDS:
            if field not in society:
                raise ValueError(f"{name} missing {field}")
            bound = 1 if field in ("trust", "knowledge", "legitimacy") else 1e12
            lower = 0.000001 if field in ("population", "production_factor") else 0
            number(society[field], f"{name}.{field}", lower, bound)
    params = config.get("parameters")
    if not isinstance(params, dict) or set(params) != set(PARAMS):
        raise ValueError(f"parameters must define exactly: {', '.join(PARAMS)}")
    for k, (low, high) in PARAMS.items():
        number(params[k], f"parameters.{k}", low, high)
    comparison = config.get("comparison")
    if comparison is not None:
        if not isinstance(comparison, dict) or comparison.get("parameter") not in PARAMS:
            raise ValueError("comparison.parameter must name a known parameter")
        key = comparison["parameter"]
        low, high = PARAMS[key]
        number(comparison.get("alternative_value"), "comparison.alternative_value", low, high)
    return deepcopy(config)


def redistribute(state: list[dict[str, Any]], resource: str, need_per_person: float,
                 transfer_rate: float, reserve_fraction: float) -> dict[str, float]:
    """Move fictional stocks between societies, with no creation or destruction."""
    aid = {s["id"]: 0.0 for s in state}
    if transfer_rate <= 0 or need_per_person <= 0:
        return aid
    deficits = {s["id"]: max(0.0, s["population"] * need_per_person - s[resource]) for s in state}
    donors = {s["id"]: max(0.0, (s[resource] - s["population"] * need_per_person *
                                    (1 + reserve_fraction)) * transfer_rate) for s in state}
    total_deficit = sum(deficits.values())
    total_available = sum(donors.values())
    if total_deficit <= 0 or total_available <= 0:
        return aid
    moved = min(total_deficit, total_available)
    lookups = {s["id"]: s for s in state}
    for name, share in donors.items():
        out = moved * share / total_available
        lookups[name][resource] -= out
        aid[name] -= out
    for name, share in deficits.items():
        incoming = moved * share / total_deficit
        lookups[name][resource] += incoming
        aid[name] += incoming
    return aid


def step(state: list[dict[str, Any]], params: dict[str, float], rng: random.Random,
         tick: int) -> dict[str, Any]:
    production = {"food": 0.0, "energy": 0.0}
    decay_and_shocks = {"food": 0.0, "energy": 0.0}
    consumption = {"food": 0.0, "energy": 0.0}
    total_before = {r: sum(s[r] for s in state) for r in ("food", "energy")}
    shocks: list[str] = []

    for s in state:
        for resource in ("food", "energy"):
            amount = (s["population"] * params[f"{resource}_production_per_person"] *
                      s["production_factor"] * (0.75 + 0.5 * s["knowledge"]))
            s[resource] += amount
            production[resource] += amount
            lost = s[resource] * params["resource_decay"]
            s[resource] -= lost
            decay_and_shocks[resource] += lost
            if rng.random() < params["resource_shock_probability"]:
                lost = s[resource] * params["resource_shock_fraction"]
                s[resource] -= lost
                decay_and_shocks[resource] += lost
                shocks.append(f"{s['id']}:{resource}")

    aid_received = {s["id"]: 0.0 for s in state}
    for resource in ("food", "energy"):
        received = redistribute(state, resource, params[f"{resource}_need_per_person"],
                                params["redistribution_rate"], params["reserve_fraction"])
        for name, value in received.items():
            aid_received[name] += max(0.0, value)

    shortage_totals = {"food": 0.0, "energy": 0.0}
    for s in state:
        deficits = []
        for resource in ("food", "energy"):
            need = s["population"] * params[f"{resource}_need_per_person"]
            consumed = min(need, s[resource])
            s[resource] -= consumed
            consumption[resource] += consumed
            missing = max(0.0, need - consumed)
            shortage_totals[resource] += missing
            deficits.append(missing / need if need > 0 else 0.0)
        worst_shortage = max(deficits)
        s["population"] *= max(0.0, 1 + params["population_growth"] * s["legitimacy"] -
                               params["shortage_population_loss"] * worst_shortage)
        s["trust"] = bounded(s["trust"] - params["shortage_trust_loss"] * worst_shortage +
                             (params["aid_trust_gain"] if aid_received[s["id"]] > 1e-9 else 0))
        s["legitimacy"] = bounded(s["legitimacy"] + 0.003 * (s["trust"] - 0.5) -
                                  0.025 * worst_shortage)
        s["knowledge"] = bounded(s["knowledge"] + params["knowledge_gain"] *
                                 (0.25 + s["legitimacy"] * 0.75))

    total_after = {r: sum(s[r] for s in state) for r in ("food", "energy")}
    ledger_error = {}
    for resource in ("food", "energy"):
        expected = total_before[resource] + production[resource] - decay_and_shocks[resource] - consumption[resource]
        ledger_error[resource] = total_after[resource] - expected
        if abs(ledger_error[resource]) > 1e-7 * max(1, expected):
            raise AssertionError(f"Resource conservation failed at tick {tick}: {resource}")
    return {"tick": tick, "shocks": shocks, "shortage": shortage_totals,
            "aid_received": aid_received, "resource_ledger_error": ledger_error}


def one_run(config: dict[str, Any], seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    state = deepcopy(config["societies"])
    initial = {s["id"]: s["population"] for s in state}
    totals = {"food": 0.0, "energy": 0.0, "shocks": 0}
    history = []
    for tick in range(1, config["ticks"] + 1):
        event = step(state, config["parameters"], rng, tick)
        for r in ("food", "energy"):
            totals[r] += event["shortage"][r]
        totals["shocks"] += len(event["shocks"])
        history.append({"tick": tick, "mean_trust": statistics.mean(s["trust"] for s in state),
                        "total_population": sum(s["population"] for s in state),
                        "total_food": sum(s["food"] for s in state),
                        "total_energy": sum(s["energy"] for s in state),
                        "food_shortfall": event["shortage"]["food"],
                        "energy_shortfall": event["shortage"]["energy"],
                        "shocks": event["shocks"],
                        "resource_ledger_error": event["resource_ledger_error"]})
    metrics = {
        "total_population": sum(s["population"] for s in state),
        "mean_trust": statistics.mean(s["trust"] for s in state),
        "lowest_trust": min(s["trust"] for s in state),
        "food_shortfall_total": totals["food"],
        "energy_shortfall_total": totals["energy"],
        "shock_count": totals["shocks"],
        "societies_below_80pct_initial_population": sum(s["population"] < 0.8 * initial[s["id"]] for s in state),
    }
    return {"seed": seed, "metrics": metrics, "final_societies": state, "trajectory": history}


def batches(config: dict[str, Any], seeds: list[int]) -> dict[str, Any]:
    runs = [one_run(config, seed) for seed in seeds]
    names = runs[0]["metrics"]
    summary = {}
    for metric in names:
        values = [run["metrics"][metric] for run in runs]
        summary[metric] = {"mean": statistics.mean(values),
                           "min": min(values), "max": max(values),
                           "sample_std": statistics.stdev(values) if len(values) > 1 else None}
    return {"summary": summary, "runs": runs}


def execute(config: dict[str, Any], seed: int = 42, runs: int = 25,
            compare: bool = False, config_hash: str = "") -> dict[str, Any]:
    config = validate(config)
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    if isinstance(runs, bool) or not isinstance(runs, int) or not 1 <= runs <= 10000:
        raise ValueError("runs must be between 1 and 10000")
    seeds = [seed + i for i in range(runs)]
    result = {
        "model": "CIVITAS 1.0 synthetic aggregate demonstration",
        "epistemic_status": "fiction_synthetic",
        "warning": "Outputs follow illustrative equations and cannot establish real social predictions or policy impacts.",
        "config_sha256": config_hash or None,
        "title": config["title"],
        "purpose": config.get("purpose", "Synthetic illustration"),
        "configuration": config,
        "seed_start": seed,
        "n_runs": runs,
        "baseline": batches(config, seeds),
    }
    if compare:
        comparison = config.get("comparison")
        if comparison is None:
            raise ValueError("--compare requires a comparison section in configuration")
        alternative = deepcopy(config)
        key = comparison["parameter"]
        alternative["parameters"][key] = comparison["alternative_value"]
        alternative_runs = batches(alternative, seeds)
        result["comparison"] = {
            "changed_parameter": key,
            "original_value": config["parameters"][key],
            "alternative_value": comparison["alternative_value"],
            "label": comparison.get("label", "Alternative parameters"),
            "same_seed_pairs": True,
            "alternative": alternative_runs,
            "mean_delta_alternative_minus_baseline": {
                metric: alternative_runs["summary"][metric]["mean"] - result["baseline"]["summary"][metric]["mean"]
                for metric in result["baseline"]["summary"]
            },
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path, help="JSON scenario")
    parser.add_argument("--runs", type=int, default=25, help="paired random seeds, max 10000")
    parser.add_argument("--seed", type=int, default=42, help="starting pseudorandom seed")
    parser.add_argument("--compare", action="store_true", help="compare config alternative with same seeds")
    parser.add_argument("--output", type=Path, help="write full JSON result")
    parser.add_argument("--csv", type=Path, help="optional flat run metrics CSV")
    args = parser.parse_args()
    try:
        config_bytes = args.config.read_bytes()
        config = json.loads(config_bytes)
        result = execute(config, args.seed, args.runs, args.compare,
                         hashlib.sha256(config_bytes).hexdigest())
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        if args.csv:
            args.csv.parent.mkdir(parents=True, exist_ok=True)
            groups = [("baseline", result["baseline"]["runs"])]
            if args.compare:
                groups.append(("alternative", result["comparison"]["alternative"]["runs"]))
            with args.csv.open("w", newline="", encoding="utf-8") as handle:
                fieldnames = ["group", "seed"] + list(result["baseline"]["runs"][0]["metrics"])
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                for group, group_runs in groups:
                    for run in group_runs:
                        writer.writerow({"group": group, "seed": run["seed"], **run["metrics"]})
        overview = {"title": result["title"], "n_runs": result["n_runs"],
                    "warning": result["warning"], "baseline_means": {
                        k: round(v["mean"], 6) for k, v in result["baseline"]["summary"].items()}}
        if args.compare:
            overview["alternative_minus_baseline"] = {
                k: round(v, 6) for k, v in result["comparison"]["mean_delta_alternative_minus_baseline"].items()}
        print(json.dumps(overview, indent=2))
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError, AssertionError) as exc:
        print(f"CIVITAS input or model error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
