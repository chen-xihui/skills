# Redis 客户端代码模板索引

本目录包含 Redis 客户端的代码模板，覆盖 Java（Lettuce/Jedis × Standalone/Sentinel/Cluster）、Go、Python。

**使用方式**：先在本索引中根据目标语言和部署模式定位需要的模板文件，再读取对应文件获取完整代码。

---

## Java 模板

### Lettuce + Standalone

| 模板文件 | 说明 | 生成目标文件 |
|---------|------|------------|
| [java-lettuce-standalone-config.md](./java-lettuce-standalone-config.md) | RedisConfig + RedisTemplate 配置 | RedisConfig.java |
| [java-lettuce-standalone-service.md](./java-lettuce-standalone-service.md) | RedisService 服务类（含 scan/pipeline） | RedisService.java |
| [java-lettuce-standalone-yml.md](./java-lettuce-standalone-yml.md) | Spring Boot 应用配置 | application.yml |

### Jedis + Standalone

| 模板文件 | 说明 | 生成目标文件 |
|---------|------|------------|
| [java-jedis-config.md](./java-jedis-config.md) | JedisPool 配置 | JedisConfig.java |
| [java-jedis-yml.md](./java-jedis-yml.md) | Spring Boot 应用配置（Jedis） | application.yml |

### Lettuce + Sentinel

| 模板文件 | 说明 | 生成目标文件 |
|---------|------|------------|
| [java-lettuce-sentinel-config.md](./java-lettuce-sentinel-config.md) | Sentinel 连接配置 | RedisSentinelConfig.java |
| [java-lettuce-sentinel-yml.md](./java-lettuce-sentinel-yml.md) | Sentinel 应用配置 | application.yml |

### Lettuce + Cluster

| 模板文件 | 说明 | 生成目标文件 |
|---------|------|------------|
| [java-lettuce-cluster-config.md](./java-lettuce-cluster-config.md) | Cluster 连接配置 | RedisClusterConfig.java |
| [java-lettuce-cluster-yml.md](./java-lettuce-cluster-yml.md) | Cluster 应用配置 | application.yml |

## Go 模板

| 模板文件 | 说明 | 生成目标文件 |
|---------|------|------------|
| [go-client.md](./go-client.md) | Redis 客户端封装 | redis_client.go |
| [go-config-yml.md](./go-config-yml.md) | Go 项目配置文件 | config.yaml |

## Python 模板

| 模板文件 | 说明 | 生成目标文件 |
|---------|------|------------|
| [python-client.md](./python-client.md) | Redis 客户端工具类 | redis_client.py |
| [python-config-yml.md](./python-config-yml.md) | Python 项目配置文件 | config.yaml |
| [python-pip-deps.md](./python-pip-deps.md) | Pip 依赖配置 | requirements.txt 片段 |

---

## 通用规范

- 所有密码字段均使用 `${REDIS_PASSWORD}` 占位符，引导用户通过环境变量注入
- 模板中已内嵌 REDIS-001 ~ REDIS-007 最佳实践注释
- Go 和 Python 模板的密码获取逻辑：优先使用传入值 → 回退到环境变量 `REDIS_PASSWORD`
