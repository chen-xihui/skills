# JEDIS-003：禁止循环内创建连接

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-003 |
| 风险等级 | 严重 |
| 规则描述 | 禁止在循环中创建 RedisClient、RedisClusterClient、JedisPool、RedissonClient 等连接资源 |

## 问题说明

在循环内反复创建 Jedis 连接、JedisPool 连接池或 RedissonClient 实例，会导致连接风暴：短时间内大量 TCP 连接建立与销毁，产生大量 TIME_WAIT 状态连接，最终耗尽文件描述符（FD）和可用端口。同时，频繁的 TCP 三次握手和连接初始化（AUTH、SELECT 等）会严重拖慢业务响应时间，并可能触发 Redis 服务端的客户端连接数限制。

## 检查方法

- 静态分析：检查 for/while 循环体内是否存在 `new Jedis()`、`pool.getResource()`、`new JedisPool()`、`new RedissonClient()` 等调用
- 脚本化检查：`python scripts/check_jedis_003.py <项目根目录>`

## 违规示例

```java
// 循环内每次迭代获取新连接，连接风暴
public Map<String, String> batchGet(List<String> keys) {
    Map<String, String> result = new HashMap<>();
    for (String key : keys) {
        Jedis jedis = pool.getResource();  // 每次循环获取新连接
        try {
            result.put(key, jedis.get(key));
        } finally {
            jedis.close();
        }
    }
    return result;
}
```

```java
// 循环内创建 JedisPool，极其危险
public void migrateData(List<String> hostPorts, String key, String value) {
    for (String hostPort : hostPorts) {
        String[] parts = hostPort.split(":");
        JedisPool pool = new JedisPool(parts[0], Integer.parseInt(parts[1]));
        try (Jedis jedis = pool.getResource()) {
            jedis.set(key, value);
        }
        pool.close();
    }
}
```

```java
// 循环内 new Jedis 直连，无连接池管理
public void publishMessages(List<String> channels, String message) {
    for (String channel : channels) {
        Jedis jedis = new Jedis("127.0.0.1", 6379);  // 每次循环新建直连
        jedis.publish(channel, message);
        jedis.close();
    }
}
```

## 合规示例

```java
// 在循环外获取连接，循环内复用
public Map<String, String> batchGet(List<String> keys) {
    Map<String, String> result = new HashMap<>();
    try (Jedis jedis = pool.getResource()) {
        for (String key : keys) {
            result.put(key, jedis.get(key));
        }
    }
    return result;
}
```

```java
// 使用 Pipeline 批量操作，减少网络往返
public Map<String, String> batchGet(List<String> keys) {
    Map<String, String> result = new HashMap<>();
    try (Jedis jedis = pool.getResource()) {
        Pipeline pipeline = jedis.pipelined();
        for (String key : keys) {
            pipeline.get(key);
        }
        List<Object> responses = pipeline.syncAndReturnAll();
        for (int i = 0; i < keys.size(); i++) {
            result.put(keys.get(i), (String) responses.get(i));
        }
    }
    return result;
}
```

```java
// 连接池作为单例 Bean 全局复用，不在循环中创建
@Configuration
public class RedisConfig {
    @Bean
    public JedisPool jedisPool() {
        JedisPoolConfig config = new JedisPoolConfig();
        config.setMaxTotal(100);
        config.setMaxIdle(50);
        config.setMinIdle(10);
        config.setMaxWaitMillis(3000);
        return new JedisPool(config, "127.0.0.1", 6379, 3000, "password");
    }
}
```
