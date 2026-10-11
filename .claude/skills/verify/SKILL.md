---
name: verify
description: Verify the AEMS documentation (aems-schema, aems-conventions, and every EGS doc that describes AEMS) against INTENT.md. Runs deterministic lints for links, example events, and known wrong claims, then drives a cold reader through a fixed question bank and grades the answers against oracle answers. Use before committing any AEMS doc change, when reviewing an AEMS PR, or when asked whether the AEMS docs are correct.
---

# Verify the AEMS docs

The product is documentation, and its user is a reader: a game developer or an agent who reads the README and glossary cold and then builds against them. Verifying means two things. The corpus passes the lints, and a fresh reader who sees only the user-facing docs answers the question bank the way `INTENT.md` does.

`INTENT.md` at the aems-schema root is the oracle. If a check and the intent disagree, fix the check or amend the intent in its own change. Never loosen a check to make a doc pass.

## Layout

The check reads sibling clones under one parent directory (`$EGS`, the directory that holds `aems-schema`): `aems-schema`, `aems-conventions`, `.github`, `runs-spec`, `runs-library`, `maps-notation`, `wocs-protocol`. It checks whatever branch each clone has checked out, so check out the branches under review first. `.github` changes may be stacked on an open PR branch; check that branch, not `main`.

## Launch

Nothing to start. Each check reads files and exits.

## Doctor

```bash
.claude/skills/verify/scripts/doctor.sh
```

It prints each clone's branch, how far it is behind `origin/main`, and its dirty-file count, and exits 1 if a clone is missing. Run it first. A clone on the wrong branch makes every later result meaningless.

## Drive

Run from the aems-schema root. Put evidence in `$EGS/.aems-verify/<UTC timestamp>/`, outside every repository.

1. Lints. `check.py` is deterministic and exits 1 on any finding.

   ```bash
   RUN="$(cd ..; pwd)/.aems-verify/$(date -u +%Y%m%dT%H%M%SZ)"; mkdir -p "$RUN"
   .claude/skills/verify/scripts/check.py --json "$RUN/lint.json" | tee "$RUN/lint.txt"
   ```

   It checks Markdown links and `#anchors` across the clones, unclosed code fences, every example event (a `d` tag, the parent reference its layer requires, no grouping tags on an Entity, no Asset-to-Entity edge, a named signer, no literal kind numbers, and a placeholder kind written exactly `<AEMS Layer kind>` so the other checks can read it), and the regex rules in `rules.json`. Each rule names the `INTENT.md` requirement it enforces. `accepted.json` lists findings held outside this corpus's scope, each with its reason, and the run prints their count. `--only rule-a,rule-b` narrows the output.

2. Cold reader. Spawn a fresh subagent with no prior context and give it the prompt this prints:

   ```bash
   .claude/skills/verify/scripts/reader-prompt.py "$RUN/answers.json"
   ```

   Add `--feature <name>` to ask only one feature's questions. The reader sees only the user-facing docs, never `INTENT.md` or the ADRs, because a reader who needs the ADRs to get the right answer shows that the README is wrong.

3. Judge. Spawn a second fresh subagent, on a different model from the reader when one is available, with:

   ```bash
   .claude/skills/verify/scripts/judge-prompt.py "$RUN/answers.json" "$RUN/verdicts.json"
   ```

   Read `verdicts.json` yourself and spot-check two FAIL reasons and two PASS reasons against the cited doc lines. A judge can be wrong.

## Evidence

A proof is `lint.txt` with `0 findings` plus `verdicts.json` with every question PASS, both from the same checkout. Record the commit SHA of each clone, which `doctor.sh` output gives, next to them in `$RUN/doctor.txt`. When you fix docs, keep the baseline run from before the change and the run after it, so the result reads as old against new.

A reader PASS shows the documents can be read correctly. It does not show they cannot be misread. Report it that way.

## Cleanup

Nothing runs in the background. Delete scratch only. Keep `$EGS/.aems-verify/` runs, since they are the evidence.

## Feature map

`features/README.md` indexes the features: what each one promises the reader, which lints and questions cover it, and its gotchas. When a doc change adds a claim the map does not cover, add a question or a rule for it in the same change.
