#!/usr/bin/env python3
"""REDISSON-002: Check Redisson.create() in loops.

Detects loop constructs containing Redisson.create() calls.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
LOOP_PATTERN = re.compile(r'^\s*(?:for\s*\(|while\s*\()')
REDISSON_CREATE_PATTERN = re.compile(r'Redisson\.create\s*\(')


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

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if LOOP_PATTERN.match(line):
                in_loop = True
                loop_start_line = i
                brace_depth = 0
                # Check same line
                if REDISSON_CREATE_PATTERN.search(stripped):
                    violations.append({
                        "file": str(path.relative_to(root)),
                        "line": i,
                        "message": f"REDISSON-002: Redisson.create() inside loop: {stripped}",
                    })
                brace_depth += stripped.count('{') - stripped.count('}')
                continue

            if in_loop:
                brace_depth += stripped.count('{') - stripped.count('}')
                if REDISSON_CREATE_PATTERN.search(stripped):
                    violations.append({
                        "file": str(path.relative_to(root)),
                        "line": i,
                        "message": f"REDISSON-002: Redisson.create() inside loop: {stripped}",
                    })
                if brace_depth <= 0 and '}' in stripped:
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
