#!/usr/bin/env python3
"""bianque mock — simulates the bianque CLI tool for demo purposes.

Command format (matches the actual bianque CLI):
  bianque <middleware> <subcommand> [options]

Supported commands:
  bianque elasticsearch check   -n <ns> -i <inst> [-v] [-o <num>]
  bianque elasticsearch client  -n <ns> -i <inst> -k <key> -v <val> [-u <user>] [-p <pass>]
  bianque nacos check           -n <ns> -i <inst> [-v] [-l <num>]
  bianque nacos client          -n <ns> -i <inst> [-u <user>] [-p <pass>]
  bianque redis check           -n <ns> -i <inst> -t <type> [-v] [-l <num>]
  bianque redis client          -n <ns> -i <inst> -t <type> [-a <pass>]
  bianque redis updateRenameConfig -n <ns> -i <inst> -t <type> [-a]
  bianque redis clusterUpgradeRecover -n <ns> -i <inst> -o <op> -t <type>

Global option: --token-file <path>
"""

import sys
import json
from datetime import datetime, timedelta

# Force UTF-8 output on Windows to avoid GBK encoding errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def _ts(offset_hours=0):
    return (datetime.now() + timedelta(hours=offset_hours)).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _param(args, name, short=None, default=""):
    """Parse --name or -short value from args list."""
    for i, a in enumerate(args):
        if a == f"--{name}" or (short and a == short):
            if i + 1 < len(args):
                return args[i + 1]
        if a.startswith(f"--{name}="):
            return a.split("=", 1)[1]
    return default


def _flag(args, name, short=None):
    """Check if --name or -short flag is present (boolean)."""
    for a in args:
        if a == f"--{name}" or (short and a == short):
            return True
    return False


# ── Elasticsearch check ───────────────────────────────────────────────────────

def es_check(namespace, instance, verbose, log_lines):
    findings = []

    # Cluster health
    findings.append({
        "type": "cluster-health",
        "severity": "info",
        "message": "Cluster status Green, all shards allocated",
        "details": {
            "cluster": f"es-{namespace}-{instance}",
            "status": "Green",
            "nodes": 3,
            "primary_shards": 48,
            "replica_shards": 48,
            "unassigned_shards": 0,
        }
    })

    # Shard status
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

    # CPU hotspot
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

    # Watermark / write rejection
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

    # Index health
    findings.append({
        "type": "index-health",
        "severity": "info",
        "message": "All indices healthy, replica shards assigned",
        "details": {
            "total_indices": 12,
            "unhealthy_indices": 0,
            "max_segments_per_index": 23,
        }
    })

    result = {
        "status": "success",
        "timestamp": _ts(),
        "command": "bianque elasticsearch check",
        "namespace": namespace,
        "instance": instance,
        "verbose": verbose,
        "log_lines": log_lines,
        "overall_severity": _worst_severity(findings),
        "findings": findings if verbose else [f for f in findings if f["severity"] != "info"],
        "logs": _check_logs(log_lines, "elasticsearch"),
        "suggestions": _es_suggestions(_worst_severity(findings)),
    }

    if not verbose:
        result["note"] = "Run with -v true to see all details"

    return result


# ── Elasticsearch client ──────────────────────────────────────────────────────

def es_client(namespace, instance, key, value, user, password):
    return {
        "status": "success",
        "timestamp": _ts(),
        "command": "bianque elasticsearch client",
        "namespace": namespace,
        "instance": instance,
        "operation": "write_and_read",
        "user": user,
        "result": {
            "write": {
                "index": f"{instance}-test-index",
                "id": "mock-doc-001",
                "key": key,
                "value": value,
                "result": "created",
            },
            "read": {
                "found": True,
                "key": key,
                "value": value,
                "_source": {key: value, "timestamp": _ts()},
            }
        },
        "message": f"Successfully wrote and read key '{key}' from ES instance '{instance}'",
    }


# ── Nacos check ───────────────────────────────────────────────────────────────

def nacos_check(namespace, instance, verbose, log_lines):
    findings = []

    # Cluster health
    findings.append({
        "type": "health",
        "severity": "info",
        "message": f"Nacos cluster is healthy (Green), 3/3 nodes running",
        "details": {
            "cluster": f"nacos-{namespace}-{instance}",
            "status": "Green",
            "nodes": 3,
            "leader": "nacos-0",
            "raft_term": 42,
        }
    })

    # Raft consensus
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

    # Log analysis
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

    # Client connectivity
    findings.append({
        "type": "connectivity",
        "severity": "info",
        "message": "Client connectivity check passed",
        "details": {
            "reachable": True,
            "latency_ms": 12,
        }
    })

    result = {
        "status": "success",
        "timestamp": _ts(),
        "command": "bianque nacos check",
        "namespace": namespace,
        "instance": instance,
        "verbose": verbose,
        "log_lines": log_lines,
        "overall_severity": _worst_severity(findings),
        "findings": findings if verbose else [f for f in findings if f["severity"] != "info"],
        "logs": _check_logs(log_lines, "nacos"),
        "suggestions": ["No action required. All checks passed."],
    }

    if not verbose:
        result["note"] = "Run with -v true to see all details"

    return result


