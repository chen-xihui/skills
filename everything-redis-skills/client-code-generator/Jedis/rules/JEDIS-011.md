# JEDIS-011：Cluster 模式下禁止业务层二次重试

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-011 |
| 风险等级 | 风险 |
| 规则描述 | Redis Cluster 客户端已有 MOVED/ASK 重试机制，业务禁止再次重试，防止指数级放大故障 |

## 问题说明

JedisCluster 内置了 MOVED/ASK 自动重定向重试机制，当槽位迁移或节点故障时客户端会自动重试。若业务层再额外包装重试逻辑，故障期间请求量将呈指数级放大：客户端 maxAttempts × 业务重试次数 = 总放大倍数。例如 maxAttempts=5 加上业务重试 10 次，故障请求被放大 50 倍，极易导致雪崩。

## 检查方法

- 静态分析：检查 Cluster 模式下是否存在 for/while 循环包裹 jedisCluster 操作
- 检查是否存在 @Retryable、RetryTemplate 等重试框架包裹 JedisCluster 操作
- 检查 Spring Boot 中是否对 redis cluster 配置了过大的 max-attempts 并同时存在业务重试
- 脚本化检查：`python scripts/check_jedis_011.py <项目根目录>`

## 违规示例

```java
// 业务层二次重试，放大 5×10=50 倍
for (int i = 0; i < 10; i++) {
    try {
        jedisCluster.get("user:1001");
        break;
    } catch (Exception e) {
        log.warn("重试第 {} 次", i + 1);
    }
}
```

```java
// @Retryable 包裹 JedisCluster 操作，客户端内置 5 次重试 × 业务 5 次 = 25 倍放大
@Retryable(value = JedisConnectionException.class, maxAttempts = 5)
public String getValue(String key) {
    return jedisCluster.get(key);
}
```

```java
// RetryTemplate 包裹 Cluster 操作
public String getValueWithRetry(String key) {
    RetryTemplate template = RetryTemplate.builder()
            .maxAttempts(5)
            .exponentialBackoff(100, 2.0, 5000)
            .build();
    return template.execute(ctx -> jedisCluster.get(key));
}
```

## 合规示例

```java
// 依赖 JedisCluster 内置重试，不额外包装
Set<HostAndPort> nodes = new HashSet<>();
nodes.add(new HostAndPort("127.0.0.1", 7001));
nodes.add(new HostAndPort("127.0.0.1", 7002));
nodes.add(new HostAndPort("127.0.0.1", 7003));
JedisCluster cluster = new JedisCluster(nodes, 2000, 3, poolConfig);
//                                                              ^^ maxAttempts=3 合理

// 直接调用，由客户端处理 MOVED/ASK 重试
String value = cluster.get("user:1001");
```

```java
// 仅对非 Cluster 重试类异常做有限重试（如业务超时），区分异常类型
public String safeGet(String key) {
    try {
        return jedisCluster.get(key);
    } catch (JedisClusterMaxAttemptsException e) {
        // 客户端已耗尽重试，不再重试
        log.error("Cluster 重试耗尽, key={}", key, e);
        throw e;
    } catch (JedisConnectionException e) {
        // 连接异常已由客户端内置重试处理，不再重试
        log.error("Cluster 连接异常, key={}", key, e);
        throw e;
    } catch (JedisDataException e) {
        // 数据异常（如命令错误），无需重试
        throw e;
    }
}
```

```yaml
# application.yml - 合理配置 maxAttempts，不在业务层重试
spring:
  redis:
    cluster:
      nodes: 127.0.0.1:7001,127.0.0.1:7002,127.0.0.1:7003
      max-attempts: 3  # 客户端内置重试 3 次，无需业务层重试
```
