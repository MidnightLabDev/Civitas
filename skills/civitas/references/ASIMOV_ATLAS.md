# Asimov Atlas | concepts, real analogues, evidence, limits and CIVITAS methods

## Contents
1. Boundaries and source hierarchy
2. Concept cards (19): Foundation cluster, Robot cluster, Empire/Spacer cluster, other works
3. Cross-cutting contradictions inside psychohistory
4. Quick map: concept to civlab tool

## 1. Boundaries

- Original summaries only. No passages are reproduced; plot detail is limited to premises needed for analysis. Story facts are E5 (fiction); publication facts are E1 and should be checked against the SF Encyclopedia or editions when exact dates matter.
- Books are canon here; the Apple TV+ *Foundation* series (2021-) changes characters and events. Say which you mean.
- Academic "psychohistory" (psychoanalytic study of historical motivation, e.g. Lloyd deMause) is unrelated to Asimov's predictive mathematics.

Each card answers five questions: **Proposed** (what Asimov imagined), **Analogue** (real science that resembles it), **Evidence** (what supports or challenges the analogue), **Limits** (what cannot be validated), **Method** (how CIVITAS turns it into a usable tool).

## 2. Concept cards

### Foundation cluster

**1. Psychohistory** (*Foundation* stories from 1942; collected 1951; origin story in *Prelude to Foundation*, 1988)
- Proposed: a mathematics predicting the behaviour of very large populations, valid only if the population is huge and largely unaware of the predictions. Asimov modelled it on the kinetic theory of gases: individual molecules are unpredictable, gas laws are not.
- Analogue: statistical mechanics; Quetelet's "social physics"; demography and actuarial science; cliodynamics (Turchin); statistical conflict forecasting (Goldstone et al. 2010); collective-behaviour models (Granovetter 1978).
- Evidence: some aggregates are highly regular (mortality tables, demographic transitions, diffusion S-curves) [E1]. Structural instability models reached useful out-of-sample accuracy for onset of instability in specific tests [E2, Goldstone et al. 2010]. Challenges: humans are not molecules; they learn, anticipate, and change rules (reflexivity, Lucas critique); social systems have heavy tails and regime changes; chaotic dynamics limit horizon (sensitive dependence) [E1].
- Limits: millennium-scale point prediction of political events is not testable and almost certainly impossible.
- Method: **conditional, probabilistic, short-to-medium horizon** models with explicit mechanisms, base rates, and scoring (ENGINE.md, FORECASTING.md). Aggregation helps only where individual noise is independent.

**2. The Seldon Plan and Seldon Crises**
- Proposed: a designed path shortening a dark age from 30,000 to 1,000 years; recurring crises where only one course is viable, so actors "choose" what the Plan foresaw.
- Analogue: backcasting and adaptive policy pathways (Haasnoot et al. 2013): pre-planned decision points with triggers; "forced moves" resemble strategic dominance in game theory.
- Evidence: adaptive pathways are used in long-lived infrastructure planning [E2]. Challenges: real crises rarely leave one option; plans fail through surprise and capture.
- Limits: a plan that only works if the planned-for population never learns of it is incompatible with accountable governance.
- Method: **signposts and trigger points** per branch; robust, staged decisions; the "crisis test": at a decision point, which options remain viable under each branch? (`robust`).

**3. The Prime Radiant**
- Proposed: a device displaying the Plan's equations, annotated and corrected over centuries by the Second Foundation.
- Analogue: version-controlled model repositories; living documentation; forecast ledgers that log predictions and deviations; data assimilation in weather forecasting.
- Evidence: model updating with incoming data improves forecasts in physical systems (numerical weather prediction) [E1]; social equivalents are weaker.
- Limits: no social model can be continuously "corrected" toward truth without ground-truth observations.
- Method: **append-only forecast ledger + model cards + deviation log** (`forecast.Ledger`, SCHEMAS.md). Every revision states what new evidence caused it.

**4. Encyclopedia Galactica and Terminus**
- Proposed: a knowledge-preservation project that is really a seed for a new civilization; the encyclopedists' scholarly passivity is itself a weakness.
- Analogue: digital preservation (redundant copies, format migration), seed banks, institutional memory; the difference between stored knowledge and usable capability (tacit skill).
- Evidence: complex skills can be lost when practitioner populations shrink or disconnect (Henrich 2004; contested in specific cases) [E2]; redundancy and format diversity reduce archive loss [E1 engineering principle].
- Limits: we cannot test millennium-scale archive survival.
- Method: **knowledge preservation design**: archive copies × format diversity × practitioner population × re-copying institutions (`run knowledge`).

**5. The Second Foundation**
- Proposed: a hidden group of mental scientists who protect the Plan by covert correction.
- Analogue: technocratic stewardship, central banks' independence, nudge units, intelligence agencies; mechanism design by an unaccountable designer.
- Evidence: delegated expert institutions can improve credibility (e.g. independent central banks) [E2], but secrecy erodes legitimacy and invites capture [E2].
- Limits: covert benevolent control has no external check and cannot be evaluated by those it governs.
- Method: **accountability audit of any steering institution**: who appoints, who audits, who can appeal, sunset clauses (AI_GOVERNANCE.md). CIVITAS rejects covert steering of real populations.

