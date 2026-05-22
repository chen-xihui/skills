# Redis 故障排查索引

本目录包含 Redis 故障排查的完整指南，包括诊断流程、常见场景、容灾排查和专项测试。

## 目录结构

| 文件 | 内容 |
|------|------|
| [diagnosis.md](./diagnosis.md) | 诊断能力详细说明（慢查询、内存碎片、主从延迟、持久化、故障转移） |
| [scenarios.md](./scenarios.md) | 常见故障场景与处理建议（响应慢、内存满、连接超时、主从不一致） |
| [disaster-recovery.md](./disaster-recovery.md) | 容灾故障排查（功能限制、切换流程、Proxy兼容性、数据同步时延） |
| [test-cases.md](./test-cases.md) | 专项测试案例（网络抖动、全量宕机、主从切换、分片故障、容灾切换） |
| [fault-tolerance.md](./fault-tolerance.md) | 容错开发检查清单（健康检查、异常处置、核心接口可靠性） |

---

## 诊断流程

### 完整流程

```
信息收集 → 集群状态检查 → 扁鹊诊断 → 补充信息收集 → 结果分析与建议
```

### 步骤详解

#### 步骤 1：信息收集

- 记录用户描述的异常现象（symptom）
- 确认必要参数：`project_id`、`env`
- 常见现象分类：
  - 连接异常：连接超时、拒绝连接
  - 性能异常：响应慢、延迟高
  - 内存异常：OOM、内存满
  - 数据异常：数据丢失、主从不一致
  - 持久化异常：RDB/AOF 保存失败

#### 步骤 2：集群状态检查

```bash
paas-cli redis info --project {project_id} --env {env}
```

关注信息：
- 集群模式（standalone/sentinel/cluster）
- 节点在线状态
- 连接数和阻塞客户端数
- 内存使用率和淘汰策略

#### 步骤 3：扁鹊诊断

```bash
bianque redis check -n {namespace} -i {instance} -t {type} -v true
```

默认超时 60 秒，如不可达降级为仅 paas-cli。

#### 步骤 4：补充信息收集

根据结果选择性执行：

```bash
# 查看内存详情
paas-cli redis memory --project {project_id} --env {env}

# 查看节点信息
paas-cli redis nodes --project {project_id} --env {env}
```

#### 步骤 5：结果分析与建议

综合诊断数据生成处理建议，按优先级排序。

---

## 扁鹊诊断命令参考

### 完整诊断命令

```bash
bianque redis check -n {namespace} -i {instance} -t {type} -v true
```

### 单项诊断

> `bianque redis check` 命令会执行综合性检查，使用 `-v true` 展示详情。如需更多日志信息，可使用 `-l` 参数指定日志检查行数。

```bash
# 综合检查并展示详情
bianque redis check -n {namespace} -i {instance} -t {type} -v true

# 指定日志检查行数（默认 1000）
bianque redis check -n {namespace} -i {instance} -t {type} -v true -l 2000

# 基本检查（不展示详情）
bianque redis check -n {namespace} -i {instance} -t {type}
```

### 返回格式

```json
{
  "status": "success|error",
  "findings": [
    {
      "type": "slowlog|memory|replication",
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

## 降级诊断方案

扁鹊不可达时，使用 paas-cli 基本诊断：

```bash
# 1. 查看集群状态
paas-cli redis info --project {project_id} --env {env}

# 2. 查看节点信息
paas-cli redis nodes --project {project_id} --env {env}

# 3. 查看内存使用
paas-cli redis memory --project {project_id} --env {env}
```

**降级局限**：无法获取慢查询详情、内存碎片率分析、主从延迟详情和故障转移日志。建议在报告中注明降级。

---

## 诊断报告输出模板

```
🔍 故障诊断报告

🩺 诊断目标：Redis / {env} / {project_id}
📡 诊断来源：扁鹊平台 / paas-cli{如降级则注明"（降级模式）"}

📊 诊断结论：{一句话结论}

📋 详细发现：
  1. {发现1}
  2. {发现2}

💡 处理建议：
  1. {建议1}（优先级：高）
  2. {建议2}（优先级：中）

📎 相关日志/数据：
{诊断脚本返回的关键数据摘要}
```