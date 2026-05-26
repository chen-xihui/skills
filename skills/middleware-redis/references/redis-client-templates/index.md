# Redis 客户端代码模板索引

本目录包含 Redis 客户端的代码模板，覆盖 Java（Lettuce/Jedis × Standalone/Sentinel/Cluster）、Go、Python。

## 模板总览

| 语言/框架 | 部署模式 | 详细文档 |
|-----------|---------|---------|
| **Java** |  |  |
| Lettuce | Standalone | [java.md](java.md#1-java--lettuce--standalone) |
| Jedis | Standalone | [java.md](java.md#2-java--jedis--standalone) |
| Lettuce | Sentinel | [java.md](java.md#3-java--lettuce--sentinel) |
| Lettuce | Cluster | [java.md](java.md#4-java--lettuce--cluster) |
| Lettuce | Cluster + TCP参数 + 连接池 | [java.md](java.md#7-java--lettuce-集群模式完整配置) |
| Jedis | 完整配置（含推荐参数） | [java.md](java.md#74-jedis-配置示例) |
| **Go** | Standalone | [go.md](go.md) |
| **Python** | Standalone | [python.md](python.md) |

## 依赖说明

- **Java + Lettuce**：`io.lettuce:lettuce-core`、`org.springframework.boot:spring-boot-starter-data-redis`
- **Java + Jedis**：`redis.clients:jedis`、`org.springframework.boot:spring-boot-starter-data-redis`
- **Go**：`github.com/redis/go-redis/v9`
- **Python**：`pip install redis`

## 客户端版本要求

| 客户端 | 推荐版本 | 说明 |
|--------|---------|------|
| Jedis | ≥4.4.0 / ≥3.10 | 4.4.0、3.10.0 版本对 DNS 解析/服务断联功能进行优化 |
| Lettuce | ≥6.3.0 | 6.3.0 版本增加 tcpTimeout 参数配置 |
| Redisson | 不推荐 | 非开源技术目录软件 |

## 安全注意事项

- 密码以 `${REDIS_PASSWORD}` 占位符形式写入配置文件，通过环境变量或密钥管理系统注入
- 连接池参数需根据实际并发量调整，禁止使用默认值 -1
- 集群模式下 Lettuce 需配置拓扑刷新开关和周期