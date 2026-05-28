# paas-cli 命令参考

> Mock v2.4.1。可执行文件：`skills/paas-cli/paas-cli.py`。配置说明见 [CONFIG.md](CONFIG.md)。工具 Skill 见 [../SKILL.md](../SKILL.md)。

---

## 一、paas-cli

PaaS 中间件运维 CLI 工具（mock 版本 v2.4.1）。

### 1.1 通用命令

| 命令 | 说明 |
|------|------|
| `paas-cli version` | 查看版本号（路径解析探测用） |
| `paas-cli --version` | 查看版本号（同上，兼容写法） |
| `paas-cli ping` | 测试网关连通性 |
| `paas-cli auth check --project <id>` | 检查项目授权状态 |

**示例：**

```bash
paas-cli version
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
| `lease status` | 查看服务租期状态 | — |
| `lease renew` | 续期服务租期 | `--duration <months>`（默认 3 个月） |
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
paas-cli nacos lease status --project j036x0 --env DEV
paas-cli nacos lease renew --project j036x0 --env DEV --duration 3
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
| `config` | 查看连接配置 | `--mode cluster\|sentinel\|standalone`、`--format json` |
| `config` | 修改内存策略 | `--maxmemory-policy <policy>` |
| `create` | 创建实例 | `--mode standalone\|cluster` |
| `scale` | 扩缩容 | `--replicas <n>` |
| `slot-migrate` | 槽位迁移 | `--from <node>` `--to <node>` `--slots <n>` |
| `lease status` | 查看服务租期状态 | — |
| `lease renew` | 续期服务租期 | `--duration <months>`（默认 3 个月） |
| `upgrade` | 版本升级 | `--version <ver>` |
| `delete` | 删除集群 | — |

**示例：**

```bash
paas-cli redis info --project j036x0 --env DEV
paas-cli redis nodes --project j036x0 --env DEV
paas-cli redis memory --project j036x0 --env DEV
paas-cli redis config --project j036x0 --env DEV --mode cluster
paas-cli redis config --project j036x0 --env DEV --format json   # 机器可读 JSON（j036x0+DEV 自动检测本地 Docker Redis）
paas-cli redis config --project j036x0 --env DEV --maxmemory-policy allkeys-lru
paas-cli redis create --project j036x0 --env DEV --mode standalone
paas-cli redis scale --project j036x0 --env DEV --replicas 5
paas-cli redis slot-migrate --project j036x0 --env DEV --from redis-0 --to redis-1 --slots 1000
paas-cli redis lease status --project j036x0 --env DEV
paas-cli redis lease renew --project j036x0 --env DEV --duration 3
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
| `lease status` | 查看服务租期状态 | — |
| `lease renew` | 续期服务租期 | `--duration <months>`（默认 3 个月） |
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
paas-cli es lease status --project j036x0 --env DEV
paas-cli es lease renew --project j036x0 --env DEV --duration 3
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

