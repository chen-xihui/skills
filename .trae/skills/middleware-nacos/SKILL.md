---
name: "middleware-nacos"
version: "1.0.0"
description: "Nacos中间件技能，提供客户端创建、代码优化检查、集群操作和故障排查能力。触发词：Nacos、注册中心、配置中心、命名空间、服务发现、服务注册"
---

# Nacos 中间件

## 功能概述

本 Skill 为 Nacos 中间件提供四项标准化运维能力：

1. **客户端创建与配置**：根据参数自动生成 Nacos 客户端代码和配置文件，支持 Java、Go、Python
2. **代码优化检查**：扫描项目代码，按 7 条规则清单逐项检查 Nacos 使用规范性
3. **集群交互**：通过 paas-cli 执行 Nacos 集群查询和运维操作，含风险分级确认机制
4. **故障排查**：通过扁鹊平台和 paas-cli 诊断 Nacos 集群异常，支持降级方案

## 通用规范

### 参数收集原则

1. **优先从上下文推断**：如用户已打开项目，从项目配置文件中提取 `project_id`、`language` 等
2. **主动询问缺失参数**：对必要参数逐一询问，提供可选值提示
3. **使用合理默认值**：对有明确默认值的参数（如 `language` 默认 Java），可先使用默认值，在输出中注明

### 安全约束

> 详细安全规则参见 `_shared-references/cli-security-rules.md`

- **参数白名单校验**：所有 paas-cli / bianque 命令参数必须经过白名单校验
- **危险字符过滤**：参数值中不得包含 `;`、`|`、`&`、`$`、`` ` ``、`(`、`)`、`{`、`}` 等 shell 元字符。如检测到，拒绝执行并提示用户
- **高风险操作确认**：🟡 中风险操作展示命令后询问；🔴 高风险操作需用户明确回复"确认"
- **敏感信息处理**：密码以占位符形式（如 `${NACOS_PASSWORD}`）写入配置文件，引导用户通过环境变量或密钥管理系统注入
- **操作审计**：每次执行的 paas-cli / bianque 命令及结果应在对话中完整展示

### 参数白名单规则

| 参数 | 合法值规则 | 示例 |
|------|-----------|------|
| project_id | 仅允许小写字母、数字，格式如 j036x0 | `j036x0` ✅ `; rm -rf` ❌ |
| env | 枚举值：DEV / SIT / SRV | `DEV` ✅ `DEV; ls` ❌ |
| service_name | 仅允许字母、数字、下划线、短横线 | `order-service` ✅ `$(whoami)` ❌ |
| group | 仅允许字母、数字、下划线、短横线 | `DEFAULT_GROUP` ✅ `$(cat)` ❌ |
| config_id | 仅允许字母、数字、下划线、短横线、点号 | `application.yml` ✅ `; rm` ❌ |
| version | 语义化版本号格式 | `2.3.0` ✅ `2.3.0 && cat /etc/passwd` ❌ |
| count / replicas | 正整数 | `3` ✅ `3 || echo hack` ❌ |

### 操作风险分级与确认

| 风险等级 | 操作类型 | 确认要求 |
|---------|---------|---------|
| 🟢 低风险 | 查询、状态检查 | 无需确认，直接执行 |
| 🟡 中风险 | 创建服务、扩缩容、配置灰度发布 | 向用户展示即将执行的命令，等待用户确认后执行 |
| 🔴 高风险 | 升级版本、删除服务 | 向用户展示命令及影响范围，必须获得明确确认（用户回复"确认"）后方可执行 |

---

## 能力一：客户端创建与配置

### 触发条件

用户请求创建 Nacos 客户端并生成配置，如：
- "创建 Nacos 客户端"
- "生成注册中心连接代码"
- "帮我配置 Nacos"
- "使用 Nacos 作为注册中心"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号，如 j036x0 |
| env | enum | 是 | — | 环境：DEV / SIT / SRV |
| auth_user | string | 是 | — | Nacos 用户名 |
| auth_pass | string | 是 | — | Nacos 密码 |
| target_path | string | 是 | — | 代码生成目标路径 |
| language | enum | 否 | Java | 项目语言：Java / Go / Python |

### 处理流程

1. **参数收集**：确认所有必要参数，缺失项主动询问用户
2. **环境信息查询**：通过终端执行 paas-cli 命令获取 Nacos 服务地址和命名空间
   ```
   paas-cli nacos config --project {project_id} --env {env}
   ```
   - 如 paas-cli 执行失败，提示用户检查安装及网络连通性，改为手动输入 Nacos 地址
3. **代码生成**：根据 `language` 选择对应模板，生成文件
   > 详细代码模板参见 `references/nacos-client-templates.md`

   | 语言 | 生成文件 |
   |------|---------|
   | Java | NacosConfigService.java、NacosDiscoveryService.java、bootstrap.yml |
   | Go | nacos_client.go、config.yaml |
   | Python | nacos_client.py、config.yaml |

4. **文件写入**：将生成的代码写入 `target_path` 指定目录
5. **依赖提示**：列出需要添加的依赖
   - **Java**：Spring Cloud Alibaba Nacos Discovery + Config
   - **Go**：`github.com/nacos-group/nacos-sdk-go/v2`
   - **Python**：`nacos-sdk-python`

### 输出格式

```
✅ 客户端代码已生成

📁 生成文件列表：
  - {文件路径1} — {文件说明}
  - {文件路径2} — {文件说明}

📝 后续步骤：
  1. 添加依赖：{依赖信息}
  2. 配置环境变量：NACOS_PASSWORD={实际密码}
  3. 启动应用验证注册

⚠️ 注意事项：
  - 密码以 ${NACOS_PASSWORD} 占位符形式写入，请通过环境变量或密钥管理系统注入实际值
  - 请确保 Nacos 服务端已开启鉴权
```

### 异常处理

- paas-cli 命令执行失败 → 提示用户检查 paas-cli 是否安装及网络连通性，改为手动输入 Nacos 地址
- 目标路径不存在 → 询问用户是否创建目录
- 文件已存在 → 询问用户是否覆盖

---

## 能力二：代码优化检查

### 触发条件

用户请求检查 Nacos 代码优化，如：
- "检查 Nacos 代码"
- "Nacos 代码审计"
- "注册中心代码优化"
- "检查配置中心代码规范"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| scan_path | string | 是 | — | 需扫描的项目根目录 |

### 检查规则清单

> 详细规则说明和检查方法参见 `references/nacos-audit-rules.md`

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| NACOS-001 | 服务订阅是否启用本地快照（enableLocalSnapshot） | 🔵 建议 |
| NACOS-002 | 长轮询超时是否合理（configLongPollTimeout 建议 ≤ 30s） | 🟡 警告 |
| NACOS-003 | 是否循环调用 getConfig 而未使用 Listener | 🔴 严重 |
| NACOS-004 | 密码是否硬编码在源码中 | 🔴 严重 |
| NACOS-005 | 心跳间隔、权重等是否符合最佳实践 | 🟡 警告 |
| NACOS-006 | 是否缺少异常处理和重试配置 | 🟡 警告 |
| NACOS-007 | 命名空间是否按环境隔离 | 🔵 建议 |

### 检查流程

1. **确认扫描路径**：确认 `scan_path` 参数，缺失时主动询问
2. **扫描 Nacos 相关代码**：使用 `search_codebase` 和 `grep_code` 工具按规则逐项搜索
   - 搜索关键词：`NacosConfigService`、`NacosDiscoveryService`、`enableLocalSnapshot`、`configLongPollTimeout`、`getConfig`、`password`、`heartBeatInterval`、`namespace` 等
3. **逐规则检查**：按 NACOS-001 ~ NACOS-007 逐项检查，记录发现的问题
4. **生成审计报告**：按输出格式生成结构化报告，按风险等级排序（🔴 → 🟡 → 🔵）

### 输出格式

```
📋 代码审计报告

📊 概要：共扫描 {N} 个文件，发现 {M} 个问题（🔴 严重 {x} | 🟡 警告 {y} | 🔵 建议 {z}）

| # | 文件路径 | 行号 | 规则ID | 问题描述 | 风险等级 | 改进建议 |
|---|---------|------|--------|---------|---------|---------|
| 1 | ... | ... | ... | ... | 🔴 严重 | ... |

💡 优先修复建议：{按风险等级排序的 Top 3 修复建议}
```

### 异常处理

- 扫描路径不存在 → 提示用户确认路径
- 未找到 Nacos 相关代码 → 告知用户未检测到 Nacos 客户端代码

---

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

> 详细操作说明和命令模板参见 `references/nacos-cluster-ops.md`

| 操作类型 | paas-cli 命令模板 | 风险等级 | 需确认 |
|---------|-------------------|---------|--------|
| 查询集群信息 | `paas-cli nacos info --project {project_id} --env {env}` | 🟢 | 否 |
| 查询服务注册实例 | `paas-cli nacos instances --project {project_id} --env {env} --service {service_name}` | 🟢 | 否 |
| 查询配置列表 | `paas-cli nacos config-list --project {project_id} --env {env}` | 🟢 | 否 |
| 创建服务 | `paas-cli nacos create --project {project_id} --env {env} --service {service_name} --group {group}` | 🟡 | 是 |
| 扩缩容 | `paas-cli nacos scale --project {project_id} --env {env} --replicas {count}` | 🟡 | 是 |
| 配置灰度发布 | `paas-cli nacos gray-publish --project {project_id} --env {env} --config {config_id}` | 🟡 | 是 |
| 升级版本 | `paas-cli nacos upgrade --project {project_id} --env {env} --version {version}` | 🔴 | 是 |
| 删除服务 | `paas-cli nacos delete --project {project_id} --env {env} --service {service_name}` | 🔴 | 是 |

### 前置条件检查

执行集群操作前，先检查：
1. 检查 paas-cli 是否可用：执行 `paas-cli --version`
   - 失败 → 提示用户安装 paas-cli，并提供安装文档链接
2. 检查网络连通性：执行 `paas-cli ping`
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
{paas-cli 命令输出内容}

⏱️ 执行耗时：{N}秒
```

### 异常处理

- paas-cli 未安装 → 提示安装方式
- 命令执行超时 → 提示用户检查网络，建议加 `--timeout` 参数重试
- 权限不足 → 提示用户联系管理员授权
- 参数包含危险字符 → 拒绝执行并提示用户

---

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
| symptom | string | 否 | — | 用户描述的异常现象 |

### 诊断流程

> 详细诊断能力说明参见 `references/nacos-troubleshooting.md`

1. **信息收集**：记录用户描述的异常现象（symptom），如连接超时、服务下线、配置不生效等
2. **集群状态检查**：通过终端执行 paas-cli 查看 Nacos 集群基本状态
   ```
   paas-cli nacos info --project {project_id} --env {env}
   ```
   - 检查集群节点状态和 Raft 一致性
3. **扁鹊诊断**：通过终端调用扁鹊平台执行 Nacos 诊断脚本
   ```
   bianque diagnose --middleware nacos --project {project_id} --env {env} --check health,raft,log
   ```
   - 扁鹊诊断命令默认超时 60 秒
   - 如扁鹊不可达，回退到仅使用 paas-cli 进行基本状态检查
4. **补充信息收集**（可选）：如扁鹊诊断结果不充分，执行 paas-cli 进一步查询服务注册实例或配置状态
5. **结果分析与建议**：综合诊断数据，生成处理建议，按优先级排序

### 诊断能力

| 诊断项 | 检查内容 | 数据来源 |
|--------|---------|---------|
| 集群健康度 | 节点状态、Raft 一致性 | 扁鹊 |
| 日志分析 | 错误日志、异常堆栈 | 扁鹊 |
| 主备状态 | Leader 选举状态、同步延迟 | 扁鹊 + paas-cli |
| 客户端连通性 | 从客户端节点到 Nacos 的网络可达性 | 扁鹊 |

### 降级方案

当扁鹊平台不可达时，仅使用 paas-cli 进行基本诊断：
1. 查看集群信息：`paas-cli nacos info`
2. 查询服务实例：`paas-cli nacos instances`
3. 查看配置列表：`paas-cli nacos config-list`
4. 基于上述信息提供有限的分析和建议

### 输出格式

```
🔍 故障诊断报告

🩺 诊断目标：Nacos / {集群标识}
📡 诊断来源：扁鹊平台 / paas-cli

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

- 扁鹊不可达 → 回退到仅使用 paas-cli 进行基本状态检查，在报告中注明诊断来源降级
- 诊断脚本返回异常 → 展示原始错误信息，建议联系扁鹊平台运维
- paas-cli 未安装 → 提示安装方式，仅提供基于代码分析和经验的一般性建议

---

## 变更记录

- v1.0.0 (2026-05-11): 初始版本，包含客户端创建与配置、代码优化检查、集群交互、故障排查四项基础能力
