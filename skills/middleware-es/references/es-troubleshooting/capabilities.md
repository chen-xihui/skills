# ES 诊断能力详细说明

## 1. 集群健康状态

| 项目 | 说明 |
|------|------|
| 数据来源 | bianque Skill + paas-cli Skill |
| 检查命令 | `bianque elasticsearch check -n {namespace} -i {instance} -v true` |
| 检查内容 | 集群 Green/Yellow/Red 状态、原因分析 |

**状态含义**：

| 状态 | 含义 | 常见原因 |
|------|------|---------|
| Green | 所有主分片和副本分片都正常 | — |
| Yellow | 主分片正常，但部分副本分片未分配 | 节点数不足、磁盘空间不足 |
| Red | 部分主分片不可用 | 节点宕机、磁盘损坏、分片损坏 |

**paas-cli 辅助命令**：
```bash
paas-cli es info --project {project_id} --env {env}
```

---

## 2. 未分配分片

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque elasticsearch check -n {namespace} -i {instance} -v true` |
| 检查内容 | UNASSIGNED 分片列表及分配失败原因 |

**常见未分配原因**：

| 原因代码 | 说明 | 处理建议 |
|---------|------|---------|
| NODE_LEFT | 节点离开集群 | 等待节点恢复或调整副本数 |
| ALLOCATION_FAILED | 分配失败（如磁盘不足） | 检查磁盘空间，调整水位线 |
| CLUSTER_RECOVERED | 集群恢复中 | 等待恢复完成 |
| INDEX_CREATED | 索引刚创建但无法分配 | 检查节点资源和分配规则 |

---

## 3. CPU 热点

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque elasticsearch check -n {namespace} -i {instance} -v true` |
| 检查内容 | 节点 CPU 使用率、热线程分析 |

**关注指标**：
- 节点 CPU 使用率 > 80%：需要关注
- 节点 CPU 使用率 > 95%：紧急处理
- 热线程类型：search / index / merge / gc

**常见原因**：
- 复杂查询或脚本查询
- 大量写入或段合并
- GC（垃圾回收）频繁
- 查询请求堆积

---

## 4. 写入拒绝

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque elasticsearch check -n {namespace} -i {instance} -v true -o 50` |
| 检查内容 | 磁盘水位线状态、线程池队列拒绝情况 |

**关注指标**：
- 磁盘使用率超过 85%（低水位线）：新分片不分配
- 磁盘使用率超过 90%（高水位线）：分片开始迁移
- 磁盘使用率超过 95%（洪水水位线）：索引设为只读
- 线程池拒绝数 > 0：请求被拒绝

**常见原因**：
- 磁盘空间不足
- 写入速度超过处理能力
- 线程池配置过小

---

## 5. 索引健康

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque elasticsearch check -n {namespace} -i {instance} -v true` |
| 检查内容 | 副本分片状态、段合并情况 |

**关注指标**：
- 副本分片未分配数
- 段数量过多的索引（> 100 个段）
- 存储大小异常的索引