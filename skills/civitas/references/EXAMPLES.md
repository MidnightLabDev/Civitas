# Examples for Claude

These are demonstrations of the workflow, not validated real-world forecasts.

## Contents
1. Persistent agent civilization game · 2. Real-world product concept · 3. Conditional long-term strategic question · Suggested prompts · 4. Executed civlab study · 5. Rule capture in an AI agent society · 6. Quick mode

## Example 1: Persistent agent civilization game

User: "Use CIVITAS to design a persistent game in which autonomous AI civilizations cooperate, trade, and fight over many generations."

Desired response shape:

**Thesis:** A persistent world in which agents inherit institutions rather than just accumulating strength. A civilization's largest advantage can become the cause of its collapse.

**World map:** Four original political systems: a federated commons, a merchant consortium, a research monastery, and a mobile nomadic network. Each has different resource needs, rights, and bottlenecks. No species, empire, or characters are taken from existing fiction.

**Mechanics:**

- World state tracks food, energy, knowledge, legitimacy, and trust.
- Agents propose actions; a rule engine checks costs, authorization, and world laws before applying effects.
- Treaties create mutual obligations and measurable enforcement challenges.
- Knowledge can be copied, lost, hoarded, or redistributed.
- Cultural norms spread through imitation and trade, not by arbitrary narration.
- Each turn advances needs, negotiation, resource transfers, technology, conflict, incident logs, and public outcomes.

**Feedback loops:** Successful cooperation increases trust and trade, which can create dependence on a single trusted institution. Excessive extraction increases short-term wealth and long-term unrest.

**Disruptions:** Collapse of a trade corridor; discovery of cheap energy; a governing agent interprets an obsolete charter too literally.

**MVP:** Run a seeded, rule-based simulation with four societies and 50 turns. Track survival, inequality, treaty durability, and agent autonomy incidents. Only after the mechanics are stable, introduce LLM decision policies in a sandbox.

**Integrity:** Game agents must not receive unrestricted real-world capabilities. Fictional success metrics are not human welfare measurements.

## Example 2: Real-world product concept

User: "Invent a next-generation digital identity tool for people who attend events."

Desired response shape:

**Concept:** A portable introduction layer where a person deliberately shares a small, context-specific identity card at each encounter and can revoke it later.

**System map:** Attendees, organizers, recipients, platform operator, and external identity providers. Attendees value convenience but also control. Organizers value discovery and measurement, which can conflict with participant privacy.

**Unusual mechanism:** A social connection remains a mutual permission relationship, not an automatically permanent data transfer.

**Two loops:** Better introductions increase participation and utility. More shared data attracts organizers while undermining user trust unless consent limits are visible and enforceable.

**Stress test:** An organizer demands a permanent full attendee export; the platform makes consent rules enforceable, gives opt-in choices, and logs access.

**MVP:** Create, share, revoke, and view interaction permissions without requiring account installation by the recipient. Test whether attendees understand what is shared and can actually revoke future access.

**Uncertainty:** Adoption and willingness to pay are unknown until tested with real users.

## Example 3: Conditional long-term strategic question

User: "What might agent-managed software companies look like in 15 years?"

Good output:

- Define what is measured (ownership, operations, liability, customer trust), not just what is futuristic.
- Identify actors including founders, workers, customers, regulators, auditors, cloud providers, and agents.
- Present continuity, fracture, and surprising alternative branches, each with conditional triggers.
- Flag infrastructure costs, attribution of responsibility, and concentration risks.
- Separate facts that require recent verification from hypothetical technology developments.
- End with actions that a company can try now without depending on a particular futuristic prediction.

Bad output: "By year 15, 83 percent of businesses will be autonomous" without a cited model and data.

## Suggested user prompts

- "Use CIVITAS in INVENT mode to invent five unusual but technically plausible AI products. For each, include a social consequence and a testable MVP."
- "Use CIVITAS in GOVERN mode to write an agent constitution for a platform that lets independent AI agents transact with one another."
- "Use CIVITAS in SIMULATE mode to design the world rules, agent incentives, and 100-turn progression of an AI civilization game."
- "Use CIVITAS in FORECAST mode to explore three conditional futures for AI infrastructure in the Gulf over the next decade, with evidence gaps and early warning signals."
- "Use CIVITAS in STRESS mode to critique this startup concept and find failures that arise even when every participant follows the stated rules."

## Example 4: Executed civlab study (actual results, seeds 42-51, 2026-10-27)

User: "Does a central sanctioning institution beat peer punishment for a commons village?"

Command: `python scripts/civitas.py run society --config examples/society_commons.json --set governance=<g> --runs 10`

| Governance | Tail cooperation mean (p05-p95) | Final Gini mean | Final legitimacy |
|---|---|---|---|
| none | 0.235 (0.197-0.275) | 0.617 | n/a |
| peer | 0.876 (0.496-0.993) | 0.245 | n/a |
| central (corruption 0.1) | 0.990 (0.985-0.995) | 0.109 | 0.781 |
| polycentric | 0.993 (0.989-0.996) | 0.104 | 0.781 |

Good answer shape: "In this model [E3, synthetic], institutions of either kind sustain cooperation that collapses without them; peer punishment is less reliable across seeds (wide interval); a low-corruption central institution performs best, but a separate run shows legitimacy collapsing at corruption 0.4-0.5, so the result hinges on integrity. Before applying this to a real village, check: monitoring costs, who controls the institution, local norms (Ostrom 1990)." Then offer a sensitivity run on corruption and multiplier.

## Example 5: Rule capture in an AI agent society (actual results)

Command: `python scripts/civitas.py compare aisociety --config examples/ai_society_capture.json --alt entrenched_sustainability=true --runs 10`

Baseline (kernel enforcement on, growth faction majority): final commons ratio 0.16, zero rule-violation incidents (the kernel blocked 2,796 over-harvest attempts per run on average), yet the commons was drained because the faction voted the cap up each period. Adding an entrenched sustainability clause raised the final commons ratio by 0.61 (Monte Carlo 95% interval 0.41 to 0.81), lowered Gini by 0.08 and hardship by 0.14 [E3].

Good answer shape: lead with the governance insight (enforcement without protected rule-making can automate capture), disclose that agents are hand-written archetypes, and propose a test with LLM policies.

## Example 6: Quick mode

User: "Was Hari Seldon's psychohistory realistic?"
Good answer (no headings): two paragraphs: what Asimov imagined and his gas-law analogy; why real social prediction works only for some aggregates and short horizons (reflexivity, heavy tails, rule change), with one real example (instability-onset models) and an offer to go deeper.
