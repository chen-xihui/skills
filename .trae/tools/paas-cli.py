#!/usr/bin/env python3
"""paas-cli mock — simulates the real paas-cli for demo purposes."""

import sys
import json
import random
import os
from datetime import datetime, timedelta

# Force UTF-8 output on Windows to avoid GBK encoding errors with emoji
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

VERSION = "2.4.1"

# ── helpers ──────────────────────────────────────────────────────────────────

def _ts(offset_hours=0):
    return (datetime.now() + timedelta(hours=offset_hours)).strftime("%Y-%m-%dT%H:%M:%S+08:00")

def _project(args):
    for i, a in enumerate(args):
        if a.startswith("--project"):
            if "=" in a:
                return a.split("=", 1)[1]
            if i + 1 < len(args):
                return args[i + 1]
    return "j036x0"

def _env(args):
    for i, a in enumerate(args):
        if a.startswith("--env"):
            if "=" in a:
                return a.split("=", 1)[1]
            if i + 1 < len(args):
                return args[i + 1]
    return "DEV"

def _param(args, name, default=""):
    for i, a in enumerate(args):
        if a.startswith(f"--{name}"):
            if "=" in a:
                return a.split("=", 1)[1]
            if i + 1 < len(args):
                return args[i + 1]
    return default

# ── top-level commands ────────────────────────────────────────────────────────

def cmd_version(_args):
    print(f"paas-cli version {VERSION}")

def cmd_ping(_args):
    print("PONG  latency=3ms  server=paas-api.internal:8443")

def cmd_auth_check(args):
    pid = _project(args)
    print(f"✅ Project {pid} is authorized")
    print(f"   Role: admin")
    print(f"   Expires: {_ts(720)}")

# ── Nacos commands ────────────────────────────────────────────────────────────

def cmd_nacos_info(args):
    pid, env = _project(args), _env(args)
    print(f"Nacos Cluster Info — project={pid}  env={env}")
    print(f"  Cluster Name   : nacos-{pid}-{env.lower()}")
    print(f"  Status         : Running ✅")
    print(f"  Version        : 2.3.2")
    print(f"  Mode           : cluster (3 nodes)")
    print(f"  Leader         : nacos-0 ({_ts(-1)})")
    print(f"  Raft Term      : 42")
    print(f"  Services       : 28 registered")
    print(f"  Configs        : 156 items")
    print(f"  Endpoints      :")
    print(f"    - nacos-0.nacos-headless:8848  (healthy)")
    print(f"    - nacos-1.nacos-headless:8848  (healthy)")
    print(f"    - nacos-2.nacos-headless:8848  (healthy)")

def cmd_nacos_instances(args):
    pid, env = _project(args), _env(args)
    svc = _param(args, "service", "demo-service")
    print(f"Nacos Service Instances — service={svc}  project={pid}  env={env}")
    print(f"  Group: DEFAULT_GROUP")
    print(f"  Cluster: DEFAULT")
    print(f"  Healthy Instances: 2/2")
    print(f"  ┌──────────────────────────────┬────────┬───────────┬─────────┐")
    print(f"  │ IP                           │ Port   │ Healthy   │ Weight  │")
    print(f"  ├──────────────────────────────┼────────┼───────────┼─────────┤")
    print(f"  │ 10.244.3.{random.randint(10,99):<21} │ 8080   │ ✅ true   │ 1.0     │")
    print(f"  │ 10.244.4.{random.randint(10,99):<21} │ 8080   │ ✅ true   │ 1.0     │")
    print(f"  └──────────────────────────────┴────────┴───────────┴─────────┘")

def cmd_nacos_config_list(args):
    pid, env = _project(args), _env(args)
    print(f"Nacos Config List — project={pid}  env={env}")
    print(f"  Total: 3 configs")
    print(f"  ┌─────────────────────────────────────┬──────────────┬────────────┐")
    print(f"  │ Data ID                             │ Group        │ Version    │")
    print(f"  ├─────────────────────────────────────┼──────────────┼────────────┤")
    print(f"  │ application.yml                     │ DEFAULT_GROUP│ v3         │")
    print(f"  │ datasource.properties               │ DEFAULT_GROUP│ v1         │")
    print(f"  │ logback-spring.xml                  │ DEFAULT_GROUP│ v2         │")
    print(f"  └─────────────────────────────────────┴──────────────┴────────────┘")

