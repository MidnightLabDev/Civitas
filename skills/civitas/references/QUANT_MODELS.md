# Quantitative model cards | equations CIVITAS can reason with

## Contents
1. How to use a model card
2. Growth, limits and competition
3. Diffusion and contagion
4. Cooperation, conflict and games
5. Inequality, segregation and culture
6. Stability, cascades and tipping
7. Historical and macro dynamics
8. Information and forecasting quantities
9. Choosing a model

## 1. How to use a card

Each card: **equation**, **what it captures**, **key assumptions**, **where it breaks**, **civlab** (if implemented). Writing an equation does not make a claim scientific: parameters need sources or must be labelled illustrative (E3/E5). Prefer the simplest card that answers the question; add mechanisms only when they change the conclusion.

## 2. Growth, limits and competition

**Logistic growth**: `dN/dt = r N (1 - N/K)`. Saturation toward carrying capacity K. Breaks when K itself changes (technology, degradation) or with delays (overshoot and collapse: add a lag or a degradable K).

**Overshoot with degradable capacity**: `dK/dt = g (K0 - K) - h N` couples population to resource depletion; generates boom-bust when h is large. Used qualitatively in *Limits to Growth*-type models (Meadows et al. 1972; empirical comparison: Herrington 2021, contested).

**Lotka-Volterra (predator-prey / competition)**: `dx/dt = a x - b x y`, `dy/dt = c x y - d y`. Oscillations from interaction. Useful as analogy for extractors vs resources, elites vs producers; parameters rarely identifiable socially.

**Lanchester attrition**: square law `dA/dt = -β B`, `dB/dt = -α A`: concentration of force matters quadratically under aimed fire. Breaks with terrain, morale, logistics, asymmetric war.

**Richardson arms race**: `dx/dt = k y - a x + g`. Mutual fear (k), fatigue (a), grievance (g); stable if `a b > k l`. A teaching model of security dilemmas.

## 3. Diffusion and contagion

**Bass (1969)**: `f(t) / (1 - F(t)) = p + q F(t)`; closed form `F(t) = (1 - e^{-(p+q)t}) / (1 + (q/p) e^{-(p+q)t})`; peak at `t* = ln(q/p)/(p+q)` when q > p. *civlab*: `diffusion` mode bass, with fitting. Breaks with supply limits, competing technologies, prices; early data identify market size poorly.

**SIR-type social contagion**: `dS/dt = -β S I`, `dI/dt = β S I - γ I`; threshold `R0 = β/γ > 1`. Used for rumours and behaviours, but social adoption often needs multiple exposures (complex contagion), which SIR misses.

**Threshold cascades** (Granovetter 1978; Watts 2002): adopt when fraction of adopting neighbours ≥ personal threshold φ. Global cascades possible only in a window of network density; cascade sizes are bimodal and seed-sensitive. *civlab*: `diffusion` (cascade).

## 4. Cooperation, conflict and games

**Public goods game**: payoff `π_i = (r/n) Σ c_j - c_i`; defection dominant when r < n. Cooperation sustained by repetition, reciprocity, punishment (Fehr & Gächter 2000), network structure, reputation or institutions (Ostrom 1990). *civlab*: `society`.

**Replicator dynamics**: `dx_i/dt = x_i (π_i - π̄)`: strategies grow when above average payoff. Fermi imitation `P(i copies j) = 1/(1 + e^{-s(π_j - π_i)})` is the stochastic analogue. *civlab*: `society` imitation step.

**Repeated prisoner's dilemma**: cooperation sustainable if discount factor `δ ≥ (T - R)/(T - P)`; shadow of the future matters.

**Common-pool resource with regrowth**: logistic stock with harvest; maximum sustainable yield `rK/4` at `N = K/2`. *civlab*: `aisociety` uses this for its entrenched clause.

## 5. Inequality, segregation and culture

**Gini coefficient**: `G = Σ_i Σ_j |x_i - x_j| / (2 n² x̄)`. One number; hides shape. Report shares (top 10%) too.

