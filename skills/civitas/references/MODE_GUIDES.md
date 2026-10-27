# Mode guides | twelve workflows

## Contents
RESEARCH · HISTORY · MODEL · FORECAST · WARN · SIMULATE · GOVERN · STRESS · INVENT · DESIGN · WORLDBUILD · AUDIT · Cross-mode moves · Audience adaptation

Changes from the original twelve: ECONOMY became a domain lens inside MODEL and SIMULATE; EXPERIMENT merged into SIMULATE (they shared every step); HISTORY and WARN are new because comparative history and early warning need workflows of their own.

## RESEARCH
1. Pin down the question (concept, comparison, literature).
2. Separate Asimov canon (E5), interpretation, real research (E1 to E2) and CIVITAS's own synthesis.
3. Use ASIMOV_ATLAS cards; for methods use LANDSCAPE and SOURCES.
4. Give sources you actually have; mark anything unverified. Never manufacture a passage.

## HISTORY
1. Define the outcome (territory, population, complexity, living standards, institutions).
2. Timeline of attested facts (E1), then interpretations (E2) with their proponents.
3. Apply at least two theories from CLIODYNAMICS_HISTORY; say where each fits and fails.
4. Compare with cases from other regions and eras.
5. Optional model (`sdt`, `polity`, `knowledge`), labelled E3.
6. Close with the evidence that would discriminate between explanations.

## MODEL
1. ARICII inventory (ENGINE.md).
2. Causal chains, at least one reinforcing and one balancing loop, delays, thresholds (`cld`).
3. Domain lenses as relevant: economy (stocks, flows, prices, distribution), ecology (regeneration, degradation), technology (diffusion, lock-in), information (networks, trust), demography (age, migration).
4. One competing mechanism and a test to tell them apart.
5. Choose a model card (QUANT_MODELS) only if it adds insight.

## FORECAST
1. Resolvable question (event, threshold, date, resolution source).
2. Reference class and base rate (`baserate`), then specific adjustments (`bayes`, stating each likelihood ratio).
3. Drivers and key uncertainties; three to four branches with signposts.
4. Numeric probability only with a basis; otherwise ordinal. Record in a ledger if it will be scored.
5. Decision implications: which actions are robust across branches.

## WARN
1. Define the transition to watch and why it matters.
2. Indicators: leading vs lagging, data source, frequency, threshold, owner.
3. For time series, run `ews`; report method sensitivity and the false-negative risk.
4. Combine structural indicators (CLIODYNAMICS dashboard) with dynamic ones (variance, autocorrelation, cascades).
5. Specify the response each threshold triggers and who decides.

## SIMULATE
1. Purpose and question first; decide whether simulation is needed at all.
2. Pick a civlab model (SIMULATORS.md) or design a new one with ODD documentation.
3. Write the config; run baseline with ≥ 10 seeds; then `compare` for interventions (matched seeds).
4. `sensitivity` on the parameters that carry the conclusion; check invariants.
5. Report only executed results with seeds, runs, config hash; label E3 or E5; list limitations from the envelope.
6. For new code: tests for invariants, determinism and validation; run them.

## GOVERN
1. Who is governed, by whom, affecting whom (including non-consenting third parties).
2. Rights floor and prohibited acts; permission matrix; separation of duties.
3. Independent enforcement (outside any prompt), audit log, appeal, revocation, emergency stop, amendment rules with entrenched protections.
4. Abuse cases: collusion, delegation creep, rule capture, specification gaming, automation bias.
5. Test the design in `aisociety` (enforcement on/off, capture mix, entrenched clause, oversight threshold) and report E3 findings.

## STRESS
1. Map the system (MODEL steps 1 to 2).
2. Friendly failure: everyone follows the rules and harm still happens.
3. Hostile failure: adversary, capture, deception, collusion.
4. Rare shock and correlated failures (`cascade`); reverse stress test.
5. Containment and recovery; rank fixes by regret; give a disconfirming test.

## INVENT
1. Pick a structural gap (INNOVATION_PATTERNS lenses).
2. Mechanism, users, incentives, existing alternatives (search if tools allow).
3. Second-order effect and misuse case.
4. Smallest falsifiable pilot with value metric, guardrail metric and stop rule.

## DESIGN
1. Architecture: kernel, state store, event log, policy gateway, evaluation (TECH_ARCHITECTURE).
2. Schemas (SCHEMAS.md), permissions, failure modes, replay.
3. Verify any external API against current docs before writing integration code.

## WORLDBUILD
1. Founding constraints (geography, resources, technology, contact).
2. Factions with real disagreements; institutions with interests; daily life.
3. Optional: run `polity` or `sdt` to generate an era structure, then narrate it; keep a persistence record (WORLD_HISTORY).
4. Check internal consistency (resources, demography, technology diffusion speed).
5. Original names and events only; Asimov is inspiration, not source material.

## AUDIT
1. Classify each claim by tier; list unsupported ones.
2. Inspect model design, inputs, permissions; run code and tests if available.
3. Sensitivity and alternative model; check for artefacts.
4. Societal harms and rights.
5. Verdict: pass, revise, reject, with top three fixes and one benchmark.

## Cross-mode moves
- **Double inversion**: pursue the goal and list costs; avoid it and list benefits.
- **Institutional inheritance**: what remains after founders leave?
- **Forecast feedback**: publish the forecast inside the model and let actors react.
- **Outside the boundary**: who is harmed but absent?
- **Countermodel**: the simplest model that yields the same result.

## Audience adaptation
| Audience | Style |
|---|---|
| Newcomer or student | Plain words, one analogy, one diagram in words, tiers explained once |
| Executive | Decision first, three branches, signposts, robust moves; tiers as tags |
| Researcher | Estimands, model cards, equations, sensitivity, sources with dates |
| Writer or game designer | Creative material first; mechanics and consistency notes after |
| Engineer | Interfaces, schemas, tests, failure modes, commands |
