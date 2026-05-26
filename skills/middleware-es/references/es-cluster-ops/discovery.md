# ES 服务发现

## 操作 11：创建 ClusterIP

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建 ClusterIP |
| resource | `esclusterip` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli create esclusterip --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-clusterIP.yaml
```

---

## 操作 12：获取 ClusterIP

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取 ClusterIP |
| resource | `esclusterip` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |

```bash
paas-cli get esclusterip --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-clusterIP.yaml
```

---

## 操作 13：删除 ClusterIP

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除 ClusterIP |
| resource | `esclusterip` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli delete esclusterip --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-clusterIP.yaml
```

---

## 操作 14：创建 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建 LoadBalancer |
| resource | `eslb` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli create eslb --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-lb.yaml
```

---

## 操作 15：获取 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取 LoadBalancer |
| resource | `eslb` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |

```bash
paas-cli get eslb --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-lb.yaml
```

---

## 操作 16：删除 LoadBalancer

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除 LoadBalancer |
| resource | `eslb` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli delete eslb --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-lb.yaml
```