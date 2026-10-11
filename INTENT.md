# AEMS: the intent

This note states what AEMS is for and the requirements that follow from it. The README, the glossary, the ADRs, and the conventions all answer to it. Where one of them disagrees with this note, the document is wrong, or this note is, and the disagreement is a defect to fix rather than a reading to reconcile.

## What AEMS is for

A chess Knight survives the bankruptcy of every company that ever carved one. An Ace of Spades plays poker, bridge, and solitaire, and no one gives permission. A digital sword has never outlived the server it lived on. Physical reality keeps the parts of a game object separate for free, and digital games fused them into one object that a single company hosts.

AEMS exists so that a game object outlives the game and the company that made it, the way a physical object does. Physical reality is the reference implementation. When a question about AEMS has a physical answer, that answer is the default.

## The requirements

1. **The parts of a game object stay separate.** The concept, a game's interpretation of it, one held instance, and that instance's condition are four layers: Entity, Manifestation, Asset, and State. Each layer is a signed event, and each event references its parent: a Manifestation references at least one Entity, an Asset references one Manifestation, and a State references one Asset. An Asset never references an Entity directly. The letter order in "AEMS" spells "aims" and means nothing about structure.

2. **Every event is a claim, and the protocol never rules on it.** An Entity claims a naming. A Manifestation claims an interpretation. An Asset claims possession. A State claims a condition. The protocol makes a claim attributable to its signer and checkable against its chain. It does not make a claim true, and it does not stop anyone from making one. Whoever is asked to honor a claim decides whether to, the way players at a park decide which ball to play with. This is the capability, not a weakness to mitigate.

3. **Authenticity, not scarcity.** Copying is free. Claiming a false origin is exposed by the chain. AEMS does not prevent duplication, and it does not promise uniqueness.

4. **An Entity is a naming, not the concept.** Anyone can name any concept, and rival namings are normal. A community converges on a naming by referencing it, never through a registry. A concept can be ownerless, like a sword, or have an author of record, like the Master Sword. Both are Entities, and the protocol treats them the same. Authorship is a fact about the world that a signature carries, not a flag in the data.

5. **The kernel is small.** Compliance is the four event kinds, the three parent references, and addressability by publisher key and `d` tag. What an event carries is a convention. Conventions are optional, opinionated, and forkable, and a conventions document never owns a MUST. Published events are the ecosystem, and the conventions repository points at them; it does not host them.

6. **AEMS stands alone.** AEMS needs no other EGS protocol. An Asset is the instance on the shelf, not the object a game updates every frame. Other protocols meet AEMS only at seams at the boundaries, such as building a game or loading and saving a player's things.

7. **Nostr is where the events live.** An AEMS event is a Nostr event. Nostr gives signed authorship, copies on many independent relays, and reading without permission. AEMS states what Nostr guarantees and what it does not. A claim the documents make about persistence or history holds only if Nostr, or a stated practice on top of it, actually delivers it.

## What the documents must not do

- State a convention as a requirement, or a requirement as a convention.
- Name an artifact canonical, blessed, or standard. Nothing on the commons is canonical until use makes it so, and the conventions repository records that use.
- Promise what the kernel does not define, such as transfer, history, or a current State chosen among several signers, without saying which convention or practice supplies it.
- Describe AEMS as a part of RUNS or MAPS, or as data those protocols import.
- Link to a document that does not exist.
