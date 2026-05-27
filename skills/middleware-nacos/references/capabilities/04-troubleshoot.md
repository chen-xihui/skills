## 能力四：故障排查

### 触发条件

用户请求 Nacos 故障排查或描述 Nacos 连接异常，如：
- "Nacos 故障排查"
- "我的 Nacos 连不上了"
- "注册中心异常"
- "Nacos 服务下线"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境 |
| namespace | string | 是 | — | Nacos 实例所在的 K8s 命名空间 |
| instance | string | 是 | — | Nacos 实例名称 |
| symptom | string | 否 | — | 用户描述的异常现象 |

### 诊断流程

> 详细诊断能力说明参见 `references/nacos-troubleshooting/` 目录

1. **信息收集**：记录用户描述的异常现象（symptom），如连接超时、服务下线、配置不生效等
2. **集群状态检查**：按 **paas-cli Skill** 在终端执行 `$PAAS_CLI` 查看 Nacos 集群基本状态
   ```
   $PAAS_CLI nacos info --project {project_id} --env {env}
   ```
   - 检查集群节点状态和 Raft 一致性
3. **扁鹊诊断**：通过终端调用扁鹊平台执行 Nacos 诊断命令
   ```
   $BIANQUE nacos check -n {namespace} -i {instance} -v true
   ```
   - 扁鹊诊断命令默认超时 60 秒
   - 如扁鹊不可达，回退到仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 状态检查
4. **补充信息收集**（可选）：如扁鹊诊断结果不充分，经 paas-cli Skill 执行 `$PAAS_CLI` 进一步查询服务注册实例或配置状态
5. **结果分析与建议**：综合诊断数据，生成处理建议，按优先级排序

### 诊断能力

| 诊断项 | 检查内容 | 数据来源 |
|--------|---------|---------|
| 集群健康度 | 节点状态、Raft 一致性 | 扁鹊 |
| 日志分析 | 错误日志、异常堆栈 | 扁鹊 |
| 主备状态 | Leader 选举状态、同步延迟 | bianque Skill + paas-cli Skill |
| 客户端连通性 | 从客户端节点到 Nacos 的网络可达性 | 扁鹊 |

> 上述诊断项均通过 `$BIANQUE nacos check` 命令执行，使用 `-v true` 展示详情，`-l` 指定日志检查行数

### 降级方案

当扁鹊平台不可达时，仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 诊断：
1. 查看集群信息：**paas-cli Skill**：`$PAAS_CLI nacos info`
2. 查询服务实例：**paas-cli Skill**：`$PAAS_CLI nacos instances`
3. 查看配置列表：**paas-cli Skill**：`$PAAS_CLI nacos config-list`
4. 基于上述信息提供有限的分析和建议

### 输出格式

```
🔍 故障诊断报告

🩺 诊断目标：Nacos / {集群标识}
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

## 变更记录

- v1.5.0 (2026-05-26): 所有 paas-cli 操作改为委托 **paas-cli Skill**（`paas-cli-skill-delegation.md`）
- v1.4.0 (2026-05-26): 路径由 `.trae/skills/` 调整为项目根 `skills/`
- v1.3.0 (2026-05-26): CLI 工具迁至 `skills/paas-cli`、`skills/bianque`
- v1.2.0 (2026-05-26): 增加 CLI 路径解析与 paas-cli Skill 委托（见 `cli-tooling.md`）
- v1.1.0 (2026-05-26): 能力一增加阻塞式 `auth check` 与 `nacos config` 流程；连接信息与用户名一律以 CLI 为准；移除用户必填 `auth_user`/`auth_pass`
- v1.0.0 (2026-05-11): 初始版本，包含客户端创建与配置、代码优化检查、集群交互、故障排查四项基础能力
