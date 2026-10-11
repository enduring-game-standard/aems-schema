# ADR-0010: What Nostr guarantees, and what AEMS must not promise beyond it

- **Status:** Proposed (drafted by Claude from a NIP audit; awaiting Scott's acceptance)
- **Date:** 2026-10-10
- **Deciders:** Scott (pending)
- **Scope:** AEMS (the substrate facts the kernel relies on; would amend ADR-0002, ADR-0005, ADR-0006, ADR-0007, ADR-0008, ADR-0009)

## Context

ADR-0006 commits AEMS to Nostr and says Nostr supplies unhosted existence. The README, the glossary, and ADRs 0002 and 0005-0009 then lean on properties that read as Nostr's: events and provenance are eternal, a State's earlier events are its auditable history, the legitimate chain is timestamped, a Manifestation is bound to its Entity forever, and the standard enables transfer claims.

An audit against the NIPs (nostr-protocol/nips at commit `a79e21d9`, 2026-10-05) found that several of these properties are not Nostr's:

- NIP-01 addresses an addressable event by its kind, its pubkey, and its `d` tag, and only for kinds 30000-39999. For each address, relays MUST keep the latest event and MAY discard older versions, and SHOULD return only the latest ([NIP-01 lines 99-103](https://github.com/nostr-protocol/nips/blob/a79e21d90fce5465b50ef385dd368bba99ec4a0b/01.md#L99-L103)).
- No NIP guarantees that any relay keeps any event. Relays are hosted services that refuse, prune, and honor deletion requests ([NIP-01 line 105](https://github.com/nostr-protocol/nips/blob/a79e21d90fce5465b50ef385dd368bba99ec4a0b/01.md#L105), [NIP-09](https://github.com/nostr-protocol/nips/blob/a79e21d90fce5465b50ef385dd368bba99ec4a0b/09.md), [NIP-11](https://github.com/nostr-protocol/nips/blob/a79e21d90fce5465b50ef385dd368bba99ec4a0b/11.md)).
- `created_at` is a field the signer chooses ([NIP-01 line 21](https://github.com/nostr-protocol/nips/blob/a79e21d90fce5465b50ef385dd368bba99ec4a0b/01.md#L21)). Nothing checks it.
- Single-letter tags are the only tags relays are expected to index, and only a tag's first value ([NIP-01 line 84](https://github.com/nostr-protocol/nips/blob/a79e21d90fce5465b50ef385dd368bba99ec4a0b/01.md#L84), [line 130](https://github.com/nostr-protocol/nips/blob/a79e21d90fce5465b50ef385dd368bba99ec4a0b/01.md#L130)).
- An `a` reference names an address and follows its author's later replacements. An `e` reference names exact bytes, which relays may stop serving once the address is replaced.

What Nostr does provide is still the property AEMS needs: a signed event verifies wherever it lands, and anyone can copy it to any relay without the author's permission.

## Decision

**AEMS states only what Nostr guarantees, and names who supplies the rest.**

1. **An event's address is its kind, its publisher's key, and its `d` tag.** Whatever kinds are pinned must be addressable kinds (30000-39999), or relays will not apply latest-wins.

2. **Existence needs no particular host, but someone must keep a copy.** Nostr gives landlord independence: any relay or archive can hold an event, and the event verifies wherever it is. Nostr does not give persistence. An event lasts while the commons holds copies, the way a book lasts while libraries keep it. Keeping events alive is ecosystem work, alongside the witnessing and reputation services of ADR-0008. This changes ADR-0006's premise. ADR-0006 counted unhosted existence as provided by the substrate. Under this decision Nostr provides independence from any one host, and keeping events alive is ecosystem work. Either way existence is not imposed by the schema's structure, so the five impositions stay five, and the commitment to Nostr stands on the property Nostr does provide.

3. **The kernel promises the current event at an address, not its history.** A relay keeps the latest version it has received, and a reader sees the latest among the copies it fetched. Older versions may be gone. A State history exists where someone archived it, or where a publisher gives each State its own address. Which of these practices to recommend is a conventions question.

4. **A State is its signer's claim.** The kernel does not say who signs a State. The latest State at each address is its signer's claim about the Asset's condition. A signer who keeps one `d` tag per Asset has one current State for it. A signer who gives each State its own `d` tag leaves the reader to pick the latest by `created_at`, which the signer chose. When several keys publish State for one Asset, the reader chooses whose claim to honor, as it does for every other claim (ADR-0009).

5. **A signature proves which key signed. Witnesses can bound when.** `created_at` is part of the signer's claim. Evidence the forger does not control can show an event existed by some time, for readers who trust it: a third party's signed reference to the event, or a timestamp attestation (NIP-03, currently marked unrecommended). These are ecosystem services. A reference by event id shows only that the parent existed before the child. This corrects ADR-0007's "signature-plus-timestamp prove the claim" and ADR-0008's "the legitimate chain is timestamped".

6. **A reference binds the child, not the parent's content.** A reference by address follows the parent author's refinements, which ADR-0007 licenses. A reference by id pins the bytes, which may stop being served. A signed version of the child names the parent it cited, wherever a copy of that version survives. The encoding is still unpinned. Convergence by reference (ADR-0007) needs anyone to be able to find and count the references to a naming, and a relay can answer that only for a tag it indexes, so the pinned encoding should be a single-letter tag.

7. **Transfer is not defined.** An Asset's address includes its owner's key, so a new owner cannot publish at the old address. A transfer produces a new Asset under the new owner's key. Linking it to the old Asset, and to the old Asset's State, needs a convention that does not exist yet. Until it does, no document may cite countersigned transfers as available evidence.

8. **Discovery by a multi-letter tag happens on the client.** A query by kind or author works on any relay. A filter on `category`, `game`, or another multi-letter tag generally runs only after the client has fetched the events. A convention that wants relay-side discovery uses a single-letter tag.

## Consequences

- The README's Infrastructure section, the State and Asset sections, and the glossary say what Nostr guarantees and what it does not, using the words above. "Eternal" describes signature verification only.
- ADR-0002 and ADR-0005 through ADR-0009 keep their decisions. Their status lines point here for the corrected substrate facts.
- Transfer, State history, and relay-side classification are open conventions questions. The conventions repo lists them as open rather than leaving them unmentioned.
- The verify skill's `substrate` feature checks these points (`.claude/skills/verify/features/substrate.md`).