def cmd_nacos_config(args):
    """Get Nacos connection config (used for client generation)."""
    pid, env = _project(args), _env(args)
    print(f"Nacos Connection Config — project={pid}  env={env}")
    print(f"  Server Addr : nacos-{pid}-{env.lower()}.paas.internal:8848")
    print(f"  Namespace   : {pid}-{env.lower()}")
    print(f"  Username    : nacos")
    print(f"  Password    : ******** (masked)")
    print(f"  Endpoint    : nacos-{pid}-{env.lower()}.paas.internal")
    print(f"  Port        : 8848")

def cmd_nacos_create(args):
    pid, env = _project(args), _env(args)
    svc = _param(args, "service", "demo-service")
    grp = _param(args, "group", "DEFAULT_GROUP")
    print(f"✅ Service created successfully")
    print(f"   Service : {svc}")
    print(f"   Group   : {grp}")
    print(f"   Project : {pid}")
    print(f"   Env     : {env}")

def cmd_nacos_scale(args):
    pid, env = _project(args), _env(args)
    n = _param(args, "replicas", "3")
    print(f"✅ Scale operation completed")
    print(f"   Cluster : nacos-{pid}-{env.lower()}")
    print(f"   Replicas: {n}")
    print(f"   Status  : Scaling in progress (expected 2min)")

def cmd_nacos_gray_publish(args):
    pid, env = _project(args), _env(args)
    cid = _param(args, "config", "application.yml")
    print(f"✅ Gray publish initiated")
    print(f"   Config  : {cid}")
    print(f"   Project : {pid}")
    print(f"   Env     : {env}")
    print(f"   Gray IP : 10.244.3.17")
    print(f"   Status  : Publishing...")

def cmd_nacos_upgrade(args):
    pid, env = _project(args), _env(args)
    ver = _param(args, "version", "2.4.0")
    print(f"✅ Upgrade initiated")
    print(f"   Cluster : nacos-{pid}-{env.lower()}")
    print(f"   Version : {ver}")
    print(f"   Status  : Rolling upgrade in progress")

def cmd_nacos_delete(args):
    pid, env = _project(args), _env(args)
    svc = _param(args, "service", "demo-service")
    print(f"✅ Service deleted")
    print(f"   Service : {svc}")
    print(f"   Project : {pid}")
    print(f"   Env     : {env}")

# ── Redis commands ────────────────────────────────────────────────────────────

def cmd_redis_info(args):
    pid, env = _project(args), _env(args)
    print(f"Redis Cluster Info — project={pid}  env={env}")
    print(f"  Cluster Name  : redis-{pid}-{env.lower()}")
    print(f"  Status        : Running ✅")
    print(f"  Version       : 7.2.4")
    print(f"  Mode          : cluster")
    print(f"  Nodes         : 6 (3 masters + 3 replicas)")
    print(f"  Memory Used   : 2.3 GB / 8 GB (28.8%)")
    print(f"  Connected     : 127 clients")
    print(f"  OPS           : 12,456 ops/sec")
    print(f"  Hit Rate      : 94.2%")
    print(f"  Keys          : 1,234,567")

def cmd_redis_nodes(args):
    pid, env = _project(args), _env(args)
    print(f"Redis Nodes — project={pid}  env={env}")
    print(f"  ┌────────────────────────────┬─────────┬──────────┬───────────┬────────────┐")
    print(f"  │ Node ID                    │ Role    │ Slots    │ Memory    │ Status     │")
    print(f"  ├────────────────────────────┼─────────┼──────────┼───────────┼────────────┤")
    print(f"  │ redis-0 (10.0.1.11:6379)  │ Master  │ 0-5460   │ 412 MB    │ ✅ online  │")
    print(f"  │ redis-1 (10.0.1.12:6379)  │ Master  │ 5461-10922│ 387 MB   │ ✅ online  │")
    print(f"  │ redis-2 (10.0.1.13:6379)  │ Master  │ 10923-16383│ 401 MB  │ ✅ online  │")
    print(f"  │ redis-3 (10.0.1.14:6379)  │ Replica │ 0-5460   │ 398 MB    │ ✅ online  │")
    print(f"  │ redis-4 (10.0.1.15:6379)  │ Replica │ 5461-10922│ 379 MB   │ ✅ online  │")
    print(f"  │ redis-5 (10.0.1.16:6379)  │ Replica │ 10923-16383│ 395 MB  │ ✅ online  │")
    print(f"  └────────────────────────────┴─────────┴──────────┴───────────┴────────────┘")

