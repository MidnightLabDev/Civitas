#!/usr/bin/env python3
"""CIVITAS 1.0 package validator (structure, metadata, links, code). Stdlib only.

Checks what can be checked offline: required files, SKILL.md frontmatter rules
from Anthropic's Agent Skills documentation (name <= 64 chars, lowercase
letters/digits/hyphens, no reserved words, description <= 1024 chars, no XML
tags), SKILL.md under 500 lines, every reference file linked directly from
SKILL.md, tables of contents in reference files over 100 lines, local links
resolve, version string 1.0 present and no other CIVITAS version claimed,
Python files compile, and example configs load. It cannot judge how Claude
responds or whether the science is right.
"""

import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "scripts/civitas.py", "scripts/civitas_sim.py", "scripts/validate_skill.py", "scripts/lint_response.py",
    "scripts/civlab/__init__.py", "scripts/civlab/core.py", "scripts/civlab/society.py",
    "scripts/civlab/aisociety.py", "scripts/civlab/sdt.py", "scripts/civlab/polity.py",
    "scripts/civlab/diffusion.py", "scripts/civlab/cascade.py", "scripts/civlab/knowledge.py",
    "scripts/civlab/ews.py", "scripts/civlab/cld.py", "scripts/civlab/forecast.py",
    "scripts/civlab/sensitivity.py",
    "tests/test_civitas.py", "tests/test_civlab.py", "tests/test_lint.py",
    "evals/evals.json", "evals/README.md",
    "examples/civilization_scenario.json", "examples/society_commons.json",
    "examples/ai_society_capture.json", "examples/sdt_agrarian.json", "examples/polity_world.json",
    "examples/cld_platform.json", "examples/ach_example.json",
]
REFERENCES = [
    "ENGINE", "MODE_GUIDES", "ASIMOV_ATLAS", "PSYCHOHISTORY", "CLIODYNAMICS_HISTORY", "SYSTEMS_SCIENCE",
    "SOCIAL_INSTITUTIONS", "ECONOMY_ECOLOGY", "QUANT_MODELS", "FORECASTING", "EVIDENCE_VALIDATION",
    "CRITICAL_REVIEW", "AI_GOVERNANCE", "AGENT_SOCIETIES", "SIMULATORS", "SIMULATION_ENGINEERING",
    "TECH_ARCHITECTURE", "WORLD_HISTORY", "INNOVATION_PATTERNS", "LANDSCAPE", "TEMPLATES", "SCHEMAS",
    "EXAMPLES", "PROMPTS", "SOURCES",
]


def main() -> int:
    errors = []
    for name in REQUIRED + [f"references/{r}.md" for r in REFERENCES]:
        if not (ROOT / name).is_file():
            errors.append(f"Missing: {name}")
    skill_path = ROOT / "SKILL.md"
    if not skill_path.exists():
        print("FAIL: missing SKILL.md")
        return 1
    skill = skill_path.read_text(encoding="utf-8")
    if len(skill.splitlines()) >= 500:
        errors.append("SKILL.md must stay under 500 lines")
    m = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    if not m:
        errors.append("SKILL.md needs YAML frontmatter")
    else:
        fm = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
        name, desc = fm.get("name", ""), fm.get("description", "")
        if name != "civitas":
            errors.append("name must be 'civitas'")
        if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
            errors.append("name must be <= 64 chars of lowercase letters, digits, hyphens")
        if "anthropic" in name or "claude" in name:
            errors.append("name contains a reserved word")
        if not desc or len(desc) > 1024:
            errors.append(f"description missing or > 1024 chars ({len(desc)})")
        if re.search(r"<[^>]+>", desc):
            errors.append("description must not contain XML tags")
    if "CIVITAS 1.0" not in skill:
        errors.append("Version string 'CIVITAS 1.0' missing from SKILL.md")
    for ref in REFERENCES:
        if f"references/{ref}.md" not in skill:
            errors.append(f"SKILL.md does not link references/{ref}.md")
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if not text.strip():
            errors.append(f"Empty file: {rel}")
        if path.parent.name == "references" and len(text.splitlines()) > 100 and "## Contents" not in text:
            errors.append(f"{rel} exceeds 100 lines without a '## Contents' section")
        for bad in re.findall(r"CIVITAS (?:v)?(\d+\.\d+)", text):
            if bad != "1.0":
                errors.append(f"{rel} mentions CIVITAS version {bad}; must remain 1.0")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            tp = (path.parent / target.split("#", 1)[0]).resolve()
            if not tp.exists():
                tp = (ROOT / target.split("#", 1)[0]).resolve()
            if not tp.exists():
                errors.append(f"Broken link in {rel}: {target}")
    for py in sorted(ROOT.rglob("*.py")):
        try:
            py_compile.compile(str(py), doraise=True, cfile=str(Path("/tmp") / (py.name + "c")))
        except py_compile.PyCompileError as exc:
            errors.append(f"Python does not compile: {py.relative_to(ROOT)}: {exc.msg}")
    for js in sorted((ROOT / "examples").glob("*.json")) + [ROOT / "evals" / "evals.json"]:
        try:
            json.loads(js.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid JSON: {js.relative_to(ROOT)}: {exc}")
    if (ROOT / "README.md").exists():
        errors.append("Keep README and project docs outside the skill folder")
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    n_refs = len(REFERENCES)
    print(f"PASS: CIVITAS 1.0 package: {len(REQUIRED)} core files, {n_refs} reference files linked from SKILL.md, "
          f"frontmatter valid, links resolve, Python compiles, JSON loads")
    return 0


if __name__ == "__main__":
    sys.exit(main())
