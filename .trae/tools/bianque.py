#!/usr/bin/env python3
"""bianque mock — simulates the bianque diagnostic platform for demo purposes."""

import sys
import json
import random
from datetime import datetime, timedelta

# Force UTF-8 output on Windows to avoid GBK encoding errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

def _ts(offset_hours=0):
    return (datetime.now() + timedelta(hours=offset_hours)).strftime("%Y-%m-%dT%H:%M:%S+08:00")

def _param(args, name, default=""):
    for i, a in enumerate(args):
        if a.startswith(f"--{name}"):
            if "=" in a:
                return a.split("=", 1)[1]
            if i + 1 < len(args):
                return args[i + 1]
    return default

# ── Nacos diagnostics ─────────────────────────────────────────────────────────

def diag_nacos(checks, pid, env):
    findings = []
    for chk in checks:
        if chk == "health":
            findings.append({
                "type": "health",
                "severity": "info",
                "message": f"Nacos cluster is healthy (Green), 3/3 nodes running",
                "details": {
                    "cluster": f"nacos-{pid}-{env.lower()}",
                    "status": "Green",
                    "nodes": 3,
                    "leader": "nacos-0",
                    "raft_term": 42,
                }
            })
        elif chk == "raft":
            findings.append({
                "type": "raft",
                "severity": "info",
                "message": "Raft consensus is stable, leader nacos-0, term 42",
                "details": {
                    "leader": "nacos-0",
                    "term": 42,
                    "voted_for": "nacos-0",
                    "peers": ["nacos-0", "nacos-1", "nacos-2"],
                }
            })
        elif chk == "log":
            findings.append({
                "type": "log",
                "severity": "info",
                "message": "No critical errors in recent logs (last 1h)",
                "details": {
                    "error_count_1h": 0,
                    "warn_count_1h": 3,
                    "last_error": None,
                    "recent_warnings": [
                        "Slow config publish detected (2.3s)",
                        "Connection pool near capacity (85%)",
                        "DNS resolution timeout for service xyz",
                    ]
                }
            })
    return findings

# ── Redis diagnostics ─────────────────────────────────────────────────────────

def diag_redis(checks, pid, env):
    findings = []
    for chk in checks:
        if chk == "slowlog":
            findings.append({
                "type": "slowlog",
                "severity": "warning",
                "message": "3 slow queries detected in last hour (>100ms)",
                "details": {
                    "slow_query_count": 3,
                    "top_slow_queries": [
                        {"command": "KEYS user:*", "duration_us": 523000, "timestamp": _ts(-0.5)},
                        {"command": "SMEMBERS big_set", "duration_us": 312000, "timestamp": _ts(-1.2)},
                        {"command": "SORT scores BY nosort GET # GET value_*", "duration_us": 198000, "timestamp": _ts(-2.1)},
                    ]
                }
            })
        elif chk == "memory":
            findings.append({
                "type": "memory",
                "severity": "info",
                "message": "Memory usage normal (28.8%), fragmentation ratio 1.12",
                "details": {
                    "used_memory": "2.3 GB",
                    "total_memory": "8 GB",
                    "usage_percent": 28.8,
                    "fragmentation_ratio": 1.12,
                    "evicted_keys": 123,
                    "expired_keys": 45678,
                }
            })
        elif chk == "replication":
            findings.append({
                "type": "replication",
                "severity": "info",
                "message": "Replication is healthy, all replicas in sync",
                "details": {
                    "master": "redis-0",
                    "replicas": ["redis-3", "redis-4", "redis-5"],
                    "offset_diff": [12, 8, 15],
                    "persistence": "RDB (last save: 5min ago)",
                    "failover_history": [],
                }
            })
    return findings

# ── ES diagnostics ────────────────────────────────────────────────────────────

