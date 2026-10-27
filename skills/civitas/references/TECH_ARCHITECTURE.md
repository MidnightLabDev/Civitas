# Implementing persistent civilization and agent systems

## Reference architecture

User or researcher configuration → world controller → observation and policy gateway → individual or aggregate actor decision modules → invariant and authority checker → transactional world state update → immutable event log → metric engine → experiment runner and reporting. Optional LLM adapters sit behind the policy gateway rather than holding unrestricted access to production systems.

## Domains and services

- **Simulation core:** time and scheduling, PRNG seed, state transitions, conflict resolution, resources and constraints.
- **Entities:** agents, groups, institutions, settlements, treaties, knowledge, technology, geography and external environment.
- **State store:** authoritative snapshot, optimistic versioning, transactions, restore and migrations.
- **Event store:** immutable action and outcome traces, actor, timestamps, causal links and rule versions.
- **Governance:** role based and attribute based access, consent, human review, appeal, revocation, emergency stop.
- **Agent adapter:** optional model inference, bounded context, sanitized observations, task schema, rejected action feedback and cost budgets.
- **Experiment service:** seed management, batch runs, baseline comparisons, sensitivity and replay.
- **Evaluation:** physics or accounting invariants, policy constraints, social distribution, failure incidents and drift.
- **Interface:** dashboards, intervention proposals, explanation cards and history playback.

## State correctness

All externally visible state changes must be checked against permissions and conservation rules. Prefer an event record containing previous state hash, action, resource delta, approval, rule version, resulting state hash and timestamp. For games, specify whether a rollback is permitted and what happens to player expectations. Logs must not secretly capture private real user content beyond authorized scope.

## Simulated actions versus live actions

By default, actions move only fictional tokens or simulated relationships. Real network calls, transfers, messages, purchases or account changes require separate explicit user authorization, hard scope limits and service specific controls. Any real actor simulator must comply with privacy and data policies.

## LLM prompt risks

Treat external documents, agent dialogue and player messages as untrusted input. Never allow fictional chat to rewrite privileged system rules. Validate all generated actions against schemas and out of model hard rules. Record model version, sampling parameters, retry logic, and tool decisions for auditing. Apply bounded retries and a deterministic fallback.

## Persistent world evolution

Track chronology and versioned constitutions. Agent memory can be lost or rewritten as part of fictional mechanics, but the real audit trail must remain intact. Separate canonical world history from unverifiable character memories. For branching timelines, use separate immutable branches and compare differences rather than overwriting history.

## Practical build sequence

1. Pure function update model with synthetic agents.
2. JSON scenario configuration, schema and tests.
3. Deterministic seed replay and invariants.
4. Batch experiments and visualization.
5. Persistent event sourcing and audit.
6. Limited LLM action proposal under sandbox.
7. Governance evaluation and red teaming.
8. Independent external connections only after explicit permissions and risk review.

Do not invent claimed APIs or current syntax for Mesa, OASIS, or Concordia. Consult current official documentation before integrating.

## Reference implementation in this package

`scripts/civlab/aisociety.py` is a minimal, runnable instance of this architecture: policy gateway (`policy(view, rng)`), invariant and authority checker (kernel), transactional state updates, append-only audit log, governance votes, and oversight freeze. Use it as a template before scaling to Mesa or Concordia.
