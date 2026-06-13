# ADR-0001: The AEMS acronym order is phonetic, not structural

- **Status:** Accepted
- **Date:** 2026-06-12
- **Deciders:** Scott (+ Claude)
- **Scope:** AEMS (naming vs. layer structure)

## Context

AEMS expands to **A**sset-**E**ntity-**M**anifestation-**S**tate. Read as an ordered
list, that letter sequence invites the inference that it encodes the layers' structural
order — their dependency chain, build order, or some narrative/phenomenological
progression. It does not. The four letters are arranged to spell the phonetic game verb
"aims" per meta ADR-0008 (acronyms are phonetic game verbs; expansions are mnemonic, not
load-bearing). The ordering exists to make the word, nothing more.

This keeps snagging readers — humans and AI assistants alike — who try to reconcile the
acronym order with the layers' actual relationships, find they don't match, and treat the
mismatch as a defect to fix or a hidden meaning to decode. Each attempt burns effort and
produces a back-formed rationalization (it's "build order," it's "the order you hold
things," etc.) that is simply not true.

## Decision

**The AEMS acronym order carries no structural meaning.** It is a phonetic artifact
("aims"), full stop.

The relationships and ordering among the four layers are defined **solely by the schema** —
which layer references which — and never inferred from the sequence of letters in the name.
The two orderings are independent on purpose.

Therefore:

- Do **not** reorder the layers to match the acronym.
- Do **not** reorder the acronym to match the layers.
- Do **not** invent a justification (dependency order, build order, phenomenological order,
  narrative order) that makes the letter sequence "mean" something. It means "aims."

When the layers are presented in sequence, use the structural order the schema defines, and
treat "AEMS" purely as the name.

## Consequences

- The recurring "but the letters are in the wrong order" churn is closed; it is not a bug.
- Downstream of meta ADR-0008; this is the AEMS-local application of that family rule.
- Documentation introduces the layers in their schema-defined order and never apologizes
  for, or rationalizes, the acronym order.
