#!/usr/bin/env python3
"""JEDIS-007: Check JedisPoolConfig missing required params.

When JedisPoolConfig is used, check for setMaxTotal, setMaxIdle,
setMinIdle, setMaxWaitMillis configuration.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
JEDIS_POOL_CONFIG_PATTERN = re.compile(r'(?:JedisPoolConfig|GenericObjectPoolConfig)')
REQUIRED_PARAMS = {
    'setMaxTotal': re.compile(r'\.setMaxTotal\s*\('),
    'setMaxIdle': re.compile(r'\.setMaxIdle\s*\('),
    'setMinIdle': re.compile(r'\.setMinIdle\s*\('),
    'setMaxWaitMillis': re.compile(r'\.setMaxWaitMillis\s*\('),
}


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
        # Find JedisPoolConfig usage lines
        config_lines = []
        for i, line in enumerate(lines, 1):
            if JEDIS_POOL_CONFIG_PATTERN.search(line):
                config_lines.append(i)

        if not config_lines:
            continue

        # Check which params are set in the file
        found_params = set()
        for line in lines:
            for param_name, pattern in REQUIRED_PARAMS.items():
                if pattern.search(line):
                    found_params.add(param_name)

        # Report missing params
        missing = set(REQUIRED_PARAMS.keys()) - found_params
        if missing:
            for line_no in config_lines:
                for param in sorted(missing):
                    violations.append({
                        "file": str(path.relative_to(root)),
                        "line": line_no,
                        "message": f"JEDIS-007: JedisPoolConfig missing required parameter: {param}()",
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
