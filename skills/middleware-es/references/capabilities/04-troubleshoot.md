## 能力四：故障排查

### 触发条件

用户请求 ES 故障排查或描述 ES 集群/查询异常，如：
- "ES 故障排查"
- "我的 Elasticsearch 查询很慢"
- "ES 集群 Red"
- "搜索服务异常"
- "ES 写入失败"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境 |
| namespace | string | 是 | — | ES 实例所在的 K8s 命名空间 |
| instance | string | 是 | — | ES 实例名称 |
| symptom | string | 否 | — | 用户描述的异常现象 |

### 诊断流程

> 详细诊断能力说明和诊断脚本参见 `references/es-troubleshooting/` 目录

1. **信息收集**：记录用户描述的异常现象（symptom），如集群状态异常、查询缓慢、写入拒绝等
2. **集群状态检查**：按 **paas-cli Skill** 在终端执行 `$PAAS_CLI` 查看 ES 集群基本状态
   ```
   $PAAS_CLI es info --project {project_id} --env {env}
   ```
   - 检查集群健康状态（Green / Yellow / Red）
   - 检查节点数量和状态
3. **扁鹊诊断**：通过终端调用扁鹊平台执行 ES 诊断命令
   ```
   $BIANQUE elasticsearch check -n {namespace} -i {instance} -v true -o 50
   ```
   - 扁鹊诊断命令默认超时 60 秒（部分诊断脚本执行时间较长）
   - 如扁鹊不可达，回退到仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 状态检查，在报告中注明
4. **补充信息收集**（可选）：如集群状态为 yellow/red，进一步查询：
   ```
   $PAAS_CLI es indices --project {project_id} --env {env}
   $PAAS_CLI es disk-usage --project {project_id} --env {env}
   ```
   - 查看未分配分片详情
   - 检查磁盘水位线状态
5. **结果分析与建议**：综合诊断数据，生成处理建议，按优先级排序

### 诊断能力

| 诊断项 | 检查内容 | 数据来源 |
|--------|---------|---------|
| 集群健康状态 | Red / Yellow / Green 及原因 | bianque Skill + paas-cli Skill |
| 未分配分片 | UNASSIGNED 分片及分配失败原因 | 扁鹊 |
| CPU 热点 | 节点 CPU 使用率及热线程 | 扁鹊 |
| 写入拒绝 | 磁盘水位线、线程池队列拒绝 | 扁鹊 |
| 索引健康 | 副本分片状态、段合并情况 | 扁鹊 |
| 客户端连通性 | ES 客户端读写验证 | 扁鹊 |

> 上述诊断项均通过 `$BIANQUE elasticsearch check` 命令执行，使用 `-v true` 展示详情，`-o` 指定错误日志输出行数

### 降级方案

当扁鹊平台不可达时，仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 诊断：
1. 查看集群状态：**paas-cli Skill**：`$PAAS_CLI es info`
2. 查看索引状态：**paas-cli Skill**：`$PAAS_CLI es indices`
3. 查看磁盘使用：**paas-cli Skill**：`$PAAS_CLI es disk-usage`
4. 基于上述信息提供有限的分析和建议

### 输出格式

```
🔍 故障诊断报告

🩺 诊断目标：Elasticsearch / {集群标识}
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
