# ADR-0008: Possession is an auditable claim; the protocol never adjudicates

- **Status:** Accepted
- **Date:** 2026-06-12
- **Deciders:** Scott (+ Claude)
- **Scope:** AEMS (what an Asset *is*; rejection of structural legitimacy)

## Context

Imposition 3 (ADR-0005) ports physical possession, but physical possession is
*self-evidencing* — you either hold the Knight or you don't, and physics adjudicates
for free. The digital port has no adjudicator, and ADR-0005 deliberately declined the
one mechanism (scarcity-by-consensus) that fakes one. Nothing structural stops anyone
from signing an Asset event claiming an instance of anything. The README showed only
the happy path and stayed silent on what distinguishes the earned Flameblade from a
self-minted one.

## Decision

**AEMS does not adjudicate possession. It makes possession claims persistent, signed,
and auditable — and recognition stays voluntary.** At the protocol and philosophical
level, this is the only correct answer.

- **The van Meegeren model** (imposition 5): physical reality has forgery too; what
  exposes the fake is provenance research, not a lock. The earned Asset sits in a deep,
  checkable chain — a Manifestation published long before, an acquisition in context,
  transfers countersigned by previous owners. The self-minted one is a chain one event
  deep, born yesterday. The protocol carries the evidence; it never renders the verdict.
- **PWNS at the possession level:** self-minting is *claiming* — a lie about origin —
  and the math refutes it, because the legitimate chain is timestamped and signed by
  parties the forger does not control.
- **Recognition is voluntary** (ADR-0007, one layer down): a receiving game decides
  whose provenance it honors, the way a tournament decides which trophies it believes.

**Rejected: structural legitimacy** — e.g. requiring a valid Asset to be countersigned
by the Manifestation's publisher. It fails the ADR-0005 membership test (physical
reality bundles no adjudicator into the object; possession disputes are social there
too), and it reinstates the studio as gatekeeper: a dead studio's signature becomes a
permission no future player can obtain — the exact dependency AEMS exists to remove.

## Consequences

- What people *do* with auditable claims is up to them. Culturally, people will respond
  however they respond to the constraints of the reality they live within — the
  protocol provides the constraints, never the response.
- Reputation, witnessing services, blessed-provenance curation, anti-forgery research:
  all legitimate, all ecosystem/conventions work *on top of* the claims, never protocol
  machinery.
- The README's Asset section must present the claim model honestly rather than showing
  only the happy path.
