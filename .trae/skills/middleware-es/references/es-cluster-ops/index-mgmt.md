# ES 索引管理

## 操作 17：创建索引

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建索引 |
| resource | `esindex` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli create esindex --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index.yaml
```

---

## 操作 18：获取索引

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取索引 |
| resource | `esindex` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |

```bash
paas-cli get esindex --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index.yaml
```

---

## 操作 19：更新索引

| 属性 | 说明 |
|------|------|
| 操作类型 | 更新索引 |
| resource | `esindex` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli update esindex --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index.yaml
```

---

## 操作 20：删除索引

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除索引 |
| resource | `esindex` |
| action | `delete` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |

```bash
paas-cli delete esindex --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index.yaml
```

**⚠️ 注意**：删除索引为不可逆操作，请确认数据已备份或不再需要后再执行。

---

## 操作 21：创建索引模板

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建索引模板 |
| resource | `esindextemplate` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli create esindextemplate --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index-template.yaml
```

---

## 操作 22：获取索引模板

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取索引模板 |
| resource | `esindextemplate` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |

```bash
paas-cli get esindextemplate --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index-template.yaml
```

---

## 操作 23：更新索引模板

| 属性 | 说明 |
|------|------|
| 操作类型 | 更新索引模板 |
| resource | `esindextemplate` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli update esindextemplate --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index-template.yaml
```

---

## 操作 24：删除索引模板

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除索引模板 |
| resource | `esindextemplate` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli delete esindextemplate --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-index-template.yaml
```