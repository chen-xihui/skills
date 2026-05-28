#!/usr/bin/env python3
"""REDISSON-004: Check missing keepAlive in Redisson config.

Detects YAML config without keepAlive: true setting.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.yml', '.yaml'}
REDISSON_CONFIG_PATTERN = re.compile(r'redisson', re.IGNORECASE)
KEEPALIVE_PATTERN = re.compile(r'keepAlive\s*:\s*true', re.IGNORECASE)


def _strip_comments(line: str) -> str:
    """Remove inline comments from a line of YAML/code."""
    stripped = line.lstrip()
    if stripped.startswith('#'):
        return ''
    idx = line.find(' #')
    if idx >= 0:
        line = line[:idx]
    return line


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

        # Only check files that look like Redisson config
        if not REDISSON_CONFIG_PATTERN.search(path.name) and \
           not REDISSON_CONFIG_PATTERN.search(text[:500]):
            continue

        lines = text.splitlines()
        has_keepalive = any(
            KEEPALIVE_PATTERN.search(_strip_comments(l)) for l in lines
        )
        if not has_keepalive:
            violations.append({
                "file": str(path.relative_to(root)),
                "line": 1,
                "message": "REDISSON-004: Redisson YAML config without keepAlive: true",
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
