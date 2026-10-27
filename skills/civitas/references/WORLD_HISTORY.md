# Building original long range civilizations and believable alternate histories

## Founding conditions

Define environmental carrying capacity, geography, technology limits, resource distribution, migration, initial contact networks, founding conflict, authority and social norms. Avoid copying Asimov's named organizations, plots or societies. CIVITAS is an original design language, not a continuation of Foundation canon.

## Civilization as changing institutions

Historical explanations should connect material constraints, power, legitimacy, collective action, technology, culture and accident. Reject predetermined ladders from primitive to advanced, inevitable progress, and simplistic cycles of rise and fall. Multiple social arrangements can be successful in different settings; collapse may mean transformation rather than disappearance.

## Multi era design

For each era, record: defining conditions, everyday institutions, energy and food sources, technology diffusion, social mobility, external relations, distribution of rights, powerful factions, inherited knowledge, resistance, and one plausible turning point. Institutions adapt, acquire interests, lose legitimacy or become contradictory. Add independent people with agency rather than an all knowing planner.

## Make ordinary life visible

Ask about housing, language, labor, education, family, belief, disability access, transportation, trade, legal remedies, festivals, dissent and the costs paid by people outside the governing class. Make cultures internally diverse and historically dynamic. Do not stereotype real cultures or attribute fixed traits to identity groups.

## Original CIVITAS world patterns

- **Distributed archive polity:** communities hold partial knowledge and must negotiate verification; benefit is resilience, danger is fragmented truth.
- **Maintenance economy:** prestige attaches to repair rather than discovery; benefit is reliability, danger is stagnation and gatekeeping.
- **Consent federation:** every infrastructure connection is revocable; benefit is autonomy, danger is coordination deadlock.
- **Memory commons:** memories become shared civic records by informed choice; benefit is knowledge continuity, danger is privacy leakage.
- **Temporary emergency charter:** power expands during crises but expires unless reauthorized; benefit is rapid action, danger is manipulated crises.
- **Mobile energy treaty:** power moves across settlements with environmental seasons; benefit is resource balancing, danger is leverage by transport owners.

These are original prompts. They can be recombined, but the creative result must have coherent constraints and nontrivial disagreements.

## Three narrative scales

- Personal: a life changed by institutional rules.
- Meso: a guild, laboratory, family network or city navigating incentives.
- Macro: resources, technological transitions, migration, climate, war, political and economic change.

A convincing turning point should be meaningful at all three scales without making one character omnipotent.

## Historical analysis cautions

Distinguish recorded sources, historical interpretations, uncertain chronology, missing archives, and speculative counterfactuals. Never claim a model recreates a historical society without appropriate data and historians' scrutiny. Use multiple contrasting explanations for major transitions.

## Simulation-assisted worldbuilding (1.0)

1. Run `python scripts/civitas.py run polity --config examples/polity_world.json --runs 1 --output world.json`.
2. Read the trajectory: peaks in `largest_share` are imperial eras, drops are fragmentations, rising `polities` counts are warring-states periods.
3. Optionally run `sdt` for the dominant polity's internal cycle and `knowledge` for what each fragmentation loses.
4. Narrate eras with ordinary lives, factions and dissent; keep a persistence record: era, polities, institutions, technologies, lost knowledge, open conflicts.
5. Label the history E5. Check consistency: population vs food, travel speed vs empire size, technology diffusion time.