def cmd_redis_memory(args):
    pid, env = _project(args), _env(args)
    print(f"Redis Memory Detail — project={pid}  env={env}")
    print(f"  Used Memory        : 2.3 GB")
    print(f"  Used Memory Peak   : 3.1 GB")
    print(f"  Total System Memory: 16 GB")
    print(f"  Maxmemory Policy   : allkeys-lru")
    print(f"  Fragmentation Ratio: 1.12")
    print(f"  Expired Keys       : 45,678")
    print(f"  Evicted Keys       : 123")
    print(f"  Key Count          : 1,234,567")

def cmd_redis_config(args):
    """Get Redis connection config (used for client generation)."""
    pid, env = _project(args), _env(args)
    mode = _param(args, "mode", "cluster")
    print(f"Redis Connection Config — project={pid}  env={env}")
    print(f"  Mode       : {mode}")
    print(f"  Endpoints  :")
    if mode == "cluster":
        print(f"    - redis-0.redis-headless:6379 (master, slot 0-5460)")
        print(f"    - redis-1.redis-headless:6379 (master, slot 5461-10922)")
        print(f"    - redis-2.redis-headless:6379 (master, slot 10923-16383)")
    elif mode == "sentinel":
        print(f"    - sentinel-0.redis-headless:26379")
        print(f"    - sentinel-1.redis-headless:26379")
        print(f"    - sentinel-2.redis-headless:26379")
        print(f"  Master Name: mymaster")
    else:
        print(f"    - redis-0.redis-headless:6379")
    print(f"  Password   : ******** (masked)")
    print(f"  Database   : 0")

def cmd_redis_create(args):
    pid, env = _project(args), _env(args)
    mode = _param(args, "mode", "standalone")
    print(f"✅ Redis instance creation initiated")
    print(f"   Project : {pid}")
    print(f"   Env     : {env}")
    print(f"   Mode    : {mode}")
    print(f"   Status  : Provisioning (expected 5min)")

def cmd_redis_scale(args):
    pid, env = _project(args), _env(args)
    n = _param(args, "replicas", "3")
    print(f"✅ Scale operation completed")
    print(f"   Cluster  : redis-{pid}-{env.lower()}")
    print(f"   Replicas : {n}")
    print(f"   Status   : Rebalancing slots...")

def cmd_redis_slot_migrate(args):
    pid, env = _project(args), _env(args)
    frm = _param(args, "from", "redis-0")
    to = _param(args, "to", "redis-1")
    slots = _param(args, "slots", "1000")
    print(f"✅ Slot migration initiated")
    print(f"   From Node  : {frm}")
    print(f"   To Node    : {to}")
    print(f"   Slot Range : {slots}")
    print(f"   Status     : Migrating (estimated 3min)")

def cmd_redis_config_policy(args):
    pid, env = _project(args), _env(args)
    policy = _param(args, "maxmemory-policy", "allkeys-lru")
    print(f"✅ Memory policy updated")
    print(f"   Cluster : redis-{pid}-{env.lower()}")
    print(f"   Policy  : {policy}")

def cmd_redis_upgrade(args):
    pid, env = _project(args), _env(args)
    ver = _param(args, "version", "7.2.4")
    print(f"✅ Upgrade initiated")
    print(f"   Cluster : redis-{pid}-{env.lower()}")
    print(f"   Version : {ver}")

def cmd_redis_delete(args):
    pid, env = _project(args), _env(args)
    print(f"✅ Cluster deletion initiated")
    print(f"   Cluster : redis-{pid}-{env.lower()}")
    print(f"   Warning : All data will be permanently deleted")

# ── ES commands ───────────────────────────────────────────────────────────────

def cmd_es_info(args):
    pid, env = _project(args), _env(args)
    print(f"Elasticsearch Cluster Info — project={pid}  env={env}")
    print(f"  Cluster Name   : es-{pid}-{env.lower()}")
    print(f"  Status         : Green ✅")
    print(f"  Version        : 8.12.2")
    print(f"  Nodes          : 3 (3 data)")
    print(f"  Shards         : 48 primary, 48 replica")
    print(f"  Unassigned     : 0")
    print(f"  Indices        : 12")
    print(f"  Documents      : 5,678,901")
    print(f"  Store Size     : 23.4 GB")
    print(f"  Search Rate    : 1,234 queries/sec")

def cmd_es_disk_usage(args):
    pid, env = _project(args), _env(args)
    print(f"Elasticsearch Disk Usage — project={pid}  env={env}")
    print(f"  ┌────────────────────────────┬──────────┬──────────┬───────────┐")
    print(f"  │ Node                       │ Disk Use │ Total    │ Watermark │")
    print(f"  ├────────────────────────────┼──────────┼──────────┼───────────┤")
    print(f"  │ es-data-0 (10.0.2.11)     │ 62.3 GB  │ 100 GB   │ ✅ Normal │")
    print(f"  │ es-data-1 (10.0.2.12)     │ 58.7 GB  │ 100 GB   │ ✅ Normal │")
    print(f"  │ es-data-2 (10.0.2.13)     │ 64.1 GB  │ 100 GB   │ ✅ Normal │")
    print(f"  └────────────────────────────┴──────────┴──────────┴───────────┘")
    print(f"  Watermark Thresholds: low=85%  high=90%  flood=95%")

def cmd_es_indices(args):
    pid, env = _project(args), _env(args)
    print(f"Elasticsearch Indices — project={pid}  env={env}")
    print(f"  ┌──────────────────────────┬────────┬─────────┬──────────┬──────────┐")
    print(f"  │ Index                    │ Health │ Shards  │ Docs     │ Store    │")
    print(f"  ├──────────────────────────┼────────┼─────────┼──────────┼──────────┤")
    print(f"  │ log-2026-05              │ green  │ 3p 3r   │ 1,234K   │ 5.2 GB   │")
    print(f"  │ log-2026-04              │ green  │ 3p 3r   │ 987K     │ 4.1 GB   │")
    print(f"  │ product-catalog          │ green  │ 1p 1r   │ 56K      │ 120 MB   │")
    print(f"  │ order-events             │ green  │ 5p 5r   │ 2,345K   │ 8.7 GB   │")
    print(f"  │ .geoip_databases         │ green  │ 1p 0r   │ 412      │ 18 MB    │")
    print(f"  └──────────────────────────┴────────┴─────────┴──────────┴──────────┘")
    print(f"  Total: 12 indices, 48 primary shards, 0 unassigned shards")

def cmd_es_config(args):
    """Get ES connection config (used for client generation)."""
    pid, env = _project(args), _env(args)
    print(f"Elasticsearch Connection Config — project={pid}  env={env}")
    print(f"  Hosts     : https://es-{pid}-{env.lower()}.paas.internal:9200")
    print(f"  Scheme    : https")
    print(f"  Username  : elastic")
    print(f"  Password  : ******** (masked)")
    print(f"  Version   : 8.12.2")

def cmd_es_create_index(args):
    pid, env = _project(args), _env(args)
    name = _param(args, "name", "log-2026-05")
    shards = _param(args, "shards", "3")
    replicas = _param(args, "replicas", "1")
    print(f"✅ Index created successfully")
    print(f"   Index    : {name}")
    print(f"   Shards   : {shards} primary, {replicas} replica")
    print(f"   Project  : {pid}")
    print(f"   Env      : {env}")

def cmd_es_rollover(args):
    pid, env = _project(args), _env(args)
    alias = _param(args, "alias", "logs-write")
    print(f"✅ Rollover executed")
    print(f"   Alias       : {alias}")
    print(f"   Old Index   : log-2026-05-000001")
    print(f"   New Index   : log-2026-05-000002")
    print(f"   Conditions  : max_age=7d, max_size=50gb")

def cmd_es_force_merge(args):
    pid, env = _project(args), _env(args)
    idx = _param(args, "index", "log-2026-04")
    seg = _param(args, "max-segments", "1")
    print(f"✅ Force merge initiated")
    print(f"   Index       : {idx}")
    print(f"   Max Segments: {seg}")
    print(f"   Status      : Merging... (may take several minutes)")

