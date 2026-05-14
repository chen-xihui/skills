# Redis 故障排查详细指南

本文件包含 Redis 故障排查的详细诊断流程、常见故障场景和扁鹊诊断命令。

---

## 1. 诊断流程详解

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
bianque diagnose --middleware redis --project {project_id} --env {env} --check slowlog,memory,replication
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

## 2. 诊断能力详细说明

### 2.1 慢查询分析

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware redis --check slowlog` |
| 检查内容 | slowlog 中的高频慢命令 |

**关注指标**：
- 慢查询数量和频率
- 最耗时的命令类型（如 `KEYS`、`SORT`、`HGETALL` 大 Hash）
- 慢查询的 Key 模式

### 2.2 内存碎片率

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 + paas-cli |
| 检查命令 | `bianque diagnose --middleware redis --check memory` |
| 检查内容 | mem_fragmentation_ratio |

**关注指标**：
- 碎片率 < 1.0：Redis 使用了超出分配的内存（使用了 swap）
- 碎片率 1.0-1.5：正常
- 碎片率 > 1.5：内存碎片较多，可考虑重启或开启 activedefrag

### 2.3 主从延迟

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware redis --check replication` |
| 检查内容 | replication offset 差异 |

**关注指标**：
- 主从 offset 差异大 → 同步延迟
- 从节点断开连接 → 网络问题或负载高
- 主从切换频率 → 不稳定

### 2.4 持久化状态

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware redis --check replication`（含持久化检查） |
| 检查内容 | RDB/AOF 最后保存时间及状态 |

**关注指标**：
- RDB 最后保存时间距当前过久 → 持久化可能失败
- AOF fsync 延迟 → 磁盘 I/O 瓶颈
- AOF 重写是否正常执行

### 2.5 故障转移

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware redis --check replication` |
| 检查内容 | Sentinel 选举记录、Failover 日志 |

**关注指标**：
- 近期是否发生故障转移
- 故障转移耗时
- 新主节点是否正常

---

## 3. 常见故障场景与处理建议

### 场景 1：Redis 响应慢

**症状**：Redis 读写延迟明显增加

**诊断步骤**：
1. 执行 `paas-cli redis info` 查看基本状态
2. 扁鹊诊断检查 slowlog 和 CPU

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 慢命令（keys *、sort 等） | 优化代码，使用 scan 替代 keys |
| 大 Key 操作 | 拆分大 Key，使用 hscan/sscan/zscan |
| 内存满触发淘汰 | 扩容或优化缓存策略 |
| 网络延迟 | 检查网络连通性和带宽 |
| 持久化阻塞 | 检查 RDB/AOF 配置，考虑调整 fsync 策略 |
| 连接数过多 | 检查连接池配置，排除连接泄漏 |

### 场景 2：Redis 内存满

**症状**：Redis 报 OOM 或内存使用率接近 maxmemory

**诊断步骤**：
1. 执行 `paas-cli redis memory` 查看内存详情
2. 扁鹊诊断检查内存和淘汰策略

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 未设置过期时间 | 为 Key 设置合理的 TTL（REDIS-007） |
| 淘汰策略不合理 | 调整 maxmemory-policy（如 allkeys-lru） |
| 数据量增长 | 扩容或清理不再需要的数据 |
| 内存碎片率高 | 开启 activedefrag 或重启实例 |

### 场景 3：Redis 连接超时

**症状**：客户端连接 Redis 超时

**诊断步骤**：
1. 执行 `paas-cli redis info` 查看连接数
2. 扁鹊诊断检查网络

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 连接数达上限 | 增加 maxclients 或优化连接池 |
| 网络不通 | 检查防火墙和安全组规则 |
| Redis 阻塞 | 检查是否有慢命令阻塞（如 keys *） |
| 客户端连接池配置不合理 | 调整 maxTotal/maxIdle（REDIS-004） |

### 场景 4：主从数据不一致

**症状**：从节点数据与主节点不一致

**诊断步骤**：
1. 执行 `paas-cli redis nodes` 查看主从状态
2. 扁鹊诊断检查 replication

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 网络延迟导致同步慢 | 检查主从节点间网络 |
| 主节点写入量过大 | 考虑分片或读写分离 |
| 从节点断开后重连 | 等待全量同步完成 |
| 从节点只读配置异常 | 确认从节点为只读模式 |

---

## 4. 扁鹊诊断命令参考

### 4.1 完整诊断命令

```bash
bianque diagnose --middleware redis --project {project_id} --env {env} --check slowlog,memory,replication
```

### 4.2 单项诊断

```bash
# 仅检查慢查询
bianque diagnose --middleware redis --project {project_id} --env {env} --check slowlog

# 仅检查内存
bianque diagnose --middleware redis --project {project_id} --env {env} --check memory

# 仅检查主从复制
bianque diagnose --middleware redis --project {project_id} --env {env} --check replication
```

### 4.3 返回格式

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

## 5. 降级诊断方案

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

## 6. 诊断报告输出模板

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
