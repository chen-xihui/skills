#!/usr/bin/env python3
"""CLUSTER-002: Check maxTotal without node consideration.

Detects large maxTotal (>100) in Cluster config without per-node consideration.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
MAX_TOTAL_PATTERN = re.compile(
    r'maxTotal\s*[:=]\s*(\d+)|max-total\s*[:=]\s*(\d+)',
    re.IGNORECASE
)
SET_MAX_TOTAL_PATTERN = re.compile(
    r'setMaxTotal\s*\(\s*(\d+)\s*\)',
    re.IGNORECASE
)
CLUSTER_CONTEXT_PATTERN = re.compile(
    r'(?:JedisCluster|RedisClusterClient|cluster|Cluster)',
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
            match = MAX_TOTAL_PATTERN.search(stripped)
            if match:
                for group in match.groups():
                    if group and int(group) > 100:
                        violations.append({
                            "file": str(path.relative_to(root)),
                            "line": i,
                            "message": f"CLUSTER-002: maxTotal={group} is too large for Cluster (consider per-node limits): {stripped}",
                        })

            # Check Java setter format
            match = SET_MAX_TOTAL_PATTERN.search(stripped)
            if match:
                val = int(match.group(1))
                if val > 100:
                    violations.append({
                        "file": str(path.relative_to(root)),
                        "line": i,
                        "message": f"CLUSTER-002: setMaxTotal({val}) is too large for Cluster (consider per-node limits): {stripped}",
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
