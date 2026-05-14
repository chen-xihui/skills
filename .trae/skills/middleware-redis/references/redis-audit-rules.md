# Redis 代码优化检查规则详细说明

本文件包含 REDIS-001 ~ REDIS-008 共 8 条检查规则的详细说明和检查方法。

---

## REDIS-001：禁止在循环中使用 keys *

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-001 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 禁止在循环中使用 `keys *`，应使用 `scan` |

### 问题说明

`keys *` 命令会遍历 Redis 中所有 Key，时间复杂度 O(N)，在 Key 数量多时会导致 Redis 阻塞，影响所有客户端请求。应使用 `scan` 命令增量遍历。

### 检查方法

1. 搜索循环体内的 `keys(` 调用
2. 搜索 `KEYS *` 命令
3. 即使不在循环中，生产环境也不建议使用 `keys *`

搜索模式：
- `grep_code` 搜索 `keys(`、`.keys(`
- `search_codebase` 搜索 "keys *" 相关代码

### 违规示例

```java
// ❌ 循环中使用 keys
Set<String> keys = redisTemplate.keys("user:*");
for (String key : keys) {
    // 处理每个 key...
}
```

### 合规示例

```java
// ✅ 使用 scan 替代 keys
Set<String> keys = new HashSet<>();
ScanOptions options = ScanOptions.scanOptions().match("user:*").count(100).build();
try (var cursor = redisTemplate.scan(options)) {
    while (cursor.hasNext()) {
        keys.add(cursor.next());
    }
}
```

---

## REDIS-002：大 Key 风险检查

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-002 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 大 Key 风险检查（单次操作 Value 超过 10KB 应拆分或压缩） |

### 问题说明

大 Key（Value 超过 10KB）会导致 Redis 在读写时阻塞较长时间，影响其他请求。常见场景：将大对象序列化后存入 Redis。

### 检查方法

1. 搜索大字符串直接 `set` 或大对象序列化写入
2. 搜索 `JSON.toJSONString` + `set` 组合
3. 搜索 `ObjectMapper.writeValueAsString` + Redis 操作

搜索模式：
- `grep_code` 搜索序列化操作后紧跟 Redis 写入

### 违规示例

```java
// ❌ 大对象直接写入 Redis
String json = objectMapper.writeValueAsString(largeOrderList); // 可能几十MB
redisTemplate.opsForValue().set("orders:all", json);
```

### 合规示例

```java
// ✅ 拆分为小 Key 或使用 Hash 分片
for (Order order : largeOrderList) {
    String key = "order:" + order.getId();
    redisTemplate.opsForValue().set(key, objectMapper.writeValueAsString(order), 1, TimeUnit.HOURS);
}
```

---

## REDIS-003：热 Key 风险检查

| 属性 | 说明 |
|------|------|
| 风险等级 | 🟡 警告 |
| 规则ID | REDIS-003 |
| 规则描述 | 热 Key 风险检查（高频读写的 Key 应考虑本地缓存） |

### 问题说明

热 Key（高频读写的 Key）可能导致单个 Redis 节点压力过大。建议使用本地缓存（如 Caffeine）缓存热 Key 数据，减少 Redis 访问频率。

### 检查方法

1. 分析代码中高频调用的 Redis 操作模式
2. 搜索循环中或高频方法中的 `get` 调用
3. 检查是否有本地缓存机制

搜索模式：
- `grep_code` 搜索高频方法中的 `redisTemplate.opsForValue().get`
- `search_codebase` 搜索 Redis 操作与本地缓存（Caffeine/Guava Cache）的组合

### 违规示例

```java
// ❌ 每次请求都访问 Redis
public User getUser(String userId) {
    return (User) redisTemplate.opsForValue().get("user:" + userId);
}
```

### 合规示例

```java
// ✅ 使用本地缓存 + Redis 二级缓存
@Cacheable(value = "localCache", key = "'user:' + #userId")
public User getUser(String userId) {
    return (User) redisTemplate.opsForValue().get("user:" + userId);
}
```

---

## REDIS-004：连接池参数合理性

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-004 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 连接池参数合理性（maxTotal、maxIdle、maxWaitMillis） |

### 问题说明

连接池参数设置不合理会导致连接泄漏或资源浪费。使用默认值时可能导致高并发下连接不足。

### 检查方法

1. 搜索 `maxTotal`、`maxIdle`、`maxWaitMillis` 配置
2. 搜索 `max-active`、`max-idle`、`max-wait` YAML 配置
3. 检查是否使用 Spring Boot 默认值（通常偏小）

搜索模式：
- `grep_code` 搜索 `max-active`、`max-idle`、`max-wait`、`maxTotal`、`maxIdle`
- 检查连接池配置是否存在且合理

推荐值：
- max-active：20-50（根据并发量调整）
- max-idle：10-20
- min-idle：5-10
- max-wait：3000ms

---

## REDIS-005：Pipeline 批量使用情况

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-005 |
| 风险等级 | 🔵 建议 |
| 规则描述 | Pipeline 批量使用情况（多次独立命令应使用 Pipeline） |

### 问题说明

多次独立的 Redis 命令逐条发送会产生多次网络往返，效率低。使用 Pipeline 可以将多个命令打包发送，减少网络延迟。

### 检查方法

1. 搜索连续的 Redis 命令调用
2. 检查是否使用 `pipeline()` 或 `executePipelined`
3. 关注循环中的 Redis 操作

搜索模式：
- `grep_code` 搜索循环中的 `redisTemplate.opsForValue().set` 连续调用
- `search_codebase` 搜索 "pipeline" 相关代码

### 违规示例

```java
// ❌ 逐条执行
for (Map.Entry<String, String> entry : dataMap.entrySet()) {
    redisTemplate.opsForValue().set(entry.getKey(), entry.getValue());
}
```

### 合规示例

```java
// ✅ 使用 Pipeline
redisTemplate.executePipelined((connection) -> {
    for (Map.Entry<String, String> entry : dataMap.entrySet()) {
        connection.set(
            entry.getKey().getBytes(),
            entry.getValue().getBytes()
        );
    }
    return null;
});
```

---

## REDIS-006：Lua 脚本是否使用 EVALSHA

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-006 |
| 风险等级 | 🔵 建议 |
| 规则描述 | Lua 脚本是否使用 EVALSHA 预加载（而非每次 EVAL） |

### 问题说明

每次使用 `EVAL` 都会发送完整脚本内容到 Redis，浪费网络带宽。应先使用 `SCRIPT LOAD` 预加载脚本，后续使用 `EVALSHA` 仅发送脚本 SHA1 值。

### 检查方法

1. 搜索 `eval` 调用
2. 检查是否有对应的 `scriptLoad` 或 `SCRIPT LOAD`
3. 搜索 `DefaultRedisScript` 是否缓存了 SHA

搜索模式：
- `grep_code` 搜索 `eval(`、`EVAL`、`execute(RedisScript)`
- `search_codebase` 搜索 "script" + "redis" 相关代码

### 违规示例

```java
// ❌ 每次都发送完整脚本
String script = "local current = redis.call('GET', KEYS[1]) ...";
redisTemplate.execute(new DefaultRedisScript<>(script, Long.class), keys, args);
```

### 合规示例

```java
// ✅ 预加载脚本，使用 EVALSHA
DefaultRedisScript<Long> redisScript = new DefaultRedisScript<>();
redisScript.setScriptText("local current = redis.call('GET', KEYS[1]) ...");
redisScript.setResultType(Long.class);
// DefaultRedisScript 会自动缓存 SHA，后续调用使用 EVALSHA
redisTemplate.execute(redisScript, keys, args);
```

---

## REDIS-007：是否设置合理的过期时间

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-007 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 是否设置合理的过期时间（避免 Key 永不过期导致内存泄漏） |

### 问题说明

Key 不设置过期时间会导致内存持续增长，最终可能触发 maxmemory 策略或 OOM。

### 检查方法

1. 搜索 `set` 或 `setex` 调用，检查是否有过期时间
2. 搜索 `set(key, value)` 两个参数的调用（未设置过期时间）
3. 排除确实需要永久存在的 Key（如配置类数据）

搜索模式：
- `grep_code` 搜索 `\.set\(` 调用，检查是否有过期时间参数
- `search_codebase` 搜索 "set" + "expire" 相关代码

### 违规示例

```java
// ❌ 未设置过期时间
redisTemplate.opsForValue().set("session:" + sessionId, userData);
```

### 合规示例

```java
// ✅ 设置过期时间
redisTemplate.opsForValue().set("session:" + sessionId, userData, 30, TimeUnit.MINUTES);
```

---

## REDIS-008：密码是否硬编码

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-008 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 密码是否硬编码 |

### 问题说明

将 Redis 密码硬编码在源码中存在严重安全隐患。应通过环境变量或密钥管理系统注入。

### 检查方法

1. 搜索源码中 `password` 字段的直接赋值
2. 排除配置文件中的 `${...}` 占位符形式
3. 搜索 `JedisPool`、`RedisStandaloneConfiguration` 中的硬编码密码

搜索模式：
- `grep_code` 搜索 `.java` 文件中的 `password\s*=\s*"[^${]`
- 排除 `@Value("${...}")` 形式

### 违规示例

```java
// ❌ 密码硬编码
JedisPool pool = new JedisPool(config, host, port, timeout, "MyRedisPassword123");
```

### 合规示例

```java
// ✅ 密码通过配置注入
@Value("${spring.data.redis.password}")
private String password;

// application.yml 中：
// password: ${REDIS_PASSWORD}
```
