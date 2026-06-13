# ADR-0002: An Asset references its Manifestation, not the Entity directly

- **Status:** Accepted
- **Date:** 2026-06-12
- **Deciders:** Scott (+ Claude)
- **Scope:** AEMS (layer reference graph)

## Context

The four AEMS layers form a single instantiation chain — **Entity → Manifestation →
Asset → State** — where each layer is a concrete instance of the one above it and
references its parent by provenance.

A natural-looking alternative, suggested by the founding philosophy in the *Enduring
Games* book (ch. 10), would have the **Asset reference the Entity directly**: the book
frames the Asset as "the artifact you hold in your hand… the Entity it represents," a
thing that persists across games precisely because it is bound to the timeless concept,
not to any one game. Read literally, that implies `Asset → Entity`, with the
Manifestation demoted to an ephemeral per-game expression.

This is a real fork, and the book's framing makes the rejected branch the *intuitive*
one — which is exactly why it needs recording.

## Decision

An **Asset references its Manifestation**, never the Entity directly.

An Asset is a single owned instance of one specific Manifestation (one of your twelve
Estus Flasks — not "some health potion"). The Entity is reached **transitively**, by
reading *up* the chain: `Asset → Manifestation → Entity`. There is no direct
`Asset → Entity` edge.

## Consequences

- **Provenance integrity.** An Asset always knows exactly which game-version it
  instantiates. State (charges, durability, wear) is only meaningful against a specific
  Manifestation's rules, so the Asset must anchor at the Manifestation, not the abstract
  idea.
- **Portability is preserved, not lost.** A future game follows the Manifestation's
  permanent Entity link, recognizes the idea, and offers its own equivalent. Recognition
  happens at the **Entity**, reached via the Manifestation — not by re-anchoring the
  Asset.
- **The book's metaphor ≠ the schema.** "The artifact in your hand represents the Entity"
  is philosophy. The schema realizes persistence through signing + commons storage +
  up-chain provenance, not through a direct Asset→Entity reference. (See the flagged
  ambiguity in `CONTEXT.md`.)
- Reversing this would collapse the Manifestation layer's reason to exist.
