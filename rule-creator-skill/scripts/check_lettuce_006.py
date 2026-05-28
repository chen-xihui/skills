#!/usr/bin/env python3
"""LETTUCE-006: Check missing commandTimeout.

Detects Lettuce client without setDefaultCommandTimeout or commandTimeout config.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
LETTUCE_CLIENT_PATTERN = re.compile(
    r'(?:RedisClient\s*\.\s*create|LettuceClient|LettuceConnectionFactory)'
)
COMMAND_TIMEOUT_PATTERN = re.compile(
    r'(?:setDefaultCommandTimeout|commandTimeout|setCommandTimeout)\s*\(',
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
        client_lines = []
        for i, line in enumerate(lines, 1):
            if LETTUCE_CLIENT_PATTERN.search(line):
                client_lines.append(i)

        if not client_lines:
            continue

        has_timeout = any(COMMAND_TIMEOUT_PATTERN.search(l) for l in lines)
        # Also check YAML/properties for timeout config
        if not has_timeout:
            for line in lines:
                stripped = line.strip()
                if re.match(r'(?:command-timeout|commandTimeout|timeout)\s*[:=]', stripped, re.IGNORECASE):
                    has_timeout = True
                    break

        if not has_timeout:
            for line_no in client_lines:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": "LETTUCE-006: Lettuce client without commandTimeout configuration",
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