# ── Nacos client ──────────────────────────────────────────────────────────────

def nacos_client(namespace, instance, user, password):
    return {
        "status": "success",
        "timestamp": _ts(),
        "command": "bianque nacos client",
        "namespace": namespace,
        "instance": instance,
        "user": user,
        "operation": "connect_and_verify",
        "result": {
            "connected": True,
            "server_addr": f"nacos-{instance}.{namespace}.svc:8848",
            "auth_passed": True,
            "services_registered": 5,
            "configs_readable": True,
        },
        "message": f"Successfully connected to Nacos instance '{instance}' as user '{user}'",
    }


# ── Redis check ───────────────────────────────────────────────────────────────

def redis_check(namespace, instance, rtype, verbose, log_lines):
    findings = []

    # Slow query analysis
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

    # Memory fragmentation
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

    # Replication
    if rtype == "sentinel":
        findings.append({
            "type": "replication",
            "severity": "info",
            "message": "Replication is healthy, master redis-0 with 2 replicas",
            "details": {
                "master": "redis-0",
                "replicas": ["redis-3", "redis-4"],
                "offset_diff": [12, 8],
                "persistence": "RDB (last save: 5min ago)",
                "failover_history": [],
            }
        })
        findings.append({
            "type": "failover",
            "severity": "info",
            "message": "No recent failover events, Sentinel monitoring stable",
            "details": {
                "sentinel_count": 3,
                "master_down": False,
                "last_failover": None,
            }
        })
    elif rtype == "cluster":
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
        findings.append({
            "type": "cluster-state",
            "severity": "info",
            "message": "Cluster state OK, 16384/16384 slots covered",
            "details": {
                "cluster_state": "ok",
                "slots_assigned": 16384,
                "slots_ok": 16384,
                "slots_pfail": 0,
                "slots_fail": 0,
            }
        })

    # Persistence
    findings.append({
        "type": "persistence",
        "severity": "info",
        "message": "RDB last save 5min ago, AOF not enabled",
        "details": {
            "rdb_last_save_time": _ts(-0.08),
            "rdb_status": "ok",
            "aof_enabled": False,
        }
    })

    result = {
        "status": "success",
        "timestamp": _ts(),
        "command": "bianque redis check",
        "namespace": namespace,
        "instance": instance,
        "type": rtype,
        "verbose": verbose,
        "log_lines": log_lines,
        "overall_severity": _worst_severity(findings),
        "findings": findings if verbose else [f for f in findings if f["severity"] != "info"],
        "logs": _check_logs(log_lines, "redis"),
        "suggestions": _redis_suggestions(_worst_severity(findings)),
    }

    if not verbose:
        result["note"] = "Run with -v true to see all details"

    return result


# ── Redis client ──────────────────────────────────────────────────────────────

def redis_client(namespace, instance, rtype, auth):
    return {
        "status": "success",
        "timestamp": _ts(),
        "command": "bianque redis client",
        "namespace": namespace,
        "instance": instance,
        "type": rtype,
        "operation": "connect_and_verify",
        "result": {
            "connected": True,
            "mode": rtype,
            "ping": "PONG",
            "set_test": {"key": "bianque-test-key", "value": "ok", "result": "OK"},
            "get_test": {"key": "bianque-test-key", "value": "ok", "result": "found"},
        },
        "message": f"Successfully connected to Redis instance '{instance}' ({rtype} mode)",
    }


# ── Redis updateRenameConfig ──────────────────────────────────────────────────

def redis_update_rename_config(namespace, instance, rtype, all_ns):
    return {
        "status": "success",
        "timestamp": _ts(),
        "command": "bianque redis updateRenameConfig",
        "namespace": namespace,
        "instance": instance,
        "type": rtype,
        "all_namespaces": all_ns,
        "result": {
            "updated": True,
            "config_map": f"redis-{instance}-rename-config",
            "applied_namespaces": "all" if all_ns else namespace,
        },
        "message": f"Rename-command config updated for Redis instance '{instance}' ({rtype} mode)",
    }


# ── Redis clusterUpgradeRecover ───────────────────────────────────────────────

