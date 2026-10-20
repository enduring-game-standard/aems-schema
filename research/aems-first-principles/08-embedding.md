# How Nostr practice embeds one signed event in another

Research for [issue 08](../issues/08-how-nostr-embeds-signed-events.md). Gathered 2026-10-19.

Labels: **V** means verified. I read the source or ran the check, and the cite follows. **I** means inferred. It is my reasoning and was not checked against a source or a run.

## Sources and pins

All primary sources were shallow-cloned on 2026-10-19 and read at these commits.

| Source | Commit |
|---|---|
| nostr-protocol/nips | `37db639582d857e12468dcccd99b2c7f1d657da9` |
| nbd-wtf/nostr-tools | `8ffc6287cdbb062b29e210a54bd9bb31bbe29dd3` |
| nostr-dev-kit/ndk | `4b86acd13fe3c1284fddcb81a7f0d63e491db64a` |
| damus-io/damus (with vendored nostrdb) | `4a94f666d7e159e380e10b4dbbb2967d1688709e` |
| rust-nostr/nostr | `20096765b95f4840dd3df66cad49db35e9634462` |
| hoytech/strfry | `4cd3cf64850caf47dda46c2a2abbbf3525a64d10` |
| fiatjaf/khatru | `9f99b9827a6e030bbcefc48f7af68bfe7eea1a27` |
| scsibug/nostr-rs-relay | `b5c1f642e4f4c3b9c54f5d18d66f4c53642076b4` |

Cites below use `NIP-xx.md:line` for the nips repo and `repo/path:line` for code.

Two scripts did the live checks. They are kept outside the repo in the session scratchpad and are short enough to rewrite:

- `sample-embeds.mjs` and `verify-embeds.mjs` open a websocket to a relay, request up to 300 events of one kind, pull out the embedded event (the `description` tag for kind 9735, the `request` tag for kind 6xxx, `content` otherwise), and check that it parses, that its id recomputes, that its signature verifies (nostr-tools 2.25.2 `verifyEvent`), and that its id equals the outer `e` tag.
- NIP-11 documents were fetched with `curl -H 'Accept: application/nostr+json' https://<host>/` at 2026-10-19T23:53Z.

## Summary

