# What Nostr actually guarantees

## Sub-features

- Addressable replacement: relays must keep the latest event per address and may discard older versions.
- No persistence guarantee. A signed event is re-hostable by anyone and verifies wherever it lands.
- `created_at` is self-asserted.
- Relays index single-letter tags only.
- State is scoped to its signer. Transfer is undefined.

## How to get to it (user POV)

`aems-schema/README.md`, section "Infrastructure", and the State and Asset sections. The decision record is ADR-0010.

## Driving it with check.py and the reader

`check.py --only state-history,timestamp-proof,persistence-overclaim,tag-discovery`, then `reader-prompt.py <out> --feature substrate`.

## Gotchas

- The NIP facts come from nostr-protocol/nips at commit a79e21d9 (2026-10-05): NIP-01 lines 84, 99, 103, and 130. Recheck them when NIP-01 changes.
- "Eternally verifiable" is true of a signature given the bytes. The persistence rule allows "verif" after "eternal".
