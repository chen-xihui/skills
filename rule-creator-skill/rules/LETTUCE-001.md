# LETTUCE-001：禁止阻塞命令复用普通连接池

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-001 |
| 风险等级 | 严重 |
| 规则描述 | BLPOP、SUBSCRIBE、XREAD BLOCK 等阻塞命令必须使用独立连接，不允许共享普通连接池 |

## 问题说明

Lettuce 基于单个共享连接（shareNativeConnection）处理所有命令。当 BLPOP、BRPOP、SUBSCRIBE、XREAD BLOCK 等阻塞命令占用该连接时，连接会长时间处于等待状态，导致其他请求无法获取连接。若连接池中所有连接均被阻塞命令占用，将造成连接池耗尽，整个应用的 Redis 访问不可用，引发级联故障。

## 检查方法

- 静态分析：检查阻塞命令（blpop、brpop、subscribe、xread block）是否通过普通连接池的 sync()/reactive() 调用，而非独立连接
- 检查是否存在 StatefulRedisConnection 复用场景下同时执行阻塞命令与普通命令
- 脚本化检查：`python scripts/check_lettuce_001.py <项目根目录>`

## 违规示例

```java
// 在共享连接上执行阻塞命令，连接被长期占用导致池耗尽
RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
StatefulRedisConnection<String, String> connection = client.connect();

// 普通业务请求
connection.sync().set("user:1001", "Alice");

// 阻塞命令占用了同一个连接，其他请求全部排队等待
List<KeyValue<String, String>> result = connection.sync().xread(
    XReadArgs.Builder.block(0),  // 无限阻塞
    XReadArgs.StreamOffset.from("mystream", "0-0")
);
```

```java
// Spring Data Redis Lettuce 配置下，阻塞命令复用共享连接
@Autowired
private RedisTemplate<String, String> redisTemplate;

public void listenForMessages() {
    // BLPOP 占用 Lettuce 共享连接，其他操作全部阻塞
    redisTemplate.opsForList().leftPop("taskQueue", 0, TimeUnit.SECONDS);
}
```

## 合规示例

```java
// 为阻塞命令创建独立连接，不影响普通业务连接池
RedisClient client = RedisClient.create("redis://127.0.0.1:6379");

// 普通业务连接
StatefulRedisConnection<String, String> businessConnection = client.connect();

// 阻塞命令使用独立的专用连接
StatefulRedisConnection<String, String> blockingConnection = client.connect();
RedisCommands<String, String> blockingCommands = blockingConnection.sync();

// 普通业务使用 businessConnection
businessConnection.sync().set("user:1001", "Alice");

// 阻塞命令使用专用连接，不干扰业务连接池
List<KeyValue<String, String>> result = blockingCommands.xread(
    XReadArgs.Builder.block(Duration.ofSeconds(30)),  // 设置有限阻塞时间
    XReadArgs.StreamOffset.from("mystream", "0-0")
);
```

```java
// SUBSCRIBE 使用独立连接
RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
StatefulRedisPubSubConnection<String, String> pubSubConnection = client.connectPubSub();

pubSubConnection.addListener(new RedisPubSubAdapter<String, String>() {
    @Override
    public void message(String channel, String message) {
        System.out.println("Received: " + message);
    }
});

// Pub/Sub 使用专用连接，不影响普通命令
pubSubConnection.sync().subscribe("notifications");
```
