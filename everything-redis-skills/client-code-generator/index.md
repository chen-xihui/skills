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

各客户端代码均需通过对应的专属审计规则和集群通用规则，规则按客户端类型划分：

| 客户端 | 专属规则 | 严重 | 风险 | 提示 | 集群规则 |
|--------|---------|------|------|------|---------|
| Jedis | JEDIS-001 ~ JEDIS-014 | 6 | 6 | 2 | CLUSTER-001 ~ CLUSTER-003 |
| Lettuce | LETTUCE-001 ~ LETTUCE-007 | 3 | 3 | 1 | CLUSTER-001 ~ CLUSTER-003 |
| Redisson | REDISSON-001 ~ REDISSON-005 | 3 | 2 | 0 | CLUSTER-001 ~ CLUSTER-003 |
| Spring Data Redis | SDR-001 ~ SDR-003 | 1 | 2 | 0 | CLUSTER-001 ~ CLUSTER-003 |

### 全局风险等级统计

- 🔴 **严重**: 15 条（JEDIS-001~006, LETTUCE-001~003, REDISSON-001~003, SDR-001, CLUSTER-001）
- 🟡 **风险**: 14 条（JEDIS-007~012, LETTUCE-004~006, REDISSON-004~005, SDR-002~003, CLUSTER-002~003）
- 🔵 **提示**: 3 条（JEDIS-013~014, LETTUCE-007）

详见：
- [Jedis/rules/index.md](./Jedis/rules/index.md)
- [Lettuce/rules/index.md](./Lettuce/rules/index.md)
- [Redisson/rules/index.md](./Redisson/rules/index.md)
- [SpringDataRedis/rules/index.md](./SpringDataRedis/rules/index.md)
