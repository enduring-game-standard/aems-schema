# Versioning with regular events

Question: [issues/09](../issues/09-versioning-with-regular-events.md). How does Nostr express "this event replaces that one" with regular events, how does a reader find the newest version, does `#e` work on live relays, and how do forks look?

Labels: **V** = verified against the cited source this session. **I** = inferred, not tested.

Pinned sources:

- NIPs: `nostr-protocol/nips` @ `37db639582d857e12468dcccd99b2c7f1d657da9` (2026-10-17).
- Amethyst: `vitorpamplona/amethyst` @ `163b322698d97a6fdfe2df62be781fd25665b746` (2026-10-19).
- strfry @ `4cd3cf64850caf47dda46c2a2abbbf3525a64d10`, nostr-rs-relay @ `b5c1f642e4f4c3b9c54f5d18d66f4c53642076b4`, khatru @ `9f99b9827a6e030bbcefc48f7af68bfe7eea1a27`.
- Live queries: 2026-10-19 against `wss://relay.damus.io`, `wss://nos.lol`, `wss://relay.primal.net`, `wss://relay.ngit.dev`, `wss://gitnostr.com`. Read-only. The script sends only `REQ` and `CLOSE`, never `EVENT`. Script: `/tmp/claude-1000/-home-wscottsh-repos-egs/9e397343-4f2e-4660-b3f4-3c342c9d7fc5/scratchpad/v09/tools/req.mjs`.

## 1. Three patterns exist in practice

### A. Star: every version cites the original

Each new version is a regular event with an `e` tag pointing at the **original** event, not at the previous version. The reader takes the newest by `created_at`.

- **NIP-28 kind 41 (merged).** Kind 41 updates channel metadata "without modifying the event id for the channel" and carries an `e` tag to the kind 40. "Only the most recent kind 41 per `e` tag value MAY be available." "Clients SHOULD ignore kind 41s from pubkeys other than the kind 40 pubkey." (V `28.md` L37-43.)
- **Kind 1010 "Editable Short Notes" (draft, not merged).** PR #1090 by vitorpamplona, open since 2024-02-26, head `09da0dd`, proposes `41.md`. A kind 1010 holds the new content and an `e` tag to the original kind 1. "Clients MUST check if the pubkey of the `kind:1010` is the same as the referenced `kind:1`." "Clients SHOULD render the `.content` of the most recent `kind:1010` by `created_at`." A 1010 from another key "is considered a proposal to edit". To accept it, the author signs a new 1010 that copies the proposal's content. (V `gh pr diff 1090`.)
- **Amethyst ships kind 1010** (V). `TextNoteModificationEvent.create` writes one `e` tag (the edited note), plus optional `p` and `summary` tags (`quartz/.../experimental/edits/TextNoteModificationEvent.kt` L83-101). Amethyst fetches edits with an `#e` filter: kind 1010 is in `RepliesAndReactionsKinds`, sent as `tags = mapOf("e" to ids)`, `limit = 1000` (`commons/.../watchers/FilterRepliesAndReactionsToNotes.kt` L74, L160-166). `Note.textNoteModifications()` keeps only edits signed by the note's author, drops expired ones, and sorts by `(created_at, id)` (`commons/.../model/NoteEditOverlays.kt` L51-59). The UI shows `latest()`, the last in that list, and lets the user step back through versions (`commonsUI/.../note/types/TextModification.kt` L235-259).
- **NIP-34 patch revisions (merged).** The first patch of a revision carries `["t","root-revision"]` and "SHOULD include a NIP-10 `e` `reply` to the original root patch" (V `34.md` L89-103). Every revision replies to the root, not to the previous revision.
- **NIP-37 checkpoints (merged).** Kind 1234 events with an `a` tag to a kind 31234 draft "can serve to provide a revision history of a parent event" (V `37.md` L34-45). These cite an address, not an id.

### B. Linked: each item cites the one before it

