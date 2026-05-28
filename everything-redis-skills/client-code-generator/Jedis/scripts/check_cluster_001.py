#!/usr/bin/env python3
"""CLUSTER-001: Check maxAttempts too large.

Detects maxAttempts > 5 in YAML or Java config for Redis Cluster.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
MAX_ATTEMPTS_PATTERN = re.compile(
    r'maxAttempts?\s*[:=]\s*(\d+)|max.attempts?\s*[:=]\s*(\d+)',
    re.IGNORECASE
)
SET_MAX_ATTEMPTS_PATTERN = re.compile(
    r'setMaxAttempts?\s*\(\s*(\d+)\s*\)',
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
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Check YAML/properties format
            match = MAX_ATTEMPTS_PATTERN.search(stripped)
            if match:
                for group in match.groups():
                    if group and int(group) > 5:
                        violations.append({
                            "file": str(path.relative_to(root)),
                            "line": i,
                            "message": f"CLUSTER-001: maxAttempts={group} exceeds recommended max of 5: {stripped}",
                        })
            # Check Java setter format
            match = SET_MAX_ATTEMPTS_PATTERN.search(stripped)
            if match:
                val = int(match.group(1))
                if val > 5:
                    violations.append({
                        "file": str(path.relative_to(root)),
                        "line": i,
                        "message": f"CLUSTER-001: setMaxAttempts({val}) exceeds recommended max of 5: {stripped}",
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
