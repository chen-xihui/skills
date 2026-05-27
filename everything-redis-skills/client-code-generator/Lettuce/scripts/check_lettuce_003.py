#!/usr/bin/env python3
"""LETTUCE-003: Check missing shutdown.

Detects RedisClient or Lettuce client created without .shutdown() call.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
CLIENT_CREATE_PATTERN = re.compile(
    r'(?:RedisClient|LettuceClient)\s+\w+\s*=\s*(?:RedisClient\s*\.\s*create|new\s+RedisClient)'
)
SHUTDOWN_PATTERN = re.compile(r'\.shutdown\s*\(')


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
        create_lines = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if CLIENT_CREATE_PATTERN.search(stripped):
                create_lines.append((i, stripped))

        if not create_lines:
            continue

        has_shutdown = any(SHUTDOWN_PATTERN.search(l) for l in lines)
        if not has_shutdown:
            for line_no, content in create_lines:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": f"LETTUCE-003: RedisClient created without .shutdown() call: {content}",
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
