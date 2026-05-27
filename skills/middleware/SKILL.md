---
name: middleware
version: "1.3.0"
description: >-
  Routes middleware operations to middleware-nacos, middleware-redis, or
  middleware-es skills. Use when the user mentions 中间件, middleware, 运维,
  客户端创建, 代码检查, 集群, or 故障排查 without naming a specific engine.
---

# 中间件智能运维入口

## 功能概述

识别中间件类型并路由到专项 Skill；**不在此 Skill 内执行具体运维步骤**。

| 中间件 | 专项 Skill |
|--------|-----------|
| Nacos | `middleware-nacos` |
| Redis | `middleware-redis` |
| Elasticsearch | `middleware-es` |

工具 Skill：`paas-cli`、`bianque`（由专项 Skill 按需委托加载）。

## 路由规则

| 中间件 | 触发关键词 |
|--------|-----------|
| Nacos | Nacos、注册中心、配置中心、命名空间、服务发现、naming、config-center |
| Redis | Redis、缓存、哨兵、sentinel、RedisCluster |
| ES | ES、Elasticsearch、搜索引擎、索引、Elastic |

```
用户请求 → 匹配关键词？
  ├─ 单一中间件 → 加载对应专项 Skill（及该 Skill 的能力文档）
  ├─ 多种中间件 → 依次加载各专项 Skill
  └─ 无法识别 → 询问：「请问需要 Nacos、Redis 还是 Elasticsearch？」
```

## 专项能力索引

| 能力 | 说明 |
|------|------|
| 客户端创建 | 专项 `references/capabilities/01-client.md` |
| 代码审计 | `02-audit.md` |
| 集群交互 | `03-cluster.md` |
| 故障排查 | `04-troubleshoot.md` |
| 服务接入 | `05-access-guide.md`（Redis/ES） |

## 通用规范

> `_shared-references/middleware-common.md` · `paas-cli-skill-delegation.md`

## Agent 安装（复制，非符号链接）

源码在仓库 `skills/`。安装到各 IDE 发现目录：

```bash
./scripts/install-skills.sh cursor   # → .cursor/skills/
./scripts/install-skills.sh qoder    # → .qoder/skills/
./scripts/install-skills.sh trae     # → .trae/skills/
./scripts/install-skills.sh all      # 上述三者
```

详见仓库根目录 `README.md`。

## 变更记录

- v1.3.1 (2026-05-26): 安装改为 `install-skills.sh` 复制模式；支持 Cursor / Qoder / TRAE
- v1.3.0 (2026-05-26): 路由 Skill 瘦身；指向 `capabilities/` 与安装脚本
- v1.2.0 (2026-05-26): paas-cli Skill 委托
- v1.0.0 (2026-05-11): 初始版本
