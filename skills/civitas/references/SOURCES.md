# Annotated research library | CIVITAS 1.0

## Contents
A. Asimov and literary foundations · B. History and cliodynamics · C. Complexity, networks, tipping · D. Cooperation, institutions, culture · E. Forecasting, decision and causal inference · F. Simulation and agent societies · G. AI governance and safety · H. Skill format

**Provenance.** Bibliographic details were checked against DOIs, publisher pages, arXiv or official repositories on **2026-10-27** (VERIFIED unless marked). PARTIAL = work exists, minor detail noted. Entries carried over from the original package and re-linked are marked (orig). Annotations are original. "Use" names where CIVITAS relies on the source; "Quality" states evidence type and main limitation. A citation supports only what the source itself claims.

Evidence types: PR = peer-reviewed; BK = scholarly book; PP = preprint; DOC = official documentation/report; REPO = software repository; REF = reference work.

## A. Asimov and literary foundations

| ID | Source | Link | Concepts | Use in CIVITAS | Quality |
|---|---|---|---|---|---|
| A1 | *The Encyclopedia of Science Fiction*: "Asimov, Isaac" (orig) | https://sf-encyclopedia.com/entry/asimov_isaac | Bibliography, Robot/Empire/Foundation links | ASIMOV_ATLAS dates and series structure | REF; authoritative SF reference |
| A2 | SFE: "Psychohistory" (orig) | https://sf-encyclopedia.com/entry/psychohistory | Fictional predictive science vs academic psychohistory | PSYCHOHISTORY, ATLAS card 1 | REF |
| A3 | SFE: "Laws of Robotics" (orig) | https://sf-encyclopedia.com/entry/laws_of_robotics | Three/Zeroth Laws history | ATLAS cards 7-8, AI_GOVERNANCE | REF |

