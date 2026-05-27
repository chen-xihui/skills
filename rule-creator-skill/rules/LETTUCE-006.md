# LETTUCE-006：必须设置 commandTimeout

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-006 |
| 风险等级 | 风险 |
| 规则描述 | 必须显式设置命令超时（commandTimeout），禁止使用默认无限等待，防止线程无限阻塞堆积 |

## 问题说明

Lettuce 的 RedisURI 默认 commandTimeout 为 60 秒（`RedisURI.DEFAULT_TIMEOUT`），但在某些版本或配置下可能被覆盖为 0（无限等待）。若未显式设置 commandTimeout，当 Redis 服务端响应缓慢（慢查询、BGSAVE 导致 fork 阻塞、网络拥塞）时，调用线程将无限期阻塞，导致线程池耗尽、服务级联故障。生产环境必须显式设置合理的命令超时，确保故障快速失败。

## 检查方法

- 静态分析：检查 RedisURI 创建或 Spring Boot 配置中是否显式设置了 `timeout` / `commandTimeout`
- 检查是否通过 `client.setDefaultCommandTimeout()` 设置了全局超时
- 确认超时值是否合理（建议 200ms-3s，根据业务 SLA 调整）
- 脚本化检查：`python scripts/check_lettuce_006.py <项目根目录>`

## 违规示例

```java
// 未设置 commandTimeout，使用默认值或无限等待
RedisURI uri = RedisURI.Builder.redis("127.0.0.1", 6379).build();
// RedisURI 默认 timeout 为 60 秒，过长
RedisClient client = RedisClient.create(uri);
StatefulRedisConnection<String, String> connection = client.connect();
connection.sync().get("key");  // 可能阻塞 60 秒才超时
```

```java
// 通过 URL 创建，未指定超时
RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
// 命令超时使用默认值，线程长时间阻塞风险
```

```yaml
# application.yml - 未设置超时
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    # 缺少 timeout 配置
```

## 合规示例

```java
// 在 RedisURI 中显式设置 commandTimeout
RedisURI uri = RedisURI.Builder.redis("127.0.0.1", 6379)
    .withTimeout(Duration.ofMillis(500))  // 命令超时 500ms
    .build();
RedisClient client = RedisClient.create(uri);
StatefulRedisConnection<String, String> connection = client.connect();
connection.sync().get("key");  // 最多阻塞 500ms
```

```java
// 通过 setDefaultCommandTimeout 设置全局命令超时
RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
client.setDefaultCommandTimeout(Duration.ofMillis(500));
StatefulRedisConnection<String, String> connection = client.connect();
connection.sync().get("key");  // 全局超时 500ms
```

```yaml
# application.yml - Spring Boot 配置超时
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    timeout: 500ms  # 命令超时 500ms
```

```java
// 单条命令自定义超时（覆盖全局设置）
RedisURI uri = RedisURI.Builder.redis("127.0.0.1", 6379)
    .withTimeout(Duration.ofMillis(500))
    .build();
RedisClient client = RedisClient.create(uri);
client.setDefaultCommandTimeout(Duration.ofMillis(500));

StatefulRedisConnection<String, String> connection = client.connect();
// 普通命令使用全局超时
connection.sync().get("key");

// 特殊命令使用自定义超时
RedisCommand<String, String, String> command = new Command<>(
    CommandType.GET, null, new StatusOutput<>(StringCodec.UTF8)
);
connection.dispatch(command);  // 可配合自定义超时控制
```
