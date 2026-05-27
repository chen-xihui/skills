#!/usr/bin/env bash
# Basic consistency checks for middleware skill repository.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"
FAIL=0

err() { echo "FAIL: $*" >&2; FAIL=1; }
ok() { echo "OK: $*"; }

# Mock CLI version
python3 skills/paas-cli/paas-cli.py version >/dev/null || err "paas-cli mock version"
python3 skills/bianque/bianque.py version >/dev/null || err "bianque mock version"

# SKILL.md line counts (main files should stay lean)
for f in skills/middleware-nacos/SKILL.md skills/middleware-redis/SKILL.md skills/middleware-es/SKILL.md; do
  lines=$(wc -l < "$f" | tr -d ' ')
  if [[ "$lines" -gt 120 ]]; then
    err "$f has $lines lines (target <= 120)"
  else
    ok "$f ($lines lines)"
  fi
done

# Forbidden patterns in skills/
DEPRECATED='paas-cli --version|command -v paas-cli|command -v bianque|bianque diagnose'
PRUNE='--exclude=paas-cli.py --exclude=COMMANDS.md'
if grep -rE ${PRUNE} "${DEPRECATED}" skills/ >/dev/null 2>&1; then
  err "found deprecated CLI patterns under skills/"
  grep -rE ${PRUNE} "${DEPRECATED}" skills/ || true
else
  ok "no deprecated CLI patterns under skills/"
fi

# Capability files exist
for mw in middleware-nacos middleware-redis middleware-es; do
  for cap in 01-client 02-audit 03-cluster 04-troubleshoot; do
    f="skills/${mw}/references/capabilities/${cap}.md"
    [[ -f "$f" ]] || err "missing $f"
  done
done
ok "capability files present"

# Shared references
for f in middleware-common.md harness-tools.md paas-cli-skill-delegation.md cli-tooling.md; do
  [[ -f "skills/_shared-references/$f" ]] || err "missing _shared-references/$f"
done
ok "shared references"

if [[ "$FAIL" -ne 0 ]]; then
  echo "validate-skills: FAILED" >&2
  exit 1
fi
echo "validate-skills: PASSED"