def diag_es(checks, pid, env):
    findings = []
    for chk in checks:
        if chk == "cluster-health":
            findings.append({
                "type": "cluster-health",
                "severity": "info",
                "message": "Cluster status Green, all shards allocated",
                "details": {
                    "cluster": f"es-{pid}-{env.lower()}",
                    "status": "Green",
                    "nodes": 3,
                    "primary_shards": 48,
                    "replica_shards": 48,
                    "unassigned_shards": 0,
                }
            })
        elif chk == "shard":
            findings.append({
                "type": "shard",
                "severity": "info",
                "message": "No unassigned shards, all 96 shards allocated",
                "details": {
                    "total_shards": 96,
                    "unassigned": 0,
                    "relocating": 0,
                    "initializing": 0,
                }
            })
        elif chk == "cpu":
            findings.append({
                "type": "cpu",
                "severity": "warning",
                "message": "Node es-data-2 CPU usage at 82%, hot thread: search",
                "details": {
                    "nodes": [
                        {"name": "es-data-0", "cpu": "45%", "hot_thread": "merge"},
                        {"name": "es-data-1", "cpu": "38%", "hot_thread": "index"},
                        {"name": "es-data-2", "cpu": "82%", "hot_thread": "search"},
                    ]
                }
            })
        elif chk == "watermark":
            findings.append({
                "type": "watermark",
                "severity": "info",
                "message": "All nodes below disk watermarks, no write rejections",
                "details": {
                    "nodes": [
                        {"name": "es-data-0", "disk_percent": 62.3, "status": "normal"},
                        {"name": "es-data-1", "disk_percent": 58.7, "status": "normal"},
                        {"name": "es-data-2", "disk_percent": 64.1, "status": "normal"},
                    ],
                    "write_rejections": 0,
                    "thread_pool_rejections": 0,
                }
            })
    return findings

# ── dispatch ──────────────────────────────────────────────────────────────────

DIAG_DISPATCH = {
    "nacos": diag_nacos,
    "redis": diag_redis,
    "es": diag_es,
}

def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print("bianque — Middleware diagnostic platform (mock)")
        print()
        print("Usage:")
        print("  bianque diagnose --middleware <type> --project <id> --env <env> --check <items>")
        print()
        print("Middleware types: nacos, redis, es")
        sys.exit(0)

    if args[0] != "diagnose":
        print(f"Unknown bianque command: {args[0]}")
        sys.exit(1)

    mw = _param(args[1:], "middleware", "")
    pid = _param(args[1:], "project", "j036x0")
    env = _param(args[1:], "env", "DEV")
    check_str = _param(args[1:], "check", "")
    checks = [c.strip() for c in check_str.split(",") if c.strip()]

    if mw not in DIAG_DISPATCH:
        print(f"Error: unknown middleware '{mw}'. Supported: nacos, redis, es")
        sys.exit(1)

    findings = DIAG_DISPATCH[mw](checks, pid, env)

    # Determine overall severity
    sev_order = {"critical": 0, "warning": 1, "info": 2}
    worst = "info"
    for f in findings:
        if sev_order.get(f["severity"], 2) < sev_order.get(worst, 2):
            worst = f["severity"]

    result = {
        "status": "success",
        "timestamp": _ts(),
        "middleware": mw,
        "project": pid,
        "env": env,
        "overall_severity": worst,
        "findings": findings,
        "logs": [
            f"[{_ts(-0.1)}] Diagnostic check started: {', '.join(checks)}",
            f"[{_ts()}] Diagnostic check completed successfully",
        ],
        "suggestions": _suggestions(mw, worst),
    }

    # Print as formatted JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))

def _suggestions(mw, severity):
    if severity == "info":
        return ["No action required. All checks passed."]
    elif mw == "redis":
        return [
            "Review slow queries and optimize KEYS/SMEMBERS usage",
            "Consider using SCAN instead of KEYS for large key spaces",
        ]
    elif mw == "es":
        return [
            "Monitor CPU usage on es-data-2 node",
            "Consider adding more data nodes to distribute search load",
        ]
    else:
        return ["Review warnings and take action as needed."]

if __name__ == "__main__":
    main()
