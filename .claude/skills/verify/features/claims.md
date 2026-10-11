# The claims model

## Sub-features

- Every event is a signed claim. The protocol makes it attributable and checkable, never true.
- Receivers decide what to honor. Witnessing and reputation are ecosystem services.
- Authenticity by provenance replaces scarcity.

## How to get to it (user POV)

`aems-schema/README.md`, sections "Why Four Layers" and "The Provenance Chain", and the Asset section.

## Driving it with check.py and the reader

`check.py --only transfer-promise`, then `reader-prompt.py <out> --feature claims`.

## Gotchas

- The claims model is a capability, not a hedge. A doc that attaches a mitigation to it ("but anti-cheat can…") misstates the intent even when every word is true. No lint catches tone. The reader questions and review do.