**6. The Mule**
- Proposed: a single mutant whose ability to alter emotions breaks the statistical assumptions of the Plan.
- Analogue: outliers and heavy tails; "dragon kings" (Sornette 2009): extreme events generated by distinct mechanisms; the structure-versus-agency debate in history; preference falsification (Kuran 1991) enabling sudden revolutions.
- Evidence: heavy-tailed distributions are common in conflict sizes and wealth [E1/E2]; surprise revolutions have structural precursors that observers missed [E2].
- Limits: you cannot assign a probability to an unprecedented type of actor.
- Method: **outlier stress test**: inject an actor with outsized influence (scale-free networks, hub seeding in `diffusion`, targeted attack in `cascade`); always keep a wildcard branch.

### Robot cluster

**7. The Three Laws of Robotics** (first stated explicitly in "Runaround", 1942; *I, Robot*, 1950)
- Proposed: hard-wired priorities: do not harm humans or allow harm through inaction; obey humans unless that conflicts; protect yourself unless that conflicts. The stories are mostly about how these rules fail through ambiguity, conflicting weights and literal interpretation.
- Analogue: AI specification and alignment; reward misspecification and specification gaming; constitutional training of language models (Bai et al. 2022) uses natural-language principles but trains them in statistically, not as guarantees.
- Evidence: specification gaming is widely documented in RL systems [E2]; natural-language rules are interpreted, not executed [E1].
- Limits: "harm" and "human" cannot be fully specified ahead of time.
- Method: **rule conflict red-teaming**: generate cases where every rule is obeyed and the outcome is still harmful; pair rules with permission systems and independent enforcement (`run aisociety` shows enforcement vs prompt-only rules).

**8. The Zeroth Law** (*Robots and Empire*, 1985)
- Proposed: robots may harm individuals to protect "humanity" as a whole.
- Analogue: utilitarian aggregation vs rights constraints; paternalism; who defines collective welfare.
- Evidence: philosophical, not empirical; history shows abuses justified by collective good [E2 historical].
- Limits: "humanity's interest" is contested and unmeasurable.
- Method: **rights floor**: aggregate-benefit arguments cannot override individual protections without due process, consent, appeal (AI_GOVERNANCE.md); the `aisociety` entrenched clause models non-amendable floors.

**9. Positronic brains and robopsychology** (Susan Calvin)
- Proposed: robot minds built from potentials that encode the Laws; a profession (robopsychology) diagnoses aberrant robots.
- Analogue: neural networks; mechanistic interpretability; behavioural evaluations and red-teaming.
- Evidence: interpretability is an active field with partial results [E2]; behavioural evals remain the main safety tool.
- Limits: no current method certifies a model's values.
- Method: **behaviour-first evaluation**: test suites, adversarial cases, incident logs (evals/ in this package).

**10. Multivac and the Machines** ("The Evitable Conflict", 1950; "Franchise", 1955; "The Last Question", 1956)
- Proposed: machines quietly manage the world economy, nudging away opposition; an election decided by questioning one statistically chosen citizen.
- Analogue: algorithmic governance; optimization of economic planning; survey sampling and sortition; Goodhart's law.
- Evidence: algorithmic allocation already operates in markets and logistics [E1]; opaque optimization can entrench bias and evade contestability [E2].
- Limits: legitimacy is not reducible to accuracy; "Franchise" removes voice even if it captured preferences.
- Method: **delegation analysis**: what decision is delegated, what metric is optimized, who can contest, what happens when the metric is gamed (GOVERN mode, `aisociety`).

### Empire and Spacer cluster

**11. The Galactic Empire's decline**
- Proposed: a twelve-thousand-year empire decaying through bureaucratic ossification, loss of innovation, provincial breakaway, and loss of technical competence. Asimov drew on Gibbon's *Decline and Fall of the Roman Empire*.
- Analogue: structural-demographic theory, Tainter's diminishing returns to complexity, elite overproduction, fiscal crisis (CLIODYNAMICS_HISTORY.md).
- Evidence: fiscal strain and elite conflict frequently precede state breakdown in historical samples [E2, contested in scope]. Challenges: "decline" often means transformation; collapse narratives can mislead (McAnany & Yoffee 2010).
- Limits: a galactic empire has no empirical reference class.
- Method: **decline diagnostics**: fiscal, elite, popular, legitimacy, and capability indicators (`run sdt`, `run polity`).

**12. Trantor**
- Proposed: a planet-wide capital city that imports food from many agricultural worlds and administers the Empire.
- Analogue: urban metabolism; imperial capitals' supply dependence (e.g. Rome's grain supply from Egypt and North Africa) [E1 historical]; single points of failure.
- Evidence: concentrated, import-dependent systems are vulnerable to supply disruption [E1/E2].
- Limits: scale is fictional.
- Method: **dependency mapping**: critical flows, alternative suppliers, reserve days; interdependent failure (`run cascade --set interdependent=true`).