def cmd_es_scale(args):
    pid, env = _project(args), _env(args)
    nodes = _param(args, "nodes", "5")
    print(f"✅ Scale operation initiated")
    print(f"   Cluster    : es-{pid}-{env.lower()}")
    print(f"   Target     : {nodes} nodes")
    print(f"   Status     : Adding nodes & rebalancing...")

def cmd_es_upgrade(args):
    pid, env = _project(args), _env(args)
    ver = _param(args, "version", "8.13.0")
    print(f"✅ Upgrade initiated")
    print(f"   Cluster : es-{pid}-{env.lower()}")
    print(f"   Version : {ver}")

def cmd_es_delete(args):
    pid, env = _project(args), _env(args)
    print(f"✅ Cluster deletion initiated")
    print(f"   Cluster : es-{pid}-{env.lower()}")
    print(f"   Warning : All indices and data will be permanently deleted")

# ── CRD-style commands (create/get/update/delete/switch + resource) ──────────

def _gateway_config(args):
    for a in args:
        if a.startswith("--gateway-config="):
            return a.split("=", 1)[1]
    return "config/gateway.yaml"

def _config_file(args):
    for i, a in enumerate(args):
        if a == "-f" and i + 1 < len(args):
            return args[i + 1]
    return ""

def cmd_crd(args):
    """Handle: paas-cli {action} {resource} --gateway-config=... -f ..."""
    if len(args) < 2:
        print("Error: missing action and resource")
        sys.exit(1)

    action = args[0]
    resource = args[1]
    gw = _gateway_config(args)
    cfg = _config_file(args)

    print(f"paas-cli {action} {resource}")
    print(f"  Gateway Config : {gw}")
    print(f"  Resource Config: {cfg}")
    print()

    # Generate resource-specific output
    _crd_output(action, resource, cfg)

def _crd_output(action, resource, cfg):
    now = _ts()
    name = cfg.split("/")[-1].replace(".yaml", "") if cfg else resource

    if action == "create":
        print(f"✅ Resource created successfully")
        print(f"   Resource : {resource}")
        print(f"   Name     : {name}")
        print(f"   Created  : {now}")
        print(f"   Status   : Reconciling")
        _crd_detail(resource)

    elif action == "get":
        print(f"📋 Resource details")
        print(f"   Resource : {resource}")
        print(f"   Name     : {name}")
        print(f"   Created  : {_ts(-24)}")
        print(f"   Updated  : {now}")
        print(f"   Status   : Ready ✅")
        _crd_detail(resource)

    elif action == "update":
        print(f"✅ Resource updated successfully")
        print(f"   Resource : {resource}")
        print(f"   Name     : {name}")
        print(f"   Updated  : {now}")
        print(f"   Status   : Reconciling")

    elif action == "delete":
        print(f"✅ Resource deleted successfully")
        print(f"   Resource : {resource}")
        print(f"   Name     : {name}")
        print(f"   Deleted  : {now}")

    elif action == "switch":
        print(f"✅ Switch operation completed")
        print(f"   Resource : {resource}")
        print(f"   Name     : {name}")
        print(f"   Switched : {now}")
        print(f"   Status   : Active")

def _crd_detail(resource):
    """Add resource-specific detail lines."""
    if "backup" in resource:
        print(f"   Backup ID    : bk-{random.randint(1000,9999)}")
        print(f"   Backup Size  : 256 MB")
        print(f"   Storage Path : /backup/nacos/2026-05-14/")
    elif "restore" in resource:
        print(f"   Restore From : bk-{random.randint(1000,9999)}")
        print(f"   Progress     : 0% (starting)")
    elif "accesstoken" in resource:
        print(f"   Token ID     : tk-{random.randint(100,999)}")
        print(f"   Expires      : {_ts(8760)}")
    elif "monitor" in resource:
        print(f"   Monitor Type : prometheus")
        print(f"   Endpoint     : http://prometheus.monitoring:9090")
    elif "networkpolicy" in resource:
        print(f"   Policy       : allow-internal")
        print(f"   CIDR         : 10.0.0.0/8")
    elif "activestrategy" in resource:
        print(f"   Strategy     : active-active")
        print(f"   Clusters     : 2")
        print(f"   Failover     : auto")
    elif "hotbackupstrategy" in resource:
        print(f"   Strategy     : hot-standby")
        print(f"   Sync Mode    : async")
    elif "unitstrategy" in resource:
        print(f"   Strategy     : unit-routing")
        print(f"   Unit Count   : 3")
    elif "esindex" in resource:
        print(f"   Shards       : 3 primary, 1 replica")
        print(f"   Mapping      : dynamic=strict")
    elif "esindextemplate" in resource:
        print(f"   Template     : logs-template")
        print(f"   Priority     : 100")
    elif "esclusterip" in resource:
        print(f"   IP           : 10.96.{random.randint(1,254)}.{random.randint(1,254)}")
        print(f"   Type         : ClusterIP")
    elif "eslb" in resource:
        print(f"   LB Type      : LoadBalancer")
        print(f"   External IP  : 192.168.{random.randint(1,254)}.{random.randint(1,254)}")
    elif "esclusterreplicas" in resource:
        print(f"   Replicas     : 5")
        print(f"   Rebalancing  : in progress")

