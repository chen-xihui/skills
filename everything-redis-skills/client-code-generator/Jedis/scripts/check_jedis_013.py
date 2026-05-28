#!/usr/bin/env python3
"""JEDIS-013: Check testOnBorrow not set.

Detects JedisPoolConfig without setTestOnBorrow(true).
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
POOL_CONFIG_PATTERN = re.compile(r'(?:JedisPoolConfig|GenericObjectPoolConfig)')
TEST_ON_BORROW_TRUE = re.compile(r'setTestOnBorrow\s*\(\s*true\s*\)')


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
        config_lines = []
        for i, line in enumerate(lines, 1):
            if POOL_CONFIG_PATTERN.search(line):
                config_lines.append(i)

        if not config_lines:
            continue

        has_test_on_borrow = any(TEST_ON_BORROW_TRUE.search(l) for l in lines)
        if not has_test_on_borrow:
            for line_no in config_lines:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": "JEDIS-013: JedisPoolConfig missing setTestOnBorrow(true)",
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
