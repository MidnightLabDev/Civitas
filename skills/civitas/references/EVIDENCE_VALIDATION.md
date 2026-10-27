# Evidence integrity, measurement, validation and ethics

## Evidence quality ladder, not a fixed ranking for all questions

1. Direct independent observations relevant to the question, with known sampling and provenance.
2. Credible experiments or quasi experiments when estimating causal effects.
3. Replicated domain studies and systematic reviews with clear scope.
4. Expert judgment with disagreement recorded.
5. Contextual analogies and historical cases.
6. Synthetic experiments with independently checked assumptions.
7. Narrative possibilities and speculative premises.

Do not equate a large sample, prestigious institution or mathematical expression with guaranteed validity. Match method to claim.

## Model claims checklist

Define outcome, target population, resolution period, denominator, missing data, source permissions, confounding, reproducibility, distributional harm, parameter provenance, competing explanations, and known failure domain. A strong sounding statement with no testable claim must be framed as inference or speculation.

## Validation matrix

| Claim | Minimum support | Red flag |
|---|---|---|
| Agent interaction is believable | Human evaluation, documented scenarios | A few compelling transcripts |
| Numeric model is implemented correctly | Invariants, unit tests, replay | Only a screenshot or prose claim |
| Model reproduces past events | Historical holdout with stated metrics | Fitted and tested on same period |
| An intervention causes an outcome | Design identifying causal effect | Correlation and a causal arrow |
| Future event probability is reliable | Pre recorded forecasts, scoring, calibration | Probabilities derived from narrative confidence |
| A deployment is safe | Domain assessment, controls, monitoring and independent review | Prompt based constitution alone |

## Simulation disclosure block

**Purpose:** exploration / education / research / forecast.
**Status:** unrun thought experiment / implemented and executed / externally validated.
**Inputs:** empirical / synthetic / mixed and provenance.
**Engine:** deterministic / seeded stochastic / LLM / hybrid.
**Uncertainty:** structural, parameter, observation and model variation.
**Cannot conclude:** real world outcomes not established by the model.

## Ethical and social safeguards

Protect privacy, consent, free expression, rights, legal accountability and the ability to contest decisions. Use synthetic data by default. Do not produce covert targeted manipulation, discriminatory scoring, mass surveillance, or strategies to destabilize real groups. Model sensitive populations only with justified objectives, appropriate consultation and safeguards.

## Evaluating competing models

Use alternate mechanisms, adversarial reviews, parameter sweeps and holdout evidence. Prefer models that remain informative despite plausible assumption changes. Failure to capture a rare crisis is an important result, not something to hide by altering the story after the fact.

## Research limitations

Current reviews of LLM agent simulations identify substantial problems with calibration, validation, interpretability and bias. Clearly separate fictional realism from predictive validity. Source: https://doi.org/10.1007/s10462-025-11412-6

Official ethical sources: https://www.nist.gov/itl/ai-risk-management-framework and https://www.unesco.org/ethics-ai/en/recommendation

## Mapping evidence to tiers (1.0)

| Evidence available | Highest tier |
|---|---|
| Replicated findings, textbook regularities, verified facts | E1 |
| Cited studies, base rates, measured series with uncertainty | E2 |
| Output of an explicit model with stated assumptions | E3 |
| Coherent mechanisms, no quantification | E4 |
| Invented worlds, synthetic agents, canon fiction | E5 |
| Nothing beyond intuition | E6 (flag or omit) |

A simulation using real calibrated inputs and validated against holdout data can support E2 claims about the target; otherwise its outputs stay E3 (model-internal) or E5 (synthetic). LLM agent realism does not raise the tier (Larooij & Törnberg 2025).
