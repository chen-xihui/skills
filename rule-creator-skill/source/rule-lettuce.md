# Lettuce 规则集
本文档包含 7 条规则
---
# LETTUCE-001：禁止阻塞命令复用普通连接池

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-001 |
| 风险等级 | 严重 |
| 规则描述 | BLPOP、SUBSCRIBE、XREAD BLOCK 等阻塞命令必须使用独立连接 |

## 问题说明

阻塞命令占用普通连接导致池耗尽

## 检查方法

静态分析：检查阻塞命令是否使用专用连接

## 违规示例

connection.sync().blpop(0, key); // 占用普通连接

## 合规示例

创建独立连接处理阻塞命令，不允许共享连接

# LETTUCE-002：Cluster 模式必须开启拓扑刷新

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-002 |
| 风险等级 | 严重 |
| 规则描述 | Redis Cluster failover 后必须刷新槽位缓存 |

## 问题说明

MOVED 循环、无法恢复

## 检查方法

静态分析：检查 ClusterTopologyRefreshOptions 配置

## 违规示例

// 未配置拓扑刷新

## 合规示例

ClusterTopologyRefreshOptions options = ClusterTopologyRefreshOptions.builder()<br>    .enablePeriodicRefresh(Duration.ofSeconds(30))<br>    .enableAllAdaptiveRefreshTriggers()<br>    .closeStaleConnections(true)<br>    .build();

# LETTUCE-003：应用退出必须 shutdown

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-003 |
| 风险等级 | 严重 |
| 规则描述 | 应用退出必须调用 lettuceClient.shutdown() |

## 问题说明

Netty 线程残留、classloader 泄漏

## 检查方法

静态分析：检查 main 方法或 Spring @PreDestroy 是否调用 shutdown

## 违规示例

// 未调用 shutdown

## 合规示例

@PreDestroy<br>public void destroy() {<br>    client.shutdown();<br>}

# LETTUCE-004：必须开启 TCP KeepAlive

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-004 |
| 风险等级 | 风险 |
| 规则描述 | 必须配置 SocketOptions.keepAlive(true) |

## 问题说明

长连接假死、防火墙/LB 回收

## 检查方法

静态分析：检查 SocketOptions 配置

## 违规示例

// 未开启 keepAlive

## 合规示例

ClientOptions options = ClientOptions.builder()<br>    .socketOptions(SocketOptions.builder().keepAlive(true).build())<br>    .build();

# LETTUCE-005：建议开启应用层 PING

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-005 |
| 风险等级 | 风险 |
| 规则描述 | 建议开启 pingBeforeActivateConnection 定期心跳 |

## 问题说明

TCP alive 不够检测应用层假死

## 检查方法

静态分析：检查 pingBeforeActivateConnection 配置

## 违规示例

// 未开启应用层 PING

## 合规示例

pingBeforeActivateConnection(true)

# LETTUCE-006：必须设置 commandTimeout

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-006 |
| 风险等级 | 风险 |
| 规则描述 | 必须设置命令超时，禁止默认无限等待 |

## 问题说明

线程堆积

## 检查方法

静态分析：检查是否配置 commandTimeout

## 违规示例

// 未设置超时

## 合规示例

client.setDefaultCommandTimeout(Duration.ofMillis(500));

# LETTUCE-007：shareNativeConnection 需明确配置

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-007 |
| 风险等级 | 提示 |
| 规则描述 | Lettuce 默认非池化、Netty 共享连接，需明确配置 |

## 问题说明

很多人误用 commons-pool

## 检查方法

静态分析：检查是否误用连接池

## 违规示例

// 使用了 commons-pool 但未配置

## 合规示例

明确配置 shareNativeConnection 行为

