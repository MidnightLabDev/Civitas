# Structured records for CIVITAS projects

These are design examples, not a mandatory API contract. Adapt to user requirements and check security before external integrations.

## Evidence claim JSON example

```json
{
  "id": "claim_001",
  "claim": "Shared infrastructure may increase firm entry",
  "epistemic_status": "E2",
  "evidence_urls": [],
  "assumptions": ["Capacity is available", "Access terms remain open"],
  "alternate_explanations": ["Market demand increased independently"],
  "falsification": "Compare entry rates with a matched control",
  "last_reviewed": null
}
```

Valid tiers: `E1` established, `E2` evidenced, `E3` modeled, `E4` exploratory, `E5` fiction, `E6` speculative. Simulator envelopes use the long names `established`, `evidence_estimate`, `model_projection`, `exploratory`, `fiction`, `speculation`.

## Simulated action object

```json
{
  "action_id": "a91",
  "tick": 17,
  "actor_id": "settlement_east",
  "intent": "transfer_resource",
  "parameters": {"resource": "energy", "quantity": 12, "recipient": "settlement_west"},
  "permission_required": "world_resource_transfer",
  "authorized": false,
  "status": "proposed"
}
```

Always validate permissions and resource constraints independently of model generated text.

## World state essentials

```json
{
  "world_id": "demo_civilization",
  "tick": 0,
  "seed": 42,
  "rule_version": "1.0",
  "resources": {"energy": 100, "food": 100},
  "institutions": [],
  "actors": [],
  "events": [],
  "model_assumptions": ["All resources are fictional"],
  "data_origin": "synthetic"
}
```

## Report schema

A CIVITAS scenario report should contain: `question`, `time_horizon`, `system_boundary`, `sources`, `assumptions`, `agents`, `feedback_loops`, `branches`, `decision_options`, `harm_metrics`, `model_limits`, and `next_test`. If code is executed also include `run_seed`, `model_version`, `config_hash`, `n_runs`, and source path for results.

## Simulator configuration

See the shipped `examples/civilization_scenario.json`, which includes fictional starting conditions, parameter values, and a policy comparison. The Python script validates this schema at runtime and refuses nonsensical values. Its numeric model is an explicit demonstration, not a claim about historical society.

## civlab result envelope (all models)

```json
{
  "civitas_version": "1.0",
  "model": "networked_society",
  "epistemic_status": "fiction",
  "warning": "Output describes the behaviour of a stylized model ...",
  "config_sha256": "...",
  "configuration": {},
  "assumptions": ["..."],
  "limitations": ["..."],
  "baseline": {"seeds": [42, 43], "summary": {"metric": {"n": 2, "mean": 0.5, "sd": 0.1, "p05": 0.4, "p50": 0.5, "p95": 0.6}}, "per_run": []}
}
```

## Forecast ledger line (append-only JSONL)

```json
{"ts": "2026-10-27T10:00:00Z", "type": "forecast", "qid": "q1", "question": "...", "p": 0.3,
 "resolution_criteria": "...", "resolve_by": "2027-12-31", "rationale": "base rate 3/20 + LR 1.5"}
{"ts": "2028-01-02T09:00:00Z", "type": "resolution", "qid": "q1", "outcome": 0, "source": "official bulletin"}
```

## Causal loop input

```json
{"edges": [{"from": "users", "to": "data", "sign": "+", "delay": false, "evidence": "estimate"}]}
```
`evidence` is one of `established`, `estimate`, `assumed`, `speculative`.

## Agent policy proposal (aisociety)

`{"action": "harvest", "amount": 2.0, "report": 2.0}` · `{"action": "share", "to": 7, "amount": 1.0}` · `{"action": "rest"}` · `{"action": "propose_rule"}`. Anything else is rejected and logged by the kernel.
