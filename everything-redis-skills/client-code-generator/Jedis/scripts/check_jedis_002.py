#!/usr/bin/env python3
"""JEDIS-002: Check pool.getResource() is used with try-with-resources.

Detects Jedis jedis = pool.getResource() without try-with-resources pattern.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
GET_RESOURCE_PATTERN = re.compile(r'(?:Jedis\s+\w+\s*=\s*)?(?:\w+\.)?getResource\s*\(')
TRY_WITH_RESOURCE_PATTERN = re.compile(r'try\s*\(\s*(?:Jedis|final\s+Jedis)\s+\w+')


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
            if not GET_RESOURCE_PATTERN.search(stripped):
                continue
            # If it's inside a try-with-resources, it's fine
            if TRY_WITH_RESOURCE_PATTERN.search(stripped):
                continue
            # Look backwards a few lines for try-with-resources
            found_try = False
            for offset in range(1, 6):
                if i - 1 - offset < 0:
                    break
                prev = lines[i - 1 - offset].strip()
                if TRY_WITH_RESOURCE_PATTERN.search(prev):
                    found_try = True
                    break
                if prev.startswith("}") or "try" in prev and "{" in prev:
                    break
            if not found_try:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": i,
                    "message": f"JEDIS-002: getResource() must be used with try-with-resources: {stripped}",
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