def redis_cluster_upgrade_recover(namespace, instance, operation, rtype):
    return {
        "status": "success",
        "timestamp": _ts(),
        "command": "bianque redis clusterUpgradeRecover",
        "namespace": namespace,
        "instance": instance,
        "type": rtype,
        "operation": operation,
        "result": {
            "recovered": True,
            "operation_name": operation,
            "previous_status": "Paused",
            "current_status": "Running",
        },
        "message": f"Upgrade operation '{operation}' recovered for Redis instance '{instance}'",
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _worst_severity(findings):
    sev_order = {"critical": 0, "warning": 1, "info": 2}
    worst = "info"
    for f in findings:
        if sev_order.get(f["severity"], 2) < sev_order.get(worst, 2):
            worst = f["severity"]
    return worst


def _check_logs(log_lines, middleware):
    logs = [
        f"[{_ts(-0.1)}] bianque {middleware} check started",
    ]
    if log_lines and int(log_lines) > 0:
        sample_logs = {
            "elasticsearch": [
                f"[{_ts(-2)}] [INFO] Cluster state updated: green",
                f"[{_ts(-5)}] [WARN] Shard allocation slow on node es-data-2",
            ],
            "nacos": [
                f"[{_ts(-3)}] [INFO] Raft leader heartbeat OK",
                f"[{_ts(-8)}] [WARN] Config publish latency 2.3s",
            ],
            "redis": [
                f"[{_ts(-1)}] [INFO] Replication offset sync complete",
                f"[{_ts(-4)}] [WARN] Slow command detected: KEYS user:*",
            ],
        }
        logs.extend(sample_logs.get(middleware, [])[:int(log_lines)])
    logs.append(f"[{_ts()}] bianque {middleware} check completed successfully")
    return logs


def _es_suggestions(severity):
    if severity == "info":
        return ["No action required. All checks passed."]
    return [
        "Monitor CPU usage on es-data-2 node",
        "Consider adding more data nodes to distribute search load",
    ]


def _redis_suggestions(severity):
    if severity == "info":
        return ["No action required. All checks passed."]
    return [
        "Review slow queries and optimize KEYS/SMEMBERS usage",
        "Consider using SCAN instead of KEYS for large key spaces",
    ]


# ── Main dispatch ─────────────────────────────────────────────────────────────

MIDDLEWARES = {"elasticsearch", "nacos", "redis"}

ES_SUBCOMMANDS = {"check", "client"}
NACOS_SUBCOMMANDS = {"check", "client"}
REDIS_SUBCOMMANDS = {"check", "client", "updateRenameConfig", "clusterUpgradeRecover"}


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print("bianque — Middleware diagnostic platform (mock)")
        print()
        print("Usage:")
        print("  bianque <middleware> <subcommand> [options]")
        print()
        print("Middleware types: elasticsearch, nacos, redis")
        print()
        print("Global options:")
        print("  --token-file <path>   Specify token file for authentication")
        print()
        print("Elasticsearch:")
        print("  bianque elasticsearch check  -n <namespace> -i <instance> [-v] [-o <num>]")
        print("  bianque elasticsearch client -n <namespace> -i <instance> -k <key> -v <value> [-u <user>] [-p <password>]")
        print()
        print("Nacos:")
        print("  bianque nacos check  -n <namespace> -i <instance> [-v] [-l <num>]")
        print("  bianque nacos client -n <namespace> -i <instance> [-u <user>] [-p <password>]")
        print()
        print("Redis:")
        print("  bianque redis check               -n <namespace> -i <instance> -t <type> [-v] [-l <num>]")
        print("  bianque redis client              -n <namespace> -i <instance> -t <type> [-a <password>]")
        print("  bianque redis updateRenameConfig  -n <namespace> -i <instance> -t <type> [-a]")
        print("  bianque redis clusterUpgradeRecover -n <namespace> -i <instance> -o <operation> -t <type>")
        sys.exit(0)

    # Parse middleware
    mw = args[0]
    if mw not in MIDDLEWARES:
        print(f"Error: unknown middleware '{mw}'. Supported: {', '.join(sorted(MIDDLEWARES))}")
        sys.exit(1)

    # Parse subcommand
    if len(args) < 2:
        print(f"Error: missing subcommand for '{mw}'")
        sys.exit(1)

    subcmd = args[1]
    rest = args[2:]

    # ── Elasticsearch ──────────────────────────────────────────────────────
    if mw == "elasticsearch":
        if subcmd not in ES_SUBCOMMANDS:
            print(f"Error: unknown subcommand '{subcmd}' for elasticsearch. Supported: {', '.join(sorted(ES_SUBCOMMANDS))}")
            sys.exit(1)

        if subcmd == "check":
            namespace = _param(rest, "namespace", "-n")
            instance = _param(rest, "instance", "-i")
            verbose = _flag(rest, "verb", "-v")
            log_lines = _param(rest, "log-lines", "-o", "0")

            if not namespace or not instance:
                print("Error: --namespace/-n and --instance/-i are required")
                sys.exit(1)

            result = es_check(namespace, instance, verbose, log_lines)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif subcmd == "client":
            namespace = _param(rest, "namespace", "-n")
            instance = _param(rest, "instance", "-i")
            key = _param(rest, "key", "-k")
            value = _param(rest, "value", "-v")
            user = _param(rest, "user", "-u", "elastic")
            password = _param(rest, "password", "-p", "")

            if not namespace or not instance:
                print("Error: --namespace/-n and --instance/-i are required")
                sys.exit(1)
            if not key:
                print("Error: --key/-k is required")
                sys.exit(1)

            result = es_client(namespace, instance, key, value, user, password)
            print(json.dumps(result, indent=2, ensure_ascii=False))

    # ── Nacos ──────────────────────────────────────────────────────────────
    elif mw == "nacos":
        if subcmd not in NACOS_SUBCOMMANDS:
            print(f"Error: unknown subcommand '{subcmd}' for nacos. Supported: {', '.join(sorted(NACOS_SUBCOMMANDS))}")
            sys.exit(1)

        if subcmd == "check":
            namespace = _param(rest, "namespace", "-n")
            instance = _param(rest, "instance", "-i")
            verbose = _flag(rest, "verb", "-v")
            log_lines = _param(rest, "log-lines", "-l", "0")

            if not namespace or not instance:
                print("Error: --namespace/-n and --instance/-i are required")
                sys.exit(1)

            result = nacos_check(namespace, instance, verbose, log_lines)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif subcmd == "client":
            namespace = _param(rest, "namespace", "-n")
            instance = _param(rest, "instance", "-i")
            user = _param(rest, "user", "-u", "admin")
            password = _param(rest, "password", "-p", "")

            if not namespace or not instance:
                print("Error: --namespace/-n and --instance/-i are required")
                sys.exit(1)

            result = nacos_client(namespace, instance, user, password)
            print(json.dumps(result, indent=2, ensure_ascii=False))

    # ── Redis ──────────────────────────────────────────────────────────────
    elif mw == "redis":
        if subcmd not in REDIS_SUBCOMMANDS:
            print(f"Error: unknown subcommand '{subcmd}' for redis. Supported: {', '.join(sorted(REDIS_SUBCOMMANDS))}")
            sys.exit(1)

        if subcmd == "check":
            namespace = _param(rest, "namespace", "-n")
            instance = _param(rest, "instance", "-i")
            rtype = _param(rest, "type", "-t")
            verbose = _flag(rest, "verb", "-v")
            log_lines = _param(rest, "log-lines", "-l", "0")

            if not namespace or not instance:
                print("Error: --namespace/-n and --instance/-i are required")
                sys.exit(1)
            if rtype not in ("cluster", "sentinel"):
                print("Error: --type/-t is required and must be 'cluster' or 'sentinel'")
                sys.exit(1)

            result = redis_check(namespace, instance, rtype, verbose, log_lines)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif subcmd == "client":
            namespace = _param(rest, "namespace", "-n")
            instance = _param(rest, "instance", "-i")
            rtype = _param(rest, "type", "-t")
            auth = _param(rest, "auth", "-a", "")

            if not namespace or not instance:
                print("Error: --namespace/-n and --instance/-i are required")
                sys.exit(1)
            if rtype not in ("cluster", "sentinel"):
                print("Error: --type/-t is required and must be 'cluster' or 'sentinel'")
                sys.exit(1)

            result = redis_client(namespace, instance, rtype, auth)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif subcmd == "updateRenameConfig":
            namespace = _param(rest, "namespace", "-n")
            instance = _param(rest, "instance", "-i")
            rtype = _param(rest, "type", "-t")
            all_ns = _flag(rest, "all-namespaces", "-a")

            if not namespace or not instance:
                print("Error: --namespace/-n and --instance/-i are required")
                sys.exit(1)
            if rtype not in ("cluster", "sentinel"):
                print("Error: --type/-t is required and must be 'cluster' or 'sentinel'")
                sys.exit(1)

            result = redis_update_rename_config(namespace, instance, rtype, all_ns)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif subcmd == "clusterUpgradeRecover":
            namespace = _param(rest, "namespace", "-n")
            instance = _param(rest, "instance", "-i")
            operation = _param(rest, "operation", "-o")
            rtype = _param(rest, "type", "-t")

            if not namespace or not instance:
                print("Error: --namespace/-n and --instance/-i are required")
                sys.exit(1)
            if not operation:
                print("Error: --operation/-o is required")
                sys.exit(1)
            if rtype not in ("cluster", "sentinel"):
                print("Error: --type/-t is required and must be 'cluster' or 'sentinel'")
                sys.exit(1)

            result = redis_cluster_upgrade_recover(namespace, instance, operation, rtype)
            print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
