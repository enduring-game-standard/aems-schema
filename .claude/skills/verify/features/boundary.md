# AEMS stands alone

## Sub-features

- AEMS needs no other EGS protocol.
- RUNS and MAPS meet AEMS only at optional seams: build time and load/save.
- An AEMS Asset is not a runtime object.

## How to get to it (user POV)

`aems-schema/README.md`, section "Ecosystem Connections", and `.github/profile/CORRESPONDENCE.md`, which owns the cross-protocol map.

## Driving it with check.py and the reader

`check.py --only aems-imported,entity-is-role`, then `reader-prompt.py <out> --feature boundary`.

## Gotchas

- The lint scans runs-spec, runs-library, maps-notation, and wocs-protocol too, because those docs describe AEMS to their own readers.
