# civlab simulators | model cards, parameters, outputs, commands

## Contents
1. Common contract (all models)
2. society: networked cooperation, institutions, legitimacy
3. aisociety: autonomous AI agent society with constitution kernel
4. sdt: structural-demographic stress
5. polity: civilization formation and fragmentation
6. diffusion: Bass and threshold cascades
7. cascade: failure cascades
8. knowledge: tacit skill and archive survival
9. ews, cld, forecasting and sensitivity tools
10. Plugging in an LLM policy
11. Documented behaviours (verified by tests)

## 1. Common contract

- Stdlib Python 3.9+, run from the skill folder: `python scripts/civitas.py ...`. No network, no installs.
- Config: JSON file (`--config`), keys starting with `_` are comments; override with `--set key=value`. Unknown values outside documented ranges are rejected with a clear error (exit code 2).
- Every result is an envelope: `civitas_version`, `model`, `epistemic_status` (`fiction` for synthetic runs), `warning`, `config_sha256`, `assumptions`, `limitations`, results. Full JSON goes to `--output`; stdout is compacted.
- `--runs N --seed S` runs seeds S..S+N-1. `compare` uses identical seeds for both arms and reports paired deltas with a Monte Carlo interval (simulation noise only).
- Report: model, seeds, runs, overrides, config hash, and the envelope's limitations.

## 2. society

**Purpose**: explore how cooperation, inequality and institutional legitimacy co-evolve under different governance designs.
**Entities**: agents on a network (small_world, random, scale_free, lattice), each with strategy C (cooperate), D (defect) or P (cooperate and punish), wealth, group identity.
**Schedule per round**: shock check → neighbourhood public-goods games (contribution split across games) → peer punishment (if peer/polycentric) → central institution: tax, corruption skim to richest 5%, detection probability = net budget × efficiency / N × legitimacy, fines (if central/polycentric) → subsistence → wealth ledger check → exit and replacement of ruined agents → payoff-biased imitation with in-group discount and mutation → legitimacy update.
**Key parameters**: `governance` (none, peer, central, polycentric), `multiplier`, `punish_cost`, `punish_fine`, `tax_rate`, `monitoring_efficiency`, `central_fine`, `corruption`, `ingroup_bias`, `selection_strength`, `subsistence`, `shock_probability`, `shock_severity`.
**Metrics**: `final_cooperation`, `tail_mean_cooperation`, `final_gini`, `final_mean_wealth`, `total_exits`, `final_legitimacy`, `group_cooperation_gap`.
**Invariant**: wealth ledger balances every round (tested).

## 3. aisociety

**Purpose**: test governance designs for autonomous agents sharing a scarce regenerating resource (compute, energy, bandwidth).
**Entities**: agents with archetype (steward, maximizer, deceiver, reciprocator), wealth, reputation, bounded memory, trust ledger, faction; a logistic commons; a rule set (harvest cap, audit rate, sanction, holding cap); an append-only audit log.
**Schedule per tick**: random activation order → each agent's policy proposes an action (harvest, share, rest, propose_rule) → **constitution kernel** validates (unknown actions rejected; with `kernel_enforcement=true` withdrawals are metered and clipped to the cap; otherwise reports are trusted and random audits sanction overuse) → consumption of need → commons regrowth → every `vote_every` ticks a reputation-weighted vote between restraint and growth factions amends rules → optional `entrenched_sustainability` clause caps amendments at maximum sustainable yield per agent → human oversight freezes the world if the incident rate exceeds `oversight_threshold`.
**Metrics**: `ticks_completed`, `final_commons_ratio`, `min_commons_ratio`, `final_gini`, `incidents`, `detected`, `undetected`, `blocked_by_kernel`, `rule_changes`, `mean_hardship`; plus wealth by archetype, rule history, audit-log tail.
**Headline teaching result** [E3]: an enforcement kernel faithfully enforces whatever rules exist; if a growth faction captures the amendment process, enforcement protects the capture and the commons declines. An entrenched, non-amendable sustainability floor prevents this in the model. Lesson: enforce rules *and* protect the rule-making process.

## 4. sdt

**Purpose**: illustrate structural-demographic dynamics.
**State**: population relative to capacity, wages, elite share, relative elite income, state debt ratio, crisis status.
**Mechanisms**: wages fall as population nears capacity; when wages fall below the founding level a wealth pump moves commoners into the elite; elites shrink when their income per head falls; state spending scales with elite patronage and population; a PSI-like composite (immiseration × elite competition × fiscal distress) sets an annual crisis hazard; crises kill commoners, cull elites and repudiate debt for `crisis_duration` years.
**Policy levers**: `elite_tax` (damps the wealth pump), `wage_support`, `fiscal_discipline`, `pop_growth`, `capacity_growth`.
**Metrics**: `crisis_count`, `share_years_in_crisis`, `mean_years_between_crises`, `peak_psi`, `mean_psi`, `final_elite_share`, `min_wage`.
**Read with care**: cycle lengths are artefacts of the chosen rates.

