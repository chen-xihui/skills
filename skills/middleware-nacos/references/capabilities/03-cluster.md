## 能力三：集群交互

### 触发条件

用户请求与 Nacos 集群进行交互，如：
- "查看 Nacos 集群信息"
- "查询注册实例"
- "Nacos 创建服务"
- "Nacos 扩缩容"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境：DEV / SIT / SRV |
| action | enum | 是 | — | 操作类型（见操作矩阵） |

### 操作矩阵

> 详细操作说明和命令模板参见 `references/nacos-cluster-ops/` 目录

| 操作类型 | 命令模板（paas-cli Skill，`$PAAS_CLI`） | 风险等级 | 需确认 |
|---------|-------------------|---------|--------|
| 查询集群信息 | `$PAAS_CLI nacos info --project {project_id} --env {env}` | 🟢 | 否 |
| 查询服务注册实例 | `$PAAS_CLI nacos instances --project {project_id} --env {env} --service {service_name}` | 🟢 | 否 |
| 查询配置列表 | `$PAAS_CLI nacos config-list --project {project_id} --env {env}` | 🟢 | 否 |
| 创建服务 | `$PAAS_CLI nacos create --project {project_id} --env {env} --service {service_name} --group {group}` | 🟡 | 是 |
| 扩缩容 | `$PAAS_CLI nacos scale --project {project_id} --env {env} --replicas {count}` | 🟡 | 是 |
| 配置灰度发布 | `$PAAS_CLI nacos gray-publish --project {project_id} --env {env} --config {config_id}` | 🟡 | 是 |
| 升级版本 | `$PAAS_CLI nacos upgrade --project {project_id} --env {env} --version {version}` | 🔴 | 是 |
| 删除服务 | `$PAAS_CLI nacos delete --project {project_id} --env {env} --service {service_name}` | 🔴 | 是 |

### 前置条件检查

执行集群操作前，先检查：
1. **解析 CLI 路径**：按 `_shared-references/cli-tooling.md` 设置 `PAAS_CLI`
2. 按 **paas-cli Skill** 检查 `$PAAS_CLI` 是否可用：执行 `$PAAS_CLI version`
   - 失败 → 提示用户遵循 **paas-cli Skill** 或确认 `skills/paas-cli/paas-cli.py` 存在，见 **paas-cli Skill**（`skills/paas-cli/SKILL.md`）
3. 检查网络连通性：执行 `$PAAS_CLI ping`
   - 失败 → 提示用户检查网络连接

### 确认流程

1. 🟢 低风险操作：直接执行，无需确认
2. 🟡 中风险操作：
   - 向用户展示即将执行的完整命令
   - 询问"是否继续执行？"
   - 获得肯定回复后执行；拒绝则取消
3. 🔴 高风险操作：
   - 向用户展示完整命令及操作影响说明
   - 要求用户明确回复"确认"后方可执行
   - 用户拒绝或超时未确认 → 取消操作，不执行任何命令

### 输出格式

```
🔧 集群操作结果

操作：{操作类型}
目标：Nacos / {环境} / {集群标识}
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
