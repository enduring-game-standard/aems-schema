#!/usr/bin/env python3
"""Deterministic checks of the AEMS documentation corpus against INTENT.md.

Usage: check.py [--json OUT] [--only RULE[,RULE...]]
Exit 0 when no findings, 1 otherwise.
"""
import argparse
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SCHEMA = SKILL.parent.parent.parent
EGS = SCHEMA.parent
ORG = "https://github.com/enduring-game-standard"

CORPUS = {
    "aems-schema": ["README.md", "CONTEXT.md", "INTENT.md", "docs/adr/*.md"],
    "aems-conventions": ["*.md", "docs/adr/*.md"],
    ".github": ["CONTEXT.md", "README.md", "profile/*.md"],
    "runs-spec": ["*.md"],
    "runs-library": ["README.md"],
    "maps-notation": ["*.md", "todo/*.md"],
    "wocs-protocol": ["README.md"],
}
PUBLIC_REPOS = {"aems-schema", "aems-conventions", "runs-spec", "runs-library",
                "wocs-protocol", "maps-notation", ".github"}

findings = []


def find(rule, path, line, msg):
    findings.append({"rule": rule, "file": str(path.relative_to(EGS)), "line": line, "msg": msg})


def corpus_files():
    for repo, globs in CORPUS.items():
        for g in globs:
            yield from sorted((EGS / repo).glob(g))


def slug(heading):
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def anchors(path):
    out, fence = set(), False
    for line in path.read_text().splitlines():
        if line.startswith("```"):
            fence = not fence
        elif not fence and (m := re.match(r"#{1,6}\s+(.*)", line)):
            out.add(slug(m.group(1)))
    return out


LINK = re.compile(r"\]\(([^)\s]+)\)|^\[[^\]]+\]:\s*(\S+)")


def check_links(path, text):
    for n, line in enumerate(text.splitlines(), 1):
        for m in LINK.finditer(line):
            url = m.group(1) or m.group(2)
            target, _, anchor = url.partition("#")
            if url.startswith("#"):
                local = path
            elif target.startswith(ORG):
                rest = target[len(ORG):].strip("/")
                if not rest:
                    continue
                repo, _, sub = rest.partition("/")
                if repo not in PUBLIC_REPOS:
                    find("link-private", path, n, f"links to {repo}, which is not a public repo: {url}")
                    continue
                sub = re.sub(r"^(blob|tree)/main/?", "", sub)
                local = EGS / repo / sub
            elif re.match(r"https?://", target):
                continue
            else:
                local = (path.parent / target).resolve()
            if not local.exists():
                find("link-missing", path, n, f"target does not exist: {url}")
            elif anchor and local.is_file() and anchor not in anchors(local):
                find("link-anchor", path, n, f"no heading for #{anchor} in {local.relative_to(EGS)}")


PARENT = {"Manifestation": "entity", "Asset": "manifestation", "State": "asset"}
GROUPING = {"category", "type", "subtype", "origin", "game", "suit"}


def check_examples(path, text):
    lines = text.splitlines()
    starts = [i for i, l in enumerate(lines) if l.startswith("```")]
    if len(starts) % 2:
        find("fence-unclosed", path, starts[-1] + 1, "code fence never closed")
        starts = starts[:-1]
    for a, b in zip(starts[::2], starts[1::2]):
        body = "\n".join(lines[a + 1:b])
        kind = re.search(r'"kind":\s*(?:"([^"\n]*)"|([^,\s}\]]+))', body)
        if not kind:
            continue
        k = kind.group(1) if kind.group(1) is not None else kind.group(2)
        if re.fullmatch(r"\d+", k) and re.match(r"(aems-|\.github)", str(path.relative_to(EGS))):
            find("kind-literal", path, a + 1, f"literal kind number {k}; kinds are unpinned")
            continue
        layer = re.fullmatch(r"<AEMS (\w+) kind>", k)
        if not layer:
            if k.startswith("<AEMS"):
                find("kind-placeholder", path, a + 1, f"placeholder {k!r} is not <AEMS Layer kind>, so the example goes unchecked")
            continue
        layer = layer.group(1)
        tags = re.findall(r'\[\s*"([^"]+)"', body)
        if "d" not in tags:
            find("example-no-d", path, a + 1, f"{layer} example has no d tag")
        if layer in PARENT and PARENT[layer] not in tags:
            find("example-no-parent", path, a + 1, f"{layer} example lacks its `{PARENT[layer]}` reference")
        if layer == "Entity" and GROUPING & set(tags):
            find("entity-grouping-tag", path, a + 1, f"Entity example carries {sorted(GROUPING & set(tags))}")
        if re.search(r'"pubkey":\s*"\.\.\."', body):
            find("example-anonymous-signer", path, a + 1, f"{layer} example leaves the signer unnamed")
        if layer == "Asset" and "entity" in tags:
            find("asset-entity-edge", path, a + 1, "Asset example references an Entity directly")


def load_rules():
    return json.loads((SKILL / "rules.json").read_text())


def check_rules(path, text, rules):
    rel = str(path.relative_to(EGS))
    for r in rules:
        if not any(re.search(s, rel) for s in r["files"]):
            continue
        if any(re.search(s, rel) for s in r.get("except_files", [])):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if re.search(r["pattern"], line, re.I) and not any(
                    x.lower() in line.lower() for x in r.get("unless", [])):
                find(r["id"], path, n, f'{r["why"]} :: {line.strip()[:140]}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--only")
    args = ap.parse_args()
    rules = load_rules()
    for path in corpus_files():
        text = path.read_text()
        check_links(path, text)
        check_examples(path, text)
        check_rules(path, text, rules)
    accepted = json.loads((SKILL / "accepted.json").read_text())
    def is_accepted(f):
        return any(f["rule"] == a["rule"] and re.search(a["file"], f["file"])
                   and a.get("match", "") in f["msg"] for a in accepted)
    held = [f for f in findings if is_accepted(f)]
    keep = set(args.only.split(",")) if args.only else None
    out = [f for f in findings if not is_accepted(f) and (keep is None or f["rule"] in keep)]
    for f in out:
        print(f'{f["file"]}:{f["line"]}  [{f["rule"]}]  {f["msg"]}')
    counts = {}
    for f in out:
        counts[f["rule"]] = counts.get(f["rule"], 0) + 1
    print(f"\n{len(out)} findings " + json.dumps(counts, sort_keys=True))
    print(f"{len(held)} accepted (see accepted.json)")
    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=1))
    sys.exit(1 if out else 0)


if __name__ == "__main__":
    main()
