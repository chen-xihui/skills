# LETTUCE-002：Cluster 模式必须开启拓扑刷新

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-002 |
| 风险等级 | 严重 |
| 规则描述 | Redis Cluster 模式下必须配置 ClusterTopologyRefreshOptions，开启周期性刷新与自适应刷新，避免 failover 后 MOVED 循环和无法恢复 |

## 问题说明

Lettuce 客户端在启动时缓存 Redis Cluster 的槽位映射（slot → node）。当集群发生 failover 或扩缩容时，若客户端未刷新拓扑缓存，请求会持续发往已迁移的旧节点，触发 MOVED 重定向。若自适应刷新未开启，Lettuce 对 MOVED 响应仅做有限次重定向，可能陷入 MOVED 循环或最终抛出异常，导致业务不可恢复。在生产环境中，Cluster 节点故障是常见事件，未配置拓扑刷新将导致严重故障。

## 检查方法

- 静态分析：检查 Redis Cluster 配置中是否设置了 `ClusterTopologyRefreshOptions` 且同时开启了 `enablePeriodicRefresh` 和 `enableAllAdaptiveRefreshTriggers`
- 检查 Spring Boot 配置中是否通过 `lettuce.cluster.refresh.adaptive` 和 `lettuce.cluster.refresh.period` 开启拓扑刷新
- 脚本化检查：`python scripts/check_lettuce_002.py <项目根目录>`

## 违规示例

```java
// 未配置拓扑刷新，failover 后客户端无法感知新拓扑
RedisURI uri = RedisURI.Builder.redis("127.0.0.1").withPort(7001).build();
RedisClusterClient clusterClient = RedisClusterClient.create(uri);
// 缺少 ClusterTopologyRefreshOptions 配置

RedisAdvancedClusterCommands<String, String> commands = clusterClient.connect().sync();
commands.get("mykey");  // failover 后可能 MOVED 循环
```

```yaml
# application.yml - 未配置拓扑刷新
spring:
  redis:
    cluster:
      nodes: 127.0.0.1:7001,127.0.0.1:7002,127.0.0.1:7003
    # 缺少 lettuce.cluster.refresh 配置
```

## 合规示例

```java
// 完整配置 ClusterTopologyRefreshOptions
ClusterTopologyRefreshOptions topologyRefreshOptions = ClusterTopologyRefreshOptions.builder()
    .enablePeriodicRefresh(Duration.ofSeconds(30))     // 每 30 秒周期性刷新拓扑
    .enableAllAdaptiveRefreshTriggers()                 // 开启所有自适应刷新触发器
    .closeStaleConnections(true)                        // 关闭过期连接
    .build();

RedisURI uri = RedisURI.Builder.redis("127.0.0.1").withPort(7001).build();
RedisClusterClient clusterClient = RedisClusterClient.create(uri);
clusterClient.setOptions(ClusterClientOptions.builder()
    .topologyRefreshOptions(topologyRefreshOptions)
    .build());

RedisAdvancedClusterCommands<String, String> commands = clusterClient.connect().sync();
commands.get("mykey");  // failover 后自动刷新拓扑，正常路由
```

```yaml
# application.yml - Spring Boot 配置拓扑刷新
spring:
  redis:
    cluster:
      nodes: 127.0.0.1:7001,127.0.0.1:7002,127.0.0.1:7003
    lettuce:
      cluster:
        refresh:
          adaptive: true          # 开启自适应刷新
          period: 30s             # 周期性刷新间隔 30 秒
```
