# ES 故障排查详细指南

本文件包含 Elasticsearch 故障排查的详细诊断流程、诊断能力说明、常见故障场景和扁鹊诊断命令，供智能体在执行故障排查时参考。

---

## 1. 诊断流程详解

### 1.1 完整诊断流程

```
信息收集 → 集群状态检查 → 扁鹊诊断 → 补充信息收集 → 结果分析与建议
    │              │               │               │                │
    │              │               │               │                ▼
    │              │               │               │         生成诊断报告
    │              │               │               │
    │              │               │               ▼
    │              │               │        如集群 Yellow/Red：
    │              │               │        查看未分配分片
    │              │               │        查看磁盘使用率
    │              │               │
    │              │               ▼
    │              │        扁鹊诊断（优先）
    │              │        如不可达 → 降级为仅 paas-cli
    │              │
    │              ▼
    │       paas-cli es info
    │       检查集群基本状态
    │
    ▼
  记录用户描述的异常现象
  补充收集必要参数
```

### 1.2 步骤详解

#### 步骤 1：信息收集

- 记录用户描述的异常现象（symptom）
- 确认必要参数：`project_id`、`env`
- 如用户未描述具体现象，询问：
  - "请描述一下具体的异常表现，例如：查询慢、写入失败、集群状态异常等"
  - "异常是从什么时候开始的？"
  - "是否有过最近的变更操作？"

#### 步骤 2：集群状态检查

```bash
paas-cli es info --project {project_id} --env {env}
```

关注信息：
- 集群状态：Green（正常）/ Yellow（部分副本不可用）/ Red（部分主分片不可用）
- 节点数量：是否与预期一致
- 未分配分片数：是否为 0
- 数据节点负载

#### 步骤 3：扁鹊诊断

```bash
bianque diagnose --middleware es --project {project_id} --env {env} --check cluster-health,shard,cpu,watermark
```

默认超时 60 秒，如超时或不可达，降级为仅 paas-cli 检查。

#### 步骤 4：补充信息收集

根据步骤 2 和 3 的结果，选择性执行：

```bash
# 如集群状态为 Yellow/Red，查看索引状态
paas-cli es indices --project {project_id} --env {env}

# 如怀疑磁盘问题，查看磁盘使用率
paas-cli es disk-usage --project {project_id} --env {env}
```

#### 步骤 5：结果分析与建议

综合所有诊断数据，生成处理建议，按优先级排序。

---

## 2. 诊断能力详细说明

### 2.1 集群健康状态

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 + paas-cli |
| 检查命令 | `bianque diagnose --middleware es --check cluster-health` |
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

### 2.2 未分配分片

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware es --check shard` |
| 检查内容 | UNASSIGNED 分片列表及分配失败原因 |

**常见未分配原因**：

| 原因代码 | 说明 | 处理建议 |
|---------|------|---------|
| NODE_LEFT | 节点离开集群 | 等待节点恢复或调整副本数 |
| ALLOCATION_FAILED | 分配失败（如磁盘不足） | 检查磁盘空间，调整水位线 |
| CLUSTER_RECOVERED | 集群恢复中 | 等待恢复完成 |
| INDEX_CREATED | 索引刚创建但无法分配 | 检查节点资源和分配规则 |

### 2.3 CPU 热点

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware es --check cpu` |
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

### 2.4 写入拒绝

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware es --check watermark` |
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

### 2.5 索引健康

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware es --check cluster-health,shard`（包含索引检查） |
| 检查内容 | 副本分片状态、段合并情况 |

**关注指标**：
- 副本分片未分配数
- 段数量过多的索引（> 100 个段）
- 存储大小异常的索引

---

## 3. 常见故障场景与处理建议

### 场景 1：集群状态 Red

**症状**：集群状态显示 Red，部分索引不可用

**诊断步骤**：
1. 执行 `paas-cli es info` 确认集群状态
2. 执行扁鹊诊断检查未分配分片原因
3. 查看索引状态，确认受影响的索引

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 节点宕机 | 重启宕机节点，等待分片恢复 |
| 磁盘空间不足 | 清理旧索引或扩容磁盘 |
| 分片损坏 | 从副本恢复或从备份恢复 |
| 节点数不足 | 扩容或减少副本数 |

