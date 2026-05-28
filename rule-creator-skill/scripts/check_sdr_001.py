#!/usr/bin/env python3
"""SDR-001: Check default serializer usage.

Detects RedisTemplate bean without keySerializer/valueSerializer configuration.
"""
import re
import sys
from pathlib import Path

EXTENSIONS = {'.java', '.yml', '.yaml', '.properties', '.xml'}
REDIS_TEMPLATE_BEAN_PATTERN = re.compile(
    r'(?:RedisTemplate|redisTemplate)\s*<',
)
BEAN_METHOD_PATTERN = re.compile(
    r'(?:public|@Bean).*RedisTemplate',
)
KEY_SERIALIZER_PATTERN = re.compile(r'keySerializer|key-serializer|setKeySerializer', re.IGNORECASE)
VALUE_SERIALIZER_PATTERN = re.compile(r'valueSerializer|value-serializer|setValueSerializer', re.IGNORECASE)


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

        # Find RedisTemplate bean definitions
        template_lines = []
        for i, line in enumerate(lines, 1):
            stripped = _strip_comments(line).strip()
            if REDIS_TEMPLATE_BEAN_PATTERN.search(stripped) or BEAN_METHOD_PATTERN.search(stripped):
                template_lines.append(i)

        if not template_lines:
            continue

        # Check for serializer config (strip comments to avoid false matches)
        has_key_serializer = any(
            KEY_SERIALIZER_PATTERN.search(_strip_comments(l)) for l in lines
        )
        has_value_serializer = any(
            VALUE_SERIALIZER_PATTERN.search(_strip_comments(l)) for l in lines
        )

        missing = []
        if not has_key_serializer:
            missing.append("keySerializer")
        if not has_value_serializer:
            missing.append("valueSerializer")

        if missing:
            for line_no in template_lines:
                violations.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "message": f"SDR-001: RedisTemplate without {', '.join(missing)} config (default JDK serializer may cause issues)",
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
