#!/usr/bin/env python3
"""LETTUCE-002: Check missing ClusterTopologyRefreshOptions.

Detects RedisClusterClient without ClusterTopologyRefreshOptions configuration.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
CLUSTER_CLIENT_PATTERN = re.compile(
    r'(?:RedisClusterClient|ClusterClient|LettuceClusterClient)'
)
TOPOLOGY_REFRESH_PATTERN = re.compile(
    r'ClusterTopologyRefreshOptions'
)


def _strip_comments(line: str) -> str:
    """Remove inline comments from a line of code."""
    # Java // comments
    idx = line.find('//')
    if idx >= 0:
        line = line[:idx]
    # YAML # comments (only if preceded by whitespace or start of line)
    stripped = line.lstrip()
    if stripped.startswith('#'):
        return ''
    idx = line.find(' #')
    if idx >= 0:
        line = line[:idx]
    return line


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
        cluster_client_lines = []
        for i, line in enumerate(lines, 1):
            if CLUSTER_CLIENT_PATTERN.search(line):
                cluster_client_lines.append(i)

        if not cluster_client_lines:
            continue

        has_topology_refresh = any(
            TOPOLOGY_REFRESH_PATTERN.search(_strip_comments(l)) for l in lines
        )
        if not has_topology_refresh:
            for line_no in cluster_client_lines:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": "LETTUCE-002: ClusterClient without ClusterTopologyRefreshOptions",
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
