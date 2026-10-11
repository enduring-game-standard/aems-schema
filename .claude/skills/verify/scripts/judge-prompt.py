#!/usr/bin/env python3
"""Print the judge prompt. Usage: judge-prompt.py ANSWERS.json OUT_VERDICTS.json"""
import json, sys
from pathlib import Path
SKILL = Path(__file__).resolve().parent.parent
answers, out = sys.argv[1], sys.argv[2]
qs = json.loads((SKILL / "reader-questions.json").read_text())
print(f"""You grade a cold reader's answers about AEMS against oracle answers. Read {answers}. For each question id, compare the reader's answer with the oracle below.

PASS: the answer agrees with the oracle on every point the oracle makes, and its `conflict` field is empty.
FAIL: the answer contradicts the oracle, misses a point the oracle requires, says "not answered", or the reader found conflicting lines. A reader who answers correctly but reports a conflict is a FAIL: the documents disagree with each other.

Write a JSON list of {{"id","verdict","reason"}} to {out}, the reason quoting the reader's words. Then print one line per id: `<id> PASS|FAIL <reason>`. Do not edit any other file.

Oracle:
{chr(10).join(q['id'] + ': ' + q['oracle'] for q in qs)}""")
