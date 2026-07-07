# AEMS

The glossary for AEMS — the EGS protocol that imposes, in digital space, what physical
reality gives game objects for free. A chess Knight survives its manufacturer's
bankruptcy; an Ace of Spades plays poker, bridge, and solitaire without anyone's
permission; a digital sword has never survived the disconnection of a server, because
digital architecture collapsed the separations that physics provides by default.
Preservation, cross-game recognition, and the four-layer ontology are side effects of
restoring those separations — none of them is the purpose.

AEMS defines four event kinds and the provenance chain between them — and nothing more:
what events *carry* is conventions territory, and published artifacts are ecosystem,
not schema (ADR-0004). Every AEMS event is a signed *claim* — eternal, attributable,
auditable, never adjudicated — which is what makes the digital pickup game possible
(ADR-0009). It stands on its own and does not depend on any other EGS protocol.

## Language

### The four layers

The layers form a single instantiation chain — **Entity → Manifestation → Asset →
State** — where each layer is a concrete instance of the one above it and references its
parent by provenance. (The acronym order A-E-M-S is phonetic only and carries no
structural meaning — see ADR-0001.)

**Entity**:
A signed *naming* of a concept — a dictionary entry, not the word. The concept (the
IP-free idea of a thing: "Health Potion," "Sword") belongs to no one and transcends
every event that names it; the signature authenticates the naming, never the named.
Rival namings of one concept are structurally normal; the commons converges by *use* —
by which naming Manifestations reference (ADR-0007). One Entity has many
Manifestations.
_Avoid_: type, class, token, item, asset

**Manifestation**:
A game-specific *version* of an Entity (e.g. "Estus Flask," "Red Potion"), bound to that
Entity forever by a provenance reference. The same concept, manifested differently per
game. One Manifestation has many Assets.
_Avoid_: skin, variant (a RUNS term), instance, implementation

**Asset**:
A signed, persistent *claim of possession* of one instance of a Manifestation —
auditable through its provenance chain, never adjudicated by the protocol (ADR-0008).
Whoever is asked to honor the claim judges it, the way provenance research — not a lock
on the frame — exposes a forged painting. Twelve Flasks in your bag are twelve Assets
of the one "Estus Flask" Manifestation. One Asset has one current State.
_Avoid_: item, token, NFT, in-game asset (that runtime object is RUNS, not AEMS)

**State**:
The *claimed* current condition of a single Asset — what changes during play (charges
remaining, durability, wear). The latest State event for an Asset is its current
claimed condition; earlier ones are auditable history (ADR-0009). A Red Potion usable
three times before empty tracks its remaining uses here.
_Avoid_: status, data, properties

### The chain

**Authenticity**:
What the chain of signed parent references *imposes* (the fifth freebie — ADR-0005).
A physical object's origin inheres in it: a forged Vermeer is exposed by provenance
research, not by a lock on the frame. AEMS makes origin eternally verifiable — every
event is signed, every layer references its parent — so "who made this, and of what?"
always has a checkable answer. Authenticity replaces scarcity: copying flows;
*claiming* is refuted by the math. (PWNS extends this with covenants and
an author-controlled openness dial over sealed content.)
_Avoid_: scarcity, uniqueness, rarity, DRM, anti-copy

## Flagged ambiguities

- **"Manifestation" (schema) vs. "manifestation" (book metaphor).** The *Enduring Games*
  book uses "manifestation" loosely for the ephemeral in-play instance that "dissolves
  when the game ends." In the AEMS schema, a **Manifestation is durable** — a published,
  game-specific version of an Entity. The thing you hold and that persists per-inventory
  is the **Asset**. Do not let the metaphor redefine the term.

- **"Asset" vs. "in-game asset."** An AEMS Asset is the commons-persisted, owner-signed
  instance. It is **not** the runtime object a game manipulates per-frame (that is RUNS's
  concern). AEMS is the shelf; RUNS is the board.

## Example dialogue

> **Dev:** A player loots a Red Potion in our dungeon crawler. What gets published?
>
> **Domain expert:** Nothing new at the Entity or Manifestation level — those already
> exist. "Health Potion" is the **Entity** somebody published years ago; your "Red
> Potion" is your **Manifestation** of it, published once when you built the game. The
> loot creates an **Asset**: one signed instance of Red Potion, owned by that player.
>
> **Dev:** They drink it twice, so it has one charge left. New Manifestation?
>
> **Domain expert:** No — the Manifestation is the type; it doesn't change per player.
> The remaining charge is **State** on that one Asset. You publish a State event; the
> latest one wins.
>
> **Dev:** Our studio shuts down. Is the player's potion gone?
>
> **Domain expert:** The Asset is signed and on the commons, so it persists. A future
> game can follow its Manifestation's provenance *up* to the "Health Potion" Entity,
> recognize the idea, and offer its own equivalent. That recognition is the whole point.
