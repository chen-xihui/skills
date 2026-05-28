#!/usr/bin/env python3
"""LETTUCE-001: Check blocking commands on shared connection.

Detects .blpop(), .subscribe(), .xread() on sync() connection
which blocks the shared connection.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
SYNC_PATTERN = re.compile(r'\.sync\s*\(\)')
BLOCKING_COMMANDS = [
    (re.compile(r'\.blpop\s*\('), 'blpop'),
    (re.compile(r'\.brpop\s*\('), 'brpop'),
    (re.compile(r'\.subscribe\s*\('), 'subscribe'),
    (re.compile(r'\.xread\s*\('), 'xread'),
    (re.compile(r'\.xreadgroup\s*\('), 'xreadgroup'),
    (re.compile(r'\.bzpopmin\s*\('), 'bzpopmin'),
    (re.compile(r'\.bzpopmax\s*\('), 'bzpopmax'),
]


def check(project_root: str = ".") -> list:
    root = Path(project_root).resolve()
    violations = []
    for path in sorted(root.rglob("*")):
        if path.suffix not in EXTENSIONS:
            continue
        if path.is_dir():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            for cmd_pattern, cmd_name in BLOCKING_COMMANDS:
                if cmd_pattern.search(stripped):
                    # Check if used on sync() connection
                    if SYNC_PATTERN.search(stripped) or 'sync().' in stripped:
                        violations.append({
                            "file": str(path.relative_to(root)),
                            "line": i,
                            "message": f"LETTUCE-001: Blocking command .{cmd_name}() on shared sync() connection: {stripped}",
                        })
                    else:
                        # Also flag if sync() is used nearby in the same file
                        # and the call chain doesn't use dedicated connection
                        violations.append({
                            "file": str(path.relative_to(root)),
                            "line": i,
                            "message": f"LETTUCE-001: Blocking command .{cmd_name}() may block shared connection (use dedicated connection): {stripped}",
                        })
                    break

    return violations


def main():
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    violations = check(project_root)
    if violations:
        for v in violations:
            print(f"[FAIL] {v['file']}:{v['line']} - {v['message']}")
        sys.exit(1)
    else:
        print("[PASS] 无违规")
        sys.exit(0)


if __name__ == "__main__":
    main()
