# Spring Data Redis 代码审计规则索引

本目录包含 Spring Data Redis 专属规则（SDR-001 ~ SDR-003）和集群通用规则（CLUSTER-001 ~ CLUSTER-003）的详细说明和检查方法。

## Spring Data Redis 专属规则

| 规则ID | 规则描述 | 风险等级 | 详细文档 |
|--------|---------|---------|---------|
| SDR-001 | RedisTemplate 必须配置 keySerializer 和 valueSerializer | 🔴 严重 | [SDR-001.md](./SDR-001.md) |
| SDR-002 | 禁止使用 redisTemplate.keys() 和 opsForKeys().keys()，应使用 SCAN | 🟡 风险 | [SDR-002.md](./SDR-002.md) |
| SDR-003 | LettuceConnectionFactory 必须配置 commandTimeout | 🟡 风险 | [SDR-003.md](./SDR-003.md) |

## 集群通用规则

| 规则ID | 规则描述 | 风险等级 | 详细文档 |
|--------|---------|---------|---------|
| CLUSTER-001 | maxAttempts 应设置 3-5，禁止过大值 | 🔴 严重 | [CLUSTER-001.md](./CLUSTER-001.md) |
| CLUSTER-002 | 集群总连接数 = 节点数 × maxTotal，必须评估 | 🟡 风险 | [CLUSTER-002.md](./CLUSTER-002.md) |
| CLUSTER-003 | 禁止业务层重试循环包裹集群调用 | 🟡 风险 | [CLUSTER-003.md](./CLUSTER-003.md) |

## 风险等级统计

- 🔴 **严重**: 2 条（SDR-001, CLUSTER-001）
- 🟡 **风险**: 4 条（SDR-002~003, CLUSTER-002~003）

## 检查流程

1. 确认扫描路径
2. 运行 `python scripts/check_all.py <项目根目录>` 执行全部检查
3. 或运行单项检查，如 `python scripts/check_sdr_001.py <项目根目录>`
4. 生成结构化审计报告，按风险等级排序（🔴 → 🟡 → 🔵）
