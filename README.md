# CIVITAS 1.0

An Asimov-inspired psychohistory and civilization intelligence skill for Claude. CIVITAS turns the idea of psychohistory into a defensible practice: understand a complex human or artificial system, map its mechanisms, explore its possible futures, test interventions, and say honestly how much is known. It is not a claim that history can be predicted.

## What it does

- **Six evidence tiers (E1 established to E6 speculative)** tag every claim, so you can see what rests on data and what is conjecture.
- **The CIVITAS Loop**, an eight-stage reasoning engine: Frame, Map, Mechanize, Ground, Branch, Stress, Act, Update.
- **Twelve modes**, including civilizational analysis, AI governance and agent-society design, strategic foresight, cliodynamics, worldbuilding and game economies.
- **civlab**, a standard-library-only Python lab: agent-based cooperation and legitimacy, AI agent constitutions, structural-demographic stress, polity rise and fragmentation, diffusion, failure cascades, knowledge loss, early-warning signals, causal loop diagrams, forecasting and sensitivity analysis.
- A cross-disciplinary reference library with a verified source list.

## Install CIVITAS as a skill in Claude

The skill itself is the `skills/civitas/` folder in this repository (it holds `SKILL.md`, `references/`, `scripts/` and `examples/`).

### 1. Get the skill as a ZIP

1. On this repository's GitHub page, click **Code**, then **Download ZIP**, and unzip it.
2. Open the unzipped folder and go into `skills/`.
3. Compress the `civitas` folder itself into `civitas.zip`. The ZIP must contain the `civitas` folder at its top level, with `SKILL.md` inside it:

```
civitas.zip
└── civitas/
    ├── SKILL.md
    ├── references/
    ├── scripts/
    └── examples/
```

A ZIP with `SKILL.md` sitting directly at its root is not recognized as a skill.

### 2. Upload it to Claude (claude.ai or the Claude desktop app)

1. Make sure code execution is turned on: **Settings**, then **Capabilities**, then **Code execution and file creation**. CIVITAS runs its simulators with it.
2. Go to **Customize**, then **Skills**.
3. Click **+**, then **+ Create skill**, then **Upload a skill**.
4. Select `civitas.zip`.
5. Make sure the toggle next to CIVITAS is on.
6. Open a new conversation and ask a question CIVITAS covers. Claude loads the skill automatically when your request matches.

Custom skill upload is available on Claude's Free, Pro and Max plans; on Team and Enterprise an Owner may need to enable skills for the organization.

### Claude Code

Copy the `skills/civitas` folder into `~/.claude/skills/` (available in all your projects) or into a project's `.claude/skills/` folder (shared with everyone on that project):

```
git clone https://github.com/MidnightLabDev/Civitas
cp -r Civitas/skills/civitas ~/.claude/skills/
```

Start a new session and run `/skills` to confirm CIVITAS is listed.

## Example prompts

- "Model how an online community's moderation rules affect cooperation over five years, and tell me which assumptions matter most."
- "Stress-test this proposed AI agent constitution for capture and collusion."
- "Use structural-demographic theory to compare two historical empires' paths to crisis."
- "Design a resilient economy for my fictional desert civilization."
- "Turn the claim 'remote work will hollow out mid-size cities' into a testable model."

## Requirements and data handling

- The simulators need only Python 3 (standard library). No network access, API keys or external services.
- CIVITAS reads no personal data and sends nothing outside your Claude session. It has no MCP connectors.

## Troubleshooting

- **The upload is rejected:** check that the ZIP holds the `civitas` folder, not the files inside it, and that `SKILL.md` is in that folder.
- **The skill doesn't trigger:** check that its toggle is on, then mention CIVITAS by name or ask for a civilizational, foresight or simulation analysis.
- **A simulator fails:** check that code execution is turned on (claude.ai) or that `python3` is available (Claude Code).

## License

MIT. See LICENSE.
