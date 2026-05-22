# Nacos 集群交互操作索引

本目录包含 Nacos 集群交互的完整操作说明，基于 paas-cli 标准命令格式。

## 通用命令格式

```bash
paas-cli <action> <resource> --gateway-config=config/gateway.yaml -f <config-file>
```

- **action**: `create` / `get` / `delete` / `update` / `switch`
- **gateway-config**: PaaS 网关配置文件路径
- **-f**: YAML 配置文件路径

## 通用前置条件

```bash
# 1. 检查 paas-cli 是否可用
paas-cli --version
# 2. 检查网络连通性
paas-cli ping
```

## 操作分类索引

| 分类 | 详情 | 操作数 |
|------|------|--------|
| 集群管理 | [集群管理.md](./集群管理.md) | 3 (创建/获取/删除) |
| 实例参数 | [实例参数.md](./实例参数.md) | 3 (查询/更改/回滚) |
| 扩缩容与资源 | [扩缩容与资源.md](./扩缩容与资源.md) | 4 (扩缩容/变更规格/扩容/回滚) |
| 版本管理 | [版本管理.md](./版本管理.md) | 2 (升级/回滚) |
| 服务发现 | [服务发现.md](./服务发现.md) | 6 (ClusterIP/LB 的创建/获取/删除) |
| 多活 | [多活.md](./多活.md) | 2 (创建/删除) |
| 命名空间 | [命名空间.md](./命名空间.md) | 3 (创建/获取/删除) |
| 用户管理 | [用户管理.md](./用户管理.md) | 4 (创建/获取/删除/改密码) |
| 权限管理 | [权限管理.md](./权限管理.md) | 6 (权限CRUD + 角色绑定/解绑/列表) |
| 服务管理 | [服务管理.md](./服务管理.md) | 4 (列表/详情/实例/订阅者) |
| 过期时间 | [过期时间.md](./过期时间.md) | 1 (设置) |

## 命令速查表

| 功能分类 | resource | action | 说明 |
|----------|----------|--------|------|
| 集群管理 | `nacoscluster` | create / get / delete | 创建、获取、删除集群 |
| 实例参数 | `nacosclusterconfig` | get / update | 查询、更改实例参数 |
| 参数回滚 | `nacosclusterconfigrollback` | update | 回滚实例参数 |
| 扩缩容 | `nacosclusterreplicas` | update | 集群扩缩容 |
| 变更规格 | `nacosclusterresourceusage` | update | 变更集群规格 |
| 扩容资源 | `nacosclusterresource` | update | 扩容 CPU/Mem/PVC |
| 资源回滚 | `nacosclusterresourcerollback` | update | 回滚扩容 |
| 升级版本 | `nacosclusterupgradeversion` | update | 升级版本 |
| 回滚版本 | `nacosclusterrollbackversion` | update | 回滚版本 |
| ClusterIP | `nacosclusterip` | create / get / delete | 管理 ClusterIP 服务 |
| LoadBalancer | `nacoslb` | create / get / delete | 管理 LB 服务 |
| 多活 | `nacosclustermultizone` | create / delete | 管理多活关系 |
| 命名空间 | `nacosnamespace` | create / get / delete | 管理命名空间 |
| 用户管理 | `nacosuser` | create / get / delete / update | 管理用户 |
| 权限管理 | `nacospermissions` | create / get / delete | 管理权限 |
| 角色列表 | `nacosroles` | get | 获取角色列表 |
| 角色绑定 | `nacosrolebind` | update | 角色绑定 |
| 角色解绑 | `nacosroleunbind` | update | 角色解绑 |
| 服务列表 | `nacosservices` | get | 获取服务列表 |
| 服务详情 | `nacosservicedetail` | get | 获取服务详情 |
| 服务实例 | `nacosservicesinstance` | get | 获取服务实例列表 |
| 订阅者 | `nacossupscribers` | get | 获取订阅者列表 |
| 过期时间 | `nacoscluster` | update | 设置过期时间 |