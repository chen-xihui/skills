# 中间件智能运维 Skill 系统需求（精简版）

**版本**：V4.0-S | **日期**：2026-05-26

---

## 1. 核心概念

- **Skill**：标准化的 Markdown 指令包（SKILL.md），定义触发条件、参数规范、处理流程、输出格式和安全约束
- **IDE 智能体**：利用原生能力（代码生成、文件读写、终端命令、代码搜索）执行 Skill 指令
- **外部工具**：`paas-cli`（集群运维）、`扁鹊`（故障诊断），通过终端命令调用

**设计原则**：Skill 即指令（纯 Markdown）| 最小外部依赖 | 安全优先 | 结构化输出

---

## 2. 项目概述

**背景**：传统中间件使用运维存在使用门槛高、运维效率低、规范落地难、故障排查慢等痛点。业界已有 Elastic AI Assistant、Dynatrace Davis AI 等方案验证 AI 赋能中间件运维的可行性。

**目标**：

| 层次 | 目标 | 指标 |
|------|------|------|
| 短期（MVP） | 四项原子能力，验证 Skill 指令驱动 | 代码生成可用率 ≥ 85%，审计准确率 ≥ 80% |
| 中期（增强） | 知识库/RAG、置信度、容量预测 | 诊断准确率 ≥ 70%，满意度 ≥ 4.0/5.0 |
| 长期（智能运维） | 跨中间件关联、修复编排、MCP | 自动修复覆盖率 ≥ 60%，MTTR 降低 50% |

**范围**：Nacos/Redis/ES 三大中间件 + 四项原子能力 + 分发与增强能力。不含中间件本身开发、IDE 模型训练、独立后端服务。

---

## 3. 总体描述

**产品愿景**：通过自然语言对话即可高效使用和运维中间件，降低使用门槛和故障响应时间。

**功能总览**：

| 功能 | 实现方式 | 需外部工具 |
|------|---------|-----------|
| 客户端代码生成 | 智能体根据模板规范直接生成代码 | 否 |
| 代码优化检查 | 智能体扫描代码，依据规则清单逐项检查 | 否 |
| 集群资源管理 | 智能体通过终端执行 paas-cli 命令 | paas-cli |
| 故障排查 | 智能体通过终端调用扁鹊诊断命令 | 扁鹊 |

---

## 4. 总体设计

### 4.1 设计目标与约束

| 设计目标 | 约束 |
|---------|------|
| 零外部依赖核心能力 | 智能体需具备代码生成、文件读写、代码搜索等原生能力 |
| 纯 Markdown 指令驱动 | 智能体需能解析和执行 Markdown 格式指令 |
| 安全优先的操作管控 | 便捷性与安全性平衡 |
| 可扩展架构 | Skill 文件结构模板需保持稳定 |
| 结构化可追踪输出 | 输出格式兼顾可读性和可解析性 |

### 4.2 技术选型

| 领域 | 选型 | 理由 | 备选 |
|------|------|------|------|
| IDE 智能体 | Qoder AI IDE | 原生能力丰富，支持 Skill 自动发现 | VS Code + Copilot、Cursor |
| Skill 格式 | Markdown (SKILL.md) | 无需额外运行时，版本管理友好 | YAML + 代码插件 |
| 外部工具调用 | 终端命令执行 | 零集成成本，支持任意 CLI | MCP 协议（中期） |
| 知识库 | Markdown + RAG | 结构化文档作为附加上下文注入 | 向量数据库 + 语义检索 |
| 版本管理 | Git Tag + 语义化版本 | 与项目代码统一管理 | 独立版本注册中心 |

### 4.3 核心设计决策

| 决策 | 已选方案 | 理由 |
|------|---------|------|
| Skill 驱动 vs Agent Runtime | 纯 Skill 驱动 | 零后端依赖，MVP 足够；Agent Runtime 长期演进 |
| 终端命令 vs MCP 协议 | 终端命令（短期） | 最低成本集成；命令模板独立成段，便于切换 MCP |
| 单 Skill vs 多 Skill | 入口路由 + 专项 Skill | 职责清晰，SKILL.md < 500 行保证理解质量 |

### 4.4 系统架构

```
用户对话 → IDE 智能体 → Skill 指令层（Nacos/Redis/ES SKILL.md）
                    → 智能体原生能力层（代码生成、文件读写、代码搜索、终端执行）
                    → 外部工具（paas-cli、扁鹊） ← 终端命令
                    → 项目代码仓库 ← 文件系统
```

