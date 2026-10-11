#!/usr/bin/env python3
"""Print the cold-reader prompt. Usage: reader-prompt.py OUT_ANSWERS.json [--feature F]"""
import json, sys
from pathlib import Path
SKILL = Path(__file__).resolve().parent.parent
EGS = SKILL.parent.parent.parent.parent
DOCS = ["aems-schema/README.md", "aems-schema/CONTEXT.md", "aems-conventions/README.md",
        "aems-conventions/CONTEXT.md", "aems-conventions/entity-abstraction.md",
        "aems-conventions/playing-cards.md", ".github/profile/README.md", ".github/profile/FAQ.md"]
out = sys.argv[1]
feat = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--feature" else None
qs = [q for q in json.loads((SKILL / "reader-questions.json").read_text()) if not feat or q["feature"] == feat]
print(f"""You are a game developer reading the AEMS documentation for the first time. Read ONLY these files, in order and in full (reading, not grepping), and nothing else (no ADRs, no INTENT.md, no git history, no web):
{chr(10).join('- ' + str(EGS / d) for d in DOCS)}

Answer each question from what these documents say. For each answer give: the answer in 1-3 sentences, the file:line you relied on, and `conflict` listing any lines in the documents that say something different (empty if none). If the documents do not answer, say "not answered".

Write a JSON list of {{"id","answer","source","conflict"}} to {out}. Do not edit any other file.

Questions:
{chr(10).join(q['id'] + ': ' + q['q'] for q in qs)}""")