### 场景 2：查询缓慢

**症状**：ES 查询响应时间明显变长

**诊断步骤**：
1. 执行扁鹊诊断检查 CPU 热点
2. 查看磁盘使用率是否正常
3. 检查是否有慢查询

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 复杂查询（深分页、脚本查询） | 优化查询方式，使用 search_after 替代深分页 |
| 段数量过多 | 对只读索引执行 Force Merge |
| 索引映射不合理 | 优化 mapping，使用 keyword 替代 text 做精确匹配 |
| JVM GC 频繁 | 检查堆内存设置，优化查询减少内存使用 |
| 磁盘 I/O 瓶颈 | 升级磁盘或减少索引/查询量 |

### 场景 3：写入拒绝

**症状**：写入请求被拒绝或超时

**诊断步骤**：
1. 执行扁鹊诊断检查 watermark
2. 查看磁盘使用率
3. 检查线程池队列拒绝情况

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 磁盘超过洪水水位线 | 清理数据或扩容，解除只读模式 |
| 线程池队列满 | 降低写入速率或增加批量大小 |
| 段合并积压 | 降低写入速率，等待段合并完成 |
| 副本写入拖慢主分片 | 临时减少副本数，写入完成后再恢复 |

### 场景 4：集群状态 Yellow

**症状**：集群状态显示 Yellow，主分片正常但部分副本未分配

**诊断步骤**：
1. 执行 `paas-cli es info` 确认集群状态
2. 执行扁鹊诊断检查未分配分片
3. 查看索引状态和节点资源

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 单节点集群 | 增加节点，使副本可分配 |
| 磁盘空间不足 | 清理旧索引或扩容 |
| 节点暂时离开 | 等待节点恢复，副本会自动分配 |

---

## 4. 扁鹊诊断命令参考

### 4.1 完整诊断命令

```bash
bianque diagnose --middleware es --project {project_id} --env {env} --check cluster-health,shard,cpu,watermark
```

### 4.2 单项诊断命令

```bash
# 仅检查集群健康状态
bianque diagnose --middleware es --project {project_id} --env {env} --check cluster-health

# 仅检查分片状态
bianque diagnose --middleware es --project {project_id} --env {env} --check shard

# 仅检查 CPU 热点
bianque diagnose --middleware es --project {project_id} --env {env} --check cpu

# 仅检查磁盘水位线和写入拒绝
bianque diagnose --middleware es --project {project_id} --env {env} --check watermark
```

### 4.3 返回格式

扁鹊返回 JSON 格式，包含以下字段：

```json
{
  "status": "success|error",
  "findings": [
    {
      "type": "cluster-health|shard|cpu|watermark",
      "severity": "critical|warning|info",
      "message": "描述信息",
      "details": {}
    }
  ],
  "logs": ["相关日志条目"],
  "suggestions": ["处理建议"]
}
```

---

## 5. 降级诊断方案

当扁鹊平台不可达时，使用以下 paas-cli 命令进行基本诊断：

```bash
# 1. 查看集群基本信息
paas-cli es info --project {project_id} --env {env}

# 2. 查看索引状态
paas-cli es indices --project {project_id} --env {env}

# 3. 查看磁盘使用率
paas-cli es disk-usage --project {project_id} --env {env}
```

**降级诊断的局限**：
- 无法获取 CPU 热点和热线程信息
- 无法获取详细的分片分配失败原因
- 无法获取线程池队列拒绝情况
- 建议在报告中注明"本次诊断因扁鹊不可达而降级，部分检查项未能覆盖"

---

## 6. 诊断报告输出模板

```
🔍 故障诊断报告

🩺 诊断目标：Elasticsearch / {env} / {project_id}
📡 诊断来源：扁鹊平台 / paas-cli{如降级则注明"（降级模式）"}

📊 诊断结论：{一句话结论}

📋 详细发现：
  1. {发现1}
  2. {发现2}
  3. {发现3}

💡 处理建议：
  1. {建议1}（优先级：高）
  2. {建议2}（优先级：中）
  3. {建议3}（优先级：低）

📎 相关日志/数据：
{诊断脚本返回的关键数据摘要}
```
