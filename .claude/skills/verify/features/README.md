# AEMS feature map

Each feature is a promise the documents make to a reader. A feature is verified when its lints are clean and its questions PASS.

| Feature | File | Lints | Questions |
|---|---|---|---|
| The kernel: four kinds, three edges, addressability | [kernel.md](kernel.md) | example-*, asset-entity-edge, kind-literal, kind-placeholder, convention-mandate, two-part-address | Q01-Q03 |
| The claims model: authenticity, not scarcity | [claims.md](claims.md) | transfer-promise, origin-overclaim | Q04-Q05 |
| Entity naming conventions | [naming.md](naming.md) | entity-ownerless-only, entity-is-role, std-namespace, canonical-artifact, retired-rubric, avoided-term | Q06-Q08 |
| What Nostr actually guarantees | [substrate.md](substrate.md) | state-history, timestamp-proof, priority-proof, persistence-overclaim, tag-discovery | Q09-Q14 |
| AEMS stands alone | [boundary.md](boundary.md) | aems-imported, entity-is-role | Q15 |
| Links and references | [links.md](links.md) | link-*, fence-unclosed, private-adr-label | none |
