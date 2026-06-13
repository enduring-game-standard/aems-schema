# ADR-0009: A protocol of claims, never facts — the digital pickup game

- **Status:** Accepted
- **Date:** 2026-06-12
- **Deciders:** Scott (+ Claude)
- **Scope:** AEMS (the claims model generalized to all four layers; the paradigm it serves)

## Context

ADR-0007 resolved the Entity as a claim (a naming, not the concept) and ADR-0008
resolved the Asset as a claim (auditable possession, never adjudicated). The open
question was whether this generalizes to all four layers.

The grilling that got here kept framing the model's consequences as *concerns* —
self-minted Assets, cheat-by-State-claim, "the claims model may read as weakness."
That framing imports the **current** video game item model (server authority,
mandatory anti-cheat, enforced scarcity — every game a pro league under federation
oversight) onto a protocol whose reference implementation is the **physical** model of
board game and sports equipment, with thousands of years of precedent behind it (book
ch. 2: the Royal Game of Ur, chess, soccer — "endurance is a consequence of openness").

## Decision

**Every AEMS event is someone's signed claim** — a naming (Entity), an interpretation
(Manifestation), a possession (Asset), a condition (State). **The protocol guarantees
claims are eternal, attributable, and auditable; it never guarantees they are true.**
Truth lives where it lives in physical reality: in the judgment of whoever is asked to
act on the claim.

**And this is desirable, not a hedge.** It is what allows people to play the digital
equivalent of a pickup game. Nobody at the park adjudicates whose ball is legitimate;
the players present decide what equipment they accept, and that has sufficed for every
enduring game in human history. Strict equipment standards exist — pro leagues, FIFA
match balls — and they are **conventions**, voluntarily adopted per context. The
taped-up ball is still soccer.

## Consequences

- "Validation logic excluded" stops being a policy row and becomes a **theorem** of the
  claims model.
- Anti-cheat, reputation, witnessing, blessed-provenance curation: ecosystem services
  for contexts that want pro-league strictness (coordinated via WOCS, per the tier
  model in ADR-0004). The pickup game needs none of them and must never pay for them.
- The README states the claims model as a positive capability — the thing that makes
  digital pickup play possible — never defensively, never with a mitigation attached.
- Design-instinct check for all future work: when a question triggers the current
  item-model's anxieties (duplication, forgery, cheating, balance), consult the
  physical precedent first. "Socially, and it has been fine for millennia" is a valid
  and usually correct answer.
