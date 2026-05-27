#!/usr/bin/env python3
"""JEDIS-001: Check for .keys() calls that may block Redis.

Searches for jedis.keys(), redisTemplate.keys(), sync.keys(), opsForKeys().keys()
and similar patterns that use the KEYS command instead of SCAN.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
# Match .keys( but exclude scan/SCAN patterns nearby
KEYS_PATTERN = re.compile(r'\.keys\s*\(')
SCAN_NEARBY = re.compile(r'(?:scan|SCAN)', re.IGNORECASE)


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
        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if KEYS_PATTERN.search(stripped):
                # Skip if the line itself mentions scan (e.g. scanKeys)
                if SCAN_NEARBY.search(stripped):
                    continue
                # Check specific dangerous patterns
                if any(p in stripped for p in [
                    'redisTemplate.keys(', 'jedis.keys(',
                    '.keys("*"', '.keys(\'*\'',
                    'sync.keys(', 'opsForKeys().keys(',
                ]):
                    violations.append({
                        "file": str(path.relative_to(root)),
                        "line": i,
                        "message": f"JEDIS-001: Avoid .keys() call (use SCAN instead): {stripped.strip()}",
                    })
                else:
                    # Generic .keys() usage
                    violations.append({
                        "file": str(path.relative_to(root)),
                        "line": i,
                        "message": f"JEDIS-001: Avoid .keys() call (use SCAN instead): {stripped.strip()}",
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
