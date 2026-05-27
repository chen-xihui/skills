# Redis 客户端代码生成能力索引

本目录提供 Redis Java 客户端代码生成能力，按客户端类型组织。

## 能力总览

| 客户端 | 触发关键词 | 支持模式 | 说明 |
|--------|-----------|---------|------|
| [Jedis](./Jedis/index.md) | jedis、Jedis | Standalone / Sentinel / Cluster | 轻量级同步客户端 |
| [Lettuce](./Lettuce/index.md) | lettuce、Lettuce | Standalone / Sentinel / Cluster | 异步/响应式支持 |
| [Redisson](./Redisson/index.md) | redisson、Redisson | Standalone / Sentinel / Cluster / Replicated | 分布式数据结构 |
| [Spring Data Redis](./SpringDataRedis/index.md) | spring data redis、SpringDataRedis | Standalone / Sentinel / Cluster | Spring 统一抽象 |

## 触发规则

当用户请求以下场景时，自动路由到对应客户端：

| 用户意图 | 路由目标 | 说明 |
|---------|---------|------|
| "创建 Redis 客户端"、"配置 Redis" | Jedis | 默认推荐（非 Spring 项目） |
| "Spring Data Redis"、"RedisTemplate" | Spring Data Redis | Spring 项目（底层使用 Lettuce） |
| "分布式锁"、"Redisson 锁" | Redisson | 分布式锁/集合场景 |
| "Lettuce" | Lettuce | 指定 Lettuce |
| "Jedis" | Jedis | 指定 Jedis |

## 通用参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | - | 项目组编号 |
| env | enum | 是 | - | 环境：DEV / SIT / SRV |
| mode | enum | 否 | standalone | 部署模式：standalone / sentinel / cluster |
| target_path | string | 是 | - | 代码生成目标路径 |
| redis_password | string | 是 | - | Redis 密码（写入为占位符） |

## 客户端选择指南

```
                        是否需要分布式锁/集合？
                                │
                ┌───────────────┴───────────────┐
                │                               │
               是                               否
                │                               │
                ▼                               ▼
        ┌───────────────┐              是否使用 Spring？
        │ Redisson      │                      │
        │ 分布式锁/集合  │              ┌────────┴────────┐
        └───────────────┘              │                 │
                                       │                 │
                                      是                 否
                                       │                 │
                                       ▼                 ▼
                               ┌───────────────┐ ┌───────────────┐
                               │ Spring Data   │ │ Jedis         │
                               │ Redis         │ │ (默认推荐)    │
                               │ 底层使用Lettuce│ └───────────────┘
                               └───────────────┘
```

## 生成文件清单

| 客户端类型 | 生成文件 |
|-----------|---------|
| Jedis | JedisConfig.java, JedisService.java, application.yml |
| Lettuce | RedisConfig.java, RedisService.java, application.yml |
| Redisson | RedissonConfig.java, application.yml |
| Spring Data Redis | RedisConfig.java, RedisTemplate 配置, application.yml |

## 审计规则

所有客户端代码均需通过以下 14 条审计规则：
- 🔴 严重：REDIS-001、REDIS-008、REDIS-009、REDIS-010
- 🟡 警告：REDIS-002、REDIS-003、REDIS-004、REDIS-007、REDIS-011、REDIS-013、REDIS-014
- 🔵 建议：REDIS-005、REDIS-006、REDIS-012

详见：[Jedis/rules/index.md](./Jedis/rules/index.md)