Primary texts (Asimov's novels and stories) are cited by title and year only; consult lawful editions for exact wording.

## B. History and cliodynamics

| ID | Source | Link | Concepts | Use | Quality |
|---|---|---|---|---|---|
| B1 | Goldstone, J. A. (1991). *Revolution and Rebellion in the Early Modern World*. UC Press. | https://doi.org/10.4324/9781315408620 (25th-anniv. ed.) | Demographic-structural causes of state breakdown | SDT theory; `sdt` PSI | BK; comparative early-modern cases |
| B2 | Turchin, P. & Nefedov, S. A. (2009). *Secular Cycles*. Princeton UP. | https://doi.org/10.1515/9781400830688 | Integrative/disintegrative phases, elite overproduction | CLIODYNAMICS, `sdt` | BK; cycle interpretation debated |
| B3 | Turchin, P. (2016). *Ages of Discord*. Beresta Books. | no DOI; review https://doi.org/10.21237/C7clio8237156 | Structural-demographic analysis of the US, PSI | Modern SDT application, with caveats | BK; contested application |
| B4 | Goldstone, J. A. et al. (2010). A global model for forecasting political instability. *AJPS* 54(1), 190-208 (online Dec 2009). | https://doi.org/10.1111/j.1540-5907.2009.00426.x | Instability onset forecasting with few variables | FORECASTING, HISTORY diagnostics | PR; predicts onset risk not timing |
| B5 | Turchin, P. et al. (2018). Quantitative historical analysis uncovers a single dimension of complexity that structures global variation in human social organization. *PNAS* 115(2). | https://doi.org/10.1073/pnas.1708800115 | Seshat data; complexity dimension | Reference classes | PR; coding choices matter |
| B6 | Tainter, J. A. (1988). *The Collapse of Complex Societies*. Cambridge UP. | review https://doi.org/10.1017/S0003598X00075256 | Diminishing returns to complexity | CLIODYNAMICS theory table | BK; hard to measure returns |
| B7 | Acemoglu, D. & Robinson, J. A. (2012). *Why Nations Fail*; (2019) *The Narrow Corridor*. | reviews https://doi.org/10.30541/v51i3pp.276-278 | Inclusive vs extractive institutions; state-society balance | SOCIAL_INSTITUTIONS, HISTORY | BK; causal identification debated |
| B8 | Scheidel, W. (2017). *The Great Leveler*. Princeton UP. | https://doi.org/10.1515/9781400884605 | Violent shocks and inequality compression | Inequality mechanisms | BK; data quality varies |
| B9 | McAnany, P. A. & Yoffee, N. (eds) (2010). *Questioning Collapse*. Cambridge UP. | https://doi.org/10.1017/CBO9780511757815 | Resilience; critique of collapse narratives | Ground rules in CLIODYNAMICS; CRITICAL_REVIEW bias checks | BK (edited) |
| B10 | Kuran, T. (1991). Now out of never. *World Politics* 44(1), 7-48. | https://doi.org/10.2307/2010422 | Preference falsification, surprise revolutions | Reflexivity, Mule card, cascades | PR |
| B11 | Kremer, M. (1993). Population growth and technological change: One million B.C. to 1990. *QJE* 108(3), 681-716. | https://doi.org/10.2307/2118405 | Population-idea feedback | QUANT_MODELS | PR; long-run macro only |
| B12 | Henrich, J. (2004). Demography and cultural evolution... the Tasmanian case. *American Antiquity* 69(2), 197-214. | https://doi.org/10.2307/4128416 | Skill loss in small populations | `knowledge`, Encyclopedia Galactica card | PR; case application contested |
| B13 | Meadows, D. H. et al. (1972). *The Limits to Growth*; Herrington, G. (2021). Update to limits to growth. *J. Industrial Ecology* 25(3), 614-626. | https://doi.org/10.1111/jiec.13084 | Overshoot, World3 | ECONOMY_ECOLOGY; QUANT overshoot | BK + PR; scenario model, contested |
| B14 | Kemp, L. et al. (2022). Climate Endgame. *PNAS* 119(34), e2108146119. | https://doi.org/10.1073/pnas.2108146119 | Catastrophic climate scenarios | Long-range risk branches | PR (perspective) |

## C. Complexity, networks, tipping

| ID | Source | Link | Concepts | Use | Quality |
|---|---|---|---|---|---|
| C1 | Scheffer, M. et al. (2009). Early-warning signals for critical transitions. *Nature* 461, 53-59. | https://doi.org/10.1038/nature08227 | Critical slowing down | `ews`, WARN mode | PR; review |
| C2 | Dakos, V. et al. (2012). Methods for detecting early warnings of critical transitions in time series illustrated using simulated ecological data. *PLoS ONE* 7(7), e41010. (PARTIAL: full title) | https://doi.org/10.1371/journal.pone.0041010 | Rolling-window indicators, Kendall tau, surrogates | `ews` implementation | PR |
| C3 | Watts, D. J. & Strogatz, S. H. (1998). Collective dynamics of 'small-world' networks. *Nature* 393, 440-442. | https://doi.org/10.1038/30918 | Small-world graphs | `core.watts_strogatz` | PR |
| C4 | Watts, D. J. (2002). A simple model of global cascades on random networks. *PNAS* 99(9), 5766-5771. | https://doi.org/10.1073/pnas.082090499 | Cascade window | `diffusion` cascade | PR |
| C5 | Granovetter, M. (1978). Threshold models of collective behavior. *AJS* 83(6), 1420-1443. | https://doi.org/10.1086/226707 | Thresholds, riots, adoption | `diffusion`, Mule card | PR |
| C6 | Motter, A. E. & Lai, Y.-C. (2002). Cascade-based attacks on complex networks. *Phys. Rev. E* 66, 065102. | https://doi.org/10.1103/PhysRevE.66.065102 | Load-redistribution cascades | `cascade` | PR |
| C7 | Buldyrev, S. V. et al. (2010). Catastrophic cascade of failures in interdependent networks. *Nature* 464, 1025-1028. | https://doi.org/10.1038/nature08932 | Interdependence | `cascade --set interdependent=true` | PR |
| C8 | Sornette, D. (2009). Dragon-kings, black swans and the prediction of crises. arXiv:0907.4290. | https://arxiv.org/abs/0907.4290 | Extremes from amplifying mechanisms | Mule card, STRESS | PR/PP |
| C9 | Holling, C. S. (2001). Understanding the complexity of economic, ecological, and social systems. *Ecosystems* 4, 390-405. | https://doi.org/10.1007/s10021-001-0101-5 | Adaptive cycle, panarchy | SYSTEMS_SCIENCE, resilience | PR; heuristic |
| C10 | Arthur, W. B. (1989). Competing technologies, increasing returns, and lock-in by historical events. *Economic Journal* 99(394), 116ff. | https://doi.org/10.2307/2234208 | Path dependence | ECONOMY_ECOLOGY | PR |
| C11 | Sterman, J. D. (2000). *Business Dynamics*. Irwin/McGraw-Hill. | https://mitmgmtfaculty.mit.edu/jsterman/business-dynamics/ | Stocks, flows, feedback | `cld`, SYSTEMS_SCIENCE | BK |
| C12 | Epstein, J. M. & Axtell, R. (1996). *Growing Artificial Societies*. MIT Press. | https://doi.org/10.7551/mitpress/3374.001.0001 | Sugarscape, generative social science | SIMULATION_ENGINEERING | BK |
| C13 | Epstein, J. M. (1999). Agent-based computational models and generative social science. *Complexity* 4(5), 41-60. | https://doi.org/10.1002/(SICI)1099-0526(199905/06)4:5<41::AID-CPLX9>3.0.CO;2-F | "If you didn't grow it, you didn't explain it" | Explanation standard for ABMs | PR |

## D. Cooperation, institutions, culture

| ID | Source | Link | Concepts | Use | Quality |
|---|---|---|---|---|---|
| D1 | Ostrom, E. (1990). *Governing the Commons*. Cambridge UP. | https://doi.org/10.1017/CBO9780511807763 | Commons institutions, design principles | SOCIAL_INSTITUTIONS, `society`, `aisociety` | BK; field evidence |
| D2 | Nobel Prize 2009 (Ostrom, Williamson) press release (orig) | https://www.nobelprize.org/prizes/economic-sciences/2009/press-release/ | Recognition of governance research | Context | DOC |
| D3 | Fehr, E. & Gächter, S. (2000). Cooperation and punishment in public goods experiments. *AER* 90(4), 980-994. | https://doi.org/10.1257/aer.90.4.980 | Costly punishment sustains cooperation | `society` peer punishment | PR; lab samples |
| D4 | Axelrod, R. (1997). The dissemination of culture. *J. Conflict Resolution* 41(2), 203-226. | https://doi.org/10.1177/0022002797041002001 | Local convergence, global polarization | QUANT_MODELS | PR |
| D5 | Schelling, T. C. (1971). Dynamic models of segregation. *J. Math. Sociology* 1(2), 143-186. | https://doi.org/10.1080/0022250X.1971.9989794 | Micro-motives, macro-behaviour | QUANT_MODELS | PR |
| D6 | Merton, R. K. (1948). The self-fulfilling prophecy. *Antioch Review* 8(2), 193ff. | https://doi.org/10.2307/4609267 | Reflexive predictions | ENGINE BRANCH reflexivity | PR (essay) |
| D7 | Lucas, R. E. (1976). Econometric policy evaluation: A critique. *Carnegie-Rochester Conf. Series* 1, 19-46. | https://doi.org/10.1016/S0167-2231(76)80003-6 | Behaviour changes with policy | Reflexivity, CRITICAL_REVIEW #15 | PR |

## E. Forecasting, decision and causal inference

| ID | Source | Link | Concepts | Use | Quality |
|---|---|---|---|---|---|
| E1 | Mellers, B. et al. (2014). Psychological strategies for winning a geopolitical forecasting tournament. *Psychological Science* 25(5), 1106-1115. | https://doi.org/10.1177/0956797614524255 | Training, teaming, tracking forecasters | FORECASTING practice | PR |
| E2 | Tetlock, P. E. & Gardner, D. (2015). *Superforecasting*. Crown. | (book) | Calibration habits | FORECASTING | BK (popular) |
| E3 | Satopää, V. A. et al. (2014). Combining multiple probability predictions using a simple logit model. *IJF* 30(2), 344-356. | https://doi.org/10.1016/j.ijforecast.2013.09.009 | Logit pooling, extremizing | `pool` | PR |
| E4 | Gneiting, T. & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102(477), 359-378. | https://doi.org/10.1198/016214506000001437 | Proper scores | `score` | PR |
| E5 | Flyvbjerg, B. (2006). From Nobel Prize to project management: Getting risks right. *Project Management Journal* 37(3), 5-15. | https://doi.org/10.1177/875697280603700302 | Reference class forecasting | GROUND stage | PR |
| E6 | Kahneman, D. & Tversky, A. (1979). Intuitive prediction: Biases and corrective procedures. *TIMS Studies in Management Science* 12, 313-327 (PARTIAL: reprint verified, 1982). Lovallo, D. & Kahneman, D. (2003). Delusions of success. *HBR*, July. | https://doi.org/10.1017/CBO9780511809477.031 | Outside view | GROUND stage | PR/BK |
| E7 | Arrow, K. J. et al. (2008). The promise of prediction markets. *Science* 320, 877-878. | https://doi.org/10.1126/science.1157679 | Markets as aggregators | FORECASTING options | PR (policy forum) |
| E8 | Lempert, R. J., Popper, S. W. & Bankes, S. C. (2003). *Shaping the Next One Hundred Years* (MR-1626). RAND. | https://doi.org/10.7249/MR1626 | Robust decision making, regret | `robust`, ACT stage | DOC |
| E9 | Haasnoot, M. et al. (2013). Dynamic adaptive policy pathways. *Global Environmental Change* 23(2), 485-498. | https://doi.org/10.1016/j.gloenvcha.2012.12.006 | Pathways, tipping points of policies | Seldon crisis card, ACT | PR |
| E10 | Morris, M. D. (1991). Factorial sampling plans for preliminary computational experiments. *Technometrics* 33(2), 161-174. | https://doi.org/10.1080/00401706.1991.10484804 | Elementary effects | `sensitivity` morris | PR |
| E11 | Saltelli, A. et al. (2008). *Global Sensitivity Analysis: The Primer*. Wiley. | https://doi.org/10.1002/9780470725184 | Sensitivity methods | SIMULATION_ENGINEERING | BK |
| E12 | Hernán, M. A. & Robins, J. M. (2020). *Causal Inference: What If*. CRC (online, revised). | https://miguelhernan.org/whatifbook | Potential outcomes, DAGs | SYSTEMS_SCIENCE causal workflow | BK; cite version date |
| E13 | Pearl, J. et al., *Probabilistic and Causal Inference: The Works of Judea Pearl* (ACM Books 2022) (orig) | https://ftp.cs.ucla.edu/pub/stat_ser/ACMBook-published-2022.pdf | Causal calculus | Causal workflow | BK |
| E14 | OECD Strategic Foresight (orig) | https://www.oecd.org/en/about/programmes/strategic-foresight.html | Horizon scanning, scenarios | FORECASTING | DOC |

## F. Simulation and agent societies

| ID | Source | Link | Concepts | Use | Quality |
|---|---|---|---|---|---|
| F1 | Grimm, V. et al. (2020). The ODD protocol... second update. *JASSS* 23(2). | https://doi.org/10.18564/jasss.4259 | Model documentation | SIMULATION_ENGINEERING, SIMULATORS | PR |
| F2 | Park, J. S. et al. (2023). Generative agents: Interactive simulacra of human behavior. *UIST '23*. | https://doi.org/10.1145/3586183.3606763 | Memory, reflection, planning | AGENT_SOCIETIES, `aisociety` memory | PR |
| F3 | Vezhnevets, A. S. et al. (2023). Generative agent-based modeling with actions grounded in physical, social, or digital space using Concordia. arXiv:2312.03664. Repo Apache-2.0. | https://arxiv.org/abs/2312.03664 | Game-master grounding | Kernel design | PP + REPO |
| F4 | Piao, J. et al. (2025). AgentSociety. arXiv:2502.08691. | https://arxiv.org/abs/2502.08691 | Large-scale LLM social simulation | LANDSCAPE | PP |
| F5 | Altera.AL et al. (2024). Project Sid: Many-agent simulations toward AI civilization. arXiv:2411.00114. | https://arxiv.org/abs/2411.00114 | Specialization, collective rules | AGENT_SOCIETIES | PP |
| F6 | Piatti, G. et al. (2024). Cooperate or collapse: Emergence of sustainable cooperation in a society of LLM agents. NeurIPS 2024. | https://arxiv.org/abs/2404.16698 | LLM commons dilemmas | `aisociety` benchmark idea, evals | PR |
| F7 | Leibo, J. Z. et al. (2021). Scalable evaluation of multi-agent reinforcement learning with Melting Pot. ICML (PMLR 139), 6187-6199. (PARTIAL: title) | https://arxiv.org/abs/2107.06857 | Social dilemma generalization | AGENT_SOCIETIES test matrix | PR |
| F8 | Yang, Z. et al. (2024). OASIS: Open agent social interaction simulations with one million agents. arXiv:2411.11581. Repo Apache-2.0. | https://arxiv.org/abs/2411.11581 | Social media simulation | LANDSCAPE | PP + REPO |
| F9 | ter Hoeven, E. et al. (2025). Mesa 3: Agent-based modeling with Python in 2025. *JOSS* 10(107), 7668. Repo Apache-2.0. | https://doi.org/10.21105/joss.07668 | Python ABM | External engine | PR + REPO |
| F10 | Larooij, M. & Törnberg, P. (2025). Validation is the central challenge for generative social simulation: A critical review of LLMs in agent-based modeling. *AI Review* 59(1), art. 15. | https://doi.org/10.1007/s10462-025-11412-6 | Validity limits of LLM ABMs | EVIDENCE_VALIDATION | PR |
| F11 | Taillandier et al. (2025). Integrating LLM in agent-based social simulation: Opportunities and challenges. arXiv:2507.19364 (orig; not re-verified) | https://arxiv.org/abs/2507.19364 | LLM-ABM integration | AGENT_SOCIETIES | PP |
| F12 | NetLogo (orig) | https://www.netlogo.org/ | ABM environment | LANDSCAPE | REPO/DOC |
| F13 | AgentCiv (MIT) | https://github.com/agentciv/agentciv | Emergent AI civilization experiments | LANDSCAPE | REPO |
| F14 | Project Psychohistory (electronistu), proprietary license | https://github.com/electronistu/Project_Psychohistory | Narrative "generative historian" prompt | LANDSCAPE only; nothing reused | REPO |

## G. AI governance and safety

| ID | Source | Link | Concepts | Use | Quality |
|---|---|---|---|---|---|
| G1 | Bai, Y. et al. (2022). Constitutional AI: Harmlessness from AI feedback. arXiv:2212.08073. | https://arxiv.org/abs/2212.08073 | Training with written principles | Three Laws card; AI_GOVERNANCE | PP (widely cited) |
| G2 | Regulation (EU) 2024/1689 (AI Act), OJ L 12.7.2024. | http://data.europa.eu/eli/reg/2024/1689/oj | Risk-based AI law | AI_GOVERNANCE | Law |
| G3 | NIST AI Risk Management Framework 1.0 (orig) | https://www.nist.gov/itl/ai-risk-management-framework | Risk management practice | AI_GOVERNANCE | DOC |
| G4 | NIST AI 600-1 Generative AI Profile (orig) | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence | GenAI risks | AI_GOVERNANCE | DOC |
| G5 | UNESCO Recommendation on the Ethics of AI (2021) (orig) | https://www.unesco.org/ethics-ai/en/recommendation | Rights-based principles | AI_GOVERNANCE | DOC |
| G6 | Hendrycks, D., Mazeika, M. & Woodside, T. (2023). An overview of catastrophic AI risks. arXiv:2306.12001. | https://arxiv.org/abs/2306.12001 | Risk taxonomy | Long-range branches | PP |
| G7 | Dafoe, A. et al. (2020). Open problems in cooperative AI. arXiv:2012.08630. | https://arxiv.org/abs/2012.08630 | Cooperation among AI agents | AGENT_SOCIETIES, GOVERN | PP |
| G8 | Hammond, L. et al. (2025). Multi-agent risks from advanced AI. Cooperative AI Foundation Tech. Rep. #1. arXiv:2502.14143. | https://arxiv.org/abs/2502.14143 | Miscoordination, conflict, collusion | AI_GOVERNANCE multi-agent section | DOC/PP |

## H. Skill format

| ID | Source | Link | Use |
|---|---|---|---|
| H1 | Anthropic, Agent Skills overview | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | Folder + SKILL.md structure, frontmatter |
| H2 | Anthropic, Skill authoring best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | < 500-line SKILL.md, one-level references, TOCs, scripts that handle errors |
| H3 | Claude Help Center, How to create custom skills (orig) | https://support.claude.com/en/articles/12512198-how-to-create-custom-skills | Packaging and upload |
