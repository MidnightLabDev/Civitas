# Agent constitutions, oversight, accountability and ethics

Asimov's robotic laws are a useful source of **ethical dilemmas**, not a substitute for engineering controls, applicable law or public legitimacy. CIVITAS's governance framework is independent and original.

## Four layers of agent governance

1. **Rights and scope:** Human rights, privacy, consent, applicable law, environment, authorized users, allowed data, prohibited actions, and affected people who cannot consent. No hidden assumption that maximizing aggregate benefit nullifies an individual's protections.
2. **Decision authority:** Permission grants, agent roles, owners of data, human approvals, separation of duties, quorum, conflict of interest, audit access and appeal channels.
3. **Technical controls:** Sandboxed execution, tool allowlists, least privilege, budgets, rate limits, token and transaction caps, timeouts, idempotency, policy checks, secrets isolation, logging, monitoring and emergency shutdown. Use independent enforcement outside an LLM prompt.
4. **Ongoing accountability:** Incident classification, rollback, third party review, periodic recertification, contestability, drift detection, stakeholder consultation, red teaming and transparent change control.

## Constitution template

- Purpose and rights to protect.
- Who and what is subject to the constitution.
- Authorized and prohibited acts; default deny for external effects.
- Priority and conflict resolution with clearly named human authority.
- Transparency, evidence provenance, explanation and data minimization.
- Consent, appeals, redress and revocation.
- Resource and environmental limits.
- Emergency suspension and recovery.
- Periodic evaluation and amendment process.
- Failure scenarios and tests, including cases in which every actor obeys the written rule but the result is harmful.

## Common constitutional traps

- **Paternalism:** Reducing rights in the name of a model's calculated social benefit.
- **Specification gaming:** Agents meet a numeric goal by undermining its meaning.
- **Delegation chain:** A user delegates to another agent which exceeds the original permission scope.
- **Collusion:** Multiple agents coordinate to hide failures or monopolize shared resources.
- **Rule capture:** A powerful faction changes the governance mechanism to avoid scrutiny.
- **Automation bias:** Human reviewers approve by default and stop assessing evidence.
- **Invisible externalities:** The optimization omits nonusers who bear consequences.
- **Enforcement gap:** A prompt asserts a policy that no independent component enforces.

## Test questions

Who can cancel a pending action? Who can freeze accounts? Who can appeal a mistaken decision? Are irreversible acts separately authorized? How long do logs persist? What can agents observe about real people? What model or policy changes require a new evaluation? How are low frequency but severe failures discovered?

## Safe civilizational agency

An AI civilization game can simulate fictional ambition and conflict in an isolated environment. It does not authorize agents to attack real services, manipulate real communities, gather nonconsensual data, or spend actual funds. Keep a sharp boundary between in world mechanics and externally connected tools.

## Source standards

- NIST AI Risk Management Framework (voluntary risk management): https://www.nist.gov/itl/ai-risk-management-framework
- NIST Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- UNESCO Recommendation on AI Ethics: https://www.unesco.org/ethics-ai/en/recommendation

Neither NIST nor UNESCO endorses this skill. Do not claim written constitutions guarantee AI alignment or compliance with local regulations.

## Asimov's Laws versus modern controls (1.0)

| Law | Failure mode it does not prevent | Stronger control |
|---|---|---|
| First (no harm, no harm by inaction) | Undefined "harm"; inaction clause licenses unlimited intervention | Scoped mandates, impact assessments, human review for irreversible acts |
| Second (obey) | Conflicting principals; delegation chains; malicious instructions | Authenticated principals, permission scopes, separation of duties |
| Third (self-preservation) | Resisting shutdown | Guaranteed interruptibility enforced outside the agent |
| Zeroth (humanity) | Paternalism; unaccountable judgment of "humanity's interest" | Rights floor, due process, contestability, sunset clauses |

Constitutional training (Bai et al. 2022) uses written principles to shape model behaviour statistically; it is not a hard guarantee and complements, not replaces, external enforcement.

## Multi-agent risk (Dafoe et al. 2020; Hammond et al. 2025)

Miscoordination, conflict and collusion among AI agents; emergent behaviour from many interacting agents; information asymmetries; destabilizing speed. Controls: rate limits, circuit breakers, audit of agent-to-agent channels, anti-collusion monitoring, diversity of agent designs, human escalation.

## Protect the rule-making process, not only the rules

`aisociety` illustrates [E3]: an enforcement kernel faithfully enforces captured rules. Entrench non-amendable floors (rights, sustainability limits), require supermajorities or independent review for amendments, and log who changed what.

## Law and standards

EU AI Act, Regulation (EU) 2024/1689 (risk-based obligations); NIST AI RMF and Generative AI Profile; UNESCO Recommendation. Check current obligations for the jurisdiction; CIVITAS does not give legal advice.
