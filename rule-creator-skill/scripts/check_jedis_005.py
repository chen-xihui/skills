#!/usr/bin/env python3
"""JEDIS-005: Check MULTI without discard in catch.

Detects .multi() usage without corresponding .discard() in exception handlers.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
MULTI_PATTERN = re.compile(r'\.multi\s*\(\)')
DISCARD_PATTERN = re.compile(r'\.discard\s*\(\)')
CATCH_PATTERN = re.compile(r'\bcatch\s*\(')


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
        # Track multi() locations and find if discard() exists in catch blocks
        multi_lines = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if MULTI_PATTERN.search(stripped):
                # Extract the variable name if possible
                var_match = re.search(r'(\w+)\.multi\s*\(\)', stripped)
                var_name = var_match.group(1) if var_match else None
                multi_lines.append((i, var_name, stripped))

        if not multi_lines:
            continue

        # Check if file has any .discard() calls
        file_has_discard = any(DISCARD_PATTERN.search(l) for l in lines)

        # If .multi() is used but .discard() is never called, flag it
        if not file_has_discard:
            for line_no, var_name, content in multi_lines:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": f"JEDIS-005: .multi() without .discard() in catch block: {content}",
                })
        else:
            # More precise: check that each multi has a corresponding discard
            # For simplicity, check if catch block near each multi has discard
            for line_no, var_name, content in multi_lines:
                has_discard_in_catch = False
                # Search forward for catch blocks with discard
                for j in range(line_no, min(line_no + 30, len(lines))):
                    if CATCH_PATTERN.search(lines[j]):
                        # Found catch, look for discard within this catch block
                        depth = 0
                        for k in range(j, min(j + 20, len(lines))):
                            if DISCARD_PATTERN.search(lines[k]):
                                has_discard_in_catch = True
                                break
                            depth += lines[k].count('{') - lines[k].count('}')
                            if depth < 0:
                                break
                        break
                if not has_discard_in_catch:
                    violations.append({
                        "file": str(path.relative_to(root)),
                        "line": line_no,
                        "message": f"JEDIS-005: .multi() without .discard() in catch block: {content}",
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