**关键**：无独立后端服务，Skill 是"操作手册"非可执行代码

**Skill 文件结构**：
```
skills/
 ├── middleware/SKILL.md          # 通用入口（路由层）
 ├── middleware-nacos/SKILL.md    # Nacos 专项
 ├── middleware-redis/SKILL.md    # Redis 专项
 ├── middleware-es/SKILL.md       # ES 专项
 ├── paas-cli/SKILL.md            # 运维 CLI 工具说明
 └── bianque/SKILL.md             # 诊断 CLI 工具说明
```

---

## 3. Skill 通用规范

| 检查方法 | 智能体工具 | 适用规则 |
|---------|-----------|---------|
| 关键字搜索 | grep_code | 硬编码密码、配置缺失 |
| 语义搜索 | search_codebase | 反模式检测（循环调用、keys *） |
| 配置值分析 | read_file + grep_code | 参数合理性检查 |
| 代码模式匹配 | search_codebase | 批量操作、深分页 |

### 5.4 集群交互组件

**命令构造**：操作矩阵匹配 → 命令模板获取 → 参数白名单校验 → 风险分级确认 → 执行 → 结果解析

**风险分级确认**：

| 风险 | 流程 |
|------|------|
| 🟢 低 | 直接执行 |
| 🟡 中 | 展示命令，等用户确认 |
| 🔴 高 | 展示命令+影响说明，用户须回复"确认" |

### 5.5 故障排查组件

**模式**：阶梯式诊断（信息收集 → paas-cli 基础检查 → 扁鹊深度诊断 → 补充查询 → 综合分析）

**降级策略**：扁鹊不可达 → 仅 paas-cli 基本检查 → 注明诊断可能不完整

**推理链**（Phase 4）：展示诊断推导路径 + 置信度评分

### 5.6 数据流

| 能力 | 数据流 |
|------|--------|
| 客户端生成 | 参数校验 → paas-cli 获取环境 → 模板选择 → 参数填充 → 写入 → 依赖提示 |
| 代码审计 | 遍历文件 → 逐条规则匹配 → 结果聚合 → 风险排序 → 报告输出 |
| 集群操作 | 操作匹配 → 命令获取 → 参数校验 → 风险确认 → 终端执行 → 结果解析 |
| 故障排查 | 信息收集 → paas-cli 检查 → 扁鹊诊断 → 补充查询 → 综合分析 |

---

## 6. Skill 通用规范

### 6.1 文件结构模板

```markdown
---
name: "middleware-{type}"
version: "1.0.0"
description: "{中间件}技能：客户端创建、代码审查、集群操作、故障排查"
---
# {中间件名称}
## 功能概述
## 能力一：客户端创建与配置 → 触发条件 | 必要参数 | 处理流程 | 输出格式 | 异常处理
## 能力二：代码优化检查 → 触发条件 | 必要参数 | 规则清单表 | 输出格式 | 异常处理
## 能力三：集群交互 → 触发条件 | 必要参数 | 操作矩阵表 | 确认流程 | 输出格式 | 异常处理
## 能力四：故障排查 → 触发条件 | 必要参数 | 诊断流程 | 输出格式 | 异常处理
```

### 6.2 输出格式

| 能力 | 格式要点 |
|------|---------|
| 客户端生成 | ✅ 生成文件列表 + 📝 后续步骤 + ⚠️ 注意事项 |
| 代码审计 | 📋 扫描概要 + 问题表（文件/行号/规则ID/风险/建议） + 💡 Top3 修复建议 |
| 集群操作 | 🔧 操作结果（类型/目标/状态） + 📊 返回信息 + ⏱️ 耗时 |
| 故障排查 | 🔍 诊断结论 + 📋 详细发现 + 💡 处理建议（含优先级） + 📎 关键数据 |

### 6.3 风险与确认

| 风险 | 操作类型 | 确认要求 |
|------|---------|---------|
| 🟢 低 | 查询、状态检查 | 直接执行 |
| 🟡 中 | 扩缩容、配置变更 | 展示命令，等用户确认 |
| 🔴 高 | 删除、升级、主备切换 | 展示命令+影响，用户须回复"确认" |

---

## 7. Nacos Skill 需求

