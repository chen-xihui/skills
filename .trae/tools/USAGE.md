# Mock CLI Tools 使用命令文档

本目录包含两个 mock 命令行工具，用于中间件 Skill 演示场景。

## 前置准备

将本目录加入 PATH（PowerShell）：

```powershell
$env:PATH = "D:\Users\chenxihui\skill\.trae\tools;" + $env:PATH
$env:PATHEXT = ".CMD;.PY;" + $env:PATHEXT
```

之后即可在任意位置直接使用 `paas-cli` 和 `bianque` 命令。

---

## 一、paas-cli

PaaS 中间件运维 CLI 工具（mock 版本 v2.4.1）。

### 1.1 通用命令

| 命令 | 说明 |
|------|------|
| `paas-cli --version` | 查看版本号 |
| `paas-cli ping` | 测试网关连通性 |
| `paas-cli auth check --project <id>` | 检查项目授权状态 |

**示例：**

```bash
paas-cli --version
paas-cli ping
paas-cli auth check --project j036x0
```

### 1.2 Nacos 命令

格式：`paas-cli nacos <subcommand> --project <id> --env <env>`

| 子命令 | 说明 | 额外参数 |
|--------|------|----------|
| `info` | 查看集群信息 | — |
| `instances` | 查看服务实例 | `--service <name>` |
| `config-list` | 查看配置列表 | — |
| `config` | 查看连接配置 | — |
| `create` | 创建服务 | `--service <name>` `--group <group>` |
| `scale` | 扩缩容 | `--replicas <n>` |
| `gray-publish` | 灰度发布 | `--config <dataId>` |
| `upgrade` | 版本升级 | `--version <ver>` |
| `delete` | 删除服务 | `--service <name>` |

**示例：**

```bash
paas-cli nacos info --project j036x0 --env DEV
paas-cli nacos instances --project j036x0 --env DEV --service demo-service
paas-cli nacos config-list --project j036x0 --env DEV
paas-cli nacos config --project j036x0 --env DEV
paas-cli nacos create --project j036x0 --env DEV --service demo-service --group DEFAULT_GROUP
paas-cli nacos scale --project j036x0 --env DEV --replicas 5
paas-cli nacos gray-publish --project j036x0 --env DEV --config application.yml
paas-cli nacos upgrade --project j036x0 --env DEV --version 2.4.0
paas-cli nacos delete --project j036x0 --env DEV --service demo-service
```

### 1.3 Redis 命令

格式：`paas-cli redis <subcommand> --project <id> --env <env>`

| 子命令 | 说明 | 额外参数 |
|--------|------|----------|
| `info` | 查看集群信息 | — |
| `nodes` | 查看节点列表 | — |
| `memory` | 查看内存详情 | — |
| `config` | 查看连接配置 | `--mode cluster\|sentinel\|standalone` |
| `config` | 修改内存策略 | `--maxmemory-policy <policy>` |
| `create` | 创建实例 | `--mode standalone\|cluster` |
| `scale` | 扩缩容 | `--replicas <n>` |
| `slot-migrate` | 槽位迁移 | `--from <node>` `--to <node>` `--slots <n>` |
| `upgrade` | 版本升级 | `--version <ver>` |
| `delete` | 删除集群 | — |

**示例：**

```bash
paas-cli redis info --project j036x0 --env DEV
paas-cli redis nodes --project j036x0 --env DEV
paas-cli redis memory --project j036x0 --env DEV
paas-cli redis config --project j036x0 --env DEV --mode cluster
paas-cli redis config --project j036x0 --env DEV --maxmemory-policy allkeys-lru
paas-cli redis create --project j036x0 --env DEV --mode standalone
paas-cli redis scale --project j036x0 --env DEV --replicas 5
paas-cli redis slot-migrate --project j036x0 --env DEV --from redis-0 --to redis-1 --slots 1000
paas-cli redis upgrade --project j036x0 --env DEV --version 7.2.4
paas-cli redis delete --project j036x0 --env DEV
```

### 1.4 Elasticsearch 命令

格式：`paas-cli es <subcommand> --project <id> --env <env>`

| 子命令 | 说明 | 额外参数 |
|--------|------|----------|
| `info` | 查看集群信息 | — |
| `disk-usage` | 查看磁盘水位 | — |
| `indices` | 查看索引列表 | — |
| `config` | 查看连接配置 | — |
| `create-index` | 创建索引 | `--name <idx>` `--shards <n>` `--replicas <n>` |
| `rollover` | 滚动索引 | `--alias <name>` |
| `force-merge` | 强制合并段 | `--index <idx>` `--max-segments <n>` |
| `scale` | 扩缩容 | `--nodes <n>` |
| `upgrade` | 版本升级 | `--version <ver>` |
| `delete` | 删除集群 | — |

**示例：**

