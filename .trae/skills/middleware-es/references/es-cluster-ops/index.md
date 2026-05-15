# ES 集群交互操作索引

本目录包含 ES 集群交互的 9 项操作详细说明。智能体执行集群操作时，先查阅本索引确认操作类型和风险等级，再按需加载具体操作文件。

## 前置条件

> 执行任何操作前必须完成前置检查，详见 [prerequisites.md](prerequisites.md)

## 操作列表

| 操作 | 风险等级 | 需确认 | 详细文件 |
|------|---------|--------|---------|
| 1. 查看集群状态 | 🟢 低 | 否 | [op-01-cluster-info.md](op-01-cluster-info.md) |
| 2. 查看节点磁盘使用率 | 🟢 低 | 否 | [op-02-disk-usage.md](op-02-disk-usage.md) |
| 3. 查看索引状态 | 🟢 低 | 否 | [op-03-indices.md](op-03-indices.md) |
| 4. 创建索引 | 🟡 中 | 是 | [op-04-create-index.md](op-04-create-index.md) |
| 5. 索引滚动 | 🟡 中 | 是 | [op-05-rollover.md](op-05-rollover.md) |
| 6. Force Merge | 🟡 中 | 是 | [op-06-force-merge.md](op-06-force-merge.md) |
| 7. 扩缩容 | 🟡 中 | 是 | [op-07-scale.md](op-07-scale.md) |
| 8. 升级版本 | 🔴 高 | 是 | [op-08-upgrade.md](op-08-upgrade.md) |
| 9. 删除集群 | 🔴 高 | 是 | [op-09-delete.md](op-09-delete.md) |

## 确认流程速查

| 风险等级 | 确认要求 |
|---------|---------|
| 🟢 低风险 | 无需确认，直接执行 |
| 🟡 中风险 | 展示命令，询问"是否继续执行？"，获得肯定回复后执行 |
| 🔴 高风险 | 展示命令及影响说明，用户必须明确回复"确认"后方可执行 |
