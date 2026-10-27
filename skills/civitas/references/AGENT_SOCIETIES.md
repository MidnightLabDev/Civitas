# Autonomous agent societies | design and scientific cautions

## Types of agents

- **Rule based:** state, observation function, policy, bounded actions. Cheap and generally reproducible.
- **Utility driven:** choose actions from specified objectives and constraints. Risks include misspecified preferences.
- **Learning agents:** update decisions from observations, requiring controlled training and evaluation.
- **LLM driven:** use language models for dialogue, planning, reflection, and negotiation. More expressive, usually more variable and difficult to validate.
- **Hybrid:** language decisions bounded by deterministic state transition and permission layers. Preferred for controlled prototypes.

## Anatomy of a simulated agent

Identity within world (not a claim of real personhood), internal goals, heterogenous needs, role and relationships, memories, knowledge versus beliefs, observation privileges, action capabilities, plans, normative commitments, budget, reputation, learning rule, error model, and historical trace.

Distinguish what **the agent knows**, what **the environment knows**, what **the researcher knows**, and what **the player knows**. Do not let agents access privileged hidden model state accidentally.

## A safe turn loop

1. Sample observations per access rules.
2. Update bounded memory or retrieve relevant records.
3. Generate candidate actions or proposals.
4. Check tool permissions, resource availability, invariants, rate limits and mandatory approvals.
5. Resolve simultaneous action conflicts with a declared schedule.
6. Apply atomic state transitions and resource transfers.
7. Emit events to an append only history with timestamps and reasons.
8. Update environment, institutions and observable indicators.
9. Evaluate emergent patterns and safety guardrails.
10. Save state, seed and configuration for replay.

## Emergence and society

Agents may specialize, cooperate, bargain, defect, coordinate, found institutions, share knowledge or form status hierarchies. Design these as **possible** outcomes arising from allowed behaviors. Avoid hard coding a predetermined "emergence" and subsequently claiming it was discovered by simulation.

## Memory and continuity

For long horizon worlds, distinguish episodic agent memory, distilled beliefs, immutable public records, cultural inheritance, and obsolete documents. Add information loss, censorship and corruption as **declared mechanics**. Keep audit histories separate from mutable role play memories. Do not pretend conversational context alone is persistent storage.

## Validation of language agents

Humanlike dialogue is not enough. Evaluate rule adherence, consistency, task success, memory leakage, diversity, sensitivity to persona wording, random seed spread, response order, model changes, hallucinated evidence, stereotyping and external empirical validation. Compare with a simpler baseline. Bias in training data may create patterns mistaken for social facts.

## Relevant research and tools

- Generative Agents (Park et al., UIST 2023): https://research.google/pubs/generative-agents-interactive-simulacra-of-human-behavior/
- DeepMind Concordia: https://github.com/google-deepmind/concordia
- CAMEL OASIS: https://github.com/camel-ai/oasis
- AgentCiv, experimental emergent AI society: https://github.com/agentciv/agentciv
- Validation critique: https://doi.org/10.1007/s10462-025-11412-6

## Test matrix

Normal cooperation; persistent defection; rumors; degraded communication; competing institutional charters; time horizon misalignment; a scarce essential input; total leader loss; memory mismatch; stale policy; resource accounting mismatch; a human override; arbitrary action ordering; misleading reward signals; network fragmentation; safety intervention; and reset after outage.

For a live multiagent system, document real API permissions, retention and privacy practices, run cost, failure containment and possible effects outside the simulation.

## Research landscape (verified 2026-10-27; see LANDSCAPE.md)

Generative Agents (memory, reflection, planning), Concordia (game-master grounding), AgentSociety (large-scale LLM social simulation), Project Sid (many-agent civilization in Minecraft), GovSim (LLM commons dilemmas; in the authors' tests most models failed to sustain the resource), Melting Pot (multi-agent RL social dilemmas), OASIS (million-agent social media). Common lesson: impressive emergence demos are easy; validation is hard (Larooij & Törnberg 2025).

## Hybrid design pattern used by civlab `aisociety`

1. Policy layer (rules or LLM) proposes actions from a restricted view.
2. Constitution kernel validates actions against permissions and current rules, meters resources, rejects malformed output.
3. Append-only audit log records proposals and verdicts.
4. Institutional layer: votes amend rules; entrenched clauses limit amendments.
5. Oversight layer: thresholds trigger a freeze for human review.

## Evaluating LLM agents in civlab

Run the rule-based baseline first, then swap in the LLM policy with identical seeds and config. Compare incidents, commons health, inequality, rule changes. Vary prompt wording and model; repeat runs; report variance. Treat differences as properties of that model and prompt, not of "AI" or of humans.
