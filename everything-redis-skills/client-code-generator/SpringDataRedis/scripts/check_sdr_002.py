#!/usr/bin/env python3
"""SDR-002: Check keys() usage in Spring Data Redis.

Detects .keys() calls in Spring Data Redis context (opsForKeys, redisTemplate).
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
SDR_KEYS_PATTERN = re.compile(
    r'(?:redisTemplate|redisTemplate\.opsForKeys\(\))\s*\.\s*keys\s*\('
    r'|opsForKeys\s*\(\s*\)\s*\.\s*keys\s*\(',
    re.IGNORECASE
)


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
            if SDR_KEYS_PATTERN.search(stripped):
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": i,
                    "message": f"SDR-002: Avoid .keys() in Spring Data Redis (use SCAN): {stripped}",
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
