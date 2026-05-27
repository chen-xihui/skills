---
name: middleware-es
version: "1.7.1"
description: >-
  Creates Elasticsearch clients, audits usage, runs cluster ops via paas-cli
  Skill, troubleshoots with bianque Skill, and provides access guides. Use when
  the user mentions ES, Elasticsearch, 搜索引擎, 索引, or ES cluster issues.
disable-model-invocation: true
---

# Elasticsearch 中间件

## 功能概述

| # | 能力 | 文档 |
|---|------|------|
| 1 | 客户端创建与配置 | [references/capabilities/01-client.md](references/capabilities/01-client.md) |
| 2 | 代码优化检查 | [references/capabilities/02-audit.md](references/capabilities/02-audit.md) |
| 3 | 集群交互 | [references/capabilities/03-cluster.md](references/capabilities/03-cluster.md) |
| 4 | 故障排查 | [references/capabilities/04-troubleshoot.md](references/capabilities/04-troubleshoot.md) |
| 5 | 服务接入指引 | [references/capabilities/05-access-guide.md](references/capabilities/05-access-guide.md) |

**执行约定**：根据用户意图**只加载对应能力文档**；涉及 CLI 时先加载 `skills/paas-cli/SKILL.md` / `skills/bianque/SKILL.md`。

## 通用规范

> `_shared-references/middleware-common.md` · `paas-cli-skill-delegation.md` · `cli-security-rules.md`

### ES 扩展白名单

| 参数 | 合法值 |
|------|--------|
| index_name | 小写字母、数字、短横线 |
| alias | 字母、数字、短横线、下划线 |
| max-segments | 正整数 |

## 参考资源

| 目录 | 说明 |
|------|------|
| `references/es-client-templates/` | 客户端模板 |
| `references/es-audit-rules/` | ES-001~008 |
| `references/es-cluster-ops/` | 集群操作 |
| `references/es-troubleshooting/` | 诊断 |
| `references/es-access-guide/` | 接入指引 |

## 变更记录

- v1.7.1 (2026-05-27): 租约能力并入 `capabilities/03-cluster`、`04-troubleshoot`（对齐 master）
- v1.7.0 (2026-05-26): ES Java 模板扩展：官方 elasticsearch-java、Spring Data Starter、BBoss；新增 `java_stack` 选型
- v1.6.0 (2026-05-26): 能力一对齐 Nacos：`auth check` + `es config`；移除用户必填 auth_user/auth_pass
- v1.5.0 (2026-05-26): ECC 式瘦身——能力拆至 `references/capabilities/`
- v1.4.0 (2026-05-26): 委托 paas-cli Skill
- v1.0.0 (2026-05-11): 初始版本
