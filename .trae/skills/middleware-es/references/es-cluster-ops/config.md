# ES 实例参数管理

## 操作 4：查询实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 查询实例参数 |
| resource | `esclusterconfig` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |

```bash
paas-cli get esclusterconfig --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-config-get.yaml
```

---

## 操作 5：更改实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 更改实例参数 |
| resource | `esclusterconfig` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli update esclusterconfig --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-config-update.yaml
```

**确认流程**：
```
即将执行以下操作：
  命令：paas-cli update esclusterconfig --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-config-update.yaml
  说明：更改 ES 集群实例参数
  影响：参数变更可能触发节点重启，影响集群可用性

是否继续执行？
```

---

## 操作 6：回滚实例参数

| 属性 | 说明 |
|------|------|
| 操作类型 | 回滚实例参数 |
| resource | `esclusterconfigrollback` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli update esclusterconfigrollback --gateway-config=config/gateway.yaml -f config/es/iteration-elastcisearch-cluster-rollback-config.yaml
```