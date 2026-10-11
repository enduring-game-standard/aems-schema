#!/usr/bin/env bash
# Read-only: is the local corpus worth checking?
EGS="$(cd "$(dirname "$0")/../../../../.." && pwd)"
ok=0
for r in aems-schema aems-conventions .github runs-spec runs-library maps-notation wocs-protocol; do
  d="$EGS/$r"
  if [ ! -d "$d/.git" ]; then echo "MISSING $r (clone it next to aems-schema)"; ok=1; continue; fi
  b=$(git -C "$d" branch --show-current)
  behind=$(git -C "$d" rev-list --count HEAD..origin/main 2>/dev/null || echo "?")
  dirty=$(git -C "$d" status --porcelain | wc -l)
  echo "$r  branch=$b  behind-origin/main=$behind  dirty-files=$dirty"
done
python3 --version >/dev/null 2>&1 || { echo "python3 missing"; ok=1; }
exit $ok
