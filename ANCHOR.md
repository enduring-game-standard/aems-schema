# AEMS: the design anchor

Draft, 2026-10-19. This note states how AEMS works, reasoned from a physical game piece. INTENT.md says what AEMS is for. This note says how the four layers do it. Where another document disagrees with this note, one of them is wrong, and the disagreement is a defect to fix.

AEMS is a standard people follow because it is useful. Nothing in it forces anyone to do anything. It lets a maker prove where a piece came from, lets a holder prove what they hold and what happened to it, and lets any game check whichever of those facts it cares about.

## 1. A piece can be made two ways

A factory can carve a chess Knight, and a player can whittle one at the kitchen table. Both are real Knights, and either one can go on a board. Their quality and look can differ completely. The only difference AEMS records is who made it.

A game studio can create an in-game object, and so can a player. Both are valid AEMS pieces. A player-made Flameblade is not a fake Studio A Flameblade. It is a homemade piece, and its signature says honestly who made it. The only forgery possible is signing as someone else, and a key you do not hold cannot sign.

## 2. Each layer answers one question about a piece

| Layer | Question it answers | Physical example |
|---|---|---|
| Entity | What is it? | "Knight" |
| Manifestation | Which design, which mold? | The Staunton Knight pattern |
| Asset | Which piece, made by whom? | One Knight pressed from that mold |
| State | What condition is it in, according to whom? | The chip on that Knight's ear |

- An **Entity** names a concept. Anyone can name one. Games recognize each other's pieces through it.
- A **Manifestation** is a design: the mold. A studio or a player can author one.
- An **Asset** is one piece made from a Manifestation, signed by whoever made it. Two pieces from one mold are two Assets of one Manifestation.
- A **State** is a condition of one Asset: damage, wear, paint, a skin.

## 3. One Asset can carry many States

Two Staunton Knights come from the same mold. One is down to 2 HP and the other still has 10. Same maker, same mold, different State.

State stays separate from the Asset so that one piece can be in different conditions in different contexts. The same Asset can be whole in one game, scarred in another, and painted with a different skin in a third. Each game signs its own State for the Asset. Several States for one Asset are the design, not a conflict.

A game that wants another game's scars reads that game's State for the Asset and honors it. A game that does not want them keeps its own.

## 4. Possession is separate from making

The factory makes the Knight and you end up holding it. Who made a piece never changes. Who holds it can.

A handoff is a signed event from the current holder that names the next holder. The Asset's signature shows where a piece came from. The handoffs show where it has been.

## 5. Provability comes from linked signatures

A signature is evidence for one fact about a piece. Who signs depends on which fact someone needs to prove. AEMS never says who must sign.

- A homemade piece carries the maker's signature. Nobody else is involved, and that signature proves everything there is to prove.
- A tournament prize carries the game's signature, because the fact worth proving is that the tournament awarded it. The player's signature can sit beside it to prove they received the prize.
- Damage from a ranked match carries the game's signature on the State. Anyone who doubts the damage checks for that game's key.

One Nostr event has one signer. Two signatures attach to one fact when one signed event cites another by event id. The id is a hash of the cited event, so the citation fixes its exact content.

A player can carry everything that proves a piece: the Asset, an award, its acceptance, handoffs, and States. Any game can check that set offline, with no relay and no studio, and then decide which signers it trusts. A tournament game can trust only its own key. A kitchen-table game can accept anything.

## 6. One bundle is the default packaging

The schema has one rule for this: an AEMS event can carry the signed events it cites. Checking a bundle means checking each signature and checking that each cited id matches the event carried with it.

Nostr already does this. A NIP-57 zap receipt is signed by the recipient's server. It carries the payer's signed zap request, with its own `id`, `pubkey`, and `sig`, inside a `description` tag. The receipt copies the tags people search by onto itself.

- **Order of signing.** The inner signer signs first. For a prize, the player signs an acceptance and the game signs the award that embeds it.
- **Later evidence.** A witness cannot edit a bundle someone already signed. The witness signs a new event that embeds the old bundle. The result is still one bundle.
- **Search.** Relays do not read inside embedded JSON. The outer event can copy the tags people search by, such as the holder's npub and the citation of the Manifestation. Which tags those are is open question 3.
- **Unbundling.** A bundle can be split into separate events, and separate events can be packed into a bundle, without breaking a signature. Separate events stay valid. The bundle is the recommended packaging because a proof that travels as one piece cannot lose a part when a relay drops an event.

## Open questions

1. **Bundle size.** Each relay can cap message size (NIP-11 `max_message_length`). Years of handoffs nested inside each other would eventually exceed a cap. One option is that each event embeds only what its own claim depends on and cites the rest by id. Another is that the holder keeps the full bundle and relays keep only the outer event. A size test with realistic handoff counts can settle it.
2. **Double handoff.** A physical Knight cannot be handed to two people. A holder can sign two handoffs for one Asset. Both are signed and visible, so anyone who cares can see the fork. Whether visibility is enough is a design decision still to make.
3. **Event kinds and citation tags.** Leading option: every AEMS event is a regular Nostr event, and a new version cites the version it replaces by event id.
   - Anyone can run a relay, and a signature proves itself wherever the event is held. What matters is whether a relay can hold the full provenance.
   - NIP-01 addressable events (kinds 30000-39999) keep one event per kind, key, and `d` tag. strfry (`src/events.cpp`), khatru (`adding.go`), and nostr-rs-relay (`src/repo/sqlite.rs`) all delete the older version when a newer one arrives, and refuse an older version that arrives after a newer one. On standard relay software, the earlier versions of an addressable event cannot be held, even on the holder's own relay.
   - An address citation (`a`) follows whatever its signer publishes next, so the signer can change what everyone citing them points at. An id citation (`e`) fixes the exact bytes.
   - Regular events can all be held. The first version's id identifies the thing. Each later version cites the one it replaces, and a reader finds newer versions by asking any relay for that signer's events citing the old id.
   - Not yet tried: the exact tag names, and a full round trip through a relay.
