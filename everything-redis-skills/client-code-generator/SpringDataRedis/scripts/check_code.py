#!/usr/bin/env python3
"""Redis Java Client Code Audit Tool

This script checks Java Redis client code for common issues based on 14 audit rules.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


class RedisCodeAuditor:
    """Redis code auditor based on REDIS-001 ~ REDIS-014 rules."""
    
    RULES = {
        "REDIS-001": {
            "severity": "critical",
            "description": "禁止在循环中使用 keys *，应使用 scan",
            "patterns": [r"\.keys\s*\(", r"KEYS\s+\*", r"redisTemplate\.keys"],
            "fix": "使用 ScanOptions 替代 keys()"
        },
        "REDIS-002": {
            "severity": "warning",
            "description": "大 Key 风险检查（单次操作 Value 超过 10KB 应拆分或压缩）",
            "patterns": [r"get\s*\([^)]+\)", r"set\s*\([^)]+,[^)]+"],
            "fix": "考虑拆分大 Key 或使用压缩"
        },
        "REDIS-003": {
            "severity": "warning",
            "description": "热 Key 风险检查（高频读写的 Key 应考虑本地缓存）",
            "patterns": [r"opsForValue\(\)\.get", r"opsForValue\(\)\.set"],
            "fix": "考虑使用本地缓存（如 Caffeine）"
        },
        "REDIS-004": {
            "severity": "warning",
            "description": "连接池参数合理性（maxTotal、maxIdle、maxWaitMillis）",
            "patterns": [r"maxTotal\s*=", r"maxIdle\s*=", r"maxWait"],
            "fix": "maxTotal < 200, maxWaitMillis 禁止使用 -1"
        },
        "REDIS-005": {
            "severity": "info",
            "description": "Pipeline 批量使用情况（多次独立命令应使用 Pipeline）",
            "patterns": [r"for\s*\([^)]+\)", r"while\s*\("],
            "fix": "考虑使用 executePipelined()"
        },
        "REDIS-006": {
            "severity": "info",
            "description": "Lua 脚本是否使用 EVALSHA 预加载（而非每次 EVAL）",
            "patterns": [r"\.eval\s*\(", r"EVAL\s+"],
            "fix": "使用 EVALSHA 预加载脚本"
        },
        "REDIS-007": {
            "severity": "warning",
            "description": "是否设置合理的过期时间（避免 Key 永不过期导致内存泄漏）",
            "patterns": [r"set\s*\([^)]+\)[^;]*(?<!expire|expireAt)", r"opsForValue\(\)\.set\([^)]+\)"],
            "fix": "使用 set(key, value, timeout, unit) 设置过期时间"
        },
        "REDIS-008": {
            "severity": "critical",
            "description": "密码是否硬编码",
            "patterns": [r'password\s*=\s*["\'][^$\{][^"\']*["\']', r'"password"\s*:\s*"[^$]'],
            "fix": "使用环境变量或密钥管理系统"
        },
        "REDIS-009": {
            "severity": "critical",
            "description": "禁止使用 CONFIG、FLUSHALL、FLUSHDB 等高危命令",
            "patterns": [r"\.config\s*\(", r"FLUSHALL", r"FLUSHDB"],
            "fix": "禁止在生产代码中使用高危命令"
        },
        "REDIS-010": {
            "severity": "critical",
            "description": "禁止使用 Keys 全库匹配命令",
            "patterns": [r"KEYS\s+\*", r"keys\s*\(\s*\"\*\"", r"keys\s*\(\s*\"[^\"]*\*[^\"]*\"", r"redisTemplate\.keys"],
            "fix": "使用 SCAN 命令替代"
        },
        "REDIS-011": {
            "severity": "warning",
            "description": "避免使用集合整存整取与高时间复杂度命令",
            "patterns": [r"SMEMBERS", r"LRANGE.*-1", r"HGETALL"],
            "fix": "使用分批获取或考虑其他数据结构"
        },
        "REDIS-012": {
            "severity": "info",
            "description": "Key 命名规范检查",
            "patterns": [r"set\s*\(\s*[\"'][a-zA-Z_]+[\"']"],
            "fix": "建议格式：模块:业务:标识，如 user:profile:123"
        },
        "REDIS-013": {
            "severity": "warning",
            "description": "大 Key 集合对象检查（建议控制在 5000 项以内）",
            "patterns": [r"LLEN|SADD|SCARD|ZCARD|HLEN"],
            "fix": "集合元素建议控制在 5000 以内"
        },
        "REDIS-014": {
            "severity": "warning",
            "description": "事务命令使用检查",
            "patterns": [r"multi\(\)", r"exec\(\)", r"watch\("],
            "fix": "确保正确处理事务边界"
        }
    }
    
    def __init__(self, scan_path: str, client_type: str = "lettuce"):
        self.scan_path = Path(scan_path)
        self.client_type = client_type
        self.findings: List[Dict] = []
        self.files_scanned = 0
    
    def scan_file(self, file_path: Path) -> None:
        """Scan a single Java file."""
        if not file_path.suffix in ['.java', '.yml', '.yaml', '.properties']:
            return
            
        self.files_scanned += 1
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            for rule_id, rule in self.RULES.items():
                for line_num, line in enumerate(lines, 1):
                    for pattern in rule['patterns']:
                        if re.search(pattern, line, re.IGNORECASE):
                            self.findings.append({
                                "rule_id": rule_id,
                                "severity": rule['severity'],
                                "file": str(file_path.relative_to(self.scan_path)),
                                "line": line_num,
                                "content": line.strip(),
                                "description": rule['description'],
                                "fix": rule['fix']
                            })
        except Exception as e:
            print(f"Warning: Failed to scan {file_path}: {e}", file=sys.stderr)
    
    def scan_directory(self) -> None:
        """Scan all Java files in the directory."""
        for root, dirs, files in os.walk(self.scan_path):
            # Skip test directories
            dirs[:] = [d for d in dirs if d not in ['test', 'target', 'build', '.git']]
            for file in files:
                self.scan_file(Path(root) / file)
    
    def generate_report(self) -> Dict:
        """Generate audit report."""
        severity_order = {"critical": 0, "warning": 1, "info": 2}
        self.findings.sort(key=lambda x: (severity_order.get(x['severity'], 3), x['file'], x['line']))
        
        stats = {
            "total": len(self.findings),
            "critical": len([f for f in self.findings if f['severity'] == 'critical']),
            "warning": len([f for f in self.findings if f['severity'] == 'warning']),
            "info": len([f for f in self.findings if f['severity'] == 'info'])
        }
        
        return {
            "status": "completed",
            "scan_path": str(self.scan_path),
            "files_scanned": self.files_scanned,
            "statistics": stats,
            "findings": self.findings
        }


def main():
    parser = argparse.ArgumentParser(description="Redis Java Client Code Audit Tool")
    parser.add_argument("--path", "-p", required=True, help="Path to scan")
    parser.add_argument("--client", "-c", default="lettuce", choices=["jedis", "lettuce", "redisson", "springdata"],
                        help="Redis client type")
    parser.add_argument("--output", "-o", default="json", choices=["json", "text"],
                        help="Output format")
    
    args = parser.parse_args()
    
    auditor = RedisCodeAuditor(args.path, args.client)
    auditor.scan_directory()
    report = auditor.generate_report()
    
    if args.output == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"=== Redis Code Audit Report ===")
        print(f"Path: {report['scan_path']}")
        print(f"Files scanned: {report['files_scanned']}")
        print(f"\nFindings: {report['statistics']['total']}")
        print(f"  Critical: {report['statistics']['critical']}")
        print(f"  Warning: {report['statistics']['warning']}")
        print(f"  Info: {report['statistics']['info']}")
        
        for finding in report['findings']:
            print(f"\n[{finding['rule_id']}] {finding['description']}")
            print(f"  File: {finding['file']}:{finding['line']}")
            print(f"  Content: {finding['content'][:80]}...")
            print(f"  Fix: {finding['fix']}")


if __name__ == "__main__":
    main()
