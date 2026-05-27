---
name: everything-redis-skills
description: Redis Java 客户端开发专家，提供 Jedis/Lettuce/Redisson/Spring Data Redis 代码生成、配置生成、代码审计能力；当用户需要创建 Redis 客户端、生成缓存代码、检查 Redis 代码规范或获取 Redis 连接配置时使用
dependency:
  python:
    - redis==5.0.0
---

# Redis Java 客户端开发专家

## 功能定位

本 Skill 是 Redis Java 客户端开发专家，聚焦于根据规范提供 Redis 接入实践：

1. **代码生成**：生成符合规范的 Jedis、Lettuce、Redisson、Spring Data Redis 接入代码
2. **配置生成**：生成符合规范的连接配置
3. **代码审计**：检查生成的客户端代码，识别常用错误并给出修改建议

## 能力索引

| 能力 | 触发场景 | 详细说明 |
|------|---------|---------|
| [客户端代码生成](./client-code-generator/index.md) | "创建 Redis 客户端"、"生成缓存代码"、"帮我配置 Jedis/Lettuce/Redisson" | 根据客户端类型生成对应代码模板 |
| [代码审计检查](./client-code-generator/Jedis/rules/index.md) | "检查 Redis 代码"、"代码优化"、"审计" | 14 条审计规则覆盖常见问题 |
| [Redis 连接信息获取](./client-redis-paas-tools/README.md) | "获取 Redis 地址"、"查看 Redis 配置" | 通过命令行获取连接信息 |

## 前置准备

1. 确保 Java 环境已安装（JDK 8+）
2. 确保 Maven/Gradle 依赖管理工具可用
3. 如需使用 Redis 连接工具，确保 Python 环境已安装

## 客户端推荐规则

| 客户端 | 推荐场景 | 说明 |
|--------|---------|------|
| **Jedis** | 非 Spring 项目、简单场景 | 默认推荐，轻量级同步客户端 |
| **Lettuce** | Spring Data Redis 项目 | Spring 官方推荐，异步/响应式支持，自动重连 |
| **Redisson** | 分布式锁、分布式集合 | 支持更多数据结构，Java 语义化 |
| **Spring Data Redis** | Spring Boot 项目 | Spring 统一抽象，整合 Spring 生态（底层使用 Lettuce） |

### 推荐决策树

```
                        是否需要分布式锁/集合？
                                │
                ┌───────────────┴───────────────┐
                │                               │
               是                               否
                │                               │
                ▼                               ▼
        ┌───────────────┐              是否使用 Spring？
                │                               │
        Redisson                        ┌───────────────┴───────────────┐
        分布式锁/集合                      │                               │
                                          │                               │
                                         是                               否
                                          │                               │
                                          ▼                               ▼
                                  ┌───────────────┐              ┌───────────────┐
                                  │ Spring Data   │              │ Jedis         │
                                  │ Redis         │              │ (默认推荐)    │
                                  │ 底层使用Lettuce│              └───────────────┘
                                  └───────────────┘
```

参考 [client-code-generator/index.md](./client-code-generator/index.md) 选择对应客户端，按示例生成代码。

### 2. 代码审计

生成代码后，使用审计规则检查：
```bash
python client-code-generator/Jedis/scripts/check_code.py --path ./src
```

## 目录结构

```
everything-redis-skills/
├── SKILL.md                           # 本文件
├── client-code-generator/             # 客户端代码生成
│   ├── index.md                       # 能力索引与触发规则
│   ├── Jedis/                         # Jedis 客户端
│   │   ├── rules/                    # 审计规则（REDIS-001~014）
│   │   ├── code-template/            # 代码模板
│   │   ├── scripts/                  # 检查脚本
│   │   └── index.md                  # 子能力说明
│   ├── Lettuce/                      # Lettuce 客户端
│   ├── Redisson/                     # Redisson 客户端
│   └── SpringDataRedis/              # Spring Data Redis 客户端
└── client-redis-paas-tools/          # Redis 连接工具
    ├── paas-cli.py                   # 命令行工具（mock）
    └── config/                       # 配置文件
```

## 注意事项

- 生成的代码中密码以占位符形式（如 `${REDIS_PASSWORD}`）写入，请通过环境变量注入
- 连接池参数需根据实际并发量调整
- 生产环境禁止使用 `keys *` 命令
- 代码审计发现的严重问题必须修复后再上线

## 参考资料

- Redis 审计规则详情：[client-code-generator/Jedis/rules/index.md](./client-code-generator/Jedis/rules/index.md)
- 代码模板索引：[client-code-generator/Jedis/code-template/index.md](./client-code-generator/Jedis/code-template/index.md)
