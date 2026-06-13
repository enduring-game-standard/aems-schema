# ADR-0003: AEMS is durable commons content, not runtime state; an Asset is not the in-game object

- **Status:** Accepted
- **Date:** 2026-06-12
- **Deciders:** Scott (+ Claude)
- **Scope:** AEMS (protocol boundary vs. RUNS/MAPS)

## Context

AEMS sits beside RUNS in EGS, and two framings invite a category error that recurs
constantly:

1. The word "asset" tempts readers to equate an **AEMS Asset** with the runtime in-game
   object a game manipulates per-frame.
2. The pipeline framing ("MAPS → AEMS → RUNS") tempts readers to describe AEMS as a
   data-feed that RUNS *imports*, or to say an AEMS layer *is* a RUNS Record / a MAPS
   noun.

Both are wrong, and both keep producing confused models that subordinate AEMS to the
other protocols.

## Decision

**AEMS is an independent protocol.** Its four layers are durable, signed,
commons-persisted *content*, touched only at lifecycle boundaries (publish/discover;
load/save). They are not runtime state.

- An **AEMS Asset is the owner-signed instance on the commons** — **not** the runtime
  object RUNS manipulates during a tick. *AEMS is the shelf; RUNS is the board.*
- No AEMS layer **is** a RUNS Record or a MAPS noun. AEMS is **not** "imported into" RUNS
  or MAPS.
- Any cross-protocol interlock is an **optional seam**, not a dependency, and is stated
  only as the [EGS correspondence map] states it (build-time and load/save touchpoints).

## Consequences

- Describing AEMS as "RUNS's asset/data layer" is a category error and must be avoided.
- AEMS can be published, owned, and persisted with no RUNS or MAPS present anywhere.
- This is the AEMS-local restatement of the corpus-wide independence principle; the
  correspondence map remains the owner of cross-protocol relationships.

[EGS correspondence map]: https://github.com/enduring-game-standard/.github/blob/main/profile/CORRESPONDENCE.md
