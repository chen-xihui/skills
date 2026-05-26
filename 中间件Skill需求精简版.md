# 中间件智能运维 Skill 系统需求（精简版）

**版本**：V3.0-S | **日期**：2026-05-08

---

## 1. 核心概念

- **Skill**：标准化的 Markdown 指令包（SKILL.md），定义触发条件、参数规范、处理流程、输出格式和安全约束
- **IDE 智能体**：利用原生能力（代码生成、文件读写、终端命令、代码搜索）执行 Skill 指令
- **外部工具**：`paas-cli`（集群运维）、`扁鹊`（故障诊断），通过终端命令调用

**设计原则**：Skill 即指令（纯 Markdown）| 最小外部依赖 | 安全优先 | 结构化输出

---

## 2. 系统架构

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

### 3.1 文件结构模板

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

### 3.2 参数收集

优先从上下文推断 → 主动询问缺失参数 → 使用合理默认值（注明）

### 3.3 输出格式

| 能力 | 格式要点 |
|------|---------|
| 客户端生成 | ✅ 生成文件列表 + 📝 后续步骤 + ⚠️ 注意事项 |
| 代码审计 | 📋 扫描概要 + 问题表（文件/行号/规则ID/风险/建议） + 💡 Top3 修复建议 |
| 集群操作 | 🔧 操作结果（类型/目标/状态） + 📊 返回信息 + ⏱️ 耗时 |
| 故障排查 | 🔍 诊断结论 + 📋 详细发现 + 💡 处理建议（含优先级） + 📎 关键数据 |

### 3.4 风险与确认

| 风险 | 操作类型 | 确认要求 |
|------|---------|---------|
| 🟢 低 | 查询、状态检查 | 直接执行 |
| 🟡 中 | 扩缩容、配置变更 | 展示命令，等用户确认 |
| 🔴 高 | 删除、升级、主备切换 | 展示命令+影响，用户须回复"确认" |

---

## 4. Nacos Skill 需求

### 4.1 客户端创建

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| project_id | 是 | — | 项目组编号 |
| env | 是 | — | DEV/SIT/SRV |
| target_path | 是 | — | 生成路径 |
| language | 否 | Java | Java/Go/Python |

平台字段（CLI，禁止用户覆盖）：`server_addr`、`namespace` 来自 `nacos config`；`auth_user` 来自 `nacos config` 的 `Username`；密码仅用 `${NACOS_PASSWORD}`（CLI 脱敏，不向用户索要明文）

流程：参数收集 → `paas-cli auth check`（阻塞）→ `paas-cli nacos config` 拉连接信息与用户名 → 按语言生成代码 → 写入 → 依赖提示

### 4.2 代码审计规则

| 规则ID | 描述 | 风险 |
|--------|------|------|
| NACOS-001 | 未启用本地快照 enableLocalSnapshot | 🔵 |
| NACOS-002 | configLongPollTimeout > 30s | 🟡 |
| NACOS-003 | 循环调用 getConfig 未用 Listener | 🔴 |
| NACOS-004 | 密码硬编码 | 🔴 |
| NACOS-005 | 心跳/权重不符合最佳实践 | 🟡 |
| NACOS-006 | 缺少异常处理和重试 | 🟡 |
| NACOS-007 | 命名空间未按环境隔离 | 🔵 |

### 4.3 集群操作矩阵

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

### 4.4 故障排查

流程：信息收集 → `paas-cli nacos info` 检查状态 → `bianque diagnose --middleware nacos --check health,raft,log` → 补充查询 → 分析建议

诊断项：集群健康度 | 日志分析 | 主备状态 | 客户端连通性

---

## 5. Redis Skill 需求

### 5.1 客户端创建

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| project_id | 是 | — | 项目组编号 |
| env | 是 | — | DEV/SIT/SRV |
| password | 是 | — | Redis 密码 |
| target_path | 是 | — | 生成路径 |
| mode | 否 | standalone | standalone/sentinel/cluster |
| client_type | 否 | lettuce | jedis/lettuce |
| language | 否 | Java | Java/Go/Python |

流程：参数收集 → `paas-cli redis config` → 按 mode/client_type/language 组合生成代码 → 写入 → 依赖提示

### 5.2 代码审计规则

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

### 5.3 集群操作矩阵

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

### 5.4 故障排查

流程：信息收集 → `paas-cli redis info` → `bianque diagnose --middleware redis --check slowlog,memory,replication` → 补充查询 → 分析建议

诊断项：慢查询 | 内存碎片率 | 主从延迟 | 持久化状态 | 故障转移

