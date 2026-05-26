# Nacos / ES / Redis 全量使用命令文档

## 目录
- [Nacos 命令](#nacos-命令)
- [Elasticsearch 命令](#elasticsearch-命令)
- [Redis 命令](#redis-命令)
  - [Redis 集群版](#redis-集群版)
  - [Redis 哨兵](#redis-哨兵)
  - [Redis 主从版](#redis-主从版)
  - [Redis 联邦集群](#redis-联邦集群)
  - [Redis 高阶策略](#redis-高阶策略)

---

## 通用命令格式

```bash
paas-cli <action> <resource> --gateway-config=config/gateway.yaml -f <config-file>
```

- **action**: `create` / `get` / `delete` / `update` / `switch`
- **gateway-config**: PaaS 网关配置文件路径
- **-f**: YAML 配置文件路径

---

## Nacos 命令

### 1. Nacos 集群管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建 Nacos 集群 | `nacoscluster` | create | `paas-cli create nacoscluster --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster.yaml` | `config/nacos/iteration-nacos-cluster.yaml` |
| 获取 Nacos 集群 | `nacoscluster` | get | `paas-cli get nacoscluster --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster.yaml` | `config/nacos/iteration-nacos-cluster.yaml` |
| 删除 Nacos 集群 | `nacoscluster` | delete | `paas-cli delete nacoscluster --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster.yaml` | `config/nacos/iteration-nacos-cluster.yaml` |

### 2. Nacos 实例参数

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 查询实例参数 | `nacosclusterconfig` | get | `paas-cli get nacosclusterconfig --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-config-get.yaml` | `config/nacos/iteration-nacos-cluster-config-get.yaml` |
| 更改实例参数 | `nacosclusterconfig` | update | `paas-cli update nacosclusterconfig --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-config-update.yaml` | `config/nacos/iteration-nacos-cluster-config-update.yaml` |
| 回滚实例参数 | `nacosclusterconfigrollback` | update | `paas-cli update nacosclusterconfigrollback --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-config-rollback.yaml` | `config/nacos/iteration-nacos-cluster-config-rollback.yaml` |

### 3. Nacos 扩缩容与资源

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 集群扩缩容 | `nacosclusterreplicas` | update | `paas-cli update nacosclusterreplicas --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-replicas-update.yaml` | `config/nacos/iteration-nacos-cluster-replicas-update.yaml` |
| 变更集群规格 | `nacosclusterresourceusage` | update | `paas-cli update nacosclusterresourceusage --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-resource-usage-update.yaml` | `config/nacos/iteration-nacos-cluster-resource-usage-update.yaml` |
| 扩容 CPU/Mem/PVC | `nacosclusterresource` | update | `paas-cli update nacosclusterresource --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-resource-update.yaml` | `config/nacos/iteration-nacos-cluster-resource-update.yaml` |
| 回滚扩容（PVC 不可回滚） | `nacosclusterresourcerollback` | update | `paas-cli update nacosclusterresourcerollback --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-resource-rollback.yaml` | `config/nacos/iteration-nacos-cluster-resource-rollback.yaml` |

### 4. Nacos 版本管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 升级版本 | `nacosclusterupgradeversion` | update | `paas-cli update nacosclusterupgradeversion --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-upgrade-version.yaml` | `config/nacos/iteration-nacos-cluster-upgrade-version.yaml` |
| 回滚版本 | `nacosclusterrollbackversion` | update | `paas-cli update nacosclusterrollbackversion --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-rollback-version.yaml` | `config/nacos/iteration-nacos-cluster-rollback-version.yaml` |

### 5. Nacos 服务发现

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建 ClusterIP | `nacosclusterip` | create | `paas-cli create nacosclusterip --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-clusterIP.yaml` | `config/nacos/iteration-nacos-clusterIP.yaml` |
| 获取 ClusterIP | `nacosclusterip` | get | `paas-cli get nacosclusterip --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-clusterIP.yaml` | `config/nacos/iteration-nacos-clusterIP.yaml` |
| 删除 ClusterIP | `nacosclusterip` | delete | `paas-cli delete nacosclusterip --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-clusterIP.yaml` | `config/nacos/iteration-nacos-clusterIP.yaml` |
| 创建 LoadBalancer | `nacoslb` | create | `paas-cli create nacoslb --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-lb.yaml` | `config/nacos/iteration-nacos-lb.yaml` |
| 获取 LoadBalancer | `nacoslb` | get | `paas-cli get nacoslb --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-lb.yaml` | `config/nacos/iteration-nacos-lb.yaml` |
| 删除 LoadBalancer | `nacoslb` | delete | `paas-cli delete nacoslb --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-lb.yaml` | `config/nacos/iteration-nacos-lb.yaml` |

### 6. Nacos 多活

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建多活关系 | `nacosclustermultizone` | create | `paas-cli create nacosclustermultizone --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-create-multizone.yaml` | `config/nacos/iteration-nacos-cluster-create-multizone.yaml` |
| 删除多活关系 | `nacosclustermultizone` | delete | `paas-cli delete nacosclustermultizone --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-cancel-multizone.yaml` | `config/nacos/iteration-nacos-cluster-cancel-multizone.yaml` |

### 7. Nacos 命名空间管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建命名空间 | `nacosnamespace` | create | `paas-cli create nacosnamespace --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-namespace-create.yaml` | `config/nacos/iteration-nacos-namespace-create.yaml` |
| 获取命名空间 | `nacosnamespace` | get | `paas-cli get nacosnamespace --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-namespace-get.yaml` | `config/nacos/iteration-nacos-namespace-get.yaml` |
| 删除命名空间 | `nacosnamespace` | delete | `paas-cli delete nacosnamespace --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-namespace-delete.yaml` | `config/nacos/iteration-nacos-namespace-delete.yaml` |

### 8. Nacos 用户管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建用户 | `nacosuser` | create | `paas-cli create nacosuser --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-user-create.yaml` | `config/nacos/iteration-nacos-user-create.yaml` |
| 获取用户列表 | `nacosuser` | get | `paas-cli get nacosuser --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-users-get.yaml` | `config/nacos/iteration-nacos-users-get.yaml` |
| 删除用户 | `nacosuser` | delete | `paas-cli delete nacosuser --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-user-delete.yaml` | `config/nacos/iteration-nacos-user-delete.yaml` |
| 修改用户密码 | `nacosuser` | update | `paas-cli update nacosuser --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-user-pwd-update.yaml` | `config/nacos/iteration-nacos-user-pwd-update.yaml` |

### 9. Nacos 权限管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建权限 | `nacospermissions` | create | `paas-cli create nacospermissions --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-permissions-create.yaml` | `config/nacos/iteration-nacos-permissions-create.yaml` |
| 获取权限列表 | `nacospermissions` | get | `paas-cli get nacospermissions --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-permissions-get.yaml` | `config/nacos/iteration-nacos-permissions-get.yaml` |
| 删除权限 | `nacospermissions` | delete | `paas-cli delete nacospermissions --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-permissions-delete.yaml` | `config/nacos/iteration-nacos-permissions-delete.yaml` |
| 获取角色列表 | `nacosroles` | get | `paas-cli get nacosroles --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-roles-get.yaml` | `config/nacos/iteration-nacos-roles-get.yaml` |
| 角色绑定 | `nacosrolebind` | update | `paas-cli update nacosrolebind --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-role-bind.yaml` | `config/nacos/iteration-nacos-role-bind.yaml` |
| 角色解绑 | `nacosroleunbind` | update | `paas-cli update nacosroleunbind --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-role-unbind.yaml` | `config/nacos/iteration-nacos-role-unbind.yaml` |

### 10. Nacos 服务管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 获取服务列表 | `nacosservices` | get | `paas-cli get nacosservices --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-services-get.yaml` | `config/nacos/iteration-nacos-services-get.yaml` |
| 获取服务详情 | `nacosservicedetail` | get | `paas-cli get nacosservicedetail --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-service-detail.yaml` | `config/nacos/iteration-nacos-service-detail.yaml` |
| 获取服务实例列表 | `nacosservicesinstance` | get | `paas-cli get nacosservicesinstance --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-services-instance-get.yaml` | `config/nacos/iteration-nacos-services-instance-get.yaml` |
| 获取订阅者列表 | `nacossupscribers` | get | `paas-cli get nacossupscribers --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-subscribers-get.yaml` | `config/nacos/iteration-nacos-subscribers-get.yaml` |

### 11. Nacos 过期时间

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 设置过期时间 | `nacoscluster` | update | `paas-cli update nacoscluster --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-update_expire_date.yaml` | `config/nacos/iteration-nacos-cluster-update_expire_date.yaml` |

---

## Elasticsearch 命令

### 1. ES 集群管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建 ES 集群 | `escluster` | create | `paas-cli create escluster --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster.yaml` | `config/es/iteration-elasticsearch-cluster.yaml` |
| 获取 ES 集群 | `escluster` | get | `paas-cli get escluster --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster.yaml` | `config/es/iteration-elasticsearch-cluster.yaml` |
| 删除 ES 集群 | `escluster` | delete | `paas-cli delete escluster --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster.yaml` | `config/es/iteration-elasticsearch-cluster.yaml` |

### 2. ES 实例参数

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 查询实例参数 | `esclusterconfig` | get | `paas-cli get esclusterconfig --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-config-get.yaml` | `config/es/iteration-elasticsearch-cluster-config-get.yaml` |
| 更改实例参数 | `esclusterconfig` | update | `paas-cli update esclusterconfig --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-config-update.yaml` | `config/es/iteration-elasticsearch-cluster-config-update.yaml` |
| 回滚实例参数 | `esclusterconfigrollback` | update | `paas-cli update esclusterconfigrollback --gateway-config=config/gateway.yaml -f config/es/iteration-elastcisearch-cluster-rollback-config.yaml` | `config/es/iteration-elastcisearch-cluster-rollback-config.yaml` |

### 3. ES 扩缩容与资源

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 集群扩缩容 | `esclusterreplicas` | update | `paas-cli update esclusterreplicas --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-replicas-update.yaml` | `config/es/iteration-elasticsearch-cluster-replicas-update.yaml` |
| 变更集群规格 | `esclusterresourceusage` | update | `paas-cli update esclusterresourceusage --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-resource-usage-update.yaml` | `config/es/iteration-elasticsearch-cluster-resource-usage-update.yaml` |
| 调整资源配置 | `esclusterresource` | update | `paas-cli update esclusterresource --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-resource-update.yaml` | `config/es/iteration-elasticsearch-cluster-resource-update.yaml` |
| 资源配置回滚 | `esclusterresourcerollback` | update | `paas-cli update esclusterresourcerollback --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-resource-rollback.yaml` | `config/es/iteration-elasticsearch-cluster-resource-rollback.yaml` |

### 4. ES 服务发现

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建 ClusterIP | `esclusterip` | create | `paas-cli create esclusterip --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-clusterIP.yaml` | `config/es/iteration-elasticsearch-clusterIP.yaml` |
| 获取 ClusterIP | `esclusterip` | get | `paas-cli get esclusterip --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-clusterIP.yaml` | `config/es/iteration-elasticsearch-clusterIP.yaml` |
| 删除 ClusterIP | `esclusterip` | delete | `paas-cli delete esclusterip --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-clusterIP.yaml` | `config/es/iteration-elasticsearch-clusterIP.yaml` |
| 创建 LoadBalancer | `eslb` | create | `paas-cli create eslb --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-lb.yaml` | `config/es/iteration-elasticsearch-lb.yaml` |
| 获取 LoadBalancer | `eslb` | get | `paas-cli get eslb --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-lb.yaml` | `config/es/iteration-elasticsearch-lb.yaml` |
| 删除 LoadBalancer | `eslb` | delete | `paas-cli delete eslb --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-lb.yaml` | `config/es/iteration-elasticsearch-lb.yaml` |

### 5. ES 索引管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建索引 | `esindex` | create | `paas-cli create esindex --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index.yaml` | `config/es/iteration-elasticsearch-index.yaml` |
| 获取索引 | `esindex` | get | `paas-cli get esindex --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index.yaml` | `config/es/iteration-elasticsearch-index.yaml` |
| 删除索引 | `esindex` | delete | `paas-cli delete esindex --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index.yaml` | `config/es/iteration-elasticsearch-index.yaml` |

### 6. ES 过期时间

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 设置过期时间 | `escluster` | update | `paas-cli update escluster --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-set-expire-date.yaml` | `config/es/iteration-elasticsearch-cluster-set-expire-date.yaml` |

---

## Redis 命令

### Redis 集群版

#### 1. 集群管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建集群版 | `ncrcluster` | create | `paas-cli create ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml` | `config/redis/iteration-ncr-cluster.yaml` |
| 获取集群版 | `ncrcluster` | get | `paas-cli get ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml` | `config/redis/iteration-ncr-cluster.yaml` |
| 删除集群版 | `ncrcluster` | delete | `paas-cli delete ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml` | `config/redis/iteration-ncr-cluster.yaml` |
| 更新集群版 | `ncrcluster` | update | `paas-cli update ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-update.yaml` | `config/redis/iteration-ncr-cluster-update.yaml` |

#### 2. 实例参数

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 查询实例参数 | `ncrclusterconfig` | get | `paas-cli get ncrclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-config-get.yaml` | `config/redis/iteration-ncr-cluster-config-get.yaml` |
| 变更实例参数 | `ncrclusterconfig` | update | `paas-cli update ncrclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-config-update.yaml` | `config/redis/iteration-ncr-cluster-config-update.yaml` |
| 回滚实例参数 | `ncrclusterconfigrollback` | update | `paas-cli update ncrclusterconfigrollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-config-rollback.yaml` | `config/redis/iteration-ncr-cluster-config-rollback.yaml` |

#### 3. 扩缩容与规格

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 分片扩缩容 | `ncrclusterreplicas` | update | `paas-cli update ncrclusterreplicas --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-replicas-update.yaml` | `config/redis/iteration-ncr-cluster-replicas-update.yaml` |
| 变更规格 | `ncrclusterresourceusage` | update | `paas-cli update ncrclusterresourceusage --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-resource-usage-update.yaml` | `config/redis/iteration-ncr-cluster-resource-usage-update.yaml` |
| 规格回滚 | `ncrclusterresourceusagerollback` | update | `paas-cli update ncrclusterresourceusagerollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-resource-usage-rollback.yaml` | `config/redis/iteration-ncr-cluster-resource-usage-rollback.yaml` |

#### 4. 服务发现

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建 ClusterIP | `ncrclusterip` | create | `paas-cli create ncrclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-clusterip.yaml` | `config/redis/iteration-ncr-cluster-clusterip.yaml` |
| 获取 ClusterIP | `ncrclusterip` | get | `paas-cli get ncrclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-clusterip.yaml` | `config/redis/iteration-ncr-cluster-clusterip.yaml` |
| 删除 ClusterIP | `ncrclusterip` | delete | `paas-cli delete ncrclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-clusterip.yaml` | `config/redis/iteration-ncr-cluster-clusterip.yaml` |
| 创建 LoadBalancer | `ncrclusterlb` | create | `paas-cli create ncrclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-lb.yaml` | `config/redis/iteration-ncr-cluster-lb.yaml` |
| 获取 LoadBalancer | `ncrclusterlb` | get | `paas-cli get ncrclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-lb.yaml` | `config/redis/iteration-ncr-cluster-lb.yaml` |
| 删除 LoadBalancer | `ncrclusterlb` | delete | `paas-cli delete ncrclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-lb.yaml` | `config/redis/iteration-ncr-cluster-lb.yaml` |

#### 5. 过期时间

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 设置过期时间 | `ncrcluster` | update | `paas-cli update ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-set-expire-date.yaml` | `config/redis/iteration-ncr-cluster-set-expire-date.yaml` |

---

### Redis 哨兵

#### 1. 哨兵管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建哨兵 | `ncrsentinel` | create | `paas-cli create ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel.yaml` | `config/redis/iteration-ncr-sentinel.yaml` |
| 获取哨兵 | `ncrsentinel` | get | `paas-cli get ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel.yaml` | `config/redis/iteration-ncr-sentinel.yaml` |
| 删除哨兵 | `ncrsentinel` | delete | `paas-cli delete ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel.yaml` | `config/redis/iteration-ncr-sentinel.yaml` |
| 更新哨兵 | `ncrsentinel` | update | `paas-cli update ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-update.yaml` | `config/redis/iteration-ncr-sentinel-update.yaml` |

#### 2. 哨兵规格

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 变更规格 | `ncrsentinelresourceusage` | update | `paas-cli update ncrsentinelresourceusage --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-resource-usage.yaml` | `config/redis/iteration-ncr-sentinel-resource-usage.yaml` |
| 规格回滚 | `ncrsentinelresourceusagerollback` | update | `paas-cli update ncrsentinelresourceusagerollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-resource-usage-rollback.yaml` | `config/redis/iteration-ncr-sentinel-resource-usage-rollback.yaml` |

#### 3. 哨兵服务发现

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建 LoadBalancer | `ncrsentinellb` | create | `paas-cli create ncrsentinellb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-lb.yaml` | `config/redis/iteration-ncr-sentinel-lb.yaml` |
| 获取 LoadBalancer | `ncrsentinellb` | get | `paas-cli get ncrsentinellb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-lb.yaml` | `config/redis/iteration-ncr-sentinel-lb.yaml` |
| 删除 LoadBalancer | `ncrsentinellb` | delete | `paas-cli delete ncrsentinellb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-lb.yaml` | `config/redis/iteration-ncr-sentinel-lb.yaml` |

#### 4. 哨兵过期时间

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 设置过期时间 | `ncrsentinel` | update | `paas-cli update ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-set-expire-date.yaml` | `config/redis/iteration-ncr-sentinel-set-expire-date.yaml` |

---

### Redis 主从版

#### 1. 主从集群管理

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建主从版 | `ncrsentinelcluster` | create | `paas-cli create ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` | `config/redis/iteration-ncr-sentinel-cluster.yaml` |
| 获取主从版 | `ncrsentinelcluster` | get | `paas-cli get ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` | `config/redis/iteration-ncr-sentinel-cluster.yaml` |
| 删除主从版 | `ncrsentinelcluster` | delete | `paas-cli delete ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` | `config/redis/iteration-ncr-sentinel-cluster.yaml` |
| 更新主从版 | `ncrsentinelcluster` | update | `paas-cli update ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` | `config/redis/iteration-ncr-sentinel-cluster.yaml` |

#### 2. 主从版实例参数

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 查询实例参数 | `ncrsentinelclusterconfig` | get | `paas-cli get ncrsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-config-get.yaml` | `config/redis/iteration-ncr-sentinel-cluster-config-get.yaml` |
| 变更实例参数 | `ncrsentinelclusterconfig` | update | `paas-cli update ncrsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-config-update.yaml` | `config/redis/iteration-ncr-sentinel-cluster-config-update.yaml` |
| 回滚实例参数 | `ncrsentinelclusterconfigrollback` | update | `paas-cli update ncrsentinelclusterconfigrollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-config-rollback.yaml` | `config/redis/iteration-ncr-sentinel-cluster-config-rollback.yaml` |

#### 3. 主从版规格

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 变更规格 | `ncrsentinelclusterresourceusage` | update | `paas-cli update ncrsentinelclusterresourceusage --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-resource-usage.yaml` | `config/redis/iteration-ncr-sentinel-cluster-resource-usage.yaml` |
| 规格回滚 | `ncrsentinelclusterresourceusagerollback` | update | `paas-cli update ncrsentinelclusterresourceusagerollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-resource-usage-rollback.yaml` | `config/redis/iteration-ncr-sentinel-cluster-resource-usage-rollback.yaml` |

#### 4. 主从版服务发现

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建 ClusterIP | `ncrsentinelclusterip` | create | `paas-cli create ncrsentinelclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` | `config/redis/iteration-ncr-sentinel-cluster.yaml` |
| 获取 ClusterIP | `ncrsentinelclusterip` | get | `paas-cli get ncrsentinelclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` | `config/redis/iteration-ncr-sentinel-cluster.yaml` |
| 删除 ClusterIP | `ncrsentinelclusterip` | delete | `paas-cli delete ncrsentinelclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` | `config/redis/iteration-ncr-sentinel-cluster.yaml` |
| 创建 LoadBalancer | `ncrsentinelclusterlb` | create | `paas-cli create ncrsentinelclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-lb.yaml` | `config/redis/iteration-ncr-sentinel-cluster-lb.yaml` |
| 获取 LoadBalancer | `ncrsentinelclusterlb` | get | `paas-cli get ncrsentinelclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-lb.yaml` | `config/redis/iteration-ncr-sentinel-cluster-lb.yaml` |
| 删除 LoadBalancer | `ncrsentinelclusterlb` | delete | `paas-cli delete ncrsentinelclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-lb.yaml` | `config/redis/iteration-ncr-sentinel-cluster-lb.yaml` |

#### 5. 主从版过期时间

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 设置过期时间 | `ncrsentinelcluster` | update | `paas-cli update ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-set-expire-date.yaml` | `config/redis/iteration-ncr-sentinel-cluster-set-expire-date.yaml` |

---

### Redis 联邦集群

#### 1. 联邦集群版

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建联邦集群版 | `federatedncrcluster` | create | `paas-cli create federatedncrcluster --gateway-config=config/gateway.yaml -f config/fed/ncrcluster.yaml` | `config/fed/ncrcluster.yaml` |
| 获取联邦集群版 | `federatedncrcluster` | get | `paas-cli get federatedncrcluster --gateway-config=config/gateway.yaml -f config/fed/ncrcluster.yaml` | `config/fed/ncrcluster.yaml` |
| 删除联邦集群版 | `federatedncrcluster` | delete | `paas-cli delete federatedncrcluster --gateway-config=config/gateway.yaml -f config/fed/ncrcluster.yaml` | `config/fed/ncrcluster.yaml` |
| 变更实例参数 | `federatedncrclusterconfig` | update | `paas-cli update federatedncrclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-update.yaml` | `config/fed/fed-ncrcluster-config-update.yaml` |
| 查询实例参数 | `federatedncrclusterconfig` | get | `paas-cli get federatedncrclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-get.yaml` | `config/fed/fed-ncrcluster-config-get.yaml` |

#### 2. 联邦哨兵

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建联邦哨兵 | `federatedsentinel` | create | `paas-cli create federatedsentinel --gateway-config=config/gateway.yaml -f config/fed/ncrsentinel.yaml` | `config/fed/ncrsentinel.yaml` |
| 获取联邦哨兵 | `federatedsentinel` | get | `paas-cli get federatedsentinel --gateway-config=config/gateway.yaml -f config/fed/ncrsentinel.yaml` | `config/fed/ncrsentinel.yaml` |
| 删除联邦哨兵 | `federatedsentinel` | delete | `paas-cli delete federatedsentinel --gateway-config=config/gateway.yaml -f config/fed/ncrsentinel.yaml` | `config/fed/ncrsentinel.yaml` |

#### 3. 联邦主从版

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建联邦主从版 | `federatedsentinelcluster` | create | `paas-cli create federatedsentinelcluster --gateway-config=config/gateway.yaml -f config/fed/ncrsentinelcluster.yaml` | `config/fed/ncrsentinelcluster.yaml` |
| 获取联邦主从版 | `federatedsentinelcluster` | get | `paas-cli get federatedsentinelcluster --gateway-config=config/gateway.yaml -f config/fed/ncrsentinelcluster.yaml` | `config/fed/ncrsentinelcluster.yaml` |
| 删除联邦主从版 | `federatedsentinelcluster` | delete | `paas-cli delete federatedsentinelcluster --gateway-config=config/gateway.yaml -f config/fed/ncrsentinelcluster.yaml` | `config/fed/ncrsentinelcluster.yaml` |
| 变更实例参数 | `federatedsentinelclusterconfig` | update | `paas-cli update federatedsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-update.yaml` | `config/fed/fed-ncrcluster-config-update.yaml` |
| 查询实例参数 | `federatedsentinelclusterconfig` | get | `paas-cli get federatedsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-get.yaml` | `config/fed/fed-ncrcluster-config-get.yaml` |

---

### Redis 高阶策略

#### 1. 多活策略

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建多活策略 | `activestrategy` | create | `paas-cli create activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml` | `config/redis/ncractivestrategy.yaml` |
| 获取多活策略 | `activestrategy` | get | `paas-cli get activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml` | `config/redis/ncractivestrategy.yaml` |
| 获取多活策略列表 | `activestrategy` | get | `paas-cli get activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml` | `config/redis/ncractivestrategy.yaml` |
| 删除多活策略 | `activestrategy` | delete | `paas-cli delete activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml` | `config/redis/ncractivestrategy.yaml` |
| 更新多活策略 | `activestrategy` | update | `paas-cli update activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy-update.yaml` | `config/redis/ncractivestrategy-update.yaml` |
| 更新 Proxy 读模式 | `activestrategy` | update | `paas-cli update activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy-proxyReadMode-update.yaml` | `config/redis/ncractivestrategy-proxyReadMode-update.yaml` |

#### 2. 多活切换操作

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 双集群主从切换 | `activestrategy` | switch | `paas-cli switch activestrategy --gateway-config=config/gateway.yaml -f config/redis/redis-activestrategy.yaml` | `config/redis/redis-activestrategy.yaml` |
| 多活降备 | `demoteActiveMaster` | switch | `paas-cli switch demoteActiveMaster --gateway-config=config/gateway.yaml -f config/redis/redis-demoteActiveMaster.yaml` | `config/redis/redis-demoteActiveMaster.yaml` |
| 多活升主 | `promoteActiveSlave` | switch | `paas-cli switch promoteActiveSlave --gateway-config=config/gateway.yaml -f config/redis/redis-promoteActiveSlave.yaml` | `config/redis/redis-promoteActiveSlave.yaml` |
| 切流恢复 | `activestrategy` | switch | `paas-cli switch activestrategy --gateway-config=config/gateway.yaml -f config/redis/autoSwitchResetRecovery.yaml` | `config/redis/autoSwitchResetRecovery.yaml` |
| 逻辑主恢复 | `configLogicMasterRecover` | update | `paas-cli update configLogicMasterRecover --gateway-config=config/gateway.yaml -f config/redis/configLogicMasterRecover.yaml` | `config/redis/configLogicMasterRecover.yaml` |

#### 3. 热备策略

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建热备策略 | `hotbackupstrategy` | create | `paas-cli create hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml` | `config/redis/ncrhotbackupstrategy.yaml` |
| 获取热备策略 | `hotbackupstrategy` | get | `paas-cli get hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml` | `config/redis/ncrhotbackupstrategy.yaml` |
| 获取热备策略列表 | `hotbackupstrategy` | get | `paas-cli get hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml` | `config/redis/ncrhotbackupstrategy.yaml` |
| 删除热备策略 | `hotbackupstrategy` | delete | `paas-cli delete hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml` | `config/redis/ncrhotbackupstrategy.yaml` |
| 热备切换 | `hotbackupstrategy` | switch | `paas-cli switch hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/switchredishotback.yaml` | `config/redis/switchredishotback.yaml` |

#### 4. 单元化策略

| 功能 | resource | action | 命令示例 | 配置文件 |
|------|----------|--------|----------|----------|
| 创建单元化策略 | `unitstrategy` | create | `paas-cli create unitstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrunitstrategy.yaml` | `config/redis/ncrunitstrategy.yaml` |
| 获取单元化策略 | `unitstrategy` | get | `paas-cli get unitstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrunitstrategy.yaml` | `config/redis/ncrunitstrategy.yaml` |
| 获取单元化策略列表 | `unitstrategy` | get | `paas-cli get unitstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrunitstrategy.yaml` | `config/redis/ncrunitstrategy.yaml` |
| 删除单元化策略 | `unitstrategy` | delete | `paas-cli delete unitstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrunitstrategy.yaml` | `config/redis/ncrunitstrategy.yaml` |

---

## 附录：YAML 参数说明

### Nacos 集群创建参数

```yaml
resource: nacoscluster
action: create
params:
  namespace: project1-paas       # [必选] k8s 空间
  cluster: qa-ci-cluster1        # [必选] k8s 集群
  project: j036x0                # [可选] 所属项目(系统)
  name: my-nacos                 # [必选] nacos 集群名称
  username: nacos                # [必选] nacos 集群用户名
  password: "123456"             # [必选] nacos 集群用户密码
  description: description       # [可选] 描述信息
  configTemplate: default        # [可选] 配置模板
  cpuRequest: 1                  # [可选] CPU request 默认 500m
  memRequest: 1Gi                # [可选] memory request 默认 2G
  cpuLimit: 2                    # [可选] CPU limit 默认 2
  memLimit: 2Gi                  # [可选] memory limit 默认 4G
  jvmXmx: 2048M                  # [可选] JVM 最大堆内存
  jvmXms: 2048M                  # [可选] JVM 初始堆内存
  jvmXmn: 512M                   # [可选] JVM 年轻代大小
  replicas: 3                    # [可选] 副本数 默认 3
  diskSize: 4Gi                  # [可选] 磁盘大小 默认 20G
  diskType: localstorage         # [可选] 磁盘类型
  version: 2.2.1                 # [可选] nacos 版本
  atomic: true                   # [可选] 创建失败自动删除
  waitSeconds: 600               # [可选] 最大等待秒数
```

### ES 集群创建参数

```yaml
resource: escluster
action: create
params:
  namespace: project1-paas       # [必选] k8s 空间
  cluster: qa-ci-cluster1        # [必选] k8s 集群
  name: my-es-cluster            # [必选] ES 集群名称
  self:
    password: '123456'           # [选填] 自定义密码
    clusterMode: mix             # [必选] 部署模式: mix / detach
    configTemplate: default      # [选填] 参数模板
    mix:                         # 混合部署配置
      resources:
        limits:
          cpu: 4
          memory: 8Gi
        requests:
          cpu: 100m
          memory: 200Mi
      count: 3                   # 节点数量
      storage: 4Gi               # 持久化存储
      storageClass: localstorage # 存储类型
  atomic: true                   # [选填] 创建失败自动删除
  waitSeconds: 600               # [选填] 最大等待秒数
```

### Redis 集群版创建参数

```yaml
resource: ncrcluster
action: create
params:
  namespace: j036x0-paas         # [必填] k8s 命名空间
  cluster: cluster-id            # [选填] k8s 集群
  project: j036x0                # [必填] 所属项目
  name: my-redis-cluster         # [必填] redis 集群名称
  masterNum: 3                   # [选填] 主节点数 默认 3
  port: 6379                     # [选填] 端口号
  cpuRequest: 500m               # [选填] CPU request
  memRequest: 1Gi                # [选填] memory request
  cpuLimit: 1                    # [选填] CPU limit
  memLimit: 2Gi                  # [选填] memory limit
  version: 5.0.14                # [选填] redis 版本
  password: "123456"             # [选填] redis 密码
  configTemplate: ncrcluster-default # [选填] 参数模板
  proxyCount: 2                  # [选填] proxy 数量
  proxyType: envoy               # [选填] proxy 类型
  diskSize: 4Gi                  # [选填] 本地磁盘大小
  diskType: localstorage         # [选填] 磁盘类型
  atomic: true                   # [选填] 创建失败自动删除
  waitSeconds: 600               # [选填] 最大等待秒数
```

### Redis 多活策略创建参数

```yaml
resource: activestrategy
action: create
params:
  name: active-strategy-test001  # [必填] 策略名称
  clusterType: cluster           # [必填] 集群类型: cluster / sentinel
  clusterCnt: 2                  # [必填] 多活集群数量
  clusters:                      # [必填] 集群列表
    - 1/wxx/cluster-active-0
    - 1/wxx/cluster-active-1
  failoverRecover: auto          # [选填] 故障恢复策略
  sharedDownRecover: auto        # [选填] 分片故障恢复策略
  enableHealthCheck: true        # [选填] 是否自动切流
  proxyReadMode: preferLogicMaster # [选填] 读策略
```