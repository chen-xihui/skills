#!/usr/bin/env python3
"""JEDIS-014: Check eval() without scriptLoad/evalsha.

Detects .eval() usage without prior .scriptLoad() call.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
EVAL_PATTERN = re.compile(r'\.eval\s*\(')
EVALSHA_PATTERN = re.compile(r'\.evalsha\s*\(', re.IGNORECASE)
SCRIPT_LOAD_PATTERN = re.compile(r'\.scriptLoad\s*\(', re.IGNORECASE)


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
        eval_lines = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if EVAL_PATTERN.search(stripped) and not EVALSHA_PATTERN.search(stripped):
                eval_lines.append((i, stripped))

        if not eval_lines:
            continue

        # Check if scriptLoad exists in file
        has_script_load = any(SCRIPT_LOAD_PATTERN.search(l) for l in lines)
        has_evalsha = any(EVALSHA_PATTERN.search(l) for l in lines)

        if not has_script_load and not has_evalsha:
            for line_no, content in eval_lines:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": f"JEDIS-014: .eval() without .scriptLoad()/.evalsha() (use EVALSHA for repeated scripts): {content}",
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
