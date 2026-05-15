# Nacos 集群交互操作索引

本目录包含 Nacos 集群交互的 8 项操作详细说明。

**使用方式**：先在本索引中定位需要执行的操作类型，再读取对应文件获取详细命令、参数和确认流程。

**通用前置条件**：执行任何操作前，先读取 [prerequisites.md](./prerequisites.md) 检查 paas-cli 可用性和网络连通性。

---

## 操作索引

| 操作类型 | 风险等级 | 需确认 | 详细文件 |
|---------|---------|--------|---------|
| 查询集群信息 | 🟢 低风险 | 否 | [op-01-query-cluster-info.md](./op-01-query-cluster-info.md) |
| 查询服务注册实例 | 🟢 低风险 | 否 | [op-02-query-instances.md](./op-02-query-instances.md) |
| 查询配置列表 | 🟢 低风险 | 否 | [op-03-query-config-list.md](./op-03-query-config-list.md) |
| 创建服务 | 🟡 中风险 | 是 | [op-04-create-service.md](./op-04-create-service.md) |
| 扩缩容 | 🟡 中风险 | 是 | [op-05-scale.md](./op-05-scale.md) |
| 配置灰度发布 | 🟡 中风险 | 是 | [op-06-gray-publish.md](./op-06-gray-publish.md) |
| 升级版本 | 🔴 高风险 | 是 | [op-07-upgrade.md](./op-07-upgrade.md) |
| 删除服务 | 🔴 高风险 | 是 | [op-08-delete-service.md](./op-08-delete-service.md) |

---

## 确认流程速查

- 🟢 低风险：直接执行，无需确认
- 🟡 中风险：展示命令 → 询问"是否继续？" → 获得肯定回复后执行
- 🔴 高风险：展示命令及影响范围 → 要求用户明确回复"确认" → 方可执行