- **V** Two places carry an embedded event in practice. One is `content`, used by NIP-18 reposts, NIP-72 approvals, and NIP-59 seals and gift wraps. The other is a multi-letter tag, used by NIP-57 zap receipts (`description`), NIP-90 job results (`request`), and NIP-CC verified finds (`verification`). The inner event is always a JSON string. No NIP nests it as a raw JSON object.
- **V** Every pattern copies a few small reference tags from the inner event to the outer one so relays can index the outer event. Usually that is `e` (the inner id or its target), `p` (the inner author or its target), and `k` (the inner kind). No pattern copies the inner event's own data tags.
- **V** Whether a client verifies the inner signature varies by library and by NIP. Damus verifies inner zap requests and inner reposts. nostr-tools verifies inner reposts by default and checks the id against the `e` tag. NDK verifies neither: it ignores repost `content` and refetches by id, and its zap parser never checks the inner signature.
- **V** On live relays, embedded events are common and nearly always valid. Of 900 sampled zap receipts across three relays, 896 carried a zap request and all 896 verified.
- **V** strfry and khatru cap the size of single-letter tag values (strfry's default is 1024 bytes), but not multi-letter tag values. A multi-letter tag or `content` is the place that can hold an embedded event on these relays. Live zap receipts on strfry relays carry `description` tags of up to 2546 bytes.
- **V** Of 18 relays that returned a NIP-11 document, 15 publish `max_message_length` (65535 to 1000000 bytes) and 6 publish `max_event_tags` (2000 to 10000). strfry's actual per-event cap, `maxEventSize`, defaults to 65536 bytes and does not appear in its NIP-11 document.

## Pattern by pattern

### NIP-57 zap receipts (kind 9735)

Where the inner event sits.
- **V** The zap request (kind 9734) is never published on its own. It is sent to the recipient's LNURL server (NIP-57.md:29). The receipt MUST carry it in a `description` tag "which is the JSON-encoded zap request" (NIP-57.md:136). `SHA256(description)` SHOULD match the description hash in the `bolt11` invoice (NIP-57.md:137). This makes the inner event part of what the invoice commits to.

Tags copied to the outer event.
- **V** The receipt MUST include the `p` tag, the optional `e` and `a` tags from the request, and a `P` tag holding the request's pubkey, which is the sender (NIP-57.md:134).
- **V** nostr-tools copies `e`, `p`, `a`, and adds `P`, `bolt11`, `description` (nostr-tools/nip57.ts:127-134). It does not copy the request's `k` tag. NIP-57 defines `k` on the request (NIP-57.md:40) but does not list it among the tags to copy (NIP-57.md:134).

Who verifies the inner signature.
- **V** The spec puts the inner check on the LNURL server. The request "MUST have a valid nostr signature" (NIP-57.md:109). nostr-tools implements that server check in `validateZapRequest`, which calls `verifyEvent` (nostr-tools/nip57.ts:88-99).
- **V** The client-side rules in Appendix F do not require checking the inner signature. They require the receipt's pubkey to equal the recipient's `nostrPubkey`, the invoice amount to equal the request's `amount`, and the `lnurl` to match (NIP-57.md:165-171). The spec also says the receipt is not payment proof, so "you are trusting the author of the `zap receipt`" (NIP-57.md:138).
- **V** Damus checks the receipt author against the zapper key, then verifies the inner request's id and signature (damus/Features/Zaps/Models/Zap.swift:288-318, using `validate_event` at damus/Core/Nostr/NostrEvent.swift:813-834). It skips the preimage check, with the comment "We're mostly trusting the zapper anyways" (Zap.swift:303-310).
- **V** Damus's nostrdb also counts zap totals at ingest from the `bolt11` tag alone and labels them "unverified" (damus/nostrdb/src/nostrdb.c:4515-4548).
- **V** NDK's `zapInvoiceFromEvent` parses the `description` JSON and the invoice, then trusts the result. It never verifies the inner signature or the receipt author (ndk/core/src/zap/invoice.ts:46-110). NDK's Svelte `validateNip57Zap` docstring claims "Zap request has valid signature" (ndk/svelte/src/lib/zaps/validation.ts:15), but the body only calls `zapInvoiceFromEvent` and checks the target (validation.ts:19-47). The claim in the comment is false.

Live data.
- **V** nos.lol had 298 of 300 receipts with a `description` that parsed, recomputed its id, and verified. relay.primal.net had 298 of 300, and nostr.mom had 300 of 300. The largest `description` was 2546 bytes (nos.lol). 83, 60, and 134 receipts respectively had a `description` over 1024 bytes.

### NIP-18 reposts (kind 6 and kind 16)

Where the inner event sits.
- **V** In `content`, as "the stringified JSON of the reposted note". It MAY be empty, "but that is not recommended" (NIP-18.md:12). Reposts of NIP-70 protected events SHOULD have empty content (NIP-18.md:13).
- **V** Kind 6 is for kind 1 notes. Kind 16 is a generic repost for any other kind (NIP-18.md:33-35).
- **V** For a replaceable event, the repost SHOULD carry an `a` tag. If `a` is absent, "a specific version of a replaceable event is being reposted, in which case the `content` field must contain the full JSON string of the reposted event" (NIP-18.md:40-45). This is the one place a NIP uses embedding to pin a specific version of a replaceable event, which relays otherwise discard (see [issue 07](../issues/07-can-relays-hold-addressable-history.md)).

Tags copied to the outer event.
- **V** `e` with the inner id, which MUST include a relay URL (NIP-18.md:15-17). `p` with the inner author SHOULD be included (NIP-18.md:19-20). Kind 16 SHOULD add `k` with the inner kind (NIP-18.md:37-38). nostr-tools emits exactly `e`, `p`, and for kind 16 `k` (nostr-tools/nip18.ts:22-45).

Who verifies the inner signature.
- **V** nostr-tools `getRepostedEvent` parses `content`, rejects it if its id differs from the `e` tag, and runs `verifyEvent` unless the caller passes `skipVerification` (nostr-tools/nip18.ts:82-106).
- **V** Damus verifies the inner event in `handle_boost_event` (damus/Features/Timeline/Models/HomeModel.swift:456-468). nostrdb also feeds kind 6 `content` back through its ingest path (nostrdb.c:3790-3796), and that path runs `ndb_note_verify` unless verification is switched off (nostrdb.c:3760-3770). I read both paths. I did not run them.
- **V** NDK never parses repost `content`. `repostedEvents()` fetches each `e` or `a` target from relays by id (ndk/core/src/events/kinds/repost.ts:30-46).

Live data.
- **V** Kind 6: on nos.lol, 277 of 300 reposts carried a parseable inner event, 274 verified, and 276 matched the `e` tag. On relay.primal.net, only 68 of 300 had a full inner event, and on nostr.mom only 44 of 300. On nostr.mom, 252 of the others carried a stub `{"id":"..."}` in `content` rather than an event, each from a different pubkey. All 68 and 44 full events verified.
- **V** Kind 16: the largest embedded event was 55,975 bytes on nostr.mom and 38,488 bytes on relay.primal.net. So those two relays store events of at least that size.
- **I** The 252 id-only stubs from 252 one-off keys look like one automated source, not normal client output. I did not trace them.

### NIP-59 seals (kind 13) and gift wraps (kind 1059, 21059)

Where the inner event sits.
- **V** A rumor is an unsigned event. It is JSON-serialized, encrypted with NIP-44, and put in the `content` of a seal. The seal is signed by the real author. The seal is in turn serialized, encrypted, and put in the `content` of a gift wrap signed by a one-time key (NIP-59.md:19-24, 99).
- **V** "Tags MUST always be empty in a `kind:13`. The inner event MUST always be unsigned" (NIP-59.md:56). This is the reverse of every other pattern. The innermost layer has no signature on purpose, for deniability (NIP-59.md:27-28).

Tags copied to the outer event.
- **V** None from the rumor. The seal has no tags. The gift wrap carries only routing data, such as the recipient `p` (NIP-59.md:60-61).

Who verifies the inner signature.
- **V** NIP-17 makes the binding check mandatory. "Clients MUST verify if pubkey of the `kind:13` is the same pubkey as that of the `unsignedMessageRumor`" (NIP-17.md:57).
- **V** nostr-tools `unwrapEvent` verifies the seal's signature and checks rumor pubkey against seal pubkey. It does not call `verifyEvent` on the wrap itself (nostr-tools/nip59.ts:92-117).
- **V** rust-nostr verifies the wrap, then the seal, then checks rumor pubkey against seal pubkey (nostr/src/nips/nip59.rs:94-121, 407-412).
- **V** Relays do treat gift wraps specially. strfry restricts reads of kinds 4 and 1059 to AUTH by default (strfry/src/apps/relay/golpe.yaml:25-26) and has special deletion rules for 1059 and 21059 (strfry/src/events.cpp:281, 356-359). nostr-rs-relay also special-cases kinds 4, 44, and 1059 (nostr-rs-relay/src/server.rs:1064). NIP-59 says relays may choose not to store gift wraps at all (NIP-59.md:115).

### Other embedding patterns

- **V NIP-72 approvals (kind 4550).** The approval SHOULD include "the JSON-stringified `post request` event inside the `.content`" (NIP-72.md:101). It copies `a` (the community), `e` or `a` (the post), `p` (the post author), and `k` (the post kind) (NIP-72.md:99-113). Live: 72 of 77, 62 of 64, and 179 of 183 non-empty approvals parsed, and every one that parsed verified and matched its `e` tag. The largest was 17,473 bytes on relay.primal.net.
- **V NIP-90 job results (kind 6xxx).** The result carries the job request as "stringified-JSON" in a `request` tag, plus `e` (the request id), `i` (the inputs), `p` (the customer), and `amount` (NIP-90.md:110-123). Live kind 6300: 213, 216, and 300 results parsed, all verified, and all matched their `e` tag. The largest was 701 bytes.
- **V NIP-CC verified found logs (kind 7516).** A verification event (kind 7517) signed by the cache's key "can be embedded in the `verification` tag as a JSON string" in the finder's log, published standalone, or both (NIP-CC.md:141-147, 151-159). This is the closest existing match to AEMS. A second party's signature, embedded in the holder's event, proves a fact the holder could not sign alone. I did not sample kind 7516 live.
- **V NIP-46 remote signing.** The `sign_event` result is `json_stringified(<signed_event>)` (NIP-46.md:101, 200). This is transport inside an encrypted reply, not a stored embedding.
- **V NIP-03 OpenTimestamps (kind 1040).** This attests to another event by `e` tag and puts the `.ots` proof in `content`. It does not embed the event (NIP-03.md:14-25).
- **V NIP-26 delegation** is marked `unrecommended` (NIP-26.md:1-9). It carries a signed token, not a signed event.

## Relay-side limits

### What the limits mean

- **V** `max_message_length` is the maximum bytes of incoming JSON, measured from `[` to `]`. It "effectively limits the maximum size of any event" (NIP-11.md:117-121). `max_event_tags` is the maximum number of elements in `tags` (NIP-11.md:135). `max_content_length` is the maximum number of unicode characters in `content` (NIP-11.md:137-140).
- **V** NIP-11 has no field for the size of a single tag value. Some relays do cap it, as follows.

### What the code enforces

- **V strfry.** Its defaults are `maxEventSize = 65536`, `maxNumTags = 2000`, and `maxTagValSize = 1024` (strfry/strfry.conf:21, 36, 39). The tag-value cap applies only when the tag name is one letter (strfry/src/events.cpp:37-38). A `description`, `request`, or `verification` tag is never capped by it. The whole event is capped at `maxEventSize` (events.cpp:115). strfry's NIP-11 document publishes `max_message_length` from `maxWebsocketPayloadSize` (default 131072) and does not publish `maxEventSize` or `maxNumTags` (strfry/src/apps/relay/RelayWebsocket.cpp:92-101; strfry.conf:102).
- **V khatru.** The default `MaxMessageSize` is 512000 (khatru/relay.go:45). Its optional `PreventLargeTags` and `PreventTooManyIndexableTags` policies also count only single-letter tags (khatru/policies/events.go:19-66).
- **V nostr-rs-relay.** The example config leaves `max_event_bytes`, `max_ws_message_bytes`, and `max_ws_frame_bytes` commented out at 131072 (nostr-rs-relay/config.toml:135-141). Its NIP-11 `Limitation` struct fills only `payment_required` and `restricted_writes` (nostr-rs-relay/src/info.rs:79-86). This matches the live documents, which publish neither size field.
- **V** No relay source has code that parses or checks an embedded event. A grep for 9735 and kind 6 in strfry, khatru, and nostr-rs-relay found none. The only kind-specific code is the gift-wrap handling listed above. Relays store an embedded event as an opaque string.

### Live NIP-11 sample

Fetched 2026-10-19T23:53Z. 24 hosts tried. 18 returned a JSON document. relay.0xchat.com, relay.current.fyi, and relay.nostr.bg failed to connect (curl exit 6). relay.nostr.band and nostr.fmt.wiz.biz timed out (exit 28). relay.mostr.pub returned an empty body.

| Relay | Software | `max_message_length` | `max_event_tags` | `max_content_length` |
|---|---|---|---|---|
| relay.damus.io | strfry 1.1.0-158 | 1000000 | absent | absent |
| relay.primal.net | strfry 1.1.3 | 1000000 | absent | absent |
| nos.lol | strfry 1.1.3 | 131072 | absent | absent |
| nostr.mom | strfry 1.1.3 | 131072 | absent | absent |
| offchain.pub | strfry 1.1.0 | 131072 | absent | absent |
| nostr.bitcoiner.social | strfry 1.1.0 | 131072 | absent | absent |
| nostr.oxtr.dev | strfry 1.0.4 | 131072 | absent | absent |
| relay.nos.social | strfry 1.0.3 | 262144 | absent | absent |
| relay.nostr.net | strfry 1.1.2-148 | 262144 | absent | absent |
| nostr21.com | strfry v315 | 262200 | 10000 | 262140 |
| nostr.wine | nostr.wine 0.3.3 | 524288 | 4000 | absent |
| relay.snort.social | memlay 0.2.0 | 524288 | absent | absent |
| nostr.land | NFDB 2.0 | 65535 | 2000 | absent |
| eden.nostr.land | NFDB 2.0 | 65535 | 2000 | absent |
| atlas.nostr.land | NFDB 2.0 | 65535 | 2000 | absent |
| purplepag.es | purplepag.es 0.2.0 | absent | 2000 | 131072 |
| nostr-pub.wellorder.net | nostr-rs-relay 0.9.0 | absent | absent | absent |
| relay.wellorder.net | nostr-rs-relay 0.9.0 | absent | absent | absent |

- **V** The smallest published `max_message_length` is 65535 (nostr.land, eden, atlas). The smallest published `max_event_tags` is 2000.
- **I** On the 10 strfry relays, the published number is the websocket payload cap, not the event cap. If an operator kept the default `maxEventSize`, the relay rejects events over 65536 bytes while advertising 131072 or more. The live kind 16 sample shows nostr.mom and relay.primal.net storing events of at least 56 KB and 38 KB. That fits under the default and does not tell us their real setting. Only a test publish would settle it, and I did not publish to public relays.

## What this means for AEMS bundles

All of these are **I**. They are design readings of the facts above, for Scott to weigh.

- A bundle that carries the signed events it cites has direct precedent. NIP-57 receipts, NIP-72 approvals, NIP-90 results, and NIP-CC logs each embed a second party's signed event as a JSON string. NIP-CC is closest to AEMS, because it proves a fact the holder could not sign alone.
- Put embedded events in `content` or in a multi-letter tag, never in a single-letter tag. A single-letter tag over 1024 bytes is rejected by default strfry.
- Copy only small reference tags (`e`, `p`, `k`, and `a` where relevant) to the outer event, so relays can index the outer event by what it cites. That is what every pattern does.
- Do not assume readers verify the embedded signature. Damus and nostr-tools do. NDK does not, and the NIP-57 client rules never ask for it. An AEMS reader that wants provenance has to recompute the id and verify the signature itself, and check that the id matches the outer reference tag, as nostr-tools does for reposts.
- Size the bundle against 64 KiB. That is the strfry default event cap, the smallest live `max_message_length` found (65535), and the cap most likely to be in force without being advertised. The question of bundle size is [issue 14](../issues/14-bundle-size.md).
- NIP-18's rule for replaceable events (no `a` tag means the full JSON pins a specific version) suggests that embedding is how Nostr practice already keeps a version that relays would drop.
