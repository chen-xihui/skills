## 能力三：集群交互

### 触发条件

用户请求与 Redis 集群进行交互，如：
- "查看 Redis 集群状态"
- "Redis 内存使用"
- "Redis 扩缩容"
- "查看 Redis 节点信息"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境：DEV / SIT / SRV |
| action | enum | 是 | — | 操作类型（见操作矩阵） |

### 操作矩阵

> 详细操作说明和命令模板参见 `references/redis-cluster-ops/` 目录

| 操作类型 | 命令模板（paas-cli Skill，`$PAAS_CLI`） | 风险等级 | 需确认 |
|---------|-------------------|---------|--------|
| 查看集群状态 | `$PAAS_CLI redis info --project {project_id} --env {env}` | 🟢 | 否 |
| 查看节点信息 | `$PAAS_CLI redis nodes --project {project_id} --env {env}` | 🟢 | 否 |
| 查看内存使用 | `$PAAS_CLI redis memory --project {project_id} --env {env}` | 🟢 | 否 |
| 查看服务租期 | `$PAAS_CLI redis lease status --project {project_id} --env {env}` | 🟢 | 否 |
| 续期服务租期 | `$PAAS_CLI redis lease renew --project {project_id} --env {env} --duration {months}` | 🟡 | 是 |
| 创建实例 | `$PAAS_CLI redis create --project {project_id} --env {env} --mode {mode}` | 🟡 | 是 |
| 扩缩容 | `$PAAS_CLI redis scale --project {project_id} --env {env} --replicas {count}` | 🟡 | 是 |
| Slot 迁移 | `$PAAS_CLI redis slot-migrate --project {project_id} --env {env} --from {node} --to {node} --slots {range}` | 🔴 | 是 |
| 内存策略调整 | `$PAAS_CLI redis config --project {project_id} --env {env} --maxmemory-policy {policy}` | 🟡 | 是 |
| 升级版本 | `$PAAS_CLI redis upgrade --project {project_id} --env {env} --version {version}` | 🔴 | 是 |
| 删除集群 | `$PAAS_CLI redis delete --project {project_id} --env {env}` | 🔴 | 是 |

### 前置条件检查

执行集群操作前，先检查：
1. **解析 CLI 路径**：按 `_shared-references/cli-tooling.md` 设置 `PAAS_CLI`
2. 按 **paas-cli Skill** 检查 `$PAAS_CLI` 是否可用：执行 `$PAAS_CLI version`
   - 失败 → 提示遵循 paas-cli Skill 或确认 `skills/paas-cli/paas-cli.py` 存在（见 **paas-cli Skill**（`skills/paas-cli/SKILL.md`））
3. 检查网络连通性：执行 `$PAAS_CLI ping`

### 确认流程

1. 🟢 低风险操作：直接执行，无需确认
2. 🟡 中风险操作：展示完整命令，询问"是否继续执行？"，获得肯定回复后执行
3. 🔴 高风险操作：展示完整命令及影响说明，要求用户明确回复"确认"后方可执行

### 输出格式

```
🔧 集群操作结果

操作：{操作类型}
目标：Redis / {环境} / {集群标识}
状态：✅ 成功 / ❌ 失败

📊 返回信息：
{paas-cli Skill / `$PAAS_CLI` 命令输出内容}

⏱️ 执行耗时：{N}秒
```

### 异常处理

- paas-cli Skill 不可用（`$PAAS_CLI` 解析失败） → 提示安装方式
- 命令执行超时 → 提示用户检查网络，建议加 `--timeout` 参数重试
- 权限不足 → 提示用户联系管理员授权
- 参数包含危险字符 → 拒绝执行并提示用户

---