```bash
paas-cli es info --project j036x0 --env DEV
paas-cli es disk-usage --project j036x0 --env DEV
paas-cli es indices --project j036x0 --env DEV
paas-cli es config --project j036x0 --env DEV
paas-cli es create-index --project j036x0 --env DEV --name log-2026-05 --shards 3 --replicas 1
paas-cli es rollover --project j036x0 --env DEV --alias logs-write
paas-cli es force-merge --project j036x0 --env DEV --index log-2026-04 --max-segments 1
paas-cli es scale --project j036x0 --env DEV --nodes 5
paas-cli es upgrade --project j036x0 --env DEV --version 8.13.0
paas-cli es delete --project j036x0 --env DEV
```

### 1.5 CRD 风格命令

格式：`paas-cli <action> <resource> --gateway-config=config/gateway.yaml -f config/<middleware>/<file>.yaml`

**动作（action）：** `create` | `get` | `update` | `delete` | `switch`

**Nacos 资源及对应配置文件：**

| 资源类型 | 说明 | 配置文件 |
|----------|------|----------|
| `nacosclusterbackup` | 集群备份 | `config/nacos/iteration-nacos-cluster-backup-create.yaml` |
| `nacosclusterbackup` | 查询备份 | `config/nacos/iteration-nacos-cluster-backup-get.yaml` |
| `nacosclusterrestore` | 集群恢复 | `config/nacos/iteration-nacos-cluster-restore.yaml` |
| `nacosclusteraccesstoken` | 创建令牌 | `config/nacos/iteration-nacos-cluster-access-token-create.yaml` |
| `nacosclusteraccesstoken` | 查询令牌 | `config/nacos/iteration-nacos-cluster-access-token-get.yaml` |
| `nacosclusteraccesstoken` | 删除令牌 | `config/nacos/iteration-nacos-cluster-access-token-delete.yaml` |
| `nacosclustermonitor` | 查询监控 | `config/nacos/iteration-nacos-cluster-monitor-get.yaml` |
| `nacosclustermonitor` | 更新监控 | `config/nacos/iteration-nacos-cluster-monitor-update.yaml` |
| `nacosclusternetworkpolicy` | 创建网络策略 | `config/nacos/iteration-nacos-cluster-network-policy-create.yaml` |
| `nacosclusternetworkpolicy` | 查询网络策略 | `config/nacos/iteration-nacos-cluster-network-policy-get.yaml` |
| `nacosclusternetworkpolicy` | 更新网络策略 | `config/nacos/iteration-nacos-cluster-network-policy-update.yaml` |
| `nacosclusternetworkpolicy` | 删除网络策略 | `config/nacos/iteration-nacos-cluster-network-policy-delete.yaml` |

**Redis 资源及对应配置文件：**

| 资源类型 | 说明 | 配置文件 |
|----------|------|----------|
| `ncractivestrategy` | 主备切换策略 | `config/redis/ncractivestrategy.yaml` |
| `ncrhotbackupstrategy` | 热备策略 | `config/redis/ncrhotbackupstrategy.yaml` |
| `ncrunitstrategy` | 单元化策略 | `config/redis/ncrunitstrategy.yaml` |

**ES 资源及对应配置文件：**

| 资源类型 | 说明 | 配置文件 |
|----------|------|----------|
| `esindex` | ES 索引 | `config/es/iteration-elasticsearch-index.yaml` |
| `esindextemplate` | ES 索引模板 | `config/es/iteration-elasticsearch-index-template.yaml` |
| `esclusterip` | 集群 IP | `config/es/iteration-elasticsearch-clusterIP.yaml` |
| `eslb` | 负载均衡 | `config/es/iteration-elasticsearch-lb.yaml` |
| `esclusterreplicas` | 集群副本数 | `config/es/iteration-elasticsearch-cluster-replicas-update.yaml` |

**示例：**

```bash
# Nacos — 创建集群备份
paas-cli create nacosclusterbackup --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-backup-create.yaml

# Nacos — 查询备份状态
paas-cli get nacosclusterbackup --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-backup-get.yaml

# Nacos — 集群恢复
paas-cli create nacosclusterrestore --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-restore.yaml

# Nacos — 创建访问令牌
paas-cli create nacosclusteraccesstoken --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-access-token-create.yaml

# Nacos — 更新监控配置
paas-cli update nacosclustermonitor --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-monitor-update.yaml

# Nacos — 创建网络策略
paas-cli create nacosclusternetworkpolicy --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-network-policy-create.yaml

# Nacos — 删除网络策略
paas-cli delete nacosclusternetworkpolicy --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-network-policy-delete.yaml

# Redis — 创建主备切换策略
paas-cli create ncractivestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml

# Redis — 切换热备策略
paas-cli switch ncrhotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml

# ES — 创建索引
paas-cli create esindex --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index.yaml

# ES — 更新集群副本数
paas-cli update esclusterreplicas --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-replicas-update.yaml

# ES — 创建负载均衡
paas-cli create eslb --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-lb.yaml
```

---

## 二、bianque

