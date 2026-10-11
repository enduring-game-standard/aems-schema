# AEMS: Asset-Entity-Manifestation-State

**A standard schema for game content on a public commons — four signed event kinds linked by a provenance chain.**

Conceptual, 2026-10-10

🏠 **[EGS Overview](https://github.com/enduring-game-standard)** · 📦 **[AEMS](https://github.com/enduring-game-standard/aems-schema)** · 🎯 **[AEMS Conventions](https://github.com/enduring-game-standard/aems-conventions)** · 🔧 **[RUNS](https://github.com/enduring-game-standard/runs-spec)** · 📖 **[RUNS Library](https://github.com/enduring-game-standard/runs-library)** · ⚡ **[WOCS](https://github.com/enduring-game-standard/wocs-protocol)** · 🎼 **[MAPS](https://github.com/enduring-game-standard/maps-notation)** · 🎶 **[MAPS Library](https://github.com/enduring-game-standard/maps-library)** · ❓ **[FAQ](https://github.com/enduring-game-standard/.github/blob/main/profile/FAQ.md)** · 🔤 **[Glossary](https://github.com/enduring-game-standard/.github/blob/main/profile/README.md#glossary)**

---

## What the Standard Defines

AEMS defines four event kinds and the provenance chain between them — and nothing more.

- **Four addressable event kinds** — Entity, Manifestation, Asset, State. (The acronym's letter order is phonetic — "aims" — and carries no structural meaning.)
- **Three reference edges** — every Manifestation references at least one Entity; every Asset references its Manifestation; every State references its Asset.
- **Addressability** — each event's address is its kind, its publisher's key, and its `d`-tag. At each address, the latest event is current.

Compliance is exactly this. What events *carry* — tag vocabularies, property shapes, naming patterns, transfer patterns — is deliberately out of scope. The standard defines structure; [AEMS Conventions](https://github.com/enduring-game-standard/aems-conventions) recommends shared vocabularies for interoperability; the published events themselves are the ecosystem.

> **Note**: Concrete kind numbers and the exact parent-reference encoding are deliberately not yet pinned; they will be formalized against real relay usage. Examples use named placeholders, including the tag names `entity`, `manifestation`, and `asset`. [ADR-0010](./docs/adr/0010-what-the-substrate-guarantees.md) (proposed) records two constraints on that pinning: the kinds must be Nostr addressable kinds (30000-39999) for latest-wins to apply, and finding the references to an event on a relay needs a tag that relays index.

---

## Why Four Layers

A chess Knight survives the bankruptcy of every company that ever carved one. Nobody designed that. Physical reality keeps the parts of a game object separate for free, and digital games fused them into one object that a single server hosts. AEMS imposes, in digital space, what physical reality gives a game object for free:

1. The concept outlives every object and every maker. That is the **Entity**.
2. Anyone may interpret the concept, and no interpretation captures it. That is the **Manifestation**.
3. Possession belongs to whoever holds the object. That is the **Asset**.
4. Condition travels with the object. That is the **State**.
5. Origin travels with the object. That is the **provenance chain** itself.

Four layers carry the first four. The chain carries the fifth, and it replaces scarcity. Copying is free. No one can sign with a key they do not hold, so a false claim about who made an event fails; a claim about what happened is weighed by whoever reads it. AEMS does not prevent duplication, on purpose: enforcing scarcity would need monetary-grade consensus, and a game object is an identity to recognize, not a coin to spend.

This gives a membership test: a feature belongs in AEMS only if physical reality bundles it into the object itself ([ADR-0005](./docs/adr/0005-aems-imposes-physical-reality.md)). The requirements every AEMS document answers to are in [INTENT.md](./INTENT.md).

---

## The Four Layers

```
Entity  →  Manifestation  →  Asset   →  State
  ↓             ↓              ↓           ↓
naming of    a game's       signed      claimed
a concept    interpretation possession  condition
```

Each event is signed by its publisher and references its parent, so the full chain from any State back to a named concept can be checked wherever its events are kept.

### Entity

A signed **naming of a concept** — a dictionary entry, not the word. The event names the concept so that games can reference it. Anyone can publish an Entity. Rival namings of the same concept can coexist; convergence happens by reference — by which naming Manifestations actually cite — not by registry.

A concept may be ownerless, like "Sword," or have an author of record, like the Master Sword. Both are named by Entities, and the protocol treats them the same. For an authored concept, convergence concentrates on the author's naming because the world recognizes the author, not because the protocol requires it ([ADR-0007](./docs/adr/0007-an-entity-event-is-a-naming-not-the-concept.md)).

The concept a naming points at outlasts any publisher, the way the Knight has outlasted every manufacturer that ever carved one.

```json
{
  "kind": "<AEMS Entity kind>",
  "pubkey": "<namer>",
  "tags": [
    ["d", "health-potion"]
  ],
  "content": "..."
}
```

Entities are addressable: at each address, the latest event is current, so an author can refine their own naming without losing its identity.

### Manifestation

A game's **interpretation** of one or more Entities — how a particular game expresses and balances the named concept. Staunton's Knight and a themed set's Knight are both interpretations of the same piece: each interpretation belongs to its maker; the piece belongs to neither.

Every Manifestation MUST reference at least one parent Entity. Referencing several declares each concept the game object is, such as both the Master Sword and a sword.

```json
{
  "kind": "<AEMS Manifestation kind>",
  "pubkey": "<interpreter>",
  "tags": [
    ["d", "red-potion"],
    ["entity", "<entity reference>"]
  ],
  "content": "..."
}
```

Different games interpret the same Entity differently — one publisher's "Health Potion" becomes another game's flask and a third game's splash potion — and every interpretation references the naming it descends from.

### Asset

A signed **claim of possession** of one instance of a Manifestation, published with the owner's key. Twelve flasks in a player's bag are twelve Assets of one Manifestation. The event needs no game's servers: anyone can keep a copy, and it verifies wherever it lands — the figure on the shelf belongs to whoever holds it.

Every Asset MUST reference its parent Manifestation; the Entity is reached up the chain.

```json
{
  "kind": "<AEMS Asset kind>",
  "pubkey": "<owner>",
  "tags": [
    ["d", "instance-7f3a9b2c"],
    ["manifestation", "<manifestation reference>"]
  ],
  "content": "..."
}
```

Possession claims are auditable, not adjudicated. Anyone can sign an Asset of any Manifestation, including one they never earned, and nothing in the protocol stops it. An earned Asset and a self-minted one can look the same as events. What separates them is evidence that others sign, such as a game's signed record of the acquisition or a witness. Whoever is asked to honor a claim weighs that evidence and decides — the way the art world authenticates by chain of custody rather than by locks on frames.

### State

The **claimed current condition** of a single Asset — what changes during play: charges remaining, durability, wear. Condition travels with the Asset, not with any game — the chip on the Knight's ear stays with the piece.

A State is its signer's claim. The kernel does not say who signs it: the owner, the game that observed play, or anyone else. When several keys publish State for one Asset, the reader chooses whose claim to honor.

Relays need keep only the latest event at each address. A signer who keeps one `d`-tag per Asset therefore has one current State for it, and earlier versions survive only where someone archived them. A signer who gives each State its own `d`-tag keeps every version addressable, and the reader picks the latest by a `created_at` the signer chose.

Every State MUST reference its parent Asset.

```json
{
  "kind": "<AEMS State kind>",
  "pubkey": "<claimant>",
  "tags": [
    ["d", "instance-7f3a9b2c"],
    ["asset", "<asset reference>"]
  ],
  "content": "..."
}
```

---

## The Provenance Chain

Every AEMS event is a **claim by its signer**: a naming (Entity), an interpretation (Manifestation), a possession (Asset), a condition (State). The standard makes claims attributable and auditable; it does not make them true. Reading a chain tells you who signed what, and of what. An event's timestamp is part of its signer's claim. Witnesses, such as a third party's signed reference to an event, can show it existed by some time, for readers who trust the witness. What to honor is the reader's decision: a game decides which namings it recognizes and which provenance it accepts — a design decision, not a technical constraint.

This is the capability AEMS exists to provide, not a weakness to mitigate. It makes the digital pickup game possible. Nobody at the park rules on whose ball is legitimate; the players decide what equipment they accept. Strict equipment standards, like a league's match ball, are conventions a context adopts. The taped-up ball is still soccer ([ADR-0009](./docs/adr/0009-a-protocol-of-claims-never-facts.md)).

This is the structure that authenticates physical artifacts: provenance, not enforcement. The [PWNS](https://github.com/enduring-game-standard/.github/blob/main/profile/PWNS.md) extension builds on it for authored works — covenants, anchored attribution, and an author-controlled openness dial over sealed content.

---

## A Worked Example

A community member publishes a **Sword** Entity. Studio A publishes a **Manifestation** — its "Flameblade" — referencing that Entity. A player earns one, and an **Asset** signed by the player's key records the instance. Play wears it down; **State** events record its condition.

Studio A later shuts down. Any relay or archive that kept the events still serves them, and none of them needs Studio A. Studio B's game reads the player's Asset, follows its chain up to the Sword Entity, recognizes the naming, and offers its own interpretation — or a community client simply displays the full chain. Nothing about the player's sword lived on Studio A's servers.

---

## What AEMS Deliberately Excludes

AEMS defines four event kinds, their reference edges, and nothing more. Marketplaces, validation, and rendering fail the membership test (ADR-0005). The rest follow from the kernel declaring only shapes (ADR-0004).

| Excluded | Why | Where It Belongs |
|----------|-----|------------------|
| Databases/indexing | The standard defines structure, not storage | Relay operators, clients |
| Marketplaces | The standard enables claims, not commerce | Third-party platforms, coordination layers |
| Transfer | No kernel rule defines it. An Asset's address includes its owner's key, so a transfer means a new Asset under the new owner's key | Conventions (none exists yet) |
| Validation/adjudication | Events are claims; honoring them is the reader's judgment | Games, communities, reputation services |
| Rendering | The standard describes things, not how they look | Game clients, visual engines |
| Registries/namespacing | Convergence happens by reference, not by authority | Community convention, reputation |
| Rich metadata standards | The standard is silent beyond structure | [AEMS Conventions](https://github.com/enduring-game-standard/aems-conventions) |
| Composites/hierarchies | The standard defines atoms, not molecules | Application-layer composition |

The boundary: if a detail concerns *what games should agree on* rather than *what the structure requires*, it belongs in [conventions](https://github.com/enduring-game-standard/aems-conventions).

---

## Infrastructure

AEMS events are [Nostr](https://nostr.com) events. Nostr provides the properties the schema relies on:

- **Signed authorship.** Every event verifies against its publisher's key, wherever a copy of it lands.
- **No particular host.** Any relay or archive can hold an event, and anyone can copy it to another without the author's permission. No single server's failure destroys an event that others keep.
- **Reading without the author's permission.** Anyone can query relays for events by kind and by author, though a relay may charge or require a login. Single-letter tags are the only ones relays are expected to index, so a filter on a multi-letter tag generally runs in the client after fetching.
- **Addressable replacement.** At each address (kind, key, and `d`-tag), a relay keeps the latest version it has received and may discard older ones. A reader sees the latest among the copies it fetched.

Nostr does not guarantee that anyone keeps an event. An event lasts while the commons holds copies, the way a book lasts while libraries keep it, and keeping events alive is ecosystem work. An event's `created_at` is chosen by its signer and proves nothing on its own ([ADR-0010](./docs/adr/0010-what-the-substrate-guarantees.md)).

Nostr is not an interchangeable transport layer. We know of no other protocol that provides these properties as plain text without importing the costs of monetary consensus ([ADR-0006](./docs/adr/0006-nostr-is-the-substrate-not-a-transport-choice.md)).

---

## Ecosystem Connections

AEMS is one of four independent EGS protocols; the [correspondence map](https://github.com/enduring-game-standard/.github/blob/main/profile/CORRESPONDENCE.md) owns the full topology. AEMS's own edges:

- **[RUNS](https://github.com/enduring-game-standard/runs-spec)** — AEMS defines the *things*; RUNS defines the *game*. Optional seams exist at build time (Manifestations compiled into type definitions) and at load/save boundaries (Asset and State events persisting player data). An AEMS Asset is not the runtime object a game manipulates per frame — AEMS is the shelf; RUNS is the board.
- **[MAPS](https://github.com/enduring-game-standard/maps-notation)** — AEMS names the things; MAPS notates the mechanical structures those things participate in.
- **[WOCS](https://github.com/enduring-game-standard/wocs-protocol)** — AEMS answers "what are the things?"; WOCS coordinates the work that keeps an ecosystem running.

---

## Getting Started

1. **Publish an Entity** — a naming of a concept, addressed by its kind, your key, and a `d`-tag.
2. **Discover Entities** — query relays for Entity events published by the community.
3. **Publish a Manifestation** — your game's interpretation, referencing the Entity it descends from.
4. **Publish an Asset** — when a player acquires an instance, signed by the player's key, referencing its Manifestation.
5. **Publish State** — as the instance's condition changes, referencing its Asset.

For tag conventions, property naming, and domain examples, see [AEMS Conventions](https://github.com/enduring-game-standard/aems-conventions).

---

## The Deeper Argument

This README describes the schema. The compressed diagnosis it answers — why digital games die, in structural terms — is [WHY.md](https://github.com/enduring-game-standard/.github/blob/main/profile/WHY.md); the full argument is the book *Enduring Games: Patient Capital, Durable Substrate, and the Fix for an Industry That Eats Itself* (Scott Sheppard, 2026). For the architecture-wide picture, see the [EGS overview](https://github.com/enduring-game-standard).

---

**MIT License** — Open for use and implementation.
