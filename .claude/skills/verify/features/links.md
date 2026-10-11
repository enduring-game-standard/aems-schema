# Links and references

## Sub-features

- Every org link resolves to a file in a local clone, and every `#anchor` matches a heading.
- No link to a private repo, except those in `accepted.json`.
- A citation of a private ADR says it is private.

## How to get to it (user POV)

Every nav bar and cross-reference in the corpus.

## Driving it with check.py and the reader

`check.py --only link-missing,link-anchor,link-private,fence-unclosed,private-adr-label`.

## Gotchas

- Links resolve against whatever branch each clone has checked out. A link to a file that exists only on an unmerged PR branch passes locally and 404s on GitHub until that PR merges. Note the merge order in the PR.
- External non-org URLs are not checked.
