# Lettuce 代码审计规则索引

本目录包含 Lettuce 客户端专属规则（LETTUCE-001 ~ LETTUCE-007）和集群通用规则（CLUSTER-001 ~ CLUSTER-003）的详细说明和检查方法。

## Lettuce 专属规则

| 规则ID | 规则描述 | 风险等级 | 详细文档 |
|--------|---------|---------|---------|
| LETTUCE-001 | 阻塞命令（BLPOP、SUBSCRIBE、XREAD）必须使用独立连接，不允许共享普通连接池 | 🔴 严重 | [LETTUCE-001.md](./LETTUCE-001.md) |
| LETTUCE-002 | Redis Cluster 模式下必须配置 ClusterTopologyRefreshOptions | 🔴 严重 | [LETTUCE-002.md](./LETTUCE-002.md) |
| LETTUCE-003 | 应用退出时必须调用 RedisClient.shutdown() 释放 Netty 线程 | 🔴 严重 | [LETTUCE-003.md](./LETTUCE-003.md) |
| LETTUCE-004 | 必须配置 SocketOptions.keepAlive(true) | 🟡 风险 | [LETTUCE-004.md](./LETTUCE-004.md) |
| LETTUCE-005 | 建议开启 pingBeforeActivateConnection(true) | 🟡 风险 | [LETTUCE-005.md](./LETTUCE-005.md) |
| LETTUCE-006 | 必须显式设置 commandTimeout | 🟡 风险 | [LETTUCE-006.md](./LETTUCE-006.md) |
| LETTUCE-007 | shareNativeConnection=true 需明确配置连接模式 | 🔵 提示 | [LETTUCE-007.md](./LETTUCE-007.md) |

## 集群通用规则

| 规则ID | 规则描述 | 风险等级 | 详细文档 |
|--------|---------|---------|---------|
| CLUSTER-001 | maxAttempts 应设置 3-5，禁止过大值 | 🔴 严重 | [CLUSTER-001.md](./CLUSTER-001.md) |
| CLUSTER-002 | 集群总连接数 = 节点数 × maxTotal，必须评估 | 🟡 风险 | [CLUSTER-002.md](./CLUSTER-002.md) |
| CLUSTER-003 | 禁止业务层重试循环包裹集群调用 | 🟡 风险 | [CLUSTER-003.md](./CLUSTER-003.md) |

## 风险等级统计

- 🔴 **严重**: 4 条（LETTUCE-001~003, CLUSTER-001）
- 🟡 **风险**: 5 条（LETTUCE-004~006, CLUSTER-002~003）
- 🔵 **提示**: 1 条（LETTUCE-007）

## 检查流程

1. 确认扫描路径
2. 运行 `python scripts/check_all.py <项目根目录>` 执行全部检查
3. 或运行单项检查，如 `python scripts/check_lettuce_001.py <项目根目录>`
4. 生成结构化审计报告，按风险等级排序（🔴 → 🟡 → 🔵）