**13. Spacers and Settlers** (Aurora, Solaria; *The Naked Sun*, 1957; *Robots of Dawn*, 1983)
- Proposed: long-lived, robot-dependent Spacer worlds stagnate and shrink; robot-free Settlers expand. Solaria pushes isolation to an extreme.
- Analogue: automation and human capability; low fertility and ageing; small-population cultural loss; risk aversion.
- Evidence: demographic decline and ageing are real trends in many countries [E1]; links from automation to stagnation are E4 hypotheses.
- Limits: causal story is the author's thesis, not a finding.
- Method: **capability-dependence audit**: which skills would be lost if a tool vanished? (`knowledge` tacit model).

### Other works

**14. *The End of Eternity*** (1955)
- Proposed: a timeless organization edits history to minimize suffering, and in doing so suppresses risky exploration, trapping humanity.
- Analogue: counterfactual policy evaluation; the safety-vs-exploration trade-off; precaution that forecloses option value.
- Evidence: over-cautious regimes can block beneficial innovation; under-cautious ones produce disasters: both documented in technology history [E2].
- Limits: we never observe the untaken path.
- Method: **option-value check** in ACT: does the intervention reduce future choices? Score interventions on reversibility and exploration preserved.

**15. Gaia and Galaxia** (*Foundation's Edge*, 1982; *Foundation and Earth*, 1986)
- Proposed: a planet whose people, life and matter share one consciousness; proposed extension to the whole galaxy, chosen by a single human judgment.
- Analogue: collective intelligence; superorganisms; consensus vs diversity (Condorcet-type aggregation, diversity of judgment); hive coordination.
- Evidence: aggregation of independent judgments can outperform individuals [E2]; homogenization destroys the independence that makes aggregation work [E2].
- Limits: shared consciousness is not a scientific object.
- Method: **coordination–autonomy trade-off analysis**: compare governance designs by coordination capacity, diversity, exit rights and error correction (`society` ingroup bias and governance options).

**16. "Nightfall"** (story 1941; novel with Silverberg 1990)
- Proposed: a world that sees darkness once every ~2,000 years and collapses each time; cultists preserve fragments of memory.
- Analogue: rare high-consequence events and institutional memory; normalcy bias; short observation windows.
- Evidence: rare-disaster preparedness decays between events [E2].
- Method: **rare-event memory design** (knowledge preservation + early-warning); question any model calibrated on a short window.

**17. *The Gods Themselves*** (1972)
- Proposed: a free-energy technology with hidden catastrophic externalities; incentives suppress the warning scientist.
- Analogue: externalities, regulatory capture, epistemic suppression.
- Method: **externality and dissent audit**: who measures the side effect, and who is punished for reporting it?

**18. *The Bicentennial Man*** (1976)
- Proposed: a robot's two-century pursuit of legal humanity.
- Analogue: debates on moral status, legal personhood (corporations, rivers), and AI consciousness.
- Evidence: no consensus that current AI systems are conscious [E1 for "no consensus"].
- Method: separate **functional agency, legal capacity, rights, and moral status**; never assume present AI consciousness.

**19. Late Foundation reflections** (*Foundation's Edge*, *Prelude*, *Forward the Foundation*)
- The later books themselves question the Plan: hidden guardians, robot manipulation, and Gaia undercut the idea of free statistical history. Use them as Asimov's own critique of psychohistory.

## 3. Contradictions inside psychohistory (useful for AUDIT)

1. **Secrecy vs legitimacy**: the Plan requires an uninformed population, which is incompatible with democratic accountability and makes it untestable by its subjects.
2. **Aggregation vs leverage**: it assumes individual effects average out, yet the story turns on individuals (Seldon, Mule, Trevize).
3. **Prediction vs reflexivity**: published forecasts change behaviour; the Plan's fix (hide it) is not available to open societies.
4. **Precision vs chaos**: thousand-year horizons ignore sensitive dependence and structural breaks.
5. **Guidance vs freedom**: the Second Foundation and Daneel steer history; the later books admit that "statistical inevitability" was partly manipulation.

## 4. Concept to civlab

| Concept | Tool |
|---|---|
| Psychohistory, Seldon crises | `sdt`, `polity`, `robust`, forecasting ledger |
| Prime Radiant | `forecast.Ledger`, model cards |
| Encyclopedia Galactica | `knowledge` |
| Mule | `diffusion` hub seeding, `cascade` targeted attack |
| Three/Zeroth Laws, Multivac | `aisociety` (kernel, entrenched clause, oversight) |
| Empire decline, Trantor | `sdt`, `cascade --set interdependent=true` |
| Gaia | `society` (ingroup bias, governance types) |
| Nightfall | `ews`, `knowledge` |

Sources: SF Encyclopedia entries for Asimov, psychohistory and laws of robotics (SOURCES.md, A1 to A3); research sources per card in SOURCES.md.
