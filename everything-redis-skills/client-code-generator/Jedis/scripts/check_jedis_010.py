#!/usr/bin/env python3
"""JEDIS-010: Check for infinite retry loops with Redis calls.

Detects while(true) or while (true) containing Redis/Jedis calls.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
WHILE_TRUE_PATTERN = re.compile(r'while\s*\(\s*(?:true|True|TRUE)\s*\)')
REDIS_CALL_PATTERN = re.compile(
    r'(?:jedis|redis|redisTemplate|redisson|jedisCluster|lettuce)\w*'
    r'\.\w+\s*\(',
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
        in_infinite_loop = False
        loop_start_line = 0
        brace_depth = 0
        has_redis_call = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if WHILE_TRUE_PATTERN.search(stripped):
                in_infinite_loop = True
                loop_start_line = i
                brace_depth = 0
                has_redis_call = False
                continue

            if in_infinite_loop:
                brace_depth += stripped.count('{') - stripped.count('}')
                if REDIS_CALL_PATTERN.search(stripped):
                    has_redis_call = True
                if brace_depth < 0 or (brace_depth == 0 and '}' in stripped):
                    if has_redis_call:
                        violations.append({
                            "file": str(path.relative_to(root)),
                            "line": loop_start_line,
                            "message": f"JEDIS-010: Infinite retry loop with Redis call (while(true))",
                        })
                    in_infinite_loop = False

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
