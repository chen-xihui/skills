---
name: middleware-nacos
version: "1.6.1"
description: >-
  Creates Nacos clients, audits usage, runs cluster ops via paas-cli Skill, and
  troubleshoots with bianque Skill. Use when the user mentions Nacos, 注册中心,
  配置中心, 命名空间, 服务发现, or Nacos client/cluster issues.
disable-model-invocation: true
---

# Nacos 中间件

## 功能概述

| # | 能力 | 文档 |
|---|------|------|
| 1 | 客户端创建与配置 | [references/capabilities/01-client.md](references/capabilities/01-client.md) |
| 2 | 代码优化检查 | [references/capabilities/02-audit.md](references/capabilities/02-audit.md) |
| 3 | 集群交互 | [references/capabilities/03-cluster.md](references/capabilities/03-cluster.md) |
| 4 | 故障排查 | [references/capabilities/04-troubleshoot.md](references/capabilities/04-troubleshoot.md) |

**执行约定**：根据用户意图**只加载对应能力文档**；涉及 CLI 时先加载 `skills/paas-cli/SKILL.md` / `skills/bianque/SKILL.md`。

## 通用规范

> `_shared-references/middleware-common.md` · `paas-cli-skill-delegation.md` · `cli-security-rules.md`

### Nacos 扩展白名单

| 参数 | 合法值 |
|------|--------|
| service_name / group / config_id | 字母、数字、下划线、短横线（config_id 可含 `.`） |

## 参考资源

| 目录 | 说明 |
|------|------|
| `references/nacos-client-templates/` | 客户端模板 |
| `references/nacos-audit-rules/` | 审计规则 NACOS-001~007 |
| `references/nacos-cluster-ops/` | 集群 CRD 操作 |
| `references/nacos-troubleshooting/` | 诊断细节 |

## 变更记录

- v1.6.1 (2026-05-27): 租约能力并入 `capabilities/03-cluster`、`04-troubleshoot`（对齐 master）
- v1.6.0 (2026-05-26): ECC 式瘦身——通用规范下沉、能力拆至 `references/capabilities/`；`description` 与 `$BIANQUE` 统一
- v1.5.0 (2026-05-26): 委托 paas-cli Skill
- v1.0.0 (2026-05-11): 初始版本
