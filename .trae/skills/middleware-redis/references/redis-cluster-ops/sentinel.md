# Redis 哨兵操作说明

## 二、Redis 哨兵

### 2.1 哨兵管理

#### 操作 18：创建哨兵

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建哨兵 |
| resource | `ncrsentinel` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel.yaml` |

```bash
paas-cli create ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel.yaml
```

---

#### 操作 19：获取哨兵

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取哨兵 |
| resource | `ncrsentinel` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel.yaml` |

```bash
paas-cli get ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel.yaml
```

---

#### 操作 20：删除哨兵

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除哨兵 |
| resource | `ncrsentinel` |
| action | `delete` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel.yaml` |

```bash
paas-cli delete ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel.yaml
```

---

#### 操作 21：更新哨兵

| 属性 | 说明 |
|------|------|
| 操作类型 | 更新哨兵 |
| resource | `ncrsentinel` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-update.yaml` |

```bash
paas-cli update ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-update.yaml
```

---

### 2.2 哨兵规格

#### 操作 22：变更规格

| 属性 | 说明 |
|------|------|
| 操作类型 | 变更规格 |
| resource | `ncrsentinelresourceusage` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrsentinelresourceusage --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-resource-usage.yaml` |

```bash
paas-cli update ncrsentinelresourceusage --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-resource-usage.yaml
```

---

#### 操作 23：规格回滚

| 属性 | 说明 |
|------|------|
| 操作类型 | 规格回滚 |
| resource | `ncrsentinelresourceusagerollback` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrsentinelresourceusagerollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-resource-usage-rollback.yaml` |

```bash
paas-cli update ncrsentinelresourceusagerollback --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-resource-usage-rollback.yaml
```

---

### 2.3 哨兵服务发现

#### 操作 24：创建 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建 LoadBalancer |
| resource | `ncrsentinellb` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create ncrsentinellb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-lb.yaml` |

```bash
paas-cli create ncrsentinellb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-lb.yaml
```

---

#### 操作 25：获取 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取 LoadBalancer |
| resource | `ncrsentinellb` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get ncrsentinellb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-lb.yaml` |

```bash
paas-cli get ncrsentinellb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-lb.yaml
```

---

#### 操作 26：删除 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除 LoadBalancer |
| resource | `ncrsentinellb` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete ncrsentinellb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-lb.yaml` |

```bash
paas-cli delete ncrsentinellb --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-lb.yaml
```

---

### 2.4 哨兵过期时间

#### 操作 27：设置过期时间

| 属性 | 说明 |
|------|------|
| 操作类型 | 设置过期时间 |
| resource | `ncrsentinel` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-set-expire-date.yaml` |

```bash
paas-cli update ncrsentinel --gateway-config=config/gateway.yaml -f config/redis/iteration-ncr-sentinel-set-expire-date.yaml
```