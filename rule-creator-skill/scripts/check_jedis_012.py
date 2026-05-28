#!/usr/bin/env python3
"""JEDIS-012: Check missing commandTimeout.

Detects JedisPool or JedisCluster constructed without timeout parameter.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
JEDIS_POOL_CTOR = re.compile(r'new\s+JedisPool\s*\(')
JEDIS_CLUSTER_CTOR = re.compile(r'new\s+JedisCluster\s*\(')
TIMEOUT_PARAM = re.compile(r'(?:timeout|Timeout|TIMEOUT)\s*[,)]')


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

            for ctor_pattern, name in [
                (JEDIS_POOL_CTOR, "JedisPool"),
                (JEDIS_CLUSTER_CTOR, "JedisCluster"),
            ]:
                match = ctor_pattern.search(stripped)
                if not match:
                    continue

                # Collect full constructor call (may span multiple lines)
                full_call = stripped
                j = i
                while ';' not in full_call and j < len(lines):
                    full_call += " " + lines[j].strip()
                    j += 1

                # Count parameters - if only 1-2 params, likely missing timeout
                # Typical signatures: JedisPool(poolConfig, host) - no timeout
                # JedisPool(poolConfig, host, port, timeout) - has timeout
                paren_start = full_call.index('(')
                args = full_call[paren_start + 1:]
                # Find closing paren
                depth = 1
                args_str = ""
                for ch in args:
                    if ch == '(':
                        depth += 1
                    elif ch == ')':
                        depth -= 1
                    if depth == 0:
                        break
                    args_str += ch

                # Count comma-separated arguments at depth 0
                arg_count = 1
                d = 0
                for ch in args_str:
                    if ch == '(':
                        d += 1
                    elif ch == ')':
                        d -= 1
                    elif ch == ',' and d == 0:
                        arg_count += 1

                # JedisPool with <=2 args typically means no timeout
                # JedisCluster with <=1 arg typically means no timeout
                min_args_for_timeout = 3 if name == "JedisPool" else 2
                if arg_count < min_args_for_timeout:
                    violations.append({
                        "file": str(path.relative_to(root)),
                        "line": i,
                        "message": f"JEDIS-012: {name} constructed without commandTimeout parameter",
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
