# AEMS: Asset-Entity-Manifestation-State

**A standard schema for game content on a public commons — four signed event kinds linked by a provenance chain.**

Conceptual, 2026-06-12

🏠 **[EGS Overview](https://github.com/enduring-game-standard)** · 📦 **[AEMS](https://github.com/enduring-game-standard/aems-schema)** · 🎯 **[AEMS Conventions](https://github.com/enduring-game-standard/aems-conventions)** · 🔧 **[RUNS](https://github.com/enduring-game-standard/runs-spec)** · 📖 **[RUNS Library](https://github.com/enduring-game-standard/runs-library)** · ⚡ **[WOCS](https://github.com/enduring-game-standard/wocs-protocol)** · 🎼 **[MAPS](https://github.com/enduring-game-standard/maps-notation)** · 🎶 **[MAPS Library](https://github.com/enduring-game-standard/maps-library)** · ❓ **[FAQ](https://github.com/enduring-game-standard/.github/blob/main/profile/FAQ.md)** · 🔤 **[Glossary](https://github.com/enduring-game-standard/.github/blob/main/profile/README.md#glossary)**

---

## What the Standard Defines

AEMS defines four event kinds and the provenance chain between them — and nothing more.

- **Four addressable event kinds** — Entity, Manifestation, Asset, State. (The acronym's letter order is phonetic — "aims" — and carries no structural meaning.)
- **Three reference edges** — every Manifestation references at least one Entity; every Asset references its Manifestation; every State references its Asset.
- **Addressability** — each event is identified by its publisher's key and a `d`-tag; for a given key and `d`-tag, the latest event is current.

Compliance is exactly this. What events *carry* — tag vocabularies, property shapes, naming patterns, transfer patterns — is deliberately out of scope. The standard defines structure; [AEMS Conventions](https://github.com/enduring-game-standard/aems-conventions) recommends shared vocabularies for interoperability; the published events themselves are the ecosystem.

> **Note**: Concrete kind numbers and the exact parent-reference encoding are deliberately not yet pinned; they will be formalized against real relay usage. Examples use named placeholders.

---

## The Four Layers

```
Entity  →  Manifestation  →  Asset   →  State
  ↓             ↓              ↓           ↓
naming of    a game's       signed      claimed
a concept    interpretation possession  condition
```

Each event is signed by its publisher and references its parent, so the full chain from any State back to a named concept is always checkable.

### Entity

A signed **naming of a concept** — a dictionary entry, not the word. The concept ("Sword," "Health Potion," "Monster") belongs to no one; the event names it so that games can reference it. Anyone can publish an Entity. Rival namings of the same concept can coexist; convergence happens by reference — by which naming Manifestations actually cite — not by registry.

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

Entities are addressable: for a given `pubkey` and `d`-tag, the latest event is current, so an author can refine their own naming without losing its identity.

### Manifestation

A game's **interpretation** of one or more Entities — how a particular game expresses and balances the named concept. Staunton's Knight and a themed set's Knight are both interpretations of the same piece: each interpretation belongs to its maker; the piece belongs to neither.

Every Manifestation MUST reference at least one parent Entity. Referencing several declares all the roles the game object participates in.

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

A signed **claim of possession** of one instance of a Manifestation, published with the owner's key. Twelve flasks in a player's bag are twelve Assets of one Manifestation. The event persists on the commons regardless of whether any game's servers continue operating — the figure on the shelf belongs to whoever holds it.

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

Possession claims are auditable, not adjudicated: a claim's weight is its provenance chain, and whoever is asked to honor a claim judges it — the way the art world authenticates by chain of custody rather than by locks on frames.

### State

The **claimed current condition** of a single Asset — what changes during play: charges remaining, durability, wear. The latest State event for an Asset is its current condition; earlier events are its history. Condition travels with the Asset, not with any game — the chip on the Knight's ear stays with the piece.

Every State MUST reference its parent Asset.

```json
{
  "kind": "<AEMS State kind>",
  "pubkey": "...",
  "tags": [
    ["d", "instance-7f3a9b2c"],
    ["asset", "<asset reference>"]
  ],
  "content": "..."
}
```

---

## The Provenance Chain

Every AEMS event is a **claim by its signer**: a naming (Entity), an interpretation (Manifestation), a possession (Asset), a condition (State). The standard makes claims persistent, attributable, and auditable; it does not make them true. Reading a chain tells you who published what, of what, and when. What to honor is the reader's decision: a game decides which namings it recognizes and which provenance it accepts — a design decision, not a technical constraint.

This is the structure that authenticates physical artifacts: provenance, not enforcement. The [PWNS](https://github.com/enduring-game-standard/.github/blob/main/profile/PWNS.md) extension builds on it for authored works — covenants, attribution, first-experience economics.

---

## A Worked Example

A community member publishes a **Sword** Entity. Studio A publishes a **Manifestation** — its "Flameblade" — referencing that Entity. A player earns one, and an **Asset** signed by the player's key records the instance. Play wears it down; **State** events record its condition.

Studio A later shuts down. The events remain on the commons. Studio B's game reads the player's Asset, follows its chain up to the Sword Entity, recognizes the naming, and offers its own interpretation — or a community client simply displays the full chain. Nothing about the player's sword lived on Studio A's servers.

---

## What AEMS Deliberately Excludes

AEMS defines four event kinds, their reference edges, and nothing more.

| Excluded | Why | Where It Belongs |
|----------|-----|------------------|
| Databases/indexing | The standard defines structure, not storage | Relay operators, clients |
| Marketplaces | The standard enables transfer claims, not commerce | Third-party platforms, coordination layers |
| Validation/adjudication | Events are claims; honoring them is the reader's judgment | Games, communities, reputation services |
| Rendering | The standard describes things, not how they look | Game clients, visual engines |
| Registries/namespacing | Convergence happens by reference, not by authority | Community convention, reputation |
| Rich metadata standards | The standard is silent beyond structure | [AEMS Conventions](https://github.com/enduring-game-standard/aems-conventions) |
| Composites/hierarchies | The standard defines atoms, not molecules | Application-layer composition |

The boundary: if a detail concerns *what games should agree on* rather than *what the structure requires*, it belongs in [conventions](https://github.com/enduring-game-standard/aems-conventions).

---

## Infrastructure

AEMS events are [Nostr](https://nostr.com) events. Nostr provides the properties the schema relies on: signed authorship (every event verifiable against its publisher's key), relay-distributed persistence (no single server's failure destroys the data), permissionless discovery (anyone can query for events by kind), and addressable replacement (latest-wins identity per key and `d`-tag). It is not an interchangeable transport layer: no other protocol currently provides these properties as plain text, without importing the costs of monetary consensus.

---

## Ecosystem Connections

AEMS is one of four independent EGS protocols; the [correspondence map](https://github.com/enduring-game-standard/.github/blob/main/profile/CORRESPONDENCE.md) owns the full topology. AEMS's own edges:

- **[RUNS](https://github.com/enduring-game-standard/runs-spec)** — AEMS defines the *things*; RUNS defines the *game*. Optional seams exist at build time (Manifestations compiled into type definitions) and at load/save boundaries (Asset and State events persisting player data). An AEMS Asset is not the runtime object a game manipulates per frame — AEMS is the shelf; RUNS is the board.
- **[MAPS](https://github.com/enduring-game-standard/maps-notation)** — AEMS names the things; MAPS notates the mechanical structures those things participate in.
- **[WOCS](https://github.com/enduring-game-standard/wocs-protocol)** — AEMS answers "what are the things?"; WOCS coordinates the work that keeps an ecosystem running.

---

## Getting Started

1. **Publish an Entity** — a naming of a concept, identified by your key and a `d`-tag.
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
