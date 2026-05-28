#!/usr/bin/env python3
"""LETTUCE-004: Check missing keepAlive.

Detects SocketOptions without keepAlive(true) configuration.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
SOCKET_OPTIONS_PATTERN = re.compile(r'SocketOptions')
KEEPALIVE_TRUE_PATTERN = re.compile(r'keepAlive\s*\(\s*true\s*\)')


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
        socket_lines = []
        for i, line in enumerate(lines, 1):
            if SOCKET_OPTIONS_PATTERN.search(line):
                socket_lines.append(i)

        if not socket_lines:
            continue

        has_keepalive = any(KEEPALIVE_TRUE_PATTERN.search(l) for l in lines)
        if not has_keepalive:
            for line_no in socket_lines:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": "LETTUCE-004: SocketOptions without keepAlive(true)",
                })

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
