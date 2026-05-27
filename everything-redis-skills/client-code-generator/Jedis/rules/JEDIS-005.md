# JEDIS-005：禁止事务异常后未 Discard

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-005 |
| 风险等级 | 严重 |
| 规则描述 | MULTI/EXEC 异常后必须调用 discard() 清理连接状态 |

## 问题说明

Jedis 事务通过 `MULTI` 开启，`EXEC` 提交。若事务执行过程中发生异常且未调用 `discard()`，该连接仍处于 MULTI 状态。当该连接被归还连接池后再次使用时，执行任何命令都会返回 `ERR MULTI calls can not be nested`，导致该连接被污染，后续所有操作均失败。这种连接污染会随时间扩散，影响整个连接池的可用性。

## 检查方法

- 静态分析：检查 `jedis.multi()` 调用后，异常处理路径中是否包含 `jedis.discard()` 或 `tx.discard()`
- 脚本化检查：`python scripts/check_jedis_005.py <项目根目录>`

## 违规示例

```java
// 事务异常后未 discard，连接被污染
public boolean transferPoints(String fromKey, String toKey, int points) {
    Transaction tx = jedis.multi();
    tx.decrBy(fromKey, points);
    tx.incrBy(toKey, points);
    tx.exec();
    // 若 exec() 抛出异常（如连接中断），tx 未 discard
    // 该连接归还池后仍处于 MULTI 状态，后续使用报错
    return true;
}
```

```java
// catch 块中未调用 discard
public void updateInventory(String itemId, int delta) {
    try {
        Transaction tx = jedis.multi();
        tx.hincrBy("inventory:" + itemId, "stock", delta);
        tx.hincrBy("inventory:" + itemId, "version", 1);
        tx.exec();
    } catch (Exception e) {
        log.error("Inventory update failed", e);
        // 未调用 jedis.discard()，连接处于 MULTI 状态
        throw new RuntimeException(e);
    }
}
```

```java
// 使用 Transaction 对象但未处理其异常
public void batchUpdate(Map<String, String> updates) {
    Transaction tx = jedis.multi();
    for (Map.Entry<String, String> entry : updates.entrySet()) {
        tx.set(entry.getKey(), entry.getValue());
    }
    // 若中间某次操作抛异常，事务未清理
    List<Object> results = tx.exec();
    if (results == null) {
        // EXEC 返回 null 表示事务被拒绝，但未调用 discard
        log.warn("Transaction rejected");
    }
}
```

## 合规示例

```java
// 异常路径调用 discard() 清理连接状态
public boolean transferPoints(String fromKey, String toKey, int points) {
    try {
        Transaction tx = jedis.multi();
        tx.decrBy(fromKey, points);
        tx.incrBy(toKey, points);
        List<Object> results = tx.exec();
        return results != null;
    } catch (Exception e) {
        jedis.discard();  // 清理 MULTI 状态，防止连接污染
        log.error("Points transfer failed", e);
        throw new RuntimeException(e);
    }
}
```

```java
// 使用 Spring Data Redis 的事务回调，框架自动处理 discard
@Autowired
private RedisTemplate<String, Object> redisTemplate;

public void updateInventory(String itemId, int delta) {
    redisTemplate.execute(new SessionCallback<Object>() {
        @Override
        public Object execute(RedisOperations operations) throws DataAccessException {
            operations.multi();
            operations.opsForHash().increment("inventory:" + itemId, "stock", delta);
            operations.opsForHash().increment("inventory:" + itemId, "version", 1);
            return operations.exec();  // Spring 自动处理 discard
        }
    });
}
```

```java
// 完整的事务安全模板：try-with-resources + discard 保底
public void batchUpdate(Map<String, String> updates) {
    try (Jedis jedis = pool.getResource()) {
        Transaction tx = jedis.multi();
        try {
            for (Map.Entry<String, String> entry : updates.entrySet()) {
                tx.set(entry.getKey(), entry.getValue());
            }
            List<Object> results = tx.exec();
            if (results == null) {
                log.warn("Transaction rejected by Redis");
            }
        } catch (Exception e) {
            try {
                tx.discard();  // 确保清理 MULTI 状态
            } catch (Exception discardEx) {
                log.warn("Discard failed", discardEx);
            }
            throw e;
        }
    }
}
```
