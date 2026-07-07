# ADR-0005: AEMS imposes physical reality; authenticity by provenance, not scarcity

- **Status:** Accepted
- **Date:** 2026-06-12
- **Deciders:** Scott (+ Claude)
- **Scope:** AEMS (the philosophy that defines the protocol; foundation for the README)

## Context

The README framed AEMS by its benefits — preservation ("game entities die with the
studios that create them"), portability, community ownership — leaving the four layers
to read as a storage format justified by outcomes. Grilling "what *is* AEMS" surfaced
candidate identities — a preservation scheme, a recognition language, an ontology of
game things — and all three are true, and none is the point.

The point is in the book (ch. 10): every physical game object has always lived in two
modes — artifact on the shelf, manifestation in the magic circle — and digital games
"collapsed these two modes into one opaque object that dies with the server." A chess
Knight survives its manufacturer's bankruptcy *for free*. Nobody designed that; physics
provides it, and digital architecture destroyed it.

## Decision

**AEMS imposes, in digital space, what physical reality gives game objects for free.**
Physical reality is the reference implementation. Five impositions:

1. **The concept outlives every object and every maker.** The Knight has survived
   chaturanga and every manufacturer that ever carved one. → **Entity**
2. **Anyone may interpret the concept; no interpretation captures it.** Staunton carves
   one Knight, a themed set another; the concept stays no one's. → **Manifestation**
3. **Possession is physical.** The figure on the shelf belongs to whoever holds it; no
   maker can reach into your home and remove it. → **Asset**
4. **Condition inheres in the object.** The chip on the Knight's ear travels with that
   Knight, across every game and after every game. → **State**
5. **Origin inheres in the object — authenticity by eternal provenance.** A forged
   Vermeer is exposed by chain of custody, not by a lock on the frame. The chain of
   signed parent references imposes this digitally: copying flows; *claiming* is
   refuted by the math. → **the provenance chain itself** ([PWNS] extends this with
   covenants and an author-controlled openness dial over sealed content.)

The fifth is stated as a positive that **replaces** uncopyability, not a refusal of it.
Imposing scarcity digitally requires monetary-grade consensus — the blockchain category
error: importing all the costs of solving double-spend when a game object is "not a
unit of currency to be spent but an identity to be recognized, signed, and persisted."
Authenticity does the work scarcity was assumed for.

Preservation, cross-game recognition, and the four-layer ontology are **side effects**
of the impositions, not the purpose.

## Consequences

- The README becomes derivational rather than promotional: the collapse (problem) → the
  impositions (premise) → one layer per imposition → the chain as the fifth → and
  exclusions as failures of the membership test below.
- **Membership test:** a feature belongs in AEMS only if physical reality bundles it
  into the game object itself, for free. Marketplaces fail (commerce is a social
  arrangement around objects), validation fails (rules live in the game, not the
  piece), rendering fails (how the Knight looks is the carver's business).
- "Why no anti-duplication?" has a findable answer: AEMS imposes authenticity, not
  scarcity — deliberately.

[PWNS]: https://github.com/enduring-game-standard/.github/blob/main/profile/PWNS.md
