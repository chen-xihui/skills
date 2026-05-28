#!/usr/bin/env python3
"""JEDIS-004: Check Pipeline is properly closed.

Detects .pipelined() or Pipeline usage without try-with-resources or .close().
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
PIPELINE_PATTERN = re.compile(r'(?:\.pipelined\s*\(\)|Pipeline\s+\w+\s*=)')
TRY_WITH_RESOURCE_PATTERN = re.compile(r'try\s*\(\s*(?:Pipeline|final\s+Pipeline)\s+\w+')
CLOSE_PATTERN = re.compile(r'\.close\s*\(')


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
        # Track pipeline variable names and their usage
        pipeline_vars = {}  # var_name -> line_number
        has_close_for_var = set()
        in_try_with_resource = {}  # var_name -> True

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Check for try-with-resources with Pipeline
            try_match = TRY_WITH_RESOURCE_PATTERN.search(stripped)
            if try_match:
                var_m = re.search(r'Pipeline\s+(\w+)', stripped)
                if var_m:
                    in_try_with_resource[var_m.group(1)] = True
                continue

            # Check for Pipeline variable assignment
            pipe_match = PIPELINE_PATTERN.search(stripped)
            if pipe_match:
                var_m = re.search(r'Pipeline\s+(\w+)\s*=', stripped)
                if var_m:
                    var_name = var_m.group(1)
                    # Check if it's in try-with-resources
                    if var_name not in in_try_with_resource:
                        pipeline_vars[var_name] = i
                else:
                    # .pipelined() call - check if wrapped in try
                    found_try = False
                    for offset in range(1, 4):
                        if i - 1 - offset < 0:
                            break
                        if TRY_WITH_RESOURCE_PATTERN.search(lines[i - 1 - offset].strip()):
                            found_try = True
                            break
                    if not found_try:
                        violations.append({
                            "file": str(path.relative_to(root)),
                            "line": i,
                            "message": f"JEDIS-004: Pipeline must be used with try-with-resources or .close(): {stripped}",
                        })

            # Track .close() calls
            close_m = re.search(r'(\w+)\.close\s*\(\)', stripped)
            if close_m:
                has_close_for_var.add(close_m.group(1))

        # Check pipeline vars without close
        for var_name, line_no in pipeline_vars.items():
            if var_name not in has_close_for_var and var_name not in in_try_with_resource:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": f"JEDIS-004: Pipeline variable '{var_name}' is not closed with .close() or try-with-resources",
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
