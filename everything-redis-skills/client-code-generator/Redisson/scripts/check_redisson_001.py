#!/usr/bin/env python3
"""REDISSON-001: Check lock() without leaseTime.

Detects .lock() without duration/TimeUnit args (not .lock(30, TimeUnit)).
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
LOCK_PATTERN = re.compile(r'\.lock\s*\(')
LOCK_WITH_ARGS_PATTERN = re.compile(r'\.lock\s*\(\s*\d+\s*,\s*TimeUnit')


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
            if LOCK_PATTERN.search(stripped):
                # Check if lock() has leaseTime args
                if LOCK_WITH_ARGS_PATTERN.search(stripped):
                    continue
                # lock() with no args or just lock() - needs leaseTime
                # Check if it's lock() with empty or just single boolean arg
                match = re.search(r'\.lock\s*\(([^)]*)\)', stripped)
                if match:
                    args = match.group(1).strip()
                    if not args or args.lower() in ('true', 'false'):
                        violations.append({
                            "file": str(path.relative_to(root)),
                            "line": i,
                            "message": f"REDISSON-001: .lock() without leaseTime (use .lock(leaseTime, TimeUnit)): {stripped}",
                        })
                    elif not re.search(r'\d+\s*,\s*TimeUnit', args):
                        violations.append({
                            "file": str(path.relative_to(root)),
                            "line": i,
                            "message": f"REDISSON-001: .lock() without leaseTime (use .lock(leaseTime, TimeUnit)): {stripped}",
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
