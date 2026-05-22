# Mock CLI Tools 使用命令文档

本目录包含两个 mock 命令行工具，用于中间件 Skill 演示场景。

## 目录结构

```
tools/
├── USAGE.md              # 本文件
├── bianque/              # 扁鹊诊断平台 CLI
│   ├── bianque.cmd       # Windows 入口
│   └── bianque.py        # 主程序
└── paas-cli/             # PaaS 中间件运维 CLI
    ├── paas-cli.cmd      # Windows 入口
    ├── paas-cli.py       # 主程序
    └── config/           # CRD 资源配置文件
        ├── gateway.yaml
        ├── es/
        ├── nacos/
        └── redis/
```

## 前置准备

将两个工具目录分别加入 PATH（PowerShell）：

```powershell
$env:PATH = "D:\Users\chenxihui\skill\.trae\tools\bianque;D:\Users\chenxihui\skill\.trae\tools\paas-cli;" + $env:PATH
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

> **注意**：CRD 命令中的配置文件路径相对于 `paas-cli/` 目录。建议先 `cd` 到 `paas-cli/` 目录再执行 CRD 命令，或使用绝对路径。`--gateway-config` 默认值已自动解析为脚本所在目录的 `config/gateway.yaml`。

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

### 2.1 全局参数

所有 `bianque` 命令都支持全局参数：

| 参数 | 说明 |
|------|------|
| `--token-file <path>` | 指定权限验证脚本文件路径（包含 API 地址和 Token） |

### 2.2 Elasticsearch 命令

#### check 命令

**功能**：检查 Elasticsearch 集群状态、日志错误信息

```bash
bianque elasticsearch check -n <namespace> -i <instance> [-v] [-o <num>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | ES 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | ES 实例名称 |
| `--verb` | `-v` | 否 | 是否展示详情（true/false） |
| `--log-lines` | `-o` | 否 | Pod 和 Operator 错误日志输出行数（默认 0） |

**示例：**

```bash
# 检查 ES 集群状态
bianque elasticsearch check -n myns -i myes

# 检查 ES 集群并显示详细信息
bianque elasticsearch check -n myns -i myes -v

# 指定错误日志输出行数
bianque elasticsearch check -n myns -i myes -o 50
```

#### client 命令

**功能**：创建 Elasticsearch 客户端并执行读写操作

```bash
bianque elasticsearch client -n <namespace> -i <instance> -k <key> -v <value> [-u <user>] [-p <password>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | ES 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | ES 实例名称 |
| `--key` | `-k` | 是 | 要写入的 key |
| `--value` | `-v` | 是 | 要写入的 value |
| `--user` | `-u` | 否 | 验证的用户名（默认 elastic） |
| `--password` | `-p` | 否 | 验证的密码（不填则自动获取） |

**示例：**

```bash
# 连接 ES 实例并写入测试数据
bianque elasticsearch client -n myns -i myes -k testkey -v testval

# 带认证信息连接
bianque elasticsearch client -n myns -i myes -k testkey -v testval -u myuser -p mypassword
```

### 2.3 Nacos 命令

#### check 命令

**功能**：检查 Nacos 实例的连接状态和配置

```bash
bianque nacos check -n <namespace> -i <instance> [-v] [-l <num>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Nacos 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Nacos 实例名称 |
| `--verb` | `-v` | 否 | 是否展示详情（true/false） |
| `--log-lines` | `-l` | 否 | 日志检查的行数（默认 1000） |

**示例：**

```bash
# 检查 Nacos 实例连接状态
bianque nacos check -n myns -i mynacos

# 检查 Nacos 并显示详细信息
bianque nacos check -n myns -i mynacos -v

# 指定日志检查行数
bianque nacos check -n myns -i mynacos -l 2000
```

#### client 命令

**功能**：创建 Nacos 客户端并执行操作

```bash
bianque nacos client -n <namespace> -i <instance> [-u <user>] [-p <password>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Nacos 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Nacos 实例名称 |
| `--user` | `-u` | 否 | 验证的用户名（默认 admin） |
| `--password` | `-p` | 否 | 验证的密码（不填则自动获取） |

**示例：**

```bash
# 连接 Nacos 实例
bianque nacos client -n myns -i mynacos

# 带认证信息连接
bianque nacos client -n myns -i mynacos -u myuser -p mypassword
```

### 2.4 Redis 命令

#### check 命令

**功能**：检查 Redis 实例的连接状态和配置

```bash
bianque redis check -n <namespace> -i <instance> -t <type> [-v] [-l <num>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Redis 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Redis 实例名称 |
| `--type` | `-t` | 是 | Redis 类型：cluster / sentinel |
| `--verb` | `-v` | 否 | 是否展示详情（true/false） |
| `--log-lines` | `-l` | 否 | 日志检查的行数（默认 1000） |

**示例：**

```bash
# 检查 sentinel 模式的 Redis 实例
bianque redis check -n myns -i myredis -t sentinel

# 检查 cluster 模式并显示详细信息
bianque redis check -n myns -i myredis -t cluster -v

# 指定日志检查行数
bianque redis check -n myns -i myredis -t sentinel -l 2000
```

#### client 命令

**功能**：创建 Redis 客户端并执行读写操作

```bash
bianque redis client -n <namespace> -i <instance> -t <type> [-a <password>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Redis 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Redis 实例名称 |
| `--type` | `-t` | 是 | Redis 类型：cluster / sentinel |
| `--auth` | `-a` | 否 | Redis 密码（不填则自动获取） |

**示例：**

```bash
# 连接 sentinel 模式的 Redis 实例
bianque redis client -n myns -i myredis -t sentinel

# 带认证信息连接 cluster 模式
bianque redis client -n myns -i myredis -t cluster -a "mypassword"
```

#### updateRenameConfig 命令

**功能**：更新 Redis 实例的重命名配置（rename-command）

```bash
bianque redis updateRenameConfig -n <namespace> -i <instance> -t <type> [-a]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Redis 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Redis 实例名称 |
| `--type` | `-t` | 是 | Redis 类型：cluster / sentinel |
| `--all-namespaces` | `-a` | 否 | 是否应用到所有命名空间 |

**示例：**

```bash
# 更新单个 sentinel 模式实例的重命名配置
bianque redis updateRenameConfig -n myns -i myredis -t sentinel

# 更新所有命名空间的 cluster 模式实例配置
bianque redis updateRenameConfig -n myns -i myredis -t cluster -a
```

#### clusterUpgradeRecover 命令

**功能**：恢复 Redis 集群升级操作

```bash
bianque redis clusterUpgradeRecover -n <namespace> -i <instance> -o <operation> -t <type>
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Redis 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Redis 实例名称 |
| `--operation` | `-o` | 是 | 需要恢复的 Redis operation 升级名称 |
| `--type` | `-t` | 是 | Redis 类型：cluster / sentinel |

**示例：**

```bash
bianque redis clusterUpgradeRecover -n myns -i myredis -o operation_name -t cluster
```

### 2.5 输出格式

**check 命令**输出为 JSON 结构：

```json
{
  "status": "success",
  "timestamp": "2026-05-22T10:00:00+08:00",
  "command": "bianque <middleware> check",
  "namespace": "myns",
  "instance": "myes",
  "verbose": true,
  "log_lines": "0",
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

**client 命令**输出为 JSON 结构：

```json
{
  "status": "success",
  "timestamp": "2026-05-22T10:00:00+08:00",
  "command": "bianque <middleware> client",
  "namespace": "myns",
  "instance": "myes",
  "operation": "connect_and_verify",
  "result": { ... },
  "message": "描述信息"
}
```

### 2.6 命令速查表

| 命令 | 功能 | 是否需要参数 |
|------|------|-------------|
| `bianque elasticsearch check` | 检查 ES 集群状态 | 是 |
| `bianque elasticsearch client` | 创建 ES 客户端 | 是 |
| `bianque nacos check` | 检查 Nacos 连接状态 | 是 |
| `bianque nacos client` | 创建 Nacos 客户端 | 是 |
| `bianque redis check` | 检查 Redis 连接状态 | 是 |
| `bianque redis client` | 创建 Redis 客户端 | 是 |
| `bianque redis updateRenameConfig` | 更新重命名配置 | 是 |
| `bianque redis clusterUpgradeRecover` | 恢复集群升级 | 是 |

---

## 三、配置文件说明

### 3.1 目录结构

```
tools/
├── USAGE.md
├── bianque/
│   ├── bianque.cmd
│   └── bianque.py
└── paas-cli/
    ├── paas-cli.cmd
    ├── paas-cli.py
    └── config/
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
| `--gateway-config` | `--gateway-config=<path>` | 脚本目录下 `config/gateway.yaml` | 网关配置路径（仅 CRD 命令，默认自动解析） |
| `-f` | `-f <path>` | — | 资源配置文件路径（仅 CRD 命令） |
| `--namespace` / `-n` | `-n <namespace>` | — | K8s 命名空间（bianque 命令） |
| `--instance` / `-i` | `-i <instance>` | — | 实例名称（bianque 命令） |
| `--type` / `-t` | `-t <type>` | — | Redis 类型 cluster/sentinel（bianque 命令） |
| `--verb` / `-v` | `-v` | false | 展示详情（bianque check 命令） |
| `--token-file` | `--token-file <path>` | — | 权限验证脚本文件路径（bianque 全局参数） |
