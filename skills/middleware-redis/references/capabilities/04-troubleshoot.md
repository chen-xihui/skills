## 能力四：故障排查

### 触发条件

用户请求 Redis 故障排查或描述 Redis 连接/性能异常，如：
- "Redis 故障排查"
- "缓存连不上了"
- "Redis 响应很慢"
- "内存溢出了"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境 |
| namespace | string | 是 | — | Redis 实例所在的 K8s 命名空间 |
| instance | string | 是 | — | Redis 实例名称 |
| type | enum | 是 | — | Redis 类型：cluster / sentinel |
| symptom | string | 否 | — | 用户描述的异常现象 |

### 诊断流程

> 详细诊断能力说明参见 `references/redis-troubleshooting/` 目录

1. **信息收集**：记录用户描述的异常现象（symptom），如连接超时、响应慢、内存满等
2. **集群状态检查**：按 **paas-cli Skill** 在终端执行 `$PAAS_CLI` 查看 Redis 集群基本状态
   ```
   $PAAS_CLI redis info --project {project_id} --env {env}
   ```
3. **扁鹊诊断**：通过终端调用扁鹊平台执行 Redis 诊断命令
   ```
   $BIANQUE redis check -n {namespace} -i {instance} -t {type} -v true
   ```
   - 扁鹊诊断命令默认超时 60 秒
   - 如扁鹊不可达，回退到仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 状态检查
4. **补充信息收集**（可选）：如需进一步诊断，执行内存详情或慢查询命令
   ```
   $PAAS_CLI redis memory --project {project_id} --env {env}
   $PAAS_CLI redis nodes --project {project_id} --env {env}
   ```
5. **结果分析与建议**：综合诊断数据，生成处理建议，按优先级排序

### 诊断能力

| 诊断项 | 检查内容 | 数据来源 |
|--------|---------|---------|
| 慢查询分析 | slowlog 中的高频慢命令 | 扁鹊 |
| 内存碎片率 | mem_fragmentation_ratio | bianque Skill + paas-cli Skill |
| 主从延迟 | replication offset 差异 | 扁鹊 |
| 持久化状态 | RDB/AOF 最后保存时间及状态 | 扁鹊 |
| 故障转移 | Sentinel 选举记录、Failover 日志 | 扁鹊 |
| 客户端连通性 | Redis 客户端读写验证 | 扁鹊 |

> 上述诊断项均通过 `$BIANQUE redis check` 命令执行，使用 `-v true` 展示详情，`-l` 指定日志检查行数

### 降级方案

当扁鹊平台不可达时，仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 诊断：
1. 查看集群状态：**paas-cli Skill**：`$PAAS_CLI redis info`
2. 查看节点信息：**paas-cli Skill**：`$PAAS_CLI redis nodes`
3. 查看内存使用：**paas-cli Skill**：`$PAAS_CLI redis memory`

### 输出格式

```
🔍 故障诊断报告

🩺 诊断目标：Redis / {集群标识}
📡 诊断来源：bianque Skill / paas-cli Skill

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

### 异常处理

- 扁鹊不可达 → 回退到仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 状态检查，在报告中注明诊断来源降级
- 诊断脚本返回异常 → 展示原始错误信息，建议联系扁鹊平台运维
- paas-cli Skill 不可用（`$PAAS_CLI` 解析失败） → 提示安装方式，仅提供基于代码分析和经验的一般性建议

---
