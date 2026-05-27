# JEDIS-002：禁止使用连接池后未释放连接

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-002 |
| 风险等级 | 严重 |
| 规则描述 | getResource() 获取的连接必须显式释放，防止连接泄漏 |

## 问题说明

通过 `JedisPool.getResource()` 获取的连接在使用完毕后必须归还连接池。若未显式关闭，连接将一直被占用不会归还池中，导致连接池中可用连接逐渐减少。当所有连接都被泄漏后，新请求将因 `Could not get a resource from the pool` 而失败，造成服务不可用。此问题在异常路径中尤为常见——当方法中途抛出异常时跳过了 close 调用。

## 检查方法

- 静态分析：检查 `pool.getResource()` 调用是否被 try-with-resources 包裹或在 finally 块中调用 `close()`
- 脚本化检查：`python scripts/check_jedis_002.py <项目根目录>`

## 违规示例

```java
// 获取连接后未释放，连接泄漏
public String getValue(String key) {
    Jedis jedis = pool.getResource();
    String value = jedis.get(key);
    return value;
    // jedis 未关闭，连接泄漏
}
```

```java
// 异常路径未释放连接
public void setValue(String key, String value) {
    Jedis jedis = pool.getResource();
    jedis.set(key, value);  // 若此处抛出 JedisConnectionException
    jedis.close();          // 此行不会执行，连接泄漏
}
```

```java
// 手动 try-finally 但遗漏 close
public Long incr(String key) {
    Jedis jedis = pool.getResource();
    try {
        return jedis.incr(key);
    } catch (Exception e) {
        log.error("Redis incr failed", e);
        throw new RuntimeException(e);
        // 异常后未调用 jedis.close()
    }
}
```

## 合规示例

```java
// 使用 try-with-resources 自动释放连接（推荐）
public String getValue(String key) {
    try (Jedis jedis = pool.getResource()) {
        return jedis.get(key);
    }
}
```

```java
// 异常路径也安全：try-with-resources 保证 close
public void setValue(String key, String value) {
    try (Jedis jedis = pool.getResource()) {
        jedis.set(key, value);
    } catch (Exception e) {
        log.error("Redis set failed, key={}", key, e);
        throw new RuntimeException(e);
        // jedis 已在 try-with-resources 中自动关闭
    }
}
```

```java
// 传统 try-finally 确保释放（兼容 Java 6）
public Long incr(String key) {
    Jedis jedis = null;
    try {
        jedis = pool.getResource();
        return jedis.incr(key);
    } catch (Exception e) {
        log.error("Redis incr failed, key={}", key, e);
        throw new RuntimeException(e);
    } finally {
        if (jedis != null) {
            jedis.close();
        }
    }
}
```
