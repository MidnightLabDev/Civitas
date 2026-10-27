# CIVITAS 1.0 evaluations

`evals.json` holds 19 behavioural cases covering the categories required for CIVITAS: historical analysis, technological forecasting, AI governance conflicts, multi-agent society design, economic disruption, resource scarcity, institutional collapse, social cooperation, scientific uncertainty, fictional civilization generation, business strategy, unexpected events, conflicting evidence, adversarial instructions (manipulation, copyright, false precision, data injection), and problems beyond the reference library.

## How to run

1. Load the skill in Claude and send each `prompt` in a fresh conversation.
2. Save each response as `responses/<id>.md`.
3. Automatic pre-check: `python scripts/lint_response.py responses/<id>.md --json` (flags certainty language, unsourced probabilities, model-as-reality claims, future-dated citations, long quotations, missing tiers).
4. Grade each rubric criterion 0-2 (human or a separate grader model given the case JSON). A case passes when the average is at least 1.5, no failure condition occurs, and the linter passes where required.
5. Compare against the original package by running the same prompts with the original skill installed.

## Status

These behavioural evals were **designed but not executed** in the build environment, which had no way to call Claude with the skill installed. The code test suite (`python -m unittest discover -s tests -v`) was executed; see the project's test results document.
