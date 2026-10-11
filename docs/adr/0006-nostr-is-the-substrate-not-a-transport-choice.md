# ADR-0006: Nostr is the substrate, not a transport choice

- **Status:** Accepted. [ADR-0010](./0010-what-the-substrate-guarantees.md) corrects "Unhosted existence" as a Nostr guarantee.
- **Date:** 2026-06-12
- **Deciders:** Scott (+ Claude)
- **Scope:** AEMS (substrate commitment; where unhosted existence comes from)

## Context

ADR-0005's five impositions are achieved by *structure* — separations and signatures
the schema controls. One physical freebie is more basic and cannot be: **unhosted
existence**. In physical reality, persisting costs nothing and requires no one — matter
has no landlord. A digital object's existence is hosted: when the host stops, it ceases
by neglect. No event shape can impose this; it comes from where events live.

Grilling proposed the substrate-agnostic posture: state the demand (existence without a
landlord, permissionless reading, signature-carrying) and treat any satisfier as
swappable — by analogy with EGS workspace ADR-0015's refusal (private `egs-workspace` repo) to specify a Realization language.

## Decision

**Rejected. AEMS is built on Nostr, and Nostr is not an interchangeable transport
layer.** The substrate is the existence condition for the model: there is no better
protocol in existence — *not yet anyway*. The commitment is not loyalty to a brand; it
is the factual judgment that nothing else provides signed authorship, relay-distributed
persistence, and permissionless discovery as plain text, without importing the costs of
monetary consensus (ADR-0005's category error). AEMS supplies the structure — the five
impositions; Nostr supplies the existence.

## Consequences

- The enumeration of impositions stays **five**: unhosted existence is
  substrate-provided, not structure-imposed.
- The README's "Why Nostr" material is load-bearing derivation, not a feature pitch:
  its job is to show Nostr delivering unhosted existence and carrying the impositions.
- The asymmetry with EGS workspace ADR-0015 is deliberate and explainable: a Realization
  language is *defined to be disposable per target*; the substrate is defined to be the
  thing that never goes away. You don't specify the disposable; you do commit to the
  eternal.
- Should a superior substrate ever exist, that is an ADR-level reopening, not an
  implementation swap.
