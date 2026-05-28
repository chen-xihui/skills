# LETTUCE-004：必须开启 TCP KeepAlive

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-004 |
| 风险等级 | 风险 |
| 规则描述 | 必须配置 SocketOptions.keepAlive(true)，确保长连接在防火墙或负载均衡器回收后可被及时检测 |

## 问题说明

Lettuce 默认使用 TCP 长连接。若未开启 TCP KeepAlive，当中间网络设备（防火墙、NAT 网关、负载均衡器）因空闲超时静默回收连接时，客户端无法感知连接已断开。后续请求将因写入已关闭的连接而失败，直到 TCP 重传超时（通常数分钟）才能发现连接断开。在此期间，所有发往该连接的请求均超时失败，造成业务不可用。开启 TCP KeepAlive 后，操作系统会定期发送探测包，及时检测并回收死连接。

## 检查方法

- 静态分析：检查 ClientOptions / ClusterClientOptions 中是否配置了 `SocketOptions.builder().keepAlive(true)`
- 检查 Spring Boot 配置中是否设置了 `spring.redis.lettuce.socket.keep-alive=true` 或等价配置
- 脚本化检查：`python scripts/check_lettuce_004.py <项目根目录>`

## 违规示例

```java
// 未开启 TCP KeepAlive，长连接假死无法检测
RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
// 使用默认 ClientOptions，SocketOptions.keepAlive 默认 false
StatefulRedisConnection<String, String> connection = client.connect();
connection.sync().set("key", "value");
// 若防火墙静默回收连接，后续请求将长时间超时
```

```java
// 配置了 SocketOptions 但未开启 keepAlive
ClientOptions options = ClientOptions.builder()
    .socketOptions(SocketOptions.builder()
        .connectTimeout(Duration.ofSeconds(3))  // 只配了连接超时
        .build())
    .build();
RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
client.setOptions(options);
// keepAlive 未开启，连接假死无法检测
```

## 合规示例

```java
// 正确配置 TCP KeepAlive
SocketOptions socketOptions = SocketOptions.builder()
    .keepAlive(true)                               // 开启 TCP KeepAlive
    .connectTimeout(Duration.ofSeconds(3))
    .build();

ClientOptions clientOptions = ClientOptions.builder()
    .socketOptions(socketOptions)
    .build();

RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
client.setOptions(clientOptions);
StatefulRedisConnection<String, String> connection = client.connect();
connection.sync().set("key", "value");
// 连接假死时 TCP KeepAlive 探测可及时感知并重建连接
```

```java
// Cluster 模式下同样需要配置
SocketOptions socketOptions = SocketOptions.builder()
    .keepAlive(true)
    .connectTimeout(Duration.ofSeconds(3))
    .build();

ClusterClientOptions clusterClientOptions = ClusterClientOptions.builder()
    .socketOptions(socketOptions)
    .build();

RedisClusterClient clusterClient = RedisClusterClient.create(
    RedisURI.Builder.redis("127.0.0.1").withPort(7001).build()
);
clusterClient.setOptions(clusterClientOptions);
```
