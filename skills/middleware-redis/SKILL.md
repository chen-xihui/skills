---
name: middleware-redis
version: "1.7.0"
description: >-
  Creates Redis clients, audits usage, runs cluster ops via paas-cli Skill,
  troubleshoots with bianque Skill, and provides access guides. Use when the user
  mentions Redis, 缓存, sentinel, 哨兵, or Redis cluster/client issues.
disable-model-invocation: true
---

# Redis 中间件

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

### Redis 扩展白名单

| 参数 | 合法值 |
|------|--------|
| mode | standalone / sentinel / cluster |
| client_type | jedis / lettuce |
| type | cluster / sentinel |
| policy | noeviction / allkeys-lru / volatile-lru / allkeys-lfu / volatile-lfu / allkeys-random / volatile-random / volatile-ttl |
| node | 字母、数字、短横线、冒号、点号 |

## 参考资源

| 目录 | 说明 |
|------|------|
| `references/redis-client-templates/` | 客户端模板 |
| `references/redis-audit-rules/` | REDIS-001~014 |
| `references/redis-cluster-ops/` | 集群操作 |
| `references/redis-troubleshooting/` | 诊断 |
| `references/redis-access-guide/` | 接入指引 |

## 变更记录

- v1.7.0 (2026-05-26): 能力一对齐 Nacos：`auth check` + `redis config` 拉取平台字段；移除用户必填 password
- v1.6.0 (2026-05-26): ECC 式瘦身——能力拆至 `references/capabilities/`
- v1.5.0 (2026-05-26): 委托 paas-cli Skill
- v1.0.0 (2026-05-11): 初始版本
