# 诊断流程详解

## 完整诊断流程

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

## 步骤详解

### 步骤 1：信息收集

- 记录用户描述的异常现象（symptom）
- 确认必要参数：`project_id`、`env`
- 如用户未描述具体现象，询问：
  - "请描述一下具体的异常表现，例如：查询慢、写入失败、集群状态异常等"
  - "异常是从什么时候开始的？"
  - "是否有过最近的变更操作？"

### 步骤 2：集群状态检查

```bash
paas-cli es info --project {project_id} --env {env}
```

关注信息：
- 集群状态：Green（正常）/ Yellow（部分副本不可用）/ Red（部分主分片不可用）
- 节点数量：是否与预期一致
- 未分配分片数：是否为 0
- 数据节点负载

### 步骤 3：扁鹊诊断

```bash
bianque diagnose --middleware es --project {project_id} --env {env} --check cluster-health,shard,cpu,watermark
```

默认超时 60 秒，如超时或不可达，降级为仅 paas-cli 检查。

### 步骤 4：补充信息收集

根据步骤 2 和 3 的结果，选择性执行：

```bash
# 如集群状态为 Yellow/Red，查看索引状态
paas-cli es indices --project {project_id} --env {env}

# 如怀疑磁盘问题，查看磁盘使用率
paas-cli es disk-usage --project {project_id} --env {env}
```

### 步骤 5：结果分析与建议

综合所有诊断数据，生成处理建议，按优先级排序。
