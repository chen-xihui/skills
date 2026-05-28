# CLUSTER-002：Cluster 连接数必须评估节点倍增

| 属性 | 说明 |
|------|------|
| 规则ID | CLUSTER-002 |
| 风险等级 | 风险 |
| 规则描述 | Redis Cluster 模式下总连接数 = 节点数 × 每节点连接池大小(maxTotal)，必须评估实际连接数 |

## 问题说明

Redis Cluster 客户端为每个节点维护独立连接池。例如 6 节点 Cluster 配置 maxTotal=200，实际产生 6×200=1200 个连接，远超单机预期，可能导致 Redis 服务端 FD 耗尽或客户端连接超限。

## 检查方法

- 静态分析：检查 JedisCluster/Lettuce Cluster 配置中 maxTotal 是否考虑了节点倍增效应
- 计算验证：`总连接数 = 节点数 × maxTotal`，确保总连接数在合理范围内
- 脚本化检查：`python scripts/check_cluster_002.py <项目根目录>`

## 违规示例

```java
// 6 节点 Cluster，maxTotal=200，实际产生 1200 连接
JedisPoolConfig poolConfig = new JedisPoolConfig();
poolConfig.setMaxTotal(200);  // 未考虑节点倍增，实际连接 = 6 × 200 = 1200
Set<HostAndPort> nodes = new HashSet<>();
// ... 添加 6 个节点
JedisCluster cluster = new JedisCluster(nodes, poolConfig);
```

## 合规示例

```java
// 根据节点数调整 maxTotal，保证总连接数可控
// 目标：每节点连接数 = 总预算 / 节点数
// 例如总预算 200 连接，6 节点 → maxTotal ≈ 33
JedisPoolConfig poolConfig = new JedisPoolConfig();
poolConfig.setMaxTotal(33);  // 6 × 33 ≈ 198 总连接
poolConfig.setMaxIdle(20);
poolConfig.setMinIdle(5);
Set<HostAndPort> nodes = new HashSet<>();
// ... 添加 6 个节点
JedisCluster cluster = new JedisCluster(nodes, poolConfig);
```
