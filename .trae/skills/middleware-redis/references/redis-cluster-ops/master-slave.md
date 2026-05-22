# Redis 主从版操作说明

## 三、Redis 主从版

### 3.1 主从集群管理

#### 操作 28：创建主从版

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建主从版 |
| resource | `ncrsentinelcluster` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` |

```bash
paas-cli create ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml
```

---

#### 操作 29：获取主从版

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取主从版 |
| resource | `ncrsentinelcluster` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` |

```bash
paas-cli get ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml
```

---

#### 操作 30：删除主从版

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除主从版 |
| resource | `ncrsentinelcluster` |
| action | `delete` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` |

```bash
paas-cli delete ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml
```

---

#### 操作 31：更新主从版

| 属性 | 说明 |
|------|------|
| 操作类型 | 更新主从版 |
| resource | `ncrsentinelcluster` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` |

```bash
paas-cli update ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml
```

---

### 3.2 主从版实例参数

#### 操作 32：查询实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 查询实例参数 |
| resource | `ncrsentinelclusterconfig` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get ncrsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-config-get.yaml` |

```bash
paas-cli get ncrsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-config-get.yaml
```

---

#### 操作 33：变更实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 变更实例参数 |
| resource | `ncrsentinelclusterconfig` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-config-update.yaml` |

```bash
paas-cli update ncrsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-config-update.yaml
```

---

#### 操作 34：回滚实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 回滚实例参数 |
| resource | `ncrsentinelclusterconfigrollback` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrsentinelclusterconfigrollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-config-rollback.yaml` |

```bash
paas-cli update ncrsentinelclusterconfigrollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-config-rollback.yaml
```

---

### 3.3 主从版规格

#### 操作 35：变更规格

| 属性 | 说明 |
|------|------|
| 操作类型 | 变更规格 |
| resource | `ncrsentinelclusterresourceusage` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrsentinelclusterresourceusage --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-resource-usage.yaml` |

```bash
paas-cli update ncrsentinelclusterresourceusage --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-resource-usage.yaml
```

---

#### 操作 36：规格回滚

| 属性 | 说明 |
|------|------|
| 操作类型 | 规格回滚 |
| resource | `ncrsentinelclusterresourceusagerollback` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrsentinelclusterresourceusagerollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-resource-usage-rollback.yaml` |

```bash
paas-cli update ncrsentinelclusterresourceusagerollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-resource-usage-rollback.yaml
```

---

### 3.4 主从版服务发现

#### 操作 37：创建 ClusterIP

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建 ClusterIP |
| resource | `ncrsentinelclusterip` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create ncrsentinelclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` |

```bash
paas-cli create ncrsentinelclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml
```

---

#### 操作 38：获取 ClusterIP

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取 ClusterIP |
| resource | `ncrsentinelclusterip` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get ncrsentinelclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` |

```bash
paas-cli get ncrsentinelclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml
```

---

#### 操作 39：删除 ClusterIP

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除 ClusterIP |
| resource | `ncrsentinelclusterip` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete ncrsentinelclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml` |

```bash
paas-cli delete ncrsentinelclusterip --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster.yaml
```

---

#### 操作 40：创建 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建 LoadBalancer |
| resource | `ncrsentinelclusterlb` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create ncrsentinelclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-lb.yaml` |

```bash
paas-cli create ncrsentinelclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-lb.yaml
```

---

#### 操作 41：获取 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取 LoadBalancer |
| resource | `ncrsentinelclusterlb` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get ncrsentinelclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-lb.yaml` |

```bash
paas-cli get ncrsentinelclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-lb.yaml
```

---

#### 操作 42：删除 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除 LoadBalancer |
| resource | `ncrsentinelclusterlb` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete ncrsentinelclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-lb.yaml` |

```bash
paas-cli delete ncrsentinelclusterlb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-lb.yaml
```

---

### 3.5 主从版过期时间

#### 操作 43：设置过期时间

| 属性 | 说明 |
|------|------|
| 操作类型 | 设置过期时间 |
| resource | `ncrsentinelcluster` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-set-expire-date.yaml` |

```bash
paas-cli update ncrsentinelcluster --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-cluster-set-expire-date.yaml
```