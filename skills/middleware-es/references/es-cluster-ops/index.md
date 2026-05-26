# ES 集群交互操作索引

本目录包含 ES 集群交互的完整操作说明，基于 **paas-cli Skill**（`$PAAS_CLI` + `references/COMMANDS.md`）。

## 文档结构

| 文档 | 说明 |
|------|------|
| [index.md](index.md) | 通用命令格式、前置条件、命令速查表（本文件） |
| [cluster.md](cluster.md) | 集群管理（创建、获取、删除 ES 集群） |
| [config.md](config.md) | 实例参数（查询、更改、回滚参数） |
| [scaling.md](scaling.md) | 扩缩容与资源（扩缩容、变更规格、调整资源、资源回滚） |
| [discovery.md](discovery.md) | 服务发现（ClusterIP、LoadBalancer） |
| [index-mgmt.md](index-mgmt.md) | 索引管理与过期时间 |

---

## 通用命令格式

```bash
paas-cli <action> <resource> --gateway-config=config/gateway.yaml -f <config-file>
```

- **action**: `create` / `get` / `delete` / `update` / `switch`
- **gateway-config**: PaaS 网关配置文件路径
- **-f**: YAML 配置文件路径

---

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

---

## 命令速查表

| 功能分类 | resource | action | 说明 |
|----------|----------|--------|------|
| **集群管理** | `escluster` | create / get / delete | 创建、获取、删除集群 |
| **实例参数** | `esclusterconfig` | get / update | 查询、更改实例参数 |
| **参数回滚** | `esclusterconfigrollback` | update | 回滚实例参数 |
| **扩缩容** | `esclusterreplicas` | update | 集群扩缩容 |
| **变更规格** | `esclusterresourceusage` | update | 变更集群规格 |
| **调整资源** | `esclusterresource` | update | 调整资源配置 |
| **资源回滚** | `esclusterresourcerollback` | update | 资源配置回滚 |
| **ClusterIP** | `esclusterip` | create / get / delete | 管理 ClusterIP 服务 |
| **LoadBalancer** | `eslb` | create / get / delete | 管理 LB 服务 |
| **索引管理** | `esindex` | create / get / delete | 创建、获取、删除索引 |
| **过期时间** | `escluster` | update | 设置过期时间 |