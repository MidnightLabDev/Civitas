# The CIVITAS Loop | unified psychohistory reasoning engine

## Contents
1. Design rationale
2. Stage-by-stage procedure (FRAME, MAP, MECHANIZE, GROUND, BRANCH, STRESS, ACT, UPDATE)
3. Depth dial
4. Tool hooks per stage
5. Worked example (compressed)
6. Failure modes of the engine itself

## 1. Design rationale

Asimov's psychohistory promised prediction from aggregate regularities. Real methods that deserve trust do something different: they **condition** (if these mechanisms hold, then...), **compare** (against base rates and rival explanations), **expose** (assumptions, sensitivity, who bears costs) and **learn** (score forecasts, update). The Loop is CIVITAS's original synthesis of systems dynamics, cliodynamics, structured analytic techniques, decision analysis under deep uncertainty, and forecasting practice. Every stage exists because a known failure happens without it (section 6).

## 2. Stages

### FRAME
- Rewrite the question so that it could be answered or resolved: unit, place, horizon, threshold, and source of resolution. "Will the EU fragment?" becomes, e.g., "Will any member state formally notify withdrawal under Article 50 before 2035-01-01?"
- State the **decision** the answer serves (or "understanding only"), the **audience** level, and the **tier ceiling**: fiction never exceeds E5; a real-world forecast with no data cannot exceed E4.
- Pick depth and mode.

### MAP: ARICII inventory
| Element | Ask |
|---|---|
| **A**ctors | Who acts? Heterogeneity in power, wealth, information, time horizon, identity. Who is excluded but affected? |
| **R**esources | Stocks and flows with units: food, energy, money, compute, attention, legitimacy, knowledge. What is conserved? |
| **I**nstitutions | Formal rules, informal norms, enforcement, succession, who can change the rules |
| **C**onstraints | Geography, physics, technology, law, demography, ecology, budgets |
| **I**ncentives | What each actor gains or loses from each available action, including status and survival |
| **I**nformation | Who knows what, when; networks, media, secrecy, measurement and its distortions |

### MECHANIZE
1. Write chains: `driver → incentive → behaviour → interaction → feedback → emergent outcome → observable signal`.
2. Mark loops: reinforcing (R) and balancing (B), with delays (oscillation/overshoot risk) and thresholds (tipping, hysteresis). Encode them for `python scripts/civitas.py cld` when the map is non-trivial.
3. Name at least **one competing mechanism** that produces the same observation, and the evidence that would distinguish them.
4. Choose the simplest model class that can answer the question (see `SYSTEMS_SCIENCE.md` model selection and `QUANT_MODELS.md`).

### GROUND
- Reference class first (outside view), then adjust for specifics (inside view). Record k-of-n where possible and use `baserate`.
- Historical analogues from **at least two regions or eras** when discussing civilizations; state where each analogy breaks.
- Evidence ledger: claim, tier, source, competing explanation, what would falsify it.
- For time-sensitive real-world facts, verify with current sources if tools exist.

### BRANCH
- Baseline (inertia), breakdown, and structural surprise, plus one wildcard outside the model's categories.
- For each: assumptions, causal sequence, winners and losers, signposts (observable early signs), and the actions that remain good in it.
- **Reflexivity check**: if actors learned this analysis, how would they respond, and does that defeat or fulfil it (Merton's self-fulfilling and self-defeating prophecies; Lucas critique for policy models)?
- Probabilities only with a stated basis; otherwise use ordinal language ("more plausible than") and say why.

### STRESS
- Shocks: rare large events, correlated failures, adversaries, rule capture, technology surprise, demographic or climate stress.
- Sensitivity: which assumption, if wrong, flips the conclusion? Use `sensitivity` for models.
- Pre-mortem ("it failed; why?") and reverse stress test ("what must be true for the worst case?").
- Run the CRITICAL_REVIEW gate.

### ACT
- Options compared on: expected benefit, worst case, **regret across branches**, reversibility, time to effect, distribution of costs, legitimacy, and who has authority to act.
- Prefer staged, reversible, information-generating moves. Use `robust` to compare policies across sampled futures in a model.
- Each recommendation gets: a measurable experiment or pilot, success and harm metrics, and a stop rule.
- Ask what happens **if the recommendation succeeds** (second- and third-order effects).

### UPDATE
- Early-warning indicators with thresholds and data sources (`ews` for time series).
- "What would change my mind": the single most informative piece of missing evidence and the direction it would move the conclusion.
- Log real forecasts in a ledger (`forecast.Ledger`) with resolution criteria so they can be scored later.

## 3. Depth dial

| Depth | Stages shown | Typical length | Tools |
|---|---|---|---|
| Quick | none explicitly; answer reflects FRAME, MECHANIZE, one BRANCH caution | 1 to 4 paragraphs | none |
| Standard | thesis, mechanisms/loops, branches + signposts, actions, uncertainties | 1 to 3 pages | optional `cld`, `baserate` |
| Deep | all eight, evidence ledger, model card, sensitivity, review findings | report | civlab runs, sources |

## 4. Tool hooks

| Stage | civlab hook |
|---|---|
| MECHANIZE | `cld` (loop polarity, leverage); pick model from SIMULATORS.md |
| GROUND | `baserate`, `bayes`, `ach` |
| BRANCH | `run <model>` with alternative configs; `compare` |
| STRESS | `sensitivity` (Morris), `cascade`, shock parameters |
| ACT | `robust` (minimax regret), `compare` for interventions |
| UPDATE | `ews`, `score` (ledger) |

## 5. Worked example (compressed)

**Question:** "A coastal city-state depends on one desalination consortium for 90% of its water. Is it fragile, and what should it do?" (hypothetical, tier ceiling E4)

- FRAME: decision = infrastructure policy over 15 years; resolvable proxy: days of water reserve, number of single points of failure.
- MAP: residents, consortium, energy supplier, regulator, neighbouring states; resources = water, energy, reserve storage; institution = concession contract.
- MECHANIZE: R-loop: reliability → political trust → no investment in alternatives → deeper dependence. B-loop: price rises → conservation. Competing mechanism: fragility driven by energy dependence, not water operator concentration.
- GROUND: reference class of single-supplier critical infrastructure failures [E2 where sourced]; analogues in different regions.
- BRANCH: continuity; cascade (grid outage → desal stop → reserve exhausted in N days); surprise (cheap modular desal makes the consortium's leverage vanish).
- STRESS: `cascade` with interdependent=true shows how coupling to the grid widens failure [E3]; reverse stress test: reserve < outage length.
- ACT: reserve storage target, second supplier option, islanded power for key plants; regret lowest for reserve storage; pilot + metric.
- UPDATE: indicators: reserve days, outage frequency, concession renegotiation terms.

## 6. Failure modes the Loop guards against

| Without | Typical failure |
|---|---|
| FRAME | Unfalsifiable answers, "it depends" without saying on what |
| MAP | Missing actors (the excluded bear the costs); fake precision about resources |
| MECHANIZE | Storytelling without mechanism; single-cause explanations |
| GROUND | Inside-view optimism; Eurocentric or survivorship-biased analogies |
| BRANCH | Single destiny narrative; forecasts that ignore their own effect |
| STRESS | Fragile recommendations; model artefacts taken as findings |
| ACT | Advice no one has authority to implement; harm displaced outside the boundary |
| UPDATE | No learning; forecasts that can never be wrong |
