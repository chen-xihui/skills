# JEDIS-014：SCRIPT LOAD 必须复用 SHA

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-014 |
| 风险等级 | 提示 |
| 规则描述 | Lua 脚本禁止每次 eval() 传输完整脚本，必须先 SCRIPT LOAD 获取 SHA 后使用 EVALSHA 调用 |

## 问题说明

每次调用 `eval()` 都会将完整的 Lua 脚本内容通过网络传输给 Redis 服务端，Redis 再对脚本进行解析和缓存。对于频繁执行的脚本（如限流、分布式锁、原子扣减等），重复传输完整脚本带来不必要的网络开销和 Redis CPU 解析开销。正确做法是：首次使用 SCRIPT LOAD 将脚本加载到 Redis 并获取 SHA 摘要，后续使用 EVALSHA + SHA 调用，仅传输几十字节的 SHA 而非数千字节的脚本内容。若 EVALSHA 返回 NOSCRIPT 错误，再重新 LOAD 并重试。

## 检查方法

- 静态分析：检查代码中是否存在循环或高频调用路径中使用 `eval()` 传递完整脚本字符串
- 检查是否使用 `evalsha()` 替代 `eval()`，并具备 NOSCRIPT 降级逻辑
- 脚本化检查：`python scripts/check_jedis_014.py <项目根目录>`

## 违规示例

```java
// 每次请求都传输完整 Lua 脚本，浪费网络带宽
public boolean acquireRateLimit(String key, int limit, int window) {
    String script =
        "local current = redis.call('GET', KEYS[1]) " +
        "if current and tonumber(current) >= tonumber(ARGV[1]) then " +
        "  return 0 " +
        "end " +
        "current = redis.call('INCR', KEYS[1]) " +
        "if tonumber(current) == 1 then " +
        "  redis.call('EXPIRE', KEYS[1], ARGV[2]) " +
        "end " +
        "return 1";
    // 每次都传输完整脚本
    Object result = jedis.eval(script, 1, key, String.valueOf(limit), String.valueOf(window));
    return Long.valueOf(1).equals(result);
}
```

```java
// 在循环中使用 eval 传输完整脚本
public void batchDeduct(List<String> keys, int amount) {
    String script = "local balance = redis.call('GET', KEYS[1]) " +
        "if not balance or tonumber(balance) < tonumber(ARGV[1]) then " +
        "  return -1 " +
        "end " +
        "redis.call('DECRBY', KEYS[1], ARGV[1]) " +
        "return redis.call('GET', KEYS[1])";
    for (String key : keys) {
        jedis.eval(script, 1, key, String.valueOf(amount));  // 每次循环都传输完整脚本
    }
}
```

## 合规示例

```java
// 首次 SCRIPT LOAD 获取 SHA，后续 EVALSHA 调用
public class RateLimitScript {
    private static final String SCRIPT =
        "local current = redis.call('GET', KEYS[1]) " +
        "if current and tonumber(current) >= tonumber(ARGV[1]) then " +
        "  return 0 " +
        "end " +
        "current = redis.call('INCR', KEYS[1]) " +
        "if tonumber(current) == 1 then " +
        "  redis.call('EXPIRE', KEYS[1], ARGV[2]) " +
        "end " +
        "return 1";

    private volatile String sha;

    public boolean acquireRateLimit(Jedis jedis, String key, int limit, int window) {
        if (sha == null) {
            sha = jedis.scriptLoad(SCRIPT);
        }
        try {
            Object result = jedis.evalsha(sha, 1, key, String.valueOf(limit), String.valueOf(window));
            return Long.valueOf(1).equals(result);
        } catch (JedisNoScriptException e) {
            // SHA 已被 Redis 清除（如 FLUSHALL/重启），重新 LOAD
            sha = jedis.scriptLoad(SCRIPT);
            Object result = jedis.evalsha(sha, 1, key, String.valueOf(limit), String.valueOf(window));
            return Long.valueOf(1).equals(result);
        }
    }
}
```

```java
// 批量扣减使用 EVALSHA + NOSCRIPT 降级
public class DeductScript {
    private static final String SCRIPT =
        "local balance = redis.call('GET', KEYS[1]) " +
        "if not balance or tonumber(balance) < tonumber(ARGV[1]) then " +
        "  return -1 " +
        "end " +
        "redis.call('DECRBY', KEYS[1], ARGV[1]) " +
        "return redis.call('GET', KEYS[1])";

    private volatile String sha;

    public void batchDeduct(Jedis jedis, List<String> keys, int amount) {
        if (sha == null) {
            sha = jedis.scriptLoad(SCRIPT);
        }
        for (String key : keys) {
            try {
                jedis.evalsha(sha, 1, key, String.valueOf(amount));
            } catch (JedisNoScriptException e) {
                sha = jedis.scriptLoad(SCRIPT);
                jedis.evalsha(sha, 1, key, String.valueOf(amount));
            }
        }
    }
}
```

```java
// Spring Data Redis 使用 DefaultRedisScript 自动管理 SHA
@Configuration
public class RedisScriptConfig {
    @Bean
    public DefaultRedisScript<Long> rateLimitScript() {
        DefaultRedisScript<Long> script = new DefaultRedisScript<>();
        script.setScriptText(
            "local current = redis.call('GET', KEYS[1]) " +
            "if current and tonumber(current) >= tonumber(ARGV[1]) then return 0 end " +
            "current = redis.call('INCR', KEYS[1]) " +
            "if tonumber(current) == 1 then redis.call('EXPIRE', KEYS[1], ARGV[2]) end " +
            "return 1"
        );
        script.setResultType(Long.class);
        return script;
        // RedisTemplate.execute(RedisScript) 内部自动 SCRIPT LOAD + EVALSHA
    }
}
```
