# Entity naming conventions

## Sub-features

- An Entity names object-identity: a noun for a thing, free of medium and mechanic.
- Ownerless and authored concepts are both Entities. Authorship is carried by the signature.
- Classification goes on Manifestation tags.
- Nothing is canonical, and there is no standard namespace.
- The playing-cards conventions.

## How to get to it (user POV)

`aems-conventions/README.md`, `aems-conventions/entity-abstraction.md`, and `aems-conventions/playing-cards.md`.

## Driving it with check.py and the reader

`check.py --only entity-ownerless-only,entity-is-role,std-namespace,canonical-artifact,retired-rubric,avoided-term,entity-grouping-tag`, then `reader-prompt.py <out> --feature naming`.

## Gotchas

- "IP-agnostic" in a sentence about misrepresentation is fine. The rule allows lines that say "misrepresentation" or "ownerless".
- ADRs are records of a decision and are excluded from most content rules. Correct a wrong fact in an ADR with an amendment section, not by rewriting the decision.
