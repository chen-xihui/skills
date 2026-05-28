# CLUSTER-001：Jedis Cluster maxAttempts 不能过大

| 属性 | 说明 |
|------|------|
| 规则ID | CLUSTER-001 |
| 风险等级 | 严重 |
| 规则描述 | Jedis Cluster 的 maxAttempts 建议设置 3-5，禁止设置过大值，防止故障期间线程堆积 |

## 问题说明

当 Redis Cluster 节点故障时，客户端会对每个命令进行 maxAttempts 次重试。若 maxAttempts 设置过大（如 10、20），故障期间大量线程被阻塞在重试等待中，导致应用线程池耗尽、服务雪崩。

## 检查方法

- 静态分析：检查 JedisCluster 配置中 `maxAttempts` 参数值是否在 3-5 范围内
- 脚本化检查：`python scripts/check_cluster_001.py <项目根目录>`

## 违规示例

```java
// maxAttempts 设置过大，故障时线程堆积
JedisPoolConfig poolConfig = new JedisPoolConfig();
Set<HostAndPort> nodes = new HashSet<>();
nodes.add(new HostAndPort("127.0.0.1", 7001));
JedisCluster cluster = new JedisCluster(nodes, 3000, 10, poolConfig);
//                                                                  ^^ maxAttempts=10 过大
```

```yaml
# application.yml
spring:
  redis:
    cluster:
      max-attempts: 10  # 过大
```

## 合规示例

```java
JedisPoolConfig poolConfig = new JedisPoolConfig();
Set<HostAndPort> nodes = new HashSet<>();
nodes.add(new HostAndPort("127.0.0.1", 7001));
JedisCluster cluster = new JedisCluster(nodes, 3000, 3, poolConfig);
//                                                                ^^ maxAttempts=3 合理
```

```yaml
# application.yml
spring:
  redis:
    cluster:
      max-attempts: 3  # 合理范围 3-5
```
