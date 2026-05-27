#!/usr/bin/env python3
"""JEDIS-003: Check for connection creation inside loops.

Detects new Jedis(), getResource(), or Redisson.create() inside for/while loops.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
LOOP_PATTERN = re.compile(r'^\s*(?:for\s*\(|while\s*\(|while\s+\w+\s*[<>=!])')
CONNECTION_PATTERN = re.compile(r'(?:new\s+Jedis\s*\(|\.getResource\s*\(\)|Redisson\.create\s*\()')


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
        in_loop = 0  # nesting depth
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Track loop nesting by counting braces
            if LOOP_PATTERN.match(line):
                in_loop += 1
            # Simple brace-based nesting
            open_braces = stripped.count('{')
            close_braces = stripped.count('}')
            if in_loop > 0 and CONNECTION_PATTERN.search(stripped):
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": i,
                    "message": f"JEDIS-003: Avoid creating Redis connection inside loop: {stripped}",
                })
            # Adjust nesting
            if close_braces > 0 and in_loop > 0:
                in_loop = max(0, in_loop - close_braces)
            if open_braces > 0 and not LOOP_PATTERN.match(line):
                pass  # non-loop brace, ignore
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
