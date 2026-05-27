# Redis 客户端代码生成 - 目录用途说明

本目录为 Lettuce 客户端提供以下能力：

## 目录结构

```
Lettuce/
├── index.md          # 子能力说明
├── rules/            # 审计规则（REDIS-001 ~ REDIS-014）
├── code-template/    # 代码模板
├── scripts/          # 代码检查工具
└── usage.md          # 本文件
```

## 规则说明

[rules/](rules/) 目录包含 14 条审计规则，用于检查代码是否符合 Redis 最佳实践：

| 规则ID | 风险等级 | 说明 |
|--------|---------|------|
| REDIS-001 | 🔴 严重 | 禁止使用 keys * |
| REDIS-002 | 🟡 警告 | 大 Key 风险检查 |
| REDIS-003 | 🟡 警告 | 热 Key 风险检查 |
| REDIS-004 | 🟡 警告 | 连接池参数合理性 |
| REDIS-005 | 🔵 建议 | Pipeline 批量使用 |
| REDIS-006 | 🔵 建议 | Lua 脚本优化 |
| REDIS-007 | 🟡 警告 | 过期时间设置 |
| REDIS-008 | 🔴 严重 | 密码硬编码检查 |
| REDIS-009 | 🔴 严重 | 高危命令禁止 |
| REDIS-010 | 🔴 严重 | Keys 全库匹配禁止 |
| REDIS-011 | 🟡 警告 | 高时间复杂度命令 |
| REDIS-012 | 🔵 建议 | Key 命名规范 |
| REDIS-013 | 🟡 警告 | 大 Key 集合检查 |
| REDIS-014 | 🟡 警告 | 事务命令检查 |

## 代码模板说明

[code-template/](code-template/) 目录包含：

- `RedisConfig.java` - 连接配置模板（含 TCP 优化）
- `RedisService.java` - 服务层封装模板
- `RedisClusterConfig.java` - 集群完整配置模板
- `application.yml` - 配置文件模板
- `index.md` - 模板索引

## 脚本说明

[scripts/](scripts/) 目录包含：

- `check_code.py` - 代码审计脚本

使用方式：
```bash
python scripts/check_code.py --path ./src --client lettuce
```
