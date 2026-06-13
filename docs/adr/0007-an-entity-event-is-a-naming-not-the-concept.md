# ADR-0007: An Entity event is a naming, not the concept; convergence is social, never structural

- **Status:** Accepted. Founding assumption widened by the 2026-06-13 Amendment below —
  a concept may have an author-of-record; one Entity species along a commons↔authored
  convergence gradient.
- **Date:** 2026-06-12
- **Deciders:** Scott (+ Claude)
- **Scope:** AEMS (what the Entity layer *is*; rejection of the registry model)

## Context

Two of ADR-0005's impositions collide at the Entity layer. Imposition 1: the concept is
no one's — the Knight has no author-of-record; it emerged and persists by collective
use. Imposition 5: every event is signed, and signatures establish origin forever. So
someone signs "health-potion" first, provably — over a concept that belongs to no one.
Physical reality, the reference implementation, has no signed concepts at all; this is
the one place the port needs its own answer rather than a translation. The README
asserted both halves ("belongs to no one" / "any user can publish") without resolving
them.

## Decision

**An Entity event is someone's signed *naming* of a concept — a dictionary entry, not
the word.** The word belongs to no one precisely because anyone can write an entry,
entries are rivalrous, and the language converges by *use* — by which naming the
world's Manifestations actually reference — never by registry.

- The signature authenticates the **naming** (who described this concept, when) and
  grants nothing over the **named** — PWNS's copying-vs-claiming distinction, applied
  at the concept level.
- "No registry, no gatekeeping" is a **necessity, not a policy**: gatekeeping namings
  would be owning the language.
- Parameterized replacement is licensed: an author refines *their own entry*; they are
  not mutating the concept.
- "Maintained by communities, not studios" becomes precise: the community maintains the
  **convergence** — which naming gets referenced — not the events.

## Consequences

- Rival namings of one concept are **structurally normal**, not a failure mode.
  Fragmentation is resolved socially (convergence by reference), never structurally.
- AEMS promises "any concept, nameable by anyone, converging by use" — and can never
  promise "one concept, one Entity." Anything that needs a canonical naming (blessed
  lists, `std:` curation) is conventions/ecosystem work over the commons, downstream of
  this fact.
- Recognition across games rides on the *reference*, so a receiving game recognizes
  whichever namings it chooses to understand — recognition is voluntary, like every
  act in AEMS.

## Amendment (2026-06-13): one Entity species; commons↔authored is a convergence gradient

This ADR reasoned entirely from the Knight — a concept with **no author-of-record** — and
let "the concept belongs to no one" read as a property of *every* Entity. The founding AEMS
case breaks that reading: Link, Cloud, the Master Sword, and the Buster Sword are each *one
identity* recurring across many games (the Entity — "the same every time"), interpreted
differently per game (its Manifestations — "different every time"), and each has an author of
record (Nintendo, Square). They are owned concepts, and they are Entities.

The fix is **not** a second species of Entity. Splitting "commons-identity" from
"authored-identity" structurally would weld a present-day artifact of IP law into a substrate
meant to outlive it — the move
[PWNS](https://github.com/enduring-game-standard/.github/blob/main/profile/PWNS.md) exists to
refuse ("the math replaces the institution").

**There is one Entity: a signed naming.** "Commons" and "authored" are the two ends of a
single **convergence-concentration gradient**, and the gradient is a fact about the *concept
in the world*, not a flag on the data:

- **Ownerless concepts** (`sword`, `potion`, `hero`) have no author of record; signed namings
  are many and interchangeable; convergence is **diffuse**, decided by use.
- **Authored concepts** (`link`, `cloud`, `master-sword`) have an author of record;
  convergence **concentrates** on the owner's signature — not by a protocol rule, but because
  the world recognizes the author and the signature-plus-timestamp *prove the claim*.

The protocol behaves **identically** across the whole gradient: it records signed namings,
attributes them, and lets receivers honor whichever provenance they accept. Rival namings
remain structurally normal; recognition remains voluntary (both decided above). Authorship is
therefore carried by **provenance** and lives in the social layer, so a concept may
**migrate** along the gradient over time — Sherlock Holmes, Dracula, and Robin Hood drifted
from authored toward folklore, and `link` will too when its copyright lapses — with **zero
structural surgery**, because the Entity was only ever a signed naming.

Net effect on the decision above: its mechanism stands unchanged; only its founding
*assumption* — that every concept is ownerless — is widened to "a concept may or may not have
an author of record." The CONTEXT definition's "the IP-free idea of a thing… belongs to no
one" describes the **ownerless end** of the gradient, not the definition of an Entity.
