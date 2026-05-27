# Redis 客户端代码生成 - 目录用途说明

本目录为 Redisson 客户端提供以下能力：

## 目录结构

```
Redisson/
├── index.md          # 子能力说明
├── rules/            # 审计规则
├── code-template/    # 代码模板
├── scripts/          # 代码检查工具
└── usage.md          # 本文件
```

## 规则说明

[rules/](rules/) 目录包含适用于 Redisson 的审计规则：

| 规则ID | 风险等级 | 说明 |
|--------|---------|------|
| REDIS-001 | 🔴 严重 | 禁止使用 keys * |
| REDIS-007 | 🟡 警告 | 过期时间设置 |
| REDIS-008 | 🔴 严重 | 密码硬编码检查 |
| REDIS-009 | 🔴 严重 | 高危命令禁止 |
| REDIS-010 | 🔴 严重 | Keys 全库匹配禁止 |
| REDIS-012 | 🔵 建议 | Key 命名规范 |

## 代码模板说明

[code-template/](code-template/) 目录包含：

- `RedissonConfig.java` - Redisson 配置模板
- `DistributedLockService.java` - 分布式锁服务模板
- `application.yml` - 配置文件模板

## 脚本说明

[scripts/](scripts/) 目录包含：

- `check_code.py` - 代码审计脚本

使用方式：
```bash
python scripts/check_code.py --path ./src --client redisson
```

## 注意事项

Redisson 为第三方库，非 Spring 技术目录官方推荐。使用前请评估是否满足项目需求。
