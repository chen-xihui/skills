#!/usr/bin/env python3
"""JEDIS-009: Check for large Pipeline loops.

Detects Pipeline usage inside for loops with large iteration count (>1000).
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
PIPELINE_PATTERN = re.compile(r'(?:\.pipelined\s*\(\)|Pipeline\s+\w+)')
FOR_LOOP_PATTERN = re.compile(r'for\s*\(')
LARGE_NUMBER_PATTERN = re.compile(r'(?:<\s*(\d+)|<=\s*(\d+)|=\s*(\d+))')


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
        loop_limit = 0
        brace_depth = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Detect for loop with large iteration
            if FOR_LOOP_PATTERN.search(stripped):
                nums = LARGE_NUMBER_PATTERN.findall(stripped)
                for groups in nums:
                    for n in groups:
                        if n and int(n) > 1000:
                            in_loop = True
                            loop_limit = int(n)
                            brace_depth = 0
                            break

            if in_loop:
                brace_depth += stripped.count('{') - stripped.count('}')
                if PIPELINE_PATTERN.search(stripped):
                    violations.append({
                        "file": str(path.relative_to(root)),
                        "line": i,
                        "message": f"JEDIS-009: Pipeline inside large loop (>{1000} iterations): {stripped}",
                    })
                if brace_depth <= 0 and '{' in stripped or '}' in stripped:
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
