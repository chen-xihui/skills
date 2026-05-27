# Redis 集群 规则集
本文档包含 3 条规则
---
# CLUSTER-001：Jedis Cluster maxAttempts 不能过大

| 属性 | 说明 |
|------|------|
| 规则ID | CLUSTER-001 |
| 风险等级 | 严重 |
| 规则描述 | maxAttempts 建议设置 3-5，故障期间线程堆积 |

## 问题说明

故障期间线程堆积

## 检查方法

静态分析：检查 JedisCluster maxAttempts 配置

## 违规示例

maxAttempts: 10 // 过大

## 合规示例

maxAttempts: 3

# CLUSTER-002：Cluster 连接数必须评估节点倍增

| 属性 | 说明 |
|------|------|
| 规则ID | CLUSTER-002 |
| 风险等级 | 风险 |
| 规则描述 | Redis Cluster 连接数 = 节点数 × 每节点连接 |

## 问题说明

6 节点 Cluster maxTotal=200 实际产生 1200 连接

## 检查方法

静态分析：检查 maxTotal 配置是否考虑节点数

## 违规示例

maxTotal: 200 // 6节点实际1200连接

## 合规示例

maxTotal: 200 / 节点数

# CLUSTER-003：Cluster 禁止业务层二次重试

| 属性 | 说明 |
|------|------|
| 规则ID | CLUSTER-003 |
| 风险等级 | 风险 |
| 规则描述 | 客户端已有 MOVED/ASK 重试，禁止业务再次重试 |

## 问题说明

指数级放大

## 检查方法

静态分析：检查 Cluster 模式外层重试逻辑

## 违规示例

for (int i = 0; i < 5; i++) {<br>    cluster.get(key);<br>}

## 合规示例

依赖内置重试

