# JEDIS-010：必须限制重试次数

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-010 |
| 风险等级 | 风险 |
| 规则描述 | 禁止无限重试，防止 Redis 故障时应用雪崩放大、自旋风暴 |

## 问题说明

当 Redis 发生故障时，无限重试（如 while(true) 或极大的重试次数）会导致：1）应用线程被阻塞在重试循环中，线程池迅速耗尽；2）大量请求不断重试，对 Redis 产生持续冲击，阻碍其恢复；3）级联效应导致依赖该服务的上游系统也发生超时，形成雪崩。合理的做法是根据读写场景设置有限重试次数，并配合退避策略。

## 检查方法

- 静态分析：检查是否存在 `while(true)` / `while(!success)` 包裹 Redis 操作
- 检查重试循环是否缺少最大次数限制
- 检查 @Retryable 注解的 maxAttempts 是否过大
- 脚本化检查：`python scripts/check_jedis_010.py <项目根目录>`

## 违规示例

```java
// 无限重试，Redis 故障时线程永远阻塞
while (true) {
    try {
        String value = jedis.get("user:1001");
        return value;
    } catch (JedisConnectionException e) {
        // 无限重试，永不放弃
        continue;
    }
}
```

```java
// 重试次数过大且无退避，自旋风暴
int retries = 100;
for (int i = 0; i < retries; i++) {
    try {
        jedis.set("order:123", orderData);
        break;
    } catch (JedisConnectionException e) {
        // 写请求重试 100 次，放大故障
    }
}
```

```java
// @Retryable 无限重试（默认策略可能过大）
@Retryable(maxAttempts = Integer.MAX_VALUE)
public String getValue(String key) {
    return jedis.get(key);
}
```

## 合规示例

```java
// 读请求：有限重试 + 退避策略
private static final int READ_MAX_RETRIES = 2;
private static final long RETRY_INTERVAL_MS = 50;

public String safeGet(String key) {
    for (int i = 0; i < READ_MAX_RETRIES; i++) {
        try {
            return jedis.get(key);
        } catch (JedisConnectionException e) {
            if (i == READ_MAX_RETRIES - 1) {
                log.error("Redis 读取失败, key={}", key, e);
                throw e;
            }
            try {
                Thread.sleep(RETRY_INTERVAL_MS * (i + 1));  // 退避
            } catch (InterruptedException ie) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("重试被中断", ie);
            }
        }
    }
    throw new JedisConnectionException("Redis 读取重试耗尽");
}
```

```java
// 写请求：不重试或最多重试 1 次，避免重复写入
public void safeSet(String key, String value) {
    try {
        jedis.set(key, value);
    } catch (JedisConnectionException e) {
        log.error("Redis 写入失败, key={}", key, e);
        throw e;  // 写请求直接失败，由调用方决定是否补偿
    }
}
```

```java
// MQ 消费场景：幂等消费后可重试
@Retryable(maxAttempts = 3, backoff = @Backoff(delay = 100, multiplier = 2))
public void processMessage(String messageId, String key, String value) {
    // 先做幂等检查，确认未处理过
    String existing = jedis.get("processed:" + messageId);
    if (existing != null) {
        log.info("消息已处理, messageId={}", messageId);
        return;
    }
    jedis.set(key, value);
    jedis.setex("processed:" + messageId, 86400, "1");  // 标记已处理
}
```
