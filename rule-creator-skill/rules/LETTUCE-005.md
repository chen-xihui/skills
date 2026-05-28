# LETTUCE-005：建议开启应用层 PING

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-005 |
| 风险等级 | 风险 |
| 规则描述 | 建议开启 pingBeforeActivateConnection，在连接激活前发送 PING 检测应用层可用性，弥补 TCP KeepAlive 的不足 |

## 问题说明

TCP KeepAlive 只能检测网络层连通性，无法检测 Redis 进程是否真正可用（如 Redis 慢查询卡死、内存不足拒绝写入、主从切换中只读等场景）。开启 pingBeforeActivateConnection 后，Lettuce 在连接激活前主动发送 PING 命令，若 PING 未返回 PONG 则视为连接不可用，避免将请求路由到应用层已假死的节点。同时建议配合 enablePeriodicRefresh 实现定期心跳检测。

## 检查方法

- 静态分析：检查 ClientOptions / ClusterClientOptions 中是否配置了 `pingBeforeActivateConnection(true)`
- 检查是否在 LettuceClientConfiguration 中配置了 pingBeforeActivateConnection
- 脚本化检查：`python scripts/check_lettuce_005.py <项目根目录>`

## 违规示例

```java
// 未开启应用层 PING，连接建立后直接使用，可能路由到假死节点
RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
ClientOptions options = ClientOptions.builder()
    .socketOptions(SocketOptions.builder().keepAlive(true).build())
    .build();
client.setOptions(options);
// pingBeforeActivateConnection 默认 false，连接激活前不会发送 PING
StatefulRedisConnection<String, String> connection = client.connect();
// 若 Redis 进程假死，TCP 连接正常但请求无响应
String value = connection.sync().get("key");
```

## 合规示例

```java
// 开启 pingBeforeActivateConnection，连接激活前验证应用层可用性
ClientOptions options = ClientOptions.builder()
    .pingBeforeActivateConnection(true)              // 连接激活前发送 PING
    .socketOptions(SocketOptions.builder()
        .keepAlive(true)
        .build())
    .build();

RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
client.setOptions(options);
StatefulRedisConnection<String, String> connection = client.connect();
// 连接建立后会先 PING，确认 Redis 可用后才激活连接
String value = connection.sync().get("key");
```

```java
// Cluster 模式下同样建议开启
ClusterClientOptions clusterOptions = ClusterClientOptions.builder()
    .pingBeforeActivateConnection(true)              // 连接激活前 PING
    .socketOptions(SocketOptions.builder()
        .keepAlive(true)
        .build())
    .topologyRefreshOptions(ClusterTopologyRefreshOptions.builder()
        .enablePeriodicRefresh(Duration.ofSeconds(30))
        .enableAllAdaptiveRefreshTriggers()
        .build())
    .build();

RedisClusterClient clusterClient = RedisClusterClient.create(
    RedisURI.Builder.redis("127.0.0.1").withPort(7001).build()
);
clusterClient.setOptions(clusterOptions);
```

```java
// Spring Boot Lettuce 配置
@Configuration
public class RedisConfig {

    @Bean
    public LettuceClientConfigurationBuilderCustomizer lettuceCustomizer() {
        return builder -> builder
            .clientOptions(ClientOptions.builder()
                .pingBeforeActivateConnection(true)
                .socketOptions(SocketOptions.builder().keepAlive(true).build())
                .build());
    }
}
```
