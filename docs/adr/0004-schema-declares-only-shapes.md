# ADR-0004: The schema declares only shapes — AEMS adopts the protocol/conventions/ecosystem tiers

- **Status:** Accepted (provisional — reasoned, not yet implemented; "we'll see if it breaks")
- **Date:** 2026-06-12
- **Deciders:** Scott (+ Claude)
- **Scope:** AEMS (what this repo normatively defines; tier boundaries)

## Context

The README carried content from three different tiers as if all of it were schema:
kernel structure (four event kinds, parent references), interop recommendations
(grouping-tag vocabularies, a `["property", key, value, type]` shape, an `acquired`
timestamp, a `prev_owner` transfer pattern, "Entities carry no grouping tags"), and
worked-artifact detail. Each recommendation invited the same argument: is this rule
right? — when the prior question was whether the schema should be ruling on it at all.

RUNS resolved the identical tension (its ADR-0014, private meta repo): a **Protocol**
kernel that is mandatory and declares only *shapes of data for functionality*; a
**Conventions** tier that is optional-but-recommended — the interop palette; an
**Ecosystem** tier of community artifacts published to the commons. Compliance is the
kernel, nothing more.

## Decision

**AEMS adopts the same three tiers, and this repo is the kernel.**

- **Protocol (this repo):** the four event kinds, their addressable/replacement
  semantics, and the provenance chain — a Manifestation references its Entity, an Asset
  references its Manifestation, a State references its Asset. **Compliance = exactly
  this, nothing more.**
- **Conventions (`aems-conventions`):** everything about what events *carry* — tag
  vocabularies, property shapes, naming and namespacing, transfer patterns, Entity
  content recommendations. Optional-but-recommended.
- **Ecosystem (the commons):** published AEMS events themselves (e.g. a card deck).
  Judged against conventions, not against the schema.

## Consequences

- Every content rule in the README either restates a provenance edge (stays) or exits
  to conventions. The schema is **silent** on what any layer carries beyond the chain;
  the silence is deliberate, not an omission (cf. RUNS ADR-0015's posture).
- Debates about event contents — e.g. *may an Entity carry tags?* — are conventions
  questions, out of this repo's scope by construction.
- The provenance edges are kernel MUSTs. A conventions document cannot own a
  "mandatory" rule; where `aems-conventions` currently claims the mandatory `entity`
  tag, that rule is restated as the schema's, not invented as a convention.
- Published artifacts (the french-52 deck) are ecosystem tier: their correctness is a
  conventions-conformance question and never a constraint on the schema.
