# Redis 联邦集群操作说明

## 四、Redis 联邦集群

### 4.1 联邦集群版

#### 操作 44：创建联邦集群版

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建联邦集群版 |
| resource | `federatedncrcluster` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create federatedncrcluster --gateway-config=config/gateway.yaml -f config/fed/ncrcluster.yaml` |

```bash
paas-cli create federatedncrcluster --gateway-config=config/gateway.yaml -f config/fed/ncrcluster.yaml
```

---

#### 操作 45：获取联邦集群版

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取联邦集群版 |
| resource | `federatedncrcluster` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get federatedncrcluster --gateway-config=config/gateway.yaml -f config/fed/ncrcluster.yaml` |

```bash
paas-cli get federatedncrcluster --gateway-config=config/gateway.yaml -f config/fed/ncrcluster.yaml
```

---

#### 操作 46：删除联邦集群版

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除联邦集群版 |
| resource | `federatedncrcluster` |
| action | `delete` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete federatedncrcluster --gateway-config=config/gateway.yaml -f config/fed/ncrcluster.yaml` |

```bash
paas-cli delete federatedncrcluster --gateway-config=config/gateway.yaml -f config/fed/ncrcluster.yaml
```

---

#### 操作 47：变更实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 变更实例参数 |
| resource | `federatedncrclusterconfig` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update federatedncrclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-update.yaml` |

```bash
paas-cli update federatedncrclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-update.yaml
```

---

#### 操作 48：查询实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 查询实例参数 |
| resource | `federatedncrclusterconfig` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get federatedncrclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-get.yaml` |

```bash
paas-cli get federatedncrclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-get.yaml
```

---

### 4.2 联邦哨兵

#### 操作 49：创建联邦哨兵

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建联邦哨兵 |
| resource | `federatedsentinel` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create federatedsentinel --gateway-config=config/gateway.yaml -f config/fed/ncrsentinel.yaml` |

```bash
paas-cli create federatedsentinel --gateway-config=config/gateway.yaml -f config/fed/ncrsentinel.yaml
```

---

#### 操作 50：获取联邦哨兵

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取联邦哨兵 |
| resource | `federatedsentinel` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get federatedsentinel --gateway-config=config/gateway.yaml -f config/fed/ncrsentinel.yaml` |

```bash
paas-cli get federatedsentinel --gateway-config=config/gateway.yaml -f config/fed/ncrsentinel.yaml
```

---

#### 操作 51：删除联邦哨兵

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除联邦哨兵 |
| resource | `federatedsentinel` |
| action | `delete` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete federatedsentinel --gateway-config=config/gateway.yaml -f config/fed/ncrsentinel.yaml` |

```bash
paas-cli delete federatedsentinel --gateway-config=config/gateway.yaml -f config/fed/ncrsentinel.yaml
```

---

### 4.3 联邦主从版

#### 操作 52：创建联邦主从版

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建联邦主从版 |
| resource | `federatedsentinelcluster` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli create federatedsentinelcluster --gateway-config=config/gateway.yaml -f config/fed/ncrsentinelcluster.yaml` |

```bash
paas-cli create federatedsentinelcluster --gateway-config=config/gateway.yaml -f config/fed/ncrsentinelcluster.yaml
```

---

#### 操作 53：获取联邦主从版

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取联邦主从版 |
| resource | `federatedsentinelcluster` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get federatedsentinelcluster --gateway-config=config/gateway.yaml -f config/fed/ncrsentinelcluster.yaml` |

```bash
paas-cli get federatedsentinelcluster --gateway-config=config/gateway.yaml -f config/fed/ncrsentinelcluster.yaml
```

---

#### 操作 54：删除联邦主从版

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除联邦主从版 |
| resource | `federatedsentinelcluster` |
| action | `delete` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli delete federatedsentinelcluster --gateway-config=config/gateway.yaml -f config/fed/ncrsentinelcluster.yaml` |

```bash
paas-cli delete federatedsentinelcluster --gateway-config=config/gateway.yaml -f config/fed/ncrsentinelcluster.yaml
```

---

#### 操作 55：变更实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 变更实例参数 |
| resource | `federatedsentinelclusterconfig` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli update federatedsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-update.yaml` |

```bash
paas-cli update federatedsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-update.yaml
```

---

#### 操作 56：查询实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 查询实例参数 |
| resource | `federatedsentinelclusterconfig` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli get federatedsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-get.yaml` |

```bash
paas-cli get federatedsentinelclusterconfig --gateway-config=config/gateway.yaml -f config/fed/fed-ncrcluster-config-get.yaml
```