### 7.1 客户端创建

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| project_id | 是 | — | 项目组编号 |
| env | 是 | — | DEV/SIT/SRV |
| target_path | 是 | — | 生成路径 |
| language | 否 | Java | Java/Go/Python |

平台字段（CLI，禁止用户覆盖）：`server_addr`、`namespace`、`Username` 来自 `nacos config`；密码仅用 `${NACOS_PASSWORD}`（CLI 脱敏，不向用户索要明文）

流程：参数收集 → `$PAAS_CLI auth check`（阻塞）→ `$PAAS_CLI nacos config` → 按语言生成 → 写入 → 依赖提示

### 7.2 代码审计规则

| 规则ID | 描述 | 风险 |
|--------|------|------|
| NACOS-001 | 未启用本地快照 enableLocalSnapshot | 🔵 |
| NACOS-002 | configLongPollTimeout > 30s | 🟡 |
| NACOS-003 | 循环调用 getConfig 未用 Listener | 🔴 |
| NACOS-004 | 密码硬编码 | 🔴 |
| NACOS-005 | 心跳/权重不符合最佳实践 | 🟡 |
| NACOS-006 | 缺少异常处理和重试 | 🟡 |
| NACOS-007 | 命名空间未按环境隔离 | 🔵 |

### 7.3 集群操作矩阵

| 操作 | paas-cli 命令 | 风险 |
|------|--------------|------|
| 查询集群信息 | `paas-cli nacos info --project {pid} --env {env}` | 🟢 |
| 查询注册实例 | `paas-cli nacos instances --project {pid} --env {env} --service {svc}` | 🟢 |
| 查询配置列表 | `paas-cli nacos config-list --project {pid} --env {env}` | 🟢 |
| 创建服务 | `paas-cli nacos create --project {pid} --env {env} --service {svc} --group {grp}` | 🟡 |
| 扩缩容 | `paas-cli nacos scale --project {pid} --env {env} --replicas {n}` | 🟡 |
| 配置灰度发布 | `paas-cli nacos gray-publish --project {pid} --env {env} --config {id}` | 🟡 |
| 升级版本 | `paas-cli nacos upgrade --project {pid} --env {env} --version {ver}` | 🔴 |
| 删除服务 | `paas-cli nacos delete --project {pid} --env {env} --service {svc}` | 🔴 |

### 7.4 故障排查

流程：信息收集 → `$PAAS_CLI nacos info` → `$BIANQUE nacos check -n {namespace} -i {instance} -v true` → 补充查询 → 分析建议

诊断项：集群健康度 | 日志分析 | 主备状态 | 客户端连通性

---

## 8. Redis Skill 需求

### 8.1 客户端创建

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| project_id | 是 | — | 项目组编号 |
| env | 是 | — | DEV/SIT/SRV |
| target_path | 是 | — | 生成路径 |
| mode | 否 | — | 部署模式提示；**以 CLI `Mode` 为准** |
| client_type | 否 | lettuce | jedis/lettuce |
| language | 否 | Java | Java/Go/Python |

平台字段（CLI，禁止用户覆盖）：`Mode`、`Endpoints`、`Database`（Sentinel 含 `Master Name`）来自 `redis config`；密码仅用 `${REDIS_PASSWORD}`

流程：参数收集 → `$PAAS_CLI auth check` → `$PAAS_CLI redis config` → 按 CLI Mode 与 language/client_type 生成 → 写入 → 依赖提示

### 8.2 代码审计规则

| 规则ID | 描述 | 风险 |
|--------|------|------|
| REDIS-001 | 循环中使用 keys * 应改用 scan | 🔴 |
| REDIS-002 | 大 Key 风险（>10KB 未拆分/压缩） | 🟡 |
| REDIS-003 | 热 Key 未考虑本地缓存 | 🟡 |
| REDIS-004 | 连接池参数不合理 | 🟡 |
| REDIS-005 | 批量操作未使用 Pipeline | 🔵 |
| REDIS-006 | Lua 脚本未用 EVALSHA | 🔵 |
| REDIS-007 | Key 未设过期时间 | 🟡 |
| REDIS-008 | 密码硬编码 | 🔴 |

### 8.3 集群操作矩阵

| 操作 | paas-cli 命令 | 风险 |
|------|--------------|------|
| 查看集群状态 | `paas-cli redis info --project {pid} --env {env}` | 🟢 |
| 查看节点信息 | `paas-cli redis nodes --project {pid} --env {env}` | 🟢 |
| 查看内存使用 | `paas-cli redis memory --project {pid} --env {env}` | 🟢 |
| 创建实例 | `paas-cli redis create --project {pid} --env {env} --mode {mode}` | 🟡 |
| 扩缩容 | `paas-cli redis scale --project {pid} --env {env} --replicas {n}` | 🟡 |
| Slot 迁移 | `paas-cli redis slot-migrate --project {pid} --env {env} --from {n} --to {n} --slots {r}` | 🔴 |
| 内存策略调整 | `paas-cli redis config --project {pid} --env {env} --maxmemory-policy {pol}` | 🟡 |
| 升级版本 | `paas-cli redis upgrade --project {pid} --env {env} --version {ver}` | 🔴 |
| 删除集群 | `paas-cli redis delete --project {pid} --env {env}` | 🔴 |

### 8.4 故障排查

流程：信息收集 → `$PAAS_CLI redis info` → `$BIANQUE redis check -n {namespace} -i {instance} -t {type} -v true` → 补充查询 → 分析建议

诊断项：慢查询 | 内存碎片率 | 主从延迟 | 持久化状态 | 故障转移

---

## 9. Elasticsearch Skill 需求

### 9.1 客户端创建

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| project_id | 是 | — | 项目组编号 |
| env | 是 | — | DEV/SIT/SRV |
| target_path | 是 | — | 生成路径 |
| client_version | 否 | — | new(8.x)/old(7.x)；可参考 CLI `Version` |
| java_stack | 否 | elasticsearch-java | Java 专用：elasticsearch-java / spring-data / bboss / rhlc |
| language | 否 | Java | Java/Go/Python/Node.js |

平台字段（CLI，禁止用户覆盖）：`Hosts`、`Scheme`、`Username` 来自 `es config`；密码仅用 `${ES_PASSWORD}`

流程：参数收集（含 java_stack）→ `$PAAS_CLI auth check` → `$PAAS_CLI es config` → 按模板索引生成 → 写入 → 依赖提示

### 9.2 代码审计规则

| 规则ID | 描述 | 风险 |
|--------|------|------|
| ES-001 | 深分页未用 search_after | 🔴 |
| ES-002 | bulk 批次大小不合理 | 🟡 |
| ES-003 | 索引缺少显式 mapping | 🟡 |
| ES-004 | 高消耗脚本查询(script_query/painless) | 🔴 |
| ES-005 | 循环中单条操作应改批量 | 🔵 |
| ES-006 | 连接超时/重试配置不合理 | 🟡 |
| ES-007 | 密码硬编码 | 🔴 |
| ES-008 | 未使用索引别名 | 🔵 |

### 9.3 集群操作矩阵

| 操作 | paas-cli 命令 | 风险 |
|------|--------------|------|
| 查看集群状态 | `paas-cli es info --project {pid} --env {env}` | 🟢 |
| 查看磁盘使用 | `paas-cli es disk-usage --project {pid} --env {env}` | 🟢 |
| 查看索引状态 | `paas-cli es indices --project {pid} --env {env}` | 🟢 |
| 创建索引 | `paas-cli es create-index --project {pid} --env {env} --name {idx} --shards {n} --replicas {n}` | 🟡 |
| 索引滚动 | `paas-cli es rollover --project {pid} --env {env} --alias {alias}` | 🟡 |
| Force merge | `paas-cli es force-merge --project {pid} --env {env} --index {idx} --max-segments {n}` | 🟡 |
| 扩缩容 | `paas-cli es scale --project {pid} --env {env} --nodes {n}` | 🟡 |
| 升级版本 | `paas-cli es upgrade --project {pid} --env {env} --version {ver}` | 🔴 |
| 删除集群 | `paas-cli es delete --project {pid} --env {env}` | 🔴 |

### 9.4 故障排查

流程：信息收集 → `$PAAS_CLI es info` → `$BIANQUE elasticsearch check -n {namespace} -i {instance} -v true` → 补充查询 → 分析建议

诊断项：集群健康(Red/Yellow/Green) | 未分配分片 | CPU 热点 | 写入拒绝 | 索引健康

---

## 10. 外部工具集成