# ── dispatch ──────────────────────────────────────────────────────────────────

NACOS_SUB = {
    "info": cmd_nacos_info,
    "instances": cmd_nacos_instances,
    "config-list": cmd_nacos_config_list,
    "config": cmd_nacos_config,
    "create": cmd_nacos_create,
    "scale": cmd_nacos_scale,
    "gray-publish": cmd_nacos_gray_publish,
    "upgrade": cmd_nacos_upgrade,
    "delete": cmd_nacos_delete,
}

REDIS_SUB = {
    "info": cmd_redis_info,
    "nodes": cmd_redis_nodes,
    "memory": cmd_redis_memory,
    "config": cmd_redis_config,
    "create": cmd_redis_create,
    "scale": cmd_redis_scale,
    "slot-migrate": cmd_redis_slot_migrate,
    "upgrade": cmd_redis_upgrade,
    "delete": cmd_redis_delete,
}

ES_SUB = {
    "info": cmd_es_info,
    "disk-usage": cmd_es_disk_usage,
    "indices": cmd_es_indices,
    "config": cmd_es_config,
    "create-index": cmd_es_create_index,
    "rollover": cmd_es_rollover,
    "force-merge": cmd_es_force_merge,
    "scale": cmd_es_scale,
    "upgrade": cmd_es_upgrade,
    "delete": cmd_es_delete,
}

CRD_ACTIONS = {"create", "get", "update", "delete", "switch"}

def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print("paas-cli — PaaS middleware operation CLI (mock)")
        print()
        print("Usage:")
        print("  paas-cli --version")
        print("  paas-cli ping")
        print("  paas-cli auth check --project <id>")
        print("  paas-cli <middleware> <subcommand> [options]")
        print("  paas-cli <action> <resource> --gateway-config=... -f ...")
        print()
        print("Middlewares: nacos, redis, es")
        print("CRD Actions: create, get, update, delete, switch")
        sys.exit(0)

    cmd = args[0]
    rest = args[1:]

    if cmd == "--version":
        cmd_version(rest)
    elif cmd == "ping":
        cmd_ping(rest)
    elif cmd == "auth":
        if rest and rest[0] == "check":
            cmd_auth_check(rest[1:])
        else:
            print("Unknown auth subcommand")
    elif cmd == "nacos":
        if rest and rest[0] in NACOS_SUB:
            # Check if the subcommand has --maxmemory-policy (Redis config override)
            NACOS_SUB[rest[0]](rest[1:])
        else:
            print(f"Unknown nacos subcommand: {rest[0] if rest else '(none)'}")
    elif cmd == "redis":
        if rest:
            sub = rest[0]
            sub_rest = rest[1:]
            # Special case: redis config --maxmemory-policy → policy change
            if sub == "config" and "--maxmemory-policy" in " ".join(sub_rest):
                cmd_redis_config_policy(sub_rest)
            elif sub in REDIS_SUB:
                REDIS_SUB[sub](sub_rest)
            else:
                print(f"Unknown redis subcommand: {sub}")
        else:
            print("Missing redis subcommand")
    elif cmd == "es":
        if rest and rest[0] in ES_SUB:
            ES_SUB[rest[0]](rest[1:])
        else:
            print(f"Unknown es subcommand: {rest[0] if rest else '(none)'}")
    elif cmd in CRD_ACTIONS:
        cmd_crd(args)
    else:
        print(f"Unknown command: {cmd}")
        print("Run 'paas-cli help' for usage information.")

if __name__ == "__main__":
    main()
