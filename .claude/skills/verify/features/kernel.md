# The kernel

## Sub-features

- Four event kinds: Entity, Manifestation, Asset, State.
- Three parent references: a Manifestation references at least one Entity, an Asset references its Manifestation, a State references its Asset.
- Addressability: an event's address is its kind, its publisher's key, and its `d` tag.
- Kind numbers and the reference encoding are not pinned.

## How to get to it (user POV)

`aems-schema/README.md`, sections "What the Standard Defines", "The Four Layers", and "Getting Started". The glossary is `aems-schema/CONTEXT.md`.

## Driving it with check.py and the reader

`check.py --only example-no-d,example-no-parent,example-anonymous-signer,asset-entity-edge,kind-literal,convention-mandate,entity-grouping-tag`, then `reader-prompt.py <out> --feature kernel`.

## Gotchas

- The example checker reads only fenced blocks whose `kind` is `<AEMS X kind>` or a number. A block with another placeholder is skipped silently.
- A conventions doc may restate a kernel MUST if it says so. The rule allows lines that mention the kernel or the schema.