- **NIP-34 patch series.** "Patches in a patch set SHOULD include a NIP-10 `e` `reply` tag pointing to the previous patch." (V `34.md` L87.) This is a sequence of parts, not versions of one thing. It is the only merged example I found of an event pointing at its predecessor.
- **NIP-10 threads.** Markers `root` and `reply` let one event cite both the thread root and its direct parent (V `10.md` L31-44). NIP-34 revisions reuse this marker set.

No merged NIP uses "each version cites the previous version" for edits (V: grep of all NIPs for edit, revision, supersede, latest, newest).

### C. Not a regular-event pattern

- **NIP-17** edits by delete-and-republish: "Clients MAY implement edit by deleting an event and publishing another one with the same timestamp." (V `17.md` L89.) No provenance survives.
- **NIP-23, NIP-54, NIP-15** edit via addressable events (V `23.md` L34-36, `15.md` L306). Ticket 07 found relays drop older addressable versions. NIP-54's `fork` and `defer` markers apply `a` and `e` tags to wiki events from **other authors**, "to identify the exact version it was forked from" (V `54.md` L139-149). This is the only merged spec that names forks.
- **NIP-C7 chat edits (draft).** PR #2336 by fiatjaf, open, head `0d10303`: a kind 9 with `["e", <edited>]`, `["edit"]`, and a text-diff patch in content. It relies on "messages are always received in order" from one group relay (V `gh pr diff 2336`). It is not portable to relays that don't order.

## 2. Finding the newest version

**`#e` works on live relays (V).** NIP-01 says single-letter tags are indexed so `{"#e":[id]}` returns events that reference that id, and "Only the first value in any given tag is indexed" (V `01.md` L84). Live test, original kind 1 `3ab0a675…5af83` by `bc10bd15`:

| relay | `{"#e":[id]}` returned | `{"ids":[id]}` returned |
|---|---|---|
| relay.damus.io | 4 kind 1010 events | 1 (kind 1) |
| relay.primal.net | 4 kind 1010 events | 1 (kind 1) |
| nos.lol | 0 | 0 |

All four 1010s carry `["e","3ab0a675…"]` and `["client","Amethyst"]`, and none cites another 1010 (V). They are four siblings of the original, ordered only by `created_at` (1792421743, …760, …788, 1792422021). nos.lol had neither the note nor its edits, so a reader has to ask the relays where the author published (V for this note; the general claim is I).

NIP-34 on `relay.ngit.dev`: `{"#e":["6dac51bb…"]}` on a root patch returned 5 events: 3 kind 1617 revisions, 1 kind 1632 status, 1 kind 1624 cover note (V). damus and nos.lol had no root-revision patches (V), so NIP-34 data lives on git-specific relays.

**What one query can and can't reach.** A `#e` filter matches the tag value exactly (V `01.md` L84, L130). So:

- Star: one query on the original returns every version (V, demonstrated above).
- Linked: one query returns only the direct successors. Reaching version N takes N round trips, though each hop can batch many ids in one filter (I from NIP-01 filter semantics; not tested on a deep linked set).
- `limit` caps the initial response, newest first, ties broken by lowest id (V `01.md` L151). A heavily cited original can push versions past the cap (I).

**"Newest" is the signer's claim.** Every spec and client above ranks by `created_at` (V: NIP-28, PR 1090, NIP-34 L231, Amethyst `compareBy({createdAt},{idHex})`). The signer sets `created_at`. Nothing outside the event proves when it was made, unless something like NIP-03 OpenTimestamps is attached (I). Amethyst breaks same-second ties by id (V `NoteEditOverlays.kt` L58, L117). In 500 kind 1010s from damus I found no same-second ties (V).

**Who may supersede.** Every pattern filters by signer at the client: NIP-28 keeps only the kind 40 author, PR 1090 and Amethyst keep only the note author, NIP-34 status keeps "the issue/patch author or a maintainer" (V `34.md` L231). Relays don't enforce this. Live: on note `7ae35215…` (author `6b2a0424`), damus holds two 1010s signed by `0758dac8` with a `p` tag to the author, plus a later 1010 by the author (V). The author's 1010 cites only the original. It does not cite the proposal it may have accepted, so no signed reference links acceptance to proposal (V for this case).

