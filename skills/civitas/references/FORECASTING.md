# Foresight, probabilities, calibration and adaptive decisions

## Choose the right output

- **Possibilities:** exploratory narratives with no probabilities.
- **Scenarios:** coherent conditional futures shaped by uncertain drivers.
- **Quantitative forecasts:** well specified measurable outcomes, time window and methods.
- **Decision analysis:** compare actions under uncertainty using costs, rights, options and robustness.

OECD strategic foresight recognizes horizon scanning, megatrends, scenario building, visioning and backcasting as distinct methods: https://www.oecd.org/en/about/programmes/strategic-foresight.html

## Forecast protocol

1. Turn a vague question into a resolvable question with event, location, population, threshold, dates and source of eventual resolution.
2. Gather historical base rates and comparison cases, checking the reference class. Avoid selection from winners alone.
3. Identify drivers, key structural uncertainties, feedback and where a forecast may itself change behavior.
4. Establish a baseline (including status quo and inertia) and alternative models.
5. Produce conditional forecast or scenarios. If a numeric probability is demanded, give one only when the basis can be explained and label it subjective if it is not empirically fitted.
6. Record timestamp, inputs, assumptions, and resolution criteria before the outcome is known.
7. Update probabilities when information changes; keep prior forecasts in an immutable log.
8. On resolution, calculate an appropriate scoring rule and calibration by bins if there are enough cases. A small sample cannot establish accuracy.

## Brier scoring

For a binary event, with stated probability `p` and outcome `y` in `{0,1}`, the Brier score is `(p-y)^2`; smaller is better. Calculate only for **resolved real questions**, never for a fictional branch with no ground truth. Compare against a relevant baseline, not a perfect hindsight benchmark.

## Scenario method

Select two to four major uncertainties, rather than constructing every possible combination. For each branch provide: assumptions, causal sequence, who acts, who is exposed, early indicators, hard constraints, signposts that trigger a policy change, and robust or reversible actions. Include a surprise where the model's categories themselves fail. Refuse single destiny narratives.

## Stressing scenarios

Test exogenous shocks, delayed institutional reaction, critical infrastructure failure, adversarial or collusive actors, new information, conflicting values, feedback reversals, and regime changes. Conduct both a pre mortem and a reverse stress test (what assumptions must fail to reach a bad outcome?).

## Backcasting

Define a desirable and rights respecting outcome; identify enabling conditions, institutions and investments working backward to today. Compare with a no action branch and avoid assuming that a desired endpoint is achievable or universally desirable.

## Decision robustness

Prefer moves that remain valuable across credible scenarios. Distinguish irreversible investments, options to wait, staged rollout, reversible experiments and safeguards that cap downside. Ask whether an action shifts the costs to a population outside the analysis.

## Prediction humility

When data are poor, it is more useful to identify the signals that would change a decision than to give a precise number. A simulation based on synthetic assumptions is not an empirically calibrated forecast. For real financial, medical, policy or safety decisions, use current professional evidence and relevant expert review.

Sources: https://www.oecd.org/en/about/programmes/strategic-foresight.html ; https://www.ftp.rrze.uni-erlangen.de/cran/web/packages/scoringutils/vignettes/scoring-rules.html

## Tooling added in 1.0 (civlab)

| Step | Command | Note |
|---|---|---|
| Base rate | `python scripts/civitas.py baserate --k 3 --n 20` | Beta posterior, Jeffreys prior; reference-class choice dominates |
| Update | `bayes --prior 0.15 --lr "signal A=2.5" --lr "signal B=0.7"` | Odds form; state each likelihood ratio and assume independence only if justified |
| Aggregate | `pool --p 0.3 --p 0.45 --p 0.4 --extremize 1.5` | Logit pooling; extremize only when forecasters hold partly independent information |
| Score | `score --ledger forecasts.jsonl` | Brier, log, Murphy decomposition, calibration table; < 50 resolved items cannot show calibration |
| Rival hypotheses | `ach --config file.json` | Ranks by inconsistency; flags non-diagnostic evidence |
| Robust choice | `robust <model> ...` | Minimax regret across sampled futures (Lempert et al. 2003) |
| Early warning | `ews --csv series.csv` | Critical slowing down; false negatives common |

## Practices with evidence behind them (E2)

- Training in probabilistic reasoning, teaming and tracking improved accuracy in a large geopolitical tournament (Mellers et al. 2014).
- Reference-class forecasting corrects inside-view optimism in projects (Flyvbjerg 2006).
- Logit pooling with extremizing improved aggregate accuracy in tournament data (Satopää et al. 2014).
- Adaptive policy pathways plan triggers and switches in advance for deep uncertainty (Haasnoot et al. 2013).
