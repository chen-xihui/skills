---
name: "middleware"
version: "1.2.0"
description: "中间件智能运维入口技能，识别中间件类型并路由到对应专项Skill。触发词：中间件、middleware、运维、客户端创建、代码检查、集群、故障排查"
---

# 中间件智能运维入口

## 功能概述

本 Skill 是中间件智能运维系统的通用入口，负责识别用户请求涉及的中间件类型，并将请求路由到对应的专项 Skill 执行。

当前支持的中间件：
- **Nacos** — 注册中心 / 配置中心
- **Redis** — 缓存数据库
- **Elasticsearch** — 搜索引擎

配套 CLI 工具 Skill（Mock，与本仓库 `skills/paas-cli`、`skills/bianque` 同目录）：
- **paas-cli** — 集群运维与连接配置拉取
- **bianque** — 故障诊断

---

## 路由规则

### 关键词匹配

当用户请求涉及以下关键词时，激活对应专项 Skill：

| 中间件 | 触发关键词 |
|--------|-----------|
| Nacos | Nacos、注册中心、配置中心、命名空间、服务发现、服务注册、naming、config-center |
| Redis | Redis、缓存、缓存数据库、哨兵、sentinel、集群缓存、RedisCluster |
| Elasticsearch | ES、Elasticsearch、搜索引擎、索引、搜索、Elastic、elastic |

### 路由决策逻辑

1. **单中间件请求**：用户请求仅涉及一种中间件 → 直接路由到对应专项 Skill
2. **多中间件请求**：用户请求同时涉及多种中间件 → 依次调用对应专项 Skill 并综合结果
3. **未明确中间件类型**：用户请求模糊，无法确定中间件类型 → 主动询问用户

### 决策流程

```
用户请求
  │
  ├─ 包含 Nacos 关键词？ ──是──→ 使用 middleware-nacos Skill
  │
  ├─ 包含 Redis 关键词？ ──是──→ 使用 middleware-redis Skill
  │
  ├─ 包含 ES 关键词？ ──是──→ 使用 middleware-es Skill
  │
  └─ 无法识别 ──→ 询问用户："请问您需要操作哪种中间件？支持 Nacos、Redis、Elasticsearch"
```

### 路由示例

| 用户请求 | 路由目标 |
|---------|---------|
| "创建 Nacos 客户端" | middleware-nacos |
| "检查 Redis 代码" | middleware-redis |
| "ES 集群状态怎么样" | middleware-es |
| "我的 Nacos 连不上了" | middleware-nacos |
| "缓存雪崩了" | middleware-redis |
| "搜索服务异常" | middleware-es |
| "中间件代码优化" | 询问具体中间件类型 |
| "查看集群状态" | 询问具体中间件类型 |

---

## 专项 Skill 能力概览

每个专项 Skill 提供 4~5 项原子能力：

| 能力 | 说明 | 是否需要外部工具 |
|------|------|----------------|
| 客户端创建与配置 | 经 paas-cli Skill 拉取连接信息后生成客户端与配置 | 是（paas-cli Skill） |
| 代码优化检查 | 扫描项目代码，按规则清单逐项检查 | 否 |
| 集群交互 | 经 **paas-cli Skill** 编排 `$PAAS_CLI` 执行集群操作 | 是（paas-cli Skill） |
| 故障排查 | 通过 **bianque Skill** 与 **paas-cli Skill** 诊断异常 | 是（bianque Skill + paas-cli Skill） |
| 服务接入指引 | 提供设计、开发、测试、上线全生命周期指导 | 否 | Redis、ES |
---

## 通用规范

### 参数收集

当用户请求中缺少必要参数时，智能体应：
1. **优先从上下文推断**：如用户已打开项目，从项目配置文件中提取 `project_id`、`language` 等
2. **主动询问缺失参数**：对必要参数逐一询问，提供可选值提示
3. **使用合理默认值**：对有明确默认值的参数可先使用默认值，在输出中注明

### paas-cli Skill 委托

> 详见 `_shared-references/paas-cli-skill-delegation.md`

各专项 Skill 涉及 PaaS 或诊断命令时，须先遵循 **paas-cli Skill** / **bianque Skill**，不得直接调用可执行文件。路径与子命令以 `skills/paas-cli/SKILL.md` 为准。

### 安全约束

> 详细安全规则参见 `_shared-references/cli-security-rules.md`

- **参数白名单校验**：经 paas-cli Skill / bianque Skill 执行的命令参数必须经过白名单校验
- **危险字符过滤**：参数值中不得包含 `;`、`|`、`&`、`$`、`` ` ``、`(`、`)`、`{`、`}` 等 shell 元字符
- **高风险操作确认**：🟡 中风险展示命令后询问；🔴 高风险需用户明确回复"确认"
- **敏感信息处理**：密码以占位符形式写入配置文件

---

## 变更记录

- v1.2.0 (2026-05-26): 集群/客户端相关操作统一委托 **paas-cli Skill**（见 `paas-cli-skill-delegation.md`）
- v1.1.0 (2026-05-26): Skill 根目录改为项目下 `skills/`（不再使用 `.trae/skills/`）
- v1.0.0 (2026-05-11): 初始版本，支持 Nacos、Redis、Elasticsearch 三种中间件的路由