---

## 6. Elasticsearch Skill 需求

### 6.1 客户端创建

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| project_id | 是 | — | 项目组编号 |
| env | 是 | — | DEV/SIT/SRV |
| auth_user | 是 | — | 用户名 |
| auth_pass | 是 | — | 密码 |
| target_path | 是 | — | 生成路径 |
| client_version | 否 | new | new(ElasticsearchClient 8.x+)/old(RestHighLevelClient 7.x) |
| language | 否 | Java | Java/Go/Python |

流程：参数收集 → `paas-cli es config` → 按 client_version/language 生成代码 → 写入 → 依赖提示

### 6.2 代码审计规则

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

### 6.3 集群操作矩阵

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

### 6.4 故障排查

流程：信息收集 → `paas-cli es info` → `bianque diagnose --middleware es --check cluster-health,shard,cpu,watermark` → 补充查询 → 分析建议

诊断项：集群健康(Red/Yellow/Green) | 未分配分片 | CPU 热点 | 写入拒绝 | 索引健康

---

## 7. 安全规范

### 7.1 命令注入防护

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

### 7.2 敏感信息

- 密码使用占位符（`${NACOS_PASSWORD}`），引导通过环境变量/密钥管理注入
- 连接地址优先从 paas-cli 动态获取

### 7.3 操作审计

每次执行的 paas-cli/bianque 命令及结果在对话中完整展示

---

## 8. 外部工具集成

| 工具 | 调用方式 | 超时 | 降级方案 |
|------|---------|------|---------|
| paas-cli Skill | 遵循 `skills/paas-cli/SKILL.md` 编排 `$PAAS_CLI` 后终端执行 | 30s | 提示查阅 paas-cli Skill / 检查网络 |
| 扁鹊 | `bianque diagnose --middleware {type} --project {pid} --env {env} --check {items}` | 60s | 回退到 paas-cli 基本查询 |

**CLI 委托**：中间件 Skill 须先遵循 **paas-cli Skill**（见 `paas-cli-skill-delegation.md`）。`$PAAS_CLI` 解析顺序：① `paas-cli version` 成功 → ② 降级 `python3 skills/paas-cli/paas-cli.py version`

**前置检查**：解析 `$PAAS_CLI` → `$PAAS_CLI version` → `$BIANQUE`（如需，见 bianque Skill：`bianque version`）→ `$PAAS_CLI ping`

---

## 9. 增强能力（Phase 4+）

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

## 10. 质量指标

| 指标 | 目标 |
|------|------|
| 代码生成可用率 | ≥ 85% |
| 审计准确率 | ≥ 80% |
| 审计召回率 | ≥ 70% |
| 命令执行成功率 | ≥ 95% |
| 诊断准确率 | ≥ 70% |
| 用户满意度 | ≥ 4.0/5.0 |

---

## 11. 分发策略

**仓库路径映射**：本仓库根目录 `skills/` 即为 Skill 与 CLI 安装路径；集成到其他项目时可复制到其 `skills/` 或 Cursor `.cursor/skills/`

| 安装方式 | 命令/操作 | 适用场景 |
|---------|----------|---------|
| 一键安装 | `npx skills add <org>/middleware-skills/middleware-nacos` | 个人开发者 |
| Git 子模块 | `git submodule add <repo-url> skills-external/middleware-skills` + 符号链接 | 团队协作 |
| 手动复制 | 复制 SKILL.md 到 `skills/` | 离线/临时 |

**定制覆盖**：`skills-custom/` 优先于 `skills/`，同名 Skill 覆盖标准版本

**版本管理**：Git Tag 语义化版本（Major.Minor.Patch），SKILL.md 含 version 字段

---

## 12. 交付计划

| 阶段 | 内容 | 工期 | 前置 |
|------|------|------|------|
| Phase 1 | 核心Skill + 客户端生成 + 代码审计（纯智能体能力） | 2周 | — |
| Phase 2 | 集群操作 + paas-cli 集成 + 安全防护 | 1周 | paas-cli 可用 |
| Phase 3 | 故障排查 + 扁鹊集成 + 降级方案 | 1周 | bianque 可用 |
| Phase 4 | 知识库/RAG + 置信度 + 容量预测 + 巡检 | 2周 | Phase 1-3 |
| Phase 5 | 跨中间件关联 + 修复编排 + MCP预留 | 2周 | Phase 4 |
| Phase 6 | 质量评估 + 反馈闭环 + 生态扩展 | 持续 | — |