## 5. polity

**Purpose**: generate plausible long histories of states on a map, for worldbuilding and for exploring cohesion, overstretch and alliances.
**State**: grid cells with owner and solidarity; polities with capitals.
**Mechanisms**: frontier solidarity growth, interior decay; power = size × mean solidarity × exp(-distance/reach); border cells change hands on a power margin; alliances balance against a neighbour more than `alliance_ratio` times larger; polities below `collapse_threshold` fragment into micro-polities and stateless cells.
**Metrics**: `final_polities`, `peak_largest_share`, `final_largest_share`, `mean_hhi`, `collapses`, `mean_lifespan`, `final_stateless_share`; trajectory for era narration.
**Worldbuilding use**: run, then narrate eras from the trajectory (peaks, fragmentations), labelling the history E5.

## 6. diffusion

- `--set mode=bass --set p=0.03 --set q=0.38 --set m=1 --set periods=30`; add `observed_cumulative` in a config to fit p, q, m (grid search, warns when m is unidentified).
- Cascade mode (default): `threshold_mean`, `threshold_sd`, `seed_share`, `seeding` (random, hubs, cluster), `resisters`, `graph`, `degree`. Metrics: final adoption distribution and share of runs with a global cascade (> 50%). Always report the distribution: cascades are bimodal.

## 7. cascade

Parameters: `nodes`, `graph`, `degree`, `tolerance` (capacity margin), `initial_failures`, `attack` (random or targeted at hubs), `interdependent` (couples to a second network). Metrics: `surviving_share`, `giant_component_share`, `failed_share`, `cascade_rounds`.

## 8. knowledge

Parameters: `learners`, `alpha` (copying loss), `beta` (copying dispersion), `generations`; archive `items`, `copies`, `p_loss`, `p_copy`, `periods`, `formats`, `p_format_shock`. Output includes the analytic critical learner population `N*` and expected skill change. Metrics: `tacit_skill_slope`, `archive_final_survival`, `readable_formats_left`.

## 9. Tools

- `ews --csv file.csv --column value` (or `--synthetic approach|null`): Kendall tau of rolling variance and lag-1 autocorrelation, AR(1) surrogate p-values, verdict `rising_indicators` or `no_robust_signal`. In a development check on 10 synthetic series approaching a transition (400 points, detrending bandwidth 10%, 99 surrogates), the joint signal fired in 5 of 10, with 0 of 10 false alarms on stationary controls: useful but low sensitivity. Absence of a signal never rules out a transition.
- `cld --config edges.json`: loops, polarity, delays, weakest evidence, leverage, Mermaid string.
- `baserate --k --n`, `bayes --prior --lr "label=LR"`, `pool --p ... --extremize`, `score --ledger file.jsonl`, `ach --config file.json`.
- `sensitivity <model> --metric M --range p=lo:hi [--method morris|oat]`; `robust <model> --metric M --policy name=k=v,k=v --uncertain p=lo:hi`.

## 10. Plugging in an LLM or custom policy (aisociety)

`aisociety.run(cfg, seed, policy=fn)` where `fn(view, rng) -> dict`. `view` contains only what the agent may observe (tick, own wealth, need, current rules, commons ratio, a few recent memories, observed overuse). Return `{"action": "harvest", "amount": x, "report": y}`, `{"action": "share", "to": id, "amount": x}`, `{"action": "rest"}` or `{"action": "propose_rule"}`. The kernel validates everything; malformed or unknown actions are rejected and logged. For an LLM adapter: render `view` as a prompt, parse JSON, fall back to `rest` on parse failure, record model name and sampling settings, cap calls per run, and compare against the rule-based baseline before drawing conclusions (AGENT_SOCIETIES.md).

## 11. Documented behaviours (each verified by an automated test; all E3, model-internal)

- society: peer punishment raises long-run cooperation versus no governance; high corruption collapses legitimacy of a central institution; wealth ledger always balances.
- aisociety: kernel enforcement yields zero overuse incidents; prompt-only rules allow incidents; oversight freezes runs above threshold; the entrenched clause preserves the commons under rule capture; rogue policies are blocked.
- sdt: an integrative phase precedes the first crisis; slower population growth reduces crisis count.
- polity: empires rise to large shares and fragment.
- diffusion: Bass closed form matches its analytic peak; fitting recovers known parameters; threshold cascades show a phase change.
- cascade: more tolerance means fewer failures; targeted attack on hubs is worse than random failure; interdependence never improves survival.
- knowledge: simulation matches the Henrich threshold's sign; more archive copies and more formats raise survival.
