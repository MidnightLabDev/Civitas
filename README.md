# CIVITAS 1.0

An Asimov-inspired psychohistory and civilization intelligence plugin for Claude. CIVITAS turns the idea of psychohistory into a defensible practice: understand a complex human or artificial system, map its mechanisms, explore its possible futures, test interventions, and say honestly how much is known. It is not a claim that history can be predicted.

## What it does

- **Six evidence tiers (E1 established to E6 speculative)** tag every claim, so you can see what rests on data and what is conjecture.
- **The CIVITAS Loop**, an eight-stage reasoning engine: Frame, Map, Mechanize, Ground, Branch, Stress, Act, Update.
- **Twelve modes**, including civilizational analysis, AI governance and agent-society design, strategic foresight, cliodynamics, worldbuilding and game economies.
- **civlab**, a standard-library-only Python lab: agent-based cooperation and legitimacy, AI agent constitutions, structural-demographic stress, polity rise and fragmentation, diffusion, failure cascades, knowledge loss, early-warning signals, causal loop diagrams, forecasting and sensitivity analysis.
- A cross-disciplinary reference library with a verified source list.

## Example prompts

- "Model how an online community's moderation rules affect cooperation over five years, and tell me which assumptions matter most."
- "Stress-test this proposed AI agent constitution for capture and collusion."
- "Use structural-demographic theory to compare two historical empires' paths to crisis."
- "Design a resilient economy for my fictional desert civilization."
- "Turn the claim 'remote work will hollow out mid-size cities' into a testable model."

## Install

Add CIVITAS from the Claude directory. In Claude Code you can also load it locally:

```
claude --plugin-dir ./civitas-plugin
```

The skill triggers automatically on relevant questions.

## Requirements and data handling

- The simulators need only Python 3 (standard library). No network access, API keys or external services.
- CIVITAS reads no personal data and sends nothing outside your Claude session. It has no MCP connectors.

## Troubleshooting

- **The skill doesn't trigger:** mention CIVITAS by name, or ask for a civilizational, foresight or simulation analysis.
- **A simulator fails:** check that `python3` is available; the scripts have no other dependencies.

## Version

1.0. The version number is intentionally held at 1.0.

## License

MIT. See LICENSE.
