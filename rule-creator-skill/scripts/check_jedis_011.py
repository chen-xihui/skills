#!/usr/bin/env python3
"""JEDIS-011: Check Cluster mode with business retry.

Detects loops wrapping jedisCluster calls (cluster already handles retries).
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
LOOP_PATTERN = re.compile(r'(?:for\s*\(|while\s*\()')
JEDIS_CLUSTER_PATTERN = re.compile(r'jedisCluster\w*\.\w+\s*\(', re.IGNORECASE)


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
        in_loop = False
        loop_start_line = 0
        brace_depth = 0
        has_cluster_call = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if LOOP_PATTERN.search(stripped):
                in_loop = True
                loop_start_line = i
                brace_depth = 0
                has_cluster_call = False
                # The loop line itself might have a brace
                brace_depth += stripped.count('{') - stripped.count('}')
                if JEDIS_CLUSTER_PATTERN.search(stripped):
                    has_cluster_call = True
                continue

            if in_loop:
                brace_depth += stripped.count('{') - stripped.count('}')
                if JEDIS_CLUSTER_PATTERN.search(stripped):
                    has_cluster_call = True
                if brace_depth <= 0 and '}' in stripped:
                    if has_cluster_call:
                        violations.append({
                            "file": str(path.relative_to(root)),
                            "line": loop_start_line,
                            "message": "JEDIS-011: Business retry loop wrapping jedisCluster call (cluster already retries)",
                        })
                    in_loop = False

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
