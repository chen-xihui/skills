# Redis 集群交互操作索引

本目录包含 Redis 集群交互的完整操作说明，基于 **paas-cli Skill**（`$PAAS_CLI` + `references/COMMANDS.md`）。

涵盖：Redis 集群版、Redis 哨兵、Redis 主从版、Redis 联邦集群、Redis 高阶策略。

## 通用命令格式

```bash
paas-cli <action> <resource> --gateway-config=config/gateway.yaml -f <config-file>
```

- **action**: `create` / `get` / `delete` / `update` / `switch`
- **gateway-config**: PaaS 网关配置文件路径
- **-f**: YAML 配置文件路径

## 通用前置条件

执行前须完成 **paas-cli Skill** 路径解析（`skills/paas-cli/SKILL.md` §路径解析），得到 `$PAAS_CLI` 后：

```bash
# 1. 校验 CLI 可用（须退出码为 0）
$PAAS_CLI version

# 2. 检查网关连通
$PAAS_CLI ping
```

- 解析或 `version` 失败 → 提示遵循 paas-cli Skill，勿继续执行本目录 CRD 命令
- 使用项目 Mock 时，须在 `skills/paas-cli/` 目录下执行 CRD 命令

## 目录结构

| 文件 | 说明 | 操作数 |
|------|------|--------|
| [cluster.md](cluster.md) | Redis 集群版（集群管理、实例参数、扩缩容、服务发现、过期时间） | 17 |
| [sentinel.md](sentinel.md) | Redis 哨兵（哨兵管理、规格、服务发现、过期时间） | 10 |
| [master-slave.md](master-slave.md) | Redis 主从版（主从管理、实例参数、规格、服务发现、过期时间） | 16 |
| [federated.md](federated.md) | Redis 联邦集群（联邦集群版、联邦哨兵、联邦主从版） | 13 |
| [advanced-strategy.md](advanced-strategy.md) | Redis 高阶策略（多活、热备、单元化） | 17 |

## 命令速查表

### Redis 集群版

| 功能分类 | resource | action | 说明 |
|----------|----------|--------|------|
| 集群管理 | `ncrcluster` | create / get / delete / update | 创建、获取、删除、更新集群 |
| 实例参数 | `ncrclusterconfig` | get / update | 查询、变更实例参数 |
| 参数回滚 | `ncrclusterconfigrollback` | update | 回滚实例参数 |
| 分片扩缩容 | `ncrclusterreplicas` | update | 分片扩缩容 |
| 变更规格 | `ncrclusterresourceusage` | update | 变更规格 |
| 规格回滚 | `ncrclusterresourceusagerollback` | update | 规格回滚 |
| ClusterIP | `ncrclusterip` | create / get / delete | 管理 ClusterIP |
| LoadBalancer | `ncrclusterlb` | create / get / delete | 管理 LB |
| 过期时间 | `ncrcluster` | update | 设置过期时间 |

### Redis 哨兵

| 功能分类 | resource | action | 说明 |
|----------|----------|--------|------|
| 哨兵管理 | `ncrsentinel` | create / get / delete / update | 创建、获取、删除、更新哨兵 |
| 变更规格 | `ncrsentinelresourceusage` | update | 变更规格 |
| 规格回滚 | `ncrsentinelresourceusagerollback` | update | 规格回滚 |
| LoadBalancer | `ncrsentinellb` | create / get / delete | 管理 LB |
| 过期时间 | `ncrsentinel` | update | 设置过期时间 |

### Redis 主从版

| 功能分类 | resource | action | 说明 |
|----------|----------|--------|------|
| 主从管理 | `ncrsentinelcluster` | create / get / delete / update | 创建、获取、删除、更新主从版 |
| 实例参数 | `ncrsentinelclusterconfig` | get / update | 查询、变更实例参数 |
| 参数回滚 | `ncrsentinelclusterconfigrollback` | update | 回滚实例参数 |
| 变更规格 | `ncrsentinelclusterresourceusage` | update | 变更规格 |
| 规格回滚 | `ncrsentinelclusterresourceusagerollback` | update | 规格回滚 |
| ClusterIP | `ncrsentinelclusterip` | create / get / delete | 管理 ClusterIP |
| LoadBalancer | `ncrsentinelclusterlb` | create / get / delete | 管理 LB |
| 过期时间 | `ncrsentinelcluster` | update | 设置过期时间 |

### Redis 联邦集群

| 功能分类 | resource | action | 说明 |
|----------|----------|--------|------|
| 联邦集群版 | `federatedncrcluster` | create / get / delete | 创建、获取、删除联邦集群 |
| 联邦集群参数 | `federatedncrclusterconfig` | get / update | 查询、变更实例参数 |
| 联邦哨兵 | `federatedsentinel` | create / get / delete | 创建、获取、删除联邦哨兵 |
| 联邦主从版 | `federatedsentinelcluster` | create / get / delete | 创建、获取、删除联邦主从版 |
| 联邦主从参数 | `federatedsentinelclusterconfig` | get / update | 查询、变更实例参数 |

### Redis 高阶策略

| 功能分类 | resource | action | 说明 |
|----------|----------|--------|------|
| 多活策略 | `activestrategy` | create / get / delete / update | 管理多活策略 |
| Proxy 读模式 | `activestrategy` | update | 更新 Proxy 读模式 |
| 主从切换 | `activestrategy` | switch | 双集群主从切换 |
| 多活降备 | `demoteActiveMaster` | switch | 多活降备 |
| 多活升主 | `promoteActiveSlave` | switch | 多活升主 |
| 切流恢复 | `activestrategy` | switch | 切流恢复 |
| 逻辑主恢复 | `configLogicMasterRecover` | update | 逻辑主恢复 |
| 热备策略 | `hotbackupstrategy` | create / get / delete | 管理热备策略 |
| 热备切换 | `hotbackupstrategy` | switch | 热备切换 |
| 单元化策略 | `unitstrategy` | create / get / delete | 管理单元化策略 |