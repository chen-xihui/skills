# JEDIS-001：禁止使用 KEYS 命令

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-001 |
| 风险等级 | 严重 |
| 规则描述 | KEYS 命令会阻塞 Redis 主线程，在大数据集下导致服务不可用 |

## 问题说明

KEYS 命令时间复杂度为 O(N)，会遍历 Redis 中所有键。当键数量达到百万级别时，KEYS 命令可能阻塞主线程数秒之久，期间所有其他客户端请求均被阻塞，导致 Redis 服务不可用，引发生产事故。此问题在 Redis 单线程模型下尤为严重，即使只执行一次也可能造成全局影响。

## 检查方法

- 静态分析：搜索 `.keys(` 调用，禁止使用 `redisTemplate.keys()`、`jedis.keys()`、`sync.keys()` 等 KEYS 命令变体
- 脚本化检查：`python scripts/check_jedis_001.py <项目根目录>`

## 违规示例

```java
// Spring Data Redis 使用 KEYS
@Autowired
private RedisTemplate<String, String> redisTemplate;

public Set<String> findKeysByPattern(String pattern) {
    return redisTemplate.keys(pattern);  // 阻塞主线程，O(N) 遍历
}
```

```java
// Jedis 直接使用 KEYS
public Set<String> getUserSessionKeys(String userId) {
    Jedis jedis = pool.getResource();
    try {
        return jedis.keys("session:" + userId + "*");  // 全量扫描，危险
    } finally {
        jedis.close();
    }
}
```

```java
// Lettuce 同步模式使用 KEYS
public Set<String> scanAllKeys() {
    RedisCommands<String, String> sync = connection.sync();
    return sync.keys("*");  // 遍历所有键，生产环境绝对禁止
}
```

## 合规示例

```java
// Spring Data Redis 使用 SCAN
@Autowired
private RedisTemplate<String, String> redisTemplate;

public Set<String> findKeysByPattern(String pattern) {
    Set<String> keys = new HashSet<>();
    ScanOptions scanOptions = ScanOptions.scanOptions()
            .match(pattern)
            .count(100)   // 每次 SCAN 建议 COUNT=100
            .build();
    Cursor<String> cursor = redisTemplate.scan(scanOptions);
    while (cursor.hasNext()) {
        keys.add(cursor.next());
        // 限制结果集大小，防止内存溢出
        if (keys.size() >= 1000) {
            break;
        }
    }
    return keys;
}
```

```java
// Jedis 使用 SCAN 替代 KEYS
public Set<String> getUserSessionKeys(String userId) {
    Set<String> keys = new HashSet<>();
    try (Jedis jedis = pool.getResource()) {
        String cursor = "0";
        ScanParams scanParams = new ScanParams()
                .match("session:" + userId + "*")
                .count(100);
        do {
            ScanResult<String> scanResult = jedis.scan(cursor, scanParams);
            keys.addAll(scanResult.getResult());
            cursor = scanResult.getCursor();
            // 限制结果集大小
            if (keys.size() >= 1000) {
                break;
            }
        } while (!"0".equals(cursor));
    }
    return keys;
}
```

```java
// Lettuce 使用 SCAN 替代 KEYS
public Set<String> scanAllKeys() {
    Set<String> keys = new HashSet<>();
    RedisCommands<String, String> sync = connection.sync();
    KeyScanCursor<String> cursor = sync.scan(ScanArgs.Builder.limit(100));
    while (cursor != null) {
        keys.addAll(cursor.getKeys());
        if (keys.size() >= 1000 || cursor.isFinished()) {
            break;
        }
        cursor = sync.scan(cursor);
    }
    return keys;
}
```
