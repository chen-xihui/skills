# Redis 集群版操作说明

## 一、Redis 集群版

### 1.1 集群管理

#### 操作 1：创建集群版

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建集群版 |
| resource | `ncrcluster` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml` |

```bash
paas-cli create ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml
```

**YAML 配置示例** (`iteration-ncr-cluster.yaml`)：
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

### 确认流程

```
即将执行以下操作：
  命令：paas-cli create ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml
  说明：创建 Redis 集群版实例
  影响：新增 Redis 集群，分配计算和存储资源

是否继续执行？
```

---

#### 操作 2：获取集群版

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取集群版 |
| resource | `ncrcluster` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml` |

```bash
paas-cli get ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml
```

**返回信息**：集群模式、节点数量、运行状态、连接数、各节点角色和 Slot 范围等。

---

#### 操作 3：删除集群版

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除集群版 |
| resource | `ncrcluster` |
| action | `delete` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml` |

```bash
paas-cli delete ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml
```

### 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli delete ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster.yaml
  说明：删除 Redis 集群版
  影响范围：
    - 集群中所有数据将被永久删除，不可恢复
    - 所有依赖此集群的应用将无法访问
    - 此操作不可逆

请输入"确认"以执行此操作：
```

---

#### 操作 4：更新集群版

| 属性 | 说明 |
|------|------|
| 操作类型 | 更新集群版 |
| resource | `ncrcluster` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-update.yaml` |

```bash
paas-cli update ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-update.yaml
```

---

### 1.2 实例参数

#### 操作 5：查询实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 查询实例参数 |
| resource | `ncrclusterconfig` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get ncrclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-config-get.yaml` |

```bash
paas-cli get ncrclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-config-get.yaml
```

---

#### 操作 6：变更实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 变更实例参数 |
| resource | `ncrclusterconfig` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-config-update.yaml` |

```bash
paas-cli update ncrclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-config-update.yaml
```

---

#### 操作 7：回滚实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 回滚实例参数 |
| resource | `ncrclusterconfigrollback` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrclusterconfigrollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-config-rollback.yaml` |

```bash
paas-cli update ncrclusterconfigrollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-config-rollback.yaml
```

---

### 1.3 扩缩容与规格

#### 操作 8：分片扩缩容

| 属性 | 说明 |
|------|------|
| 操作类型 | 分片扩缩容 |
| resource | `ncrclusterreplicas` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrclusterreplicas --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-replicas-update.yaml` |

```bash
paas-cli update ncrclusterreplicas --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-replicas-update.yaml
```

---

#### 操作 9：变更规格

| 属性 | 说明 |
|------|------|
| 操作类型 | 变更规格 |
| resource | `ncrclusterresourceusage` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrclusterresourceusage --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-resource-usage-update.yaml` |

```bash
paas-cli update ncrclusterresourceusage --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-resource-usage-update.yaml
```

---

#### 操作 10：规格回滚

| 属性 | 说明 |
|------|------|
| 操作类型 | 规格回滚 |
| resource | `ncrclusterresourceusagerollback` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrclusterresourceusagerollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-resource-usage-rollback.yaml` |

```bash
paas-cli update ncrclusterresourceusagerollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-resource-usage-rollback.yaml
```

---

### 1.4 服务发现

#### 操作 11：创建 ClusterIP

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建 ClusterIP |
| resource | `ncrclusterip` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create ncrclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-clusterip.yaml` |

```bash
paas-cli create ncrclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-clusterip.yaml
```

---

#### 操作 12：获取 ClusterIP

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取 ClusterIP |
| resource | `ncrclusterip` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get ncrclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-clusterip.yaml` |

```bash
paas-cli get ncrclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-clusterip.yaml
```

---

#### 操作 13：删除 ClusterIP

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除 ClusterIP |
| resource | `ncrclusterip` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete ncrclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-clusterip.yaml` |

```bash
paas-cli delete ncrclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-clusterip.yaml
```

---

#### 操作 14：创建 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建 LoadBalancer |
| resource | `ncrclusterlb` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create ncrclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-lb.yaml` |

```bash
paas-cli create ncrclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-lb.yaml
```

---

#### 操作 15：获取 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取 LoadBalancer |
| resource | `ncrclusterlb` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get ncrclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-lb.yaml` |

```bash
paas-cli get ncrclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-lb.yaml
```

---

#### 操作 16：删除 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除 LoadBalancer |
| resource | `ncrclusterlb` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete ncrclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-lb.yaml` |

```bash
paas-cli delete ncrclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-lb.yaml
```

---

### 1.5 过期时间

#### 操作 17：设置过期时间

| 属性 | 说明 |
|------|------|
| 操作类型 | 设置过期时间 |
| resource | `ncrcluster` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-set-expire-date.yaml` |

```bash
paas-cli update ncrcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-cluster-set-expire-date.yaml
```