#!/usr/bin/env python3
"""JEDIS-008: Check testWhileIdle not set to true.

Detects JedisPoolConfig/GenericObjectPoolConfig without setTestWhileIdle(true).
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
POOL_CONFIG_PATTERN = re.compile(r'(?:JedisPoolConfig|GenericObjectPoolConfig)')
TEST_WHILE_IDLE_TRUE = re.compile(r'setTestWhileIdle\s*\(\s*true\s*\)')


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

        # Check if setTestWhileIdle(true) exists in the file
        has_test_while_idle = any(TEST_WHILE_IDLE_TRUE.search(l) for l in lines)
        if not has_test_while_idle:
            for line_no in config_lines:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": "JEDIS-008: JedisPoolConfig missing setTestWhileIdle(true)",
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
