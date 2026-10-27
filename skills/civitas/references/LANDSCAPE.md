# Landscape | related projects, tools and skills, and what CIVITAS takes from each

## Contents
1. Comparison table
2. What CIVITAS borrows (ideas, never code)
3. Choosing an external engine
4. Licensing and integration rules

Checked 2026-10-27. Descriptions are original summaries of public documentation; nothing listed here was installed or run inside this skill.

## 1. Comparison table

| Project | What it is | Strength | Limitation for CIVITAS purposes | License |
|---|---|---|---|---|
| Generative Agents (Park et al., UIST 2023) | LLM agents with memory stream, reflection, planning in a sandbox town | Believable individual behaviour; memory architecture | Small, short runs; believability ≠ validity | Research code (check repo) |
| Concordia (Google DeepMind; Vezhnevets et al. 2023) | Library for generative agent-based models with a "game master" grounding actions | Clean separation of agent proposals and world adjudication | Needs LLM API; empirical validation is user's job | Apache-2.0 |
| AgentSociety (Piao et al. 2025) | Large-scale LLM-driven social simulation platform | Scale; social science experiments (e.g. polarization, policy) | Heavy infrastructure; validation contested | See repo |
| Project Sid (Altera.AL 2024) | Many-agent simulations in Minecraft toward "AI civilization" | Shows role specialization and collective rules among many agents | Domain-specific environment; developer-reported results | Paper (arXiv) |
| GovSim (Piatti et al., NeurIPS 2024) | LLM agents managing common-pool resources | Direct test of LLM cooperation and sustainability; most models failed to sustain resources in their tests | Narrow scenarios | See repo |
| Melting Pot (Leibo et al., ICML 2021) | Multi-agent RL evaluation suite of social dilemmas | Standardized generalization tests for cooperation | RL, not LLM; game-like | Apache-2.0 (check) |
| OASIS (CAMEL-AI; Yang et al. 2024) | Social media simulation with up to a million LLM agents | Information diffusion at scale | Scale is not fidelity | Apache-2.0 |
| AgentCiv | Experimental emergent AI civilization project | Open exploration of emergence | Developer claims need replication | MIT |
| Project Psychohistory (electronistu) | A single prompt-protocol "generative historian" inspired by Foundation | Narrative civilization histories | Storytelling, not modelling; **proprietary license forbids reuse or derivatives**: CIVITAS uses no part of it | Proprietary |
| Mesa (ter Hoeven et al. 2025, JOSS) | Python agent-based modelling framework | Mature, transparent ABM in Python; visualization | Requires install; behaviour design is yours | Apache-2.0 |
| NetLogo | Classic ABM environment and model library | Teaching, rapid prototyping | Separate language/runtime | GPL (check) |
| Seshat Databank | Coded historical polity data | Reference classes for history | Coding choices; access terms | See site |
| ODD protocol (Grimm et al. 2020) | Standard for documenting simulations | Replicability | Documentation ≠ validation | Open article |
| NIST AI RMF, EU AI Act | Governance frameworks and law | Real-world obligations and practices | Not a technical guarantee | Public |
| End Game Thinking, WorldCodex, Structured Analysis, Systems Thinking (Claude skills on GitHub) | Foresight, worldbuilding suite, intelligence analysis, causal loops | Deep single-purpose workflows | Narrower scope; not simulation engines | See repos |

## 2. What CIVITAS borrows (as ideas, implemented originally)

| Idea | Source of inspiration | Where in CIVITAS |
|---|---|---|
| Agents propose, an independent arbiter disposes | Concordia's game master; capability-based security | `aisociety` constitution kernel; TECH_ARCHITECTURE |
| Bounded memory and reflection | Generative Agents | `aisociety` memory; AGENT_SOCIETIES |
| Commons dilemmas as an AI-society benchmark | GovSim, Melting Pot | `aisociety` scenarios, evals |
| Standard model documentation | ODD | SIMULATION_ENGINEERING, SIMULATORS |
| Competing hypotheses matrix | Structured analytic techniques (Heuer) | `ach` tool, CRITICAL_REVIEW |
| Causal loop analysis | System dynamics (Sterman 2000) | `cld` tool |
| Backcasting and pre-mortems | Foresight practice | FORECASTING, ENGINE |
| Canon-consistency records | Worldbuilding suites | WORLD_HISTORY persistence format |

## 3. Choosing an external engine

- Rule-based, transparent, many runs → civlab first, then **Mesa** when you need spatial grids, schedulers, visualization or larger models.
- Language-driven negotiation or role-play with grounded actions → **Concordia** (keep a deterministic kernel for resources).
- Social-media diffusion with LLM agents → **OASIS**, with privacy and validity checks.
- Social dilemma benchmarking of learning agents → **Melting Pot**.
- Historical reference classes → **Seshat** data.
- Always: ODD documentation, seeds, invariants, baselines, sensitivity.

## 4. Licensing and integration rules

- CIVITAS contains only original text and original stdlib Python. No third-party code is bundled.
- Before reusing any external code, read its license file; Apache-2.0 and MIT permit reuse with attribution and notice; proprietary or unlicensed repos do not.
- Verify current APIs from official documentation before writing integration code; do not invent function names.
