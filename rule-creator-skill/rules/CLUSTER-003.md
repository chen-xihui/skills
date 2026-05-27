# CLUSTER-003：Cluster 禁止业务层二次重试

| 属性 | 说明 |
|------|------|
| 规则ID | CLUSTER-003 |
| 风险等级 | 风险 |
| 规则描述 | Redis Cluster 客户端已有 MOVED/ASK 自动重试机制，业务层禁止再次包装重试逻辑 |

## 问题说明

Redis Cluster 客户端（JedisCluster、Lettuce）内置了 MOVED/ASK 重定向重试机制。若业务层再额外包装重试循环，故障期间请求量呈指数级放大：客户端重试 N 次 × 业务重试 M 次 = N×M 倍放大，极易引发雪崩。

## 检查方法

- 静态分析：检查 Cluster 模式下是否存在 for/while 循环包裹 jedisCluster/RedisClusterClient 调用
- 检查是否存在 @Retryable、RetryTemplate 等重试框架包裹 Cluster 操作
- 脚本化检查：`python scripts/check_cluster_003.py <项目根目录>`

## 违规示例

```java
// 业务层二次重试，指数级放大故障
for (int i = 0; i < 5; i++) {
    try {
        jedisCluster.get(key);
        break;
    } catch (Exception e) {
        // 重试
    }
}
```

```java
// 使用 Spring Retry 包裹 Cluster 操作
@Retryable(maxAttempts = 5)
public String getValue(String key) {
    return jedisCluster.get(key);  // 客户端已内置重试，再加重试放大 3×5=15 倍
}
```

## 合规示例

```java
// 依赖 JedisCluster 内置重试，不额外包装
String value = jedisCluster.get(key);
```

```java
// 仅对非 Cluster 类异常（如业务超时）做有限重试，且限制总重试次数
try {
    String value = jedisCluster.get(key);
} catch (JedisConnectionException e) {
    // 连接异常由客户端内置重试处理，不再重试
    log.error("Redis 连接异常", e);
    throw e;
}
```