| 工具 | 调用方式 | 超时 | 降级方案 |
|------|---------|------|---------|
| paas-cli | 终端命令执行 | 30s | 提示安装/检查网络 |
| 扁鹊（bianque Skill） | `$BIANQUE {nacos\|redis\|elasticsearch} check ...`（见 `skills/bianque/SKILL.md`） | 60s | 回退到 `$PAAS_CLI` 基本查询 |

**前置检查**：`paas-cli --version` → `bianque --version` → `paas-cli ping`

---

## 11. 安全规范

### 11.1 命令注入防护

- **参数化构造**：变量替换，禁止字符串拼接
- **白名单校验**：

| 参数 | 合法规则 | 非法示例 |
|------|---------|---------|
| project_id | 小写字母+数字 | `; rm -rf` |
| env | DEV/SIT/SRV 枚举 | `DEV; ls` |
| service_name | 字母数字下划线短横线 | `$(whoami)` |
| version | 语义化版本号 | `7.10.2 && cat /etc/passwd` |
| count/replicas | 正整数 | `3 \|\| echo hack` |
| index_name | 小写字母数字短横线 | `log"; rm -rf /` |

- **危险字符过滤**：禁止 `;` `|` `&` `$` `` ` `` `(` `)` `{` `}`

### 11.2 敏感信息

- 密码使用占位符（`${NACOS_PASSWORD}`），引导通过环境变量/密钥管理注入
- 连接地址优先从 paas-cli 动态获取

### 11.3 操作审计

每次执行的 paas-cli/bianque 命令及结果在对话中完整展示

---

## 12. AI 技术应用方案

### 12.1 LLM 应用架构

| 层次 | 组件 | 职责 |
|------|------|------|
| 交互层 | IDE 对话窗口 | 接收自然语言，展示输出 |
| 指令层 | SKILL.md | 结构化 Prompt，定义流程与格式 |
| 执行层 | IDE 智能体 | 解析指令，调用工具 |
| 工具层 | 原生能力 + 外部工具 | 代码生成/搜索、文件读写、终端执行 |

**上下文管理**：SKILL.md < 500 行 | references 按需加载 | 核心流程优先 | 历史对话压缩

### 12.2 Prompt Engineering

Skill 即结构化 Prompt：角色设定（name/description）→ 任务分解（编号步骤）→ 输出约束（格式模板）→ 异常处理 → 安全边界

输出格式约束：✅ 📋 🔧 🔍 标记必含字段 | 成功 ✅ / 失败 ❌ 条件显示 | 禁止密码明文和跳过确认

### 12.3 RAG 技术方案

**知识库三层**：

| 层次 | 内容 | 优先级 |
|------|------|--------|
| 规范知识库 | 企业中间件标准规范 | Phase 4 |
| 历史事故知识库 | 故障现象、根因、处理方式 | Phase 4 |
| 运维 SOP 知识库 | 运维操作标准流程 | Phase 5 |

**检索增强**：读取知识库文件 → 作为附加上下文注入 → 输出增加"参考依据"字段

| 工具 | 调用方式 | 超时 | 降级方案 |
|------|---------|------|---------|
| paas-cli Skill | 遵循 `skills/paas-cli/SKILL.md` 编排 `$PAAS_CLI` 后终端执行 | 30s | 提示查阅 paas-cli Skill / 检查网络 |
| 扁鹊（bianque Skill） | `$BIANQUE {nacos\|redis\|elasticsearch} check ...`（见 `skills/bianque/SKILL.md`） | 60s | 回退到 `$PAAS_CLI` 基本查询 |

**CLI 委托**：中间件 Skill 须先遵循 **paas-cli Skill**（见 `paas-cli-skill-delegation.md`）。`$PAAS_CLI` 解析顺序：① `paas-cli version` 成功 → ② 降级 `python3 skills/paas-cli/paas-cli.py version`

**前置检查**：解析 `$PAAS_CLI` → `$PAAS_CLI version` → `$BIANQUE`（如需，见 bianque Skill：`bianque version`）→ `$PAAS_CLI ping`
| 能力 | 工具调用链 |
|------|-----------|
| 客户端生成 | search_codebase → read_file → create_file/search_replace |
| 代码审计 | grep_code × N → read_file → 输出格式化 |
| 集群操作 | run_in_terminal → 结果解析 → 输出格式化 |
| 故障排查 | run_in_terminal × 2+ → 结果分析 → 输出格式化 |

**编排原则**：步骤间无隐式依赖 | 异常步骤可跳过（降级）| 结果可回溯

**错误恢复**：工具失败 → 替代方案 | 参数校验失败 → 拒绝 | 外部不可用 → 降级 | 理解偏差 → 主动确认

### 12.5 置信度与幻觉控制

**置信度**：🟢 ≥90% 可直接修复 | 🟡 60-90% 建议确认 | 🔴 <60% 需人工分析

**幻觉缓解**：规则ID 白名单校验 | 搜索结果需真实文件路径 | 命令输出需终端实际结果 | 推理链需数据支撑

**人机协同决策点**：高风险操作确认 | 修复代码确认 | 置信度 <80% 诊断确认 | 知识库引用确认

### 12.6 AI 技术演进路线

| 阶段 | 核心技术 | 对应交付 |
|------|---------|----------|
| 短期 | 纯 Prompt + Skill | Phase 1-3 |
| 中期 | Prompt + RAG + 置信度 | Phase 4 |
| 长期 | Agent Workflow + MCP | Phase 5-6 |
| 远期 | Multi-Agent + 自学习 | 持续迭代 |

---

## 13. 增强能力（Phase 4+）

| 能力 | 核心要点 |
|------|---------|
| 知识库/RAG | 规范知识库 + 历史事故记录 + runbooks，输出增加"参考依据"字段 |
| 置信度评分 | 🟢≥90%可直接修复 / 🟡60-90%建议确认 / 🔴<60%需人工分析 |
| 容量预测 | `paas-cli {type} metrics --days 30` 趋势分析 + 瓶颈预测 |
| 主动巡检 | 预定义检查项批量执行 + 定时调度 |
| 跨中间件关联 | 依赖拓扑 + 级联故障诊断 + 多 Skill 协同 |
| 修复编排 | 代码修复(低风险) / 配置修复(中风险+diff确认) / 运维修复(高风险+二次确认) |
| MCP 集成 | 当前终端命令 → 中期 MCP 协议 → 长期 MCP 工具生态 |

---

## 14. 测试方案

### 14.1 测试策略

| 层级 | 方法 | 频率 |
|------|------|------|
| 功能测试 | 对话式 + 标准场景 | 每次变更后 |
| 安全测试 | 注入测试 + 权限测试 | 每次变更后 |
| 回归测试 | 自动化场景 | 每次变更后 |
| 兼容性测试 | 多环境验证 | 版本发布前 |
| 性能测试 | 计时测试 | 版本发布前 |

### 14.2 关键测试用例

**客户端生成（CG）**：正常生成(Java/Go/Python) | 缺参数主动询问 | 默认值注明 | 路径不存在询问 | 文件已存在询问 | 密码占位符 | Redis多模式 | ES新旧版本

**代码审计（CA）**：正常审计输出 | 无问题项目 | 风险等级排序 | 规则全覆盖 | 路径不存在提示 | 无中间件代码提示

**集群操作（CO）**：低风险直接执行 | 中风险确认 | 高风险双重确认 | 拒绝确认取消 | 危险字符拒绝 | paas-cli未安装提示 | 超时处理

**故障排查（TS）**：正常诊断 | 扁鹊不可达降级 | 诊断脚本异常处理 | 推理链展示(Phase4) | 历史事故引用(Phase4)

**安全测试（SEC）**：Shell注入 | 命令替换注入 | 管道符注入 | 枚举值校验 | 密码明文检查 | 高风险跳过确认

### 14.3 性能目标

| 指标 | 目标 |
|------|------|
| 客户端生成 | ≤ 60s |
| 代码审计 | ≤ 120s（约50个文件） |
| 集群操作 | ≤ 30s（不含确认等待） |
| 故障排查 | ≤ 90s |
| paas-cli 单次 | ≤ 15s |

### 14.4 阶段验收标准

| 阶段 | 必须通过的用例 |
|------|---------------|
| Phase 1 | CG-001~007, CA-001~004, SEC-005 |
| Phase 2 | CO-001~007, SEC-001~006 |
| Phase 3 | TS-001~003 |
| Phase 4 | TS-004~005, CA-001 增加参考依据 |
| Phase 5 | 级联诊断场景 + 一键修复场景 |

---

## 15. 质量指标

| 指标 | 目标 |
|------|------|
| 代码生成可用率 | ≥ 85% |
| 审计准确率 | ≥ 80% |
| 审计召回率 | ≥ 70% |
| 命令执行成功率 | ≥ 95% |
| 诊断准确率 | ≥ 70% |
| 用户满意度 | ≥ 4.0/5.0 |

**评估方式**：自动化测试 | A/B 测试 | 用户反馈闭环

---

## 16. 分发策略

**仓库路径映射**：源码目录 `skills/` → 各 Agent 发现目录（**复制安装**，见 `scripts/install-skills.sh`）

| Agent | 项目级目标 | 安装命令 |
|-------|-----------|----------|
| Cursor | `.cursor/skills/` | `./scripts/install-skills.sh cursor` |
| Qoder | `.qoder/skills/` | `./scripts/install-skills.sh qoder` |
| Qoder 用户级 | `~/.qoder/skills/` | `./scripts/install-skills.sh qoder --global` |
| TRAE | `.trae/skills/` | `./scripts/install-skills.sh trae` |
| 全部 | 上表三者 | `./scripts/install-skills.sh all` |

| 其他方式 | 说明 |
|---------|------|
| Git 子模块 | 将本仓库作为子模块放入业务项目，再执行 `install-skills.sh --project-dir <app>` |
| 手动复制 | 等价于脚本内部的 `cp -R skills/ → 目标目录` |

**定制覆盖**：`skills-custom/` 优先于 `skills/`，同名 Skill 覆盖标准版本

**版本管理**：Git Tag 语义化版本（Major.Minor.Patch），SKILL.md 含 version 字段

---

## 17. 经验总结

### 17.1 关键经验

| 经验 | 要点 |
|------|------|
| Skill 指令驱动有效 | 结构化指令可稳定驱动多步骤任务；局限：复杂状态管理需外部编排 |
| references 分离 | SKILL.md < 500 行时指令遵循率显著更高；详细内容放 references/ 按需加载 |
| 安全设计前置 | 事后补充安全规则工作量大；新 Skill 应同步编写操作矩阵和安全校验 |
| 输出格式一致性 | 统一格式提供跨中间件一致体验，第一个 Skill 就确定格式规范 |

### 17.2 风险应对

**技术风险**：LLM 输出不稳定（结构化约束+反馈闭环）| 上下文窗口不足（Skill 精简+按需加载）| 外部工具 API 变更（命令模板独立成段）| IDE 升级行为变化（跟踪更新日志）

**业务风险**：审计误报（置信度+反馈机制）| 高风险操作误执行（多级确认+审计）| 过度依赖 AI（置信度分级+人工确认标注）

**安全风险**：命令注入（白名单+过滤+确认）| 敏感信息泄漏（占位符+环境变量）| 权限越权（操作审计+确认流程）

### 17.3 最佳实践

**Skill 编写**：先流程后细节 | 输出格式先行 | 异常场景穷举 | 触发词丰富化 | 版本字段必填

**测试验证**：即时验证 | 边界场景优先 | 交叉一致性 | 回归验证 | 安全必测

**迭代优化**：用户反馈闭环 | 误报优先处理 | 小步快跑 | 变更记录完整 | A/B 测试

### 17.4 后续方向

**技术债**：审计规则描述精度不足 | 缺少规则排除条件 | 多轮对话上下文丢失 | 命令输出解析脆弱

**功能增强**：RocketMQ Skill | Kafka Skill | MongoDB Skill | 可视化诊断面板 | 自动修复工作流

**生态扩展**：Skill 开发者工具链 | Skill 市场 | MCP 工具生态 | 多 IDE 适配

---

## 18. 交付计划

| 阶段 | 内容 | 工期 | 前置 |
|------|------|------|------|
| Phase 1 | 核心Skill + 客户端生成 + 代码审计（纯智能体能力） | 2周 | — |
| Phase 2 | 集群操作 + paas-cli 集成 + 安全防护 | 1周 | paas-cli 可用 |
| Phase 3 | 故障排查 + 扁鹊集成 + 降级方案 | 1周 | bianque 可用 |
| Phase 4 | 知识库/RAG + 置信度 + 容量预测 + 巡检 | 2周 | Phase 1-3 |
| Phase 5 | 跨中间件关联 + 修复编排 + MCP预留 | 2周 | Phase 4 |
| Phase 6 | 质量评估 + 反馈闭环 + 生态扩展 | 持续 | — |