中间件诊断平台 CLI 工具（mock 版本）。

### 2.1 命令格式

```bash
bianque diagnose --middleware <type> --project <id> --env <env> --check <items>
```

- `--middleware`：中间件类型，支持 `nacos` / `redis` / `es`
- `--project`：项目 ID，默认 `j036x0`
- `--env`：环境，默认 `DEV`
- `--check`：检查项，逗号分隔

### 2.2 各中间件支持的检查项

**Nacos 检查项：**

| 检查项 | 说明 | 输出严重度 |
|--------|------|------------|
| `health` | 集群健康状态 | info |
| `raft` | Raft 共识状态 | info |
| `log` | 最近日志分析 | info |

**Redis 检查项：**

| 检查项 | 说明 | 输出严重度 |
|--------|------|------------|
| `slowlog` | 慢查询分析 | warning |
| `memory` | 内存使用详情 | info |
| `replication` | 主从复制状态 | info |

**ES 检查项：**

| 检查项 | 说明 | 输出严重度 |
|--------|------|------------|
| `cluster-health` | 集群健康状态 | info |
| `shard` | 分片分配状态 | info |
| `cpu` | 节点 CPU 使用率 | warning |
| `watermark` | 磁盘水位检查 | info |

### 2.3 输出格式

输出为 JSON 结构：

```json
{
  "status": "success",
  "timestamp": "2026-05-14T10:00:00+08:00",
  "middleware": "nacos|redis|es",
  "project": "j036x0",
  "env": "DEV",
  "overall_severity": "info|warning|critical",
  "findings": [
    {
      "type": "检查项",
      "severity": "info|warning|critical",
      "message": "描述信息",
      "details": { ... }
    }
  ],
  "logs": [ ... ],
  "suggestions": [ ... ]
}
```

### 2.4 示例

```bash
# Nacos — 全量检查
bianque diagnose --middleware nacos --project j036x0 --env DEV --check health,raft,log

# Nacos — 仅 Raft 检查
bianque diagnose --middleware nacos --project j036x0 --env DEV --check raft

# Redis — 慢查询 + 内存
bianque diagnose --middleware redis --project j036x0 --env DEV --check slowlog,memory

# Redis — 全量检查
bianque diagnose --middleware redis --project j036x0 --env DEV --check slowlog,memory,replication

# ES — 集群健康 + 磁盘水位
bianque diagnose --middleware es --project j036x0 --env DEV --check cluster-health,watermark

# ES — 全量检查
bianque diagnose --middleware es --project j036x0 --env DEV --check cluster-health,shard,cpu,watermark
```

---

## 三、配置文件说明

### 3.1 目录结构

```
config/
├── gateway.yaml                          # API 网关连接配置
├── nacos/                                 # Nacos CRD 资源配置
│   ├── iteration-nacos-cluster-backup-create.yaml
│   ├── iteration-nacos-cluster-backup-get.yaml
│   ├── iteration-nacos-cluster-restore.yaml
│   ├── iteration-nacos-cluster-access-token-create.yaml
│   ├── iteration-nacos-cluster-access-token-get.yaml
│   ├── iteration-nacos-cluster-access-token-delete.yaml
│   ├── iteration-nacos-cluster-monitor-get.yaml
│   ├── iteration-nacos-cluster-monitor-update.yaml
│   ├── iteration-nacos-cluster-network-policy-create.yaml
│   ├── iteration-nacos-cluster-network-policy-get.yaml
│   ├── iteration-nacos-cluster-network-policy-update.yaml
│   └── iteration-nacos-cluster-network-policy-delete.yaml
├── redis/                                 # Redis CRD 资源配置
│   ├── ncractivestrategy.yaml
│   ├── ncrhotbackupstrategy.yaml
│   └── ncrunitstrategy.yaml
└── es/                                    # ES CRD 资源配置
    ├── iteration-elasticsearch-index.yaml
    ├── iteration-elasticsearch-index-template.yaml
    ├── iteration-elasticsearch-clusterIP.yaml
    ├── iteration-elasticsearch-lb.yaml
    └── iteration-elasticsearch-cluster-replicas-update.yaml
```

### 3.2 gateway.yaml

所有 CRD 风格命令都需要通过 `--gateway-config=config/gateway.yaml` 引用此文件，其中包含 API Server 地址、超时配置和认证方式。

---

## 四、公共参数说明

以下参数在多数命令中通用：

| 参数 | 格式 | 默认值 | 说明 |
|------|------|--------|------|
| `--project` | `--project <id>` 或 `--project=<id>` | `j036x0` | 项目标识 |
| `--env` | `--env <env>` 或 `--env=<env>` | `DEV` | 环境名称 |
| `--gateway-config` | `--gateway-config=<path>` | `config/gateway.yaml` | 网关配置路径（仅 CRD 命令） |
| `-f` | `-f <path>` | — | 资源配置文件路径（仅 CRD 命令） |