## 3. Relay hazard: a regular kind can be hard-coded as replaceable

NIP-01 defines `1000 <= n < 10000 || 4 <= n < 45 || n == 1 || n == 2` as regular, "all expected to be stored by relays", so kind 41 is regular (V `01.md` L95). But strfry and nostr-rs-relay hard-code kind 41 as replaceable, keyed by pubkey and kind only:

- strfry: `isReplaceableKind` returns true for `kind == 41` (V `src/EventUtils.h` L10-15). Replaceable kinds get a virtual empty `d` tag (V `src/events.cpp` L24-27). Replacement then keys on `pubkey + d` (V `src/events.cpp` L296-318). So a key that owns two channels keeps only its newest kind 41 across both (I from the code; not tested live). This departs from NIP-28's "per `e` tag value".
- nostr-rs-relay: `is_replaceable()` includes `kind == 41` (V `src/event.rs` L175-179). The sqlite repo deletes older events of the same kind and author (V `src/repo/sqlite.rs` L171-177).
- khatru: not checked. It defers to go-nostr's kind helpers (V `adding.go` L55), which I did not clone.
- damus, nos.lol, and primal all report strfry in NIP-11 (V `software` field). damus returned 4 kind 41s from 4 distinct pubkeys for `limit:300` (V). That is consistent with per-pubkey replacement, but it doesn't prove it.

Kind 1010 is not special-cased (V: absent from both functions). damus kept all four edits of one note (V). Lesson: a regular kind is only as regular as the relays treat it. A new AEMS kind would avoid legacy special cases (I).

## 4. How forks appear to a reader

A fork means two successors of one version.

- **Star.** Two versions by the same signer are siblings of the original either way. The reader can't tell "B edits A" from "B and A both edit the original". Amethyst puts them in one timeline and shows the newer as current (V `TextModification.kt` L246, L254). The fork is invisible, and the newest `created_at` wins.
- **Star with outside signers.** Live, the proposal case above. The relay returns all three siblings. The reader's signer filter decides which count (V).
- **NIP-34 revisions.** All revisions reply to the root patch, so several revisions of one patch are a fork by construction. ngit.dev holds 6 roots with 2 or more revisions, for example root `6dac51bb…` with 3 by one author (V). Which one counts comes from a separate signed status event: "The most recent Status event … from either the issue/patch author or a maintainer is considered valid", and applied revisions are tagged in it (V `34.md` L206-233).
- **Linked (each version cites its predecessor).** A fork shows up as two events whose `e` tag names the same predecessor. One `#e` query on that predecessor returns both. The fork is visible, but the reader still needs a rule to pick one: newest `created_at`, a trusted signer, or a later event that cites both heads as a merge (I; no merged NIP defines this for regular-event versions).
- **NIP-54** marks forks explicitly with `fork` and lets a forker yield with `defer` (V `54.md` L139-149). Those are addressable events, so older versions are not kept (ticket 07).

## 5. What this means for AEMS (inferred, for Scott to decide)

- Two tags per version can serve two needs. A `root` `e` tag on the first version gives one-query discovery of all versions. A `reply` (predecessor) `e` tag records provenance and makes forks visible. NIP-10 markers already carry both, and NIP-34 uses them (V for the specs; the fit to AEMS is I).
- Star alone (kind 1010, NIP-28) is proven in shipping clients and live relays, but it hides forks and records no lineage between versions (V for the behavior; "insufficient for AEMS" is I).
- "Newest" by `created_at` is a claim by the signer. If an AEMS reader needs order it can trust, the order has to come from signed references (a version citing its predecessor) or an outside timestamp, not from the clock field (I).
- Signer filtering happens at the reader. A relay will store and return successors signed by anyone (V live).
