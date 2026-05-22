# ES 扩缩容与资源管理

## 操作 7：集群扩缩容

| 属性 | 说明 |
|------|------|
| 操作类型 | 集群扩缩容 |
| resource | `esclusterreplicas` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli update esclusterreplicas --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-replicas-update.yaml
```

**注意事项**
- 扩容时新节点加入集群后，分片会自动重新分配（rebalance）
- 缩容时需确保节点上的分片能迁移到其他节点
- 建议逐步扩缩容（每次 1-2 个节点），观察集群状态

---

## 操作 8：变更集群规格

| 属性 | 说明 |
|------|------|
| 操作类型 | 变更集群规格 |
| resource | `esclusterresourceusage` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli update esclusterresourceusage --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-resource-usage-update.yaml
```

---

## 操作 9：调整资源配置

| 属性 | 说明 |
|------|------|
| 操作类型 | 调整资源配置 |
| resource | `esclusterresource` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli update esclusterresource --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-resource-update.yaml
```

---

## 操作 10：资源配置回滚

| 属性 | 说明 |
|------|------|
| 操作类型 | 资源配置回滚 |
| resource | `esclusterresourcerollback` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli update esclusterresourcerollback --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster-resource-rollback.yaml
```