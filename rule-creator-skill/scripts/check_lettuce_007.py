#!/usr/bin/env python3
"""LETTUCE-007: Check shareNativeConnection misconfiguration.

Detects commons-pool2 dependency usage without proper pool configuration
when shareNativeConnection is set.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
SHARE_NATIVE_PATTERN = re.compile(r'shareNativeConnection\s*[:=]\s*true', re.IGNORECASE)
COMMONS_POOL_PATTERN = re.compile(r'commons-pool2')
POOL_CONFIG_PATTERN = re.compile(
    r'(?:setMaxTotal|setMaxIdle|setMinIdle|poolConfig)',
    re.IGNORECASE
)
LETTUCE_POOL_CONFIG_PATTERN = re.compile(
    r'LettucePoolingClientConfiguration|PoolConfig|pool-config',
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
            if SHARE_NATIVE_PATTERN.search(stripped):
                # shareNativeConnection=true needs proper pool config when
                # commons-pool2 is used
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": i,
                    "message": "LETTUCE-007: shareNativeConnection=true with commons-pool2 requires proper pool configuration",
                })

        # Also check: commons-pool2 in pom.xml/gradle without pool config
        if 'commons-pool2' in text:
            has_pool_config = bool(LETTUCE_POOL_CONFIG_PATTERN.search(text))
            if not has_pool_config:
                for i, line in enumerate(lines, 1):
                    if COMMONS_POOL_PATTERN.search(line):
                        violations.append({
                            "file": str(path.relative_to(root)),
                            "line": i,
                            "message": "LETTUCE-007: commons-pool2 dependency without Lettuce pool configuration",
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