**Multiplicative wealth (Kesten/yard-sale)**: random proportional exchanges concentrate wealth without any skill difference; redistribution stabilizes. Shows inequality can be emergent, not deserved.

**Schelling segregation** (1971): mild preferences for similar neighbours produce strong segregation. Lesson: macro patterns need not reflect strong micro intent.

**Axelrod culture model** (1997): local convergence of cultural traits produces global polarization when interaction requires similarity.

## 6. Stability, cascades and tipping

**Fold bifurcation / critical slowing down**: near a tipping point, recovery rate λ → 0; variance and lag-1 autocorrelation rise (Scheffer et al. 2009). *civlab*: `ews`. False positives and negatives occur.

**Load-redistribution cascades** (Motter & Lai 2002): capacity `C_i = (1 + α) L_i`; failure shifts load. Heterogeneous networks robust to random failure, fragile to targeted attack. Interdependent networks fail more abruptly (Buldyrev et al. 2010). *civlab*: `cascade`.

**Percolation**: a giant connected component exists above a critical edge density; fragmentation is abrupt.

**Dragon kings** (Sornette 2009): some extremes come from distinct amplifying mechanisms and may be more predictable than black swans.

## 7. Historical and macro dynamics

**Structural-demographic stress (stylized)**: Goldstone's `PSI = MMP × EMP × SFD` (mass mobilization × elite mobilization × state fiscal distress). *civlab*: `sdt` uses an original toy version; real PSI estimation uses measured series (Turchin 2016).

**Metaethnic frontier / asabiyyah** (Turchin 2003): solidarity grows at frontiers `dS/dt = r0 S(1-S)` and decays inside `dS/dt = -δ S`; power decays with distance `P = A S̄ e^{-d/h}`. *civlab*: `polity`.

**Henrich skill transmission** (2004): `Δz̄ ≈ -α + β(γ + ln N)`; critical `N* = e^{α/β - γ}`. *civlab*: `knowledge`.

**Kremer (1993)**: idea production proportional to population gives hyperbolic long-run growth until the demographic transition.

**Solow growth**: `k̇ = s f(k) - (n + δ) k`; growth from capital deepening stalls without technology growth.

**Increasing returns and lock-in** (Arthur 1989): small early events plus positive feedback lock in one technology regardless of merit.

## 8. Information and forecasting quantities

**Shannon entropy**: `H = -Σ p log p`; measures uncertainty and diversity (use for cultural or market diversity).

**Bayes in odds form**: posterior odds = prior odds × likelihood ratio. *civlab*: `bayes`.

**Beta-binomial base rate**: `p | k,n ~ Beta(a + k, b + n - k)`. *civlab*: `baserate`.

**Brier score** `(p - y)²`; log score `-ln p(y)`; both strictly proper (Gneiting & Raftery 2007). Murphy decomposition: BS = reliability - resolution + uncertainty. *civlab*: `score`.

**Logit pooling with extremizing** (Satopää et al. 2014): `logit p* = a · mean(logit p_i)`, a > 1 when forecasters share information only partially. *civlab*: `pool`.

## 9. Choosing a model

| Question | Start with |
|---|---|
| Will adoption take off and when? | Bass; threshold cascade if network seeding matters |
| Can a shared resource be governed? | Common-pool with regrowth; public goods with institutions (`society`, `aisociety`) |
| Why is this state unstable? | SDT indicators; legitimacy; ACH over rival explanations |
| Will failure spread? | Load-redistribution or percolation (`cascade`) |
| Is a tipping point near? | Critical slowing down (`ews`), with caveats |
| Will knowledge survive? | Henrich + archive redundancy (`knowledge`) |
| Who dominates a fictional map? | Asabiyyah frontier model (`polity`) |
| Which policy is robust? | Any model + `robust` (minimax regret) |

Sources: SOURCES.md, sections C, D, E.
