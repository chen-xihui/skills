#!/usr/bin/env python3
"""SDR-003: Check missing commandTimeout in Spring Data Redis.

Detects LettuceConnectionFactory without setCommandTimeout or timeout config.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
LETTUCE_CONN_FACTORY_PATTERN = re.compile(r'LettuceConnectionFactory')
COMMAND_TIMEOUT_PATTERN = re.compile(
    r'(?:setCommandTimeout|commandTimeout|setTimeout)\s*\(',
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
        factory_lines = []
        for i, line in enumerate(lines, 1):
            if LETTUCE_CONN_FACTORY_PATTERN.search(line):
                factory_lines.append(i)

        if not factory_lines:
            continue

        # Check for timeout config
        has_timeout = any(COMMAND_TIMEOUT_PATTERN.search(l) for l in lines)
        if not has_timeout:
            # Check YAML/properties too
            for line in lines:
                stripped = line.strip()
                if re.match(r'(?:timeout|command-timeout)\s*[:=]', stripped, re.IGNORECASE):
                    has_timeout = True
                    break

        if not has_timeout:
            for line_no in factory_lines:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": "SDR-003: LettuceConnectionFactory without commandTimeout configuration",
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
