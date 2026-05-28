#!/usr/bin/env python3
"""JEDIS-006: Search for configSet/configRewrite calls.

Detects .configSet() or .configRewrite() which should not be used at runtime.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
CONFIG_SET_PATTERN = re.compile(r'\.configSet\s*\(')
CONFIG_REWRITE_PATTERN = re.compile(r'\.configRewrite\s*\(')


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
        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if CONFIG_SET_PATTERN.search(stripped):
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": i,
                    "message": f"JEDIS-006: Avoid .configSet() at runtime (use config file): {stripped}",
                })
            if CONFIG_REWRITE_PATTERN.search(stripped):
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": i,
                    "message": f"JEDIS-006: Avoid .configRewrite() at runtime (use config file): {stripped}",
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
