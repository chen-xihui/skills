# Redisson 代码审计规则索引

本目录包含 Redisson 客户端专属规则（REDISSON-001 ~ REDISSON-005）和集群通用规则（CLUSTER-001 ~ CLUSTER-003）的详细说明和检查方法。

## Redisson 专属规则

| 规则ID | 规则描述 | 风险等级 | 详细文档 |
|--------|---------|---------|---------|
| REDISSON-001 | lock() 必须设置 leaseTime，防止锁永久持有 | 🔴 严重 | [REDISSON-001.md](./REDISSON-001.md) |
| REDISSON-002 | RedissonClient 必须单例，禁止循环内创建 | 🔴 严重 | [REDISSON-002.md](./REDISSON-002.md) |
| REDISSON-003 | 必须调用 redisson.shutdown() 释放 Netty 线程 | 🔴 严重 | [REDISSON-003.md](./REDISSON-003.md) |
| REDISSON-004 | 配置文件中必须设置 keepAlive: true | 🟡 风险 | [REDISSON-004.md](./REDISSON-004.md) |
| REDISSON-005 | tryLock 必须设置 waitTime 和 leaseTime | 🟡 风险 | [REDISSON-005.md](./REDISSON-005.md) |

## 集群通用规则

| 规则ID | 规则描述 | 风险等级 | 详细文档 |
|--------|---------|---------|---------|
| CLUSTER-001 | maxAttempts 应设置 3-5，禁止过大值 | 🔴 严重 | [CLUSTER-001.md](./CLUSTER-001.md) |
| CLUSTER-002 | 集群总连接数 = 节点数 × maxTotal，必须评估 | 🟡 风险 | [CLUSTER-002.md](./CLUSTER-002.md) |
| CLUSTER-003 | 禁止业务层重试循环包裹集群调用 | 🟡 风险 | [CLUSTER-003.md](./CLUSTER-003.md) |

## 风险等级统计

- 🔴 **严重**: 4 条（REDISSON-001~003, CLUSTER-001）
- 🟡 **风险**: 4 条（REDISSON-004~005, CLUSTER-002~003）

## 检查流程

1. 确认扫描路径
2. 运行 `python scripts/check_all.py <项目根目录>` 执行全部检查
3. 或运行单项检查，如 `python scripts/check_redisson_001.py <项目根目录>`
4. 生成结构化审计报告，按风险等级排序（🔴 → 🟡 → 🔵）
