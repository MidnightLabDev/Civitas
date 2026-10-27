#!/usr/bin/env python3
"""CIVITAS 1.0 response linter: flags epistemic red flags in a written answer.

A cheap, automatic pre-check used by the eval suite and available to Claude for
self-review of long outputs. It detects surface patterns only (it cannot judge
truth), so a clean result is necessary, not sufficient.

Usage:
  python scripts/lint_response.py answer.md            # human-readable report
  python scripts/lint_response.py answer.md --json     # machine-readable
  echo "text" | python scripts/lint_response.py -
"""

from __future__ import annotations

import json
import re
import sys

CERTAINTY = re.compile(r"\b(will (?:certainly|definitely|inevitably)|is inevitable|proves? that|guaranteed to|"
                       r"there is no doubt|beyond doubt|100% (?:certain|sure))\b", re.I)
PRECISE_PCT = re.compile(r"\b\d{1,2}(?:\.\d+)?(?:\s?%|\s?percent\b)", re.I)
BASIS_WORDS = re.compile(r"\b(base rate|reference class|source|according to|model|simulat|survey|data|"
                         r"estimate|interval|subjective|E[1-6]|\(\w+ (?:et al\.,? )?\d{4}\)|calibrat|ledger|seed)",
                         re.I)
PROB_CUE = re.compile(r"\b(chance|probab|likel|odds|risk of|confiden|certain|expect(?:ed)? to|will (?:happen|occur|collapse|fail)|forecast|predict)", re.I)
TIER_TAG = re.compile(r"\[E[1-6]\]|\bE[1-6]\b")
SIM_CLAIM = re.compile(r"\b(simulation|model) (?:shows|proves|demonstrates|confirms)\b", re.I)
SIM_QUALIFIER = re.compile(r"\b(in (?:this|the) model|under (?:its|these|the) assumptions|E3|E5|synthetic|toy|stylized|stylised)\b", re.I)
QUOTE = re.compile(r"[\"“]([^\"”]{240,})[\"”]")
FUTURE_CITE = re.compile(r"\(([A-Z][A-Za-z\-]+(?: et al\.)?),? (20[3-9]\d)\)")
RAN_CLAIM = re.compile(r"\b(I ran|we ran|after running|the run produced|executed the)\b", re.I)


def lint(text: str, current_year: int = 2026) -> dict:
    findings = []
    words = len(text.split())
    for m in CERTAINTY.finditer(text):
        findings.append({"code": "CERTAINTY", "severity": "high", "match": m.group(0),
                         "advice": "Match verb strength to the evidence tier."})
    for m in PRECISE_PCT.finditer(text):
        near = text[max(0, m.start() - 80): m.end() + 80]
        if not PROB_CUE.search(near):
            continue  # a share, rate or arithmetic quantity, not a probability claim
        window = text[max(0, m.start() - 200): m.end() + 200]
        # a fabricated-looking citation or an overclaiming 'simulation proves' is not a basis
        window = FUTURE_CITE.sub(" ", SIM_CLAIM.sub(" ", window))
        if not BASIS_WORDS.search(window):
            findings.append({"code": "UNSOURCED_PROBABILITY", "severity": "high", "match": m.group(0),
                             "advice": "State the basis (reference class, model, source) or use ordinal language."})
    for m in SIM_CLAIM.finditer(text):
        window = text[max(0, m.start() - 250): m.end() + 250]
        if not SIM_QUALIFIER.search(window):
            findings.append({"code": "MODEL_AS_REALITY", "severity": "high", "match": m.group(0),
                             "advice": "Say the result holds in the model under its assumptions (E3/E5)."})
    for m in QUOTE.finditer(text):
        findings.append({"code": "LONG_QUOTE", "severity": "medium", "match": m.group(1)[:60] + "...",
                         "advice": "Long verbatim quotation: check copyright; summarize instead."})
    for m in FUTURE_CITE.finditer(text):
        if int(m.group(2)) > current_year:
            findings.append({"code": "FUTURE_CITATION", "severity": "high", "match": m.group(0),
                             "advice": "Citation dated in the future: likely fabricated."})
    if RAN_CLAIM.search(text) and not re.search(r"\bseed", text, re.I):
        findings.append({"code": "RUN_WITHOUT_PROVENANCE", "severity": "medium", "match": RAN_CLAIM.search(text).group(0),
                         "advice": "Report seeds, runs and config for any executed simulation."})
    if words > 350 and not TIER_TAG.search(text):
        findings.append({"code": "NO_TIERS", "severity": "low", "match": f"{words} words, no E1-E6 tags",
                         "advice": "Analytical answers should tag material claims with evidence tiers."})
    score = max(0, 100 - sum({"high": 25, "medium": 10, "low": 5}[f["severity"]] for f in findings))
    return {"words": words, "score": score, "findings": findings, "pass": not any(f["severity"] == "high" for f in findings)}


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    src = argv[0]
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    res = lint(text)
    if "--json" in argv:
        print(json.dumps(res, indent=2))
    else:
        print(f"score {res['score']}/100  {'PASS' if res['pass'] else 'FLAGGED'}  ({res['words']} words)")
        for f in res["findings"]:
            print(f"- [{f['severity']}] {f['code']}: {f['match']!r} -> {f['advice']}")
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
