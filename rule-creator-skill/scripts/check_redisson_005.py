#!/usr/bin/env python3
"""REDISSON-005: Check tryLock() without wait/lease time.

Detects .tryLock() without arguments (should specify waitTime and leaseTime).
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
TRYLOCK_NO_ARGS_PATTERN = re.compile(r'\.tryLock\s*\(\s*\)')


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
            if TRYLOCK_NO_ARGS_PATTERN.search(stripped):
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": i,
                    "message": f"REDISSON-005: .tryLock() without wait/lease time args (use .tryLock(waitTime, leaseTime, TimeUnit)): {stripped}",
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
