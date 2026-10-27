# Complex systems and causal structure

CIVITAS uses tools from systems science as **methods**, not as magical forecasting laws.

## Models to choose from

| Need | Method | Output | Main weakness |
|---|---|---|---|
| See direction and delays | Causal loop diagram | Signed links, feedback, delays | Qualitative loops cannot estimate effects |
| Track accumulation | Stock and flow | Conserved stocks, inflows/outflows | Measurement and functional form errors |
| Analyze micro to macro | Agent based model | Behavior rules and observed distributions | Hard validation and parameter dependence |
| Model contagion or influence | Network model | Nodes, edges, clustering, centrality | Missing ties and endogenous network changes |
| Compare strategies | Game theory | Incentives, equilibria, repeated play | Assumed utilities and common knowledge |
| Study causal questions | Causal DAG, experimental designs | Competing pathways, identification requirements | Unobserved confounding |
| Examine uncertainty | Scenario matrix and sensitivity | Conditional pathways and robustness | May omit crucial dimensions |
| Study change after shocks | Resilience and adaptive cycle analysis | Recovery times, diversity, redundancy | Difficult transfer across systems |

## Stocks and flows

Every numeric stock needs units and update logic. For population `P`, a basic accounting identity is `P[t+1] = P[t] + births - deaths + in_migration - out_migration` with each flow measured in compatible time units. For a hypothetical trust index, an update can be proposed but is not a conserved physical quantity: clearly label its arbitrary scale and test its stability.

### Feedback loops

- **Reinforcing:** adoption → compatibility → value → adoption; can accelerate success or exclusion.
- **Balancing:** shortages → price response → conservation → shortages decrease; depends on access and delay.
- **Delayed balancing:** institutions notice a problem only after damage, increasing oscillation risk.
- **Counterproductive optimization:** measuring one metric redirects behavior, making the metric less informative.

A loop diagram is not a proof of causality. Ask which arrows have evidence, which confounders exist, how delays differ, and whether the loop could reverse in another regime.

## Critical dynamics

Explore thresholds, phase transitions, tipping points, path dependence, bottlenecks, resilience, diversification, network effects, cooperation dilemmas, power laws only when evidenced, and sensitivity to initial states. Avoid borrowing physics vocabulary to imply scientific validity in a social question.

## A practical causal workflow

1. Define treatment/intervention, outcome and comparison unit.
2. Draw possible causal paths including common causes, reverse causality, mediators, and selection.
3. Identify which variables are observable and when they occur.
4. Prefer experiments when ethical and feasible; otherwise articulate requirements for a credible quasi experimental design.
5. Compare causal and noncausal explanations. Avoid controlling for colliders or post treatment variables without justification.
6. Report estimand, identification assumptions, uncertainty and limitations. If no identification exists, stay descriptive or exploratory.

## Multi scale reasoning

Macro conditions shape incentives; micro decisions form meso organizations; organizational rules feed back to macro dynamics. Do not collapse economics, culture, information and law into one fictional score. Track interconnections while respecting distinct timescales.

## Model selection principle

Use the simplest model that can answer the decision question. Start with causal diagrams or stock accounting. Add network or ABM detail only if individual heterogeneity or interactions change the conclusion. Add LLM behavior only if language reasoning materially changes dynamics and baseline rules cannot capture it.

References: https://github.com/mesa/mesa/wiki/About-Agent-Based-Modeling ; https://doi.org/10.18564/jasss.4259 ; https://ftp.cs.ucla.edu/pub/stat_ser/ACMBook-published-2022.pdf

## Additional dynamics (1.0)

- **Chaos and horizons**: deterministic systems with sensitive dependence lose predictability exponentially; forecast skill has a horizon even with perfect models [E1]. Social systems add learning and rule change on top.
- **Statistical mechanics analogy**: aggregates are predictable when micro-states are many and weakly coupled; social contagion and hubs couple them strongly, breaking the analogy (ASIMOV_ATLAS card 1).
- **Information theory**: entropy measures uncertainty and diversity; mutual information measures how much one signal tells about another (useful for indicator selection in WARN).
- **Percolation and cascades**: connectivity thresholds make fragmentation abrupt; interdependent networks fail more suddenly (`cascade`).
- **Critical slowing down**: rising variance and autocorrelation before some tipping points (`ews`).
- **Adaptive cycle / panarchy** (Holling 2001): growth, conservation, release, reorganization across nested scales; a lens for recovery.
- **Heavy tails and dragon kings**: extremes may come from distinct amplifying mechanisms (Sornette 2009); test for them instead of assuming Gaussian noise.
- **Stochastic processes**: random walks, branching processes (cascade sizes), Poisson hazards (crisis onset in `sdt`). Report distributions, not means alone.
- **Evolutionary computation and cellular automata**: useful for exploring rule spaces (e.g. searching governance parameters) and spatial dynamics (`polity` is a CA-like model); search results are model-internal.

Tool: `python scripts/civitas.py cld --config edges.json` classifies loops, flags delays and weakest evidence, and suggests leverage points.
