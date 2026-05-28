# Jedis 代码审计规则索引

本目录包含 Jedis 客户端专属规则（JEDIS-001 ~ JEDIS-014）和集群通用规则（CLUSTER-001 ~ CLUSTER-003）的详细说明和检查方法。

## Jedis 专属规则

| 规则ID | 规则描述 | 风险等级 | 详细文档 |
|--------|---------|---------|---------|
| JEDIS-001 | 禁止使用 KEYS 命令，应使用 SCAN | 🔴 严重 | [JEDIS-001.md](./JEDIS-001.md) |
| JEDIS-002 | getResource() 必须使用 try-with-resources 防止连接泄漏 | 🔴 严重 | [JEDIS-002.md](./JEDIS-002.md) |
| JEDIS-003 | 禁止在循环中创建连接（Jedis、JedisPool、RedissonClient） | 🔴 严重 | [JEDIS-003.md](./JEDIS-003.md) |
| JEDIS-004 | Pipeline 必须调用 close() 或使用 try-with-resources | 🔴 严重 | [JEDIS-004.md](./JEDIS-004.md) |
| JEDIS-005 | MULTI/EXEC 异常后必须调用 discard() 清理连接状态 | 🔴 严重 | [JEDIS-005.md](./JEDIS-005.md) |
| JEDIS-006 | 禁止运行时执行 CONFIG SET / CONFIG REWRITE | 🔴 严重 | [JEDIS-006.md](./JEDIS-006.md) |
| JEDIS-007 | JedisPoolConfig 必须配置四项核心参数（maxTotal、maxIdle、minIdle、maxWaitMillis） | 🟡 风险 | [JEDIS-007.md](./JEDIS-007.md) |
| JEDIS-008 | 必须开启 setTestWhileIdle(true) 检测失效连接 | 🟡 风险 | [JEDIS-008.md](./JEDIS-008.md) |
| JEDIS-009 | Pipeline 批量命令数应控制在 100-1000 以内 | 🟡 风险 | [JEDIS-009.md](./JEDIS-009.md) |
| JEDIS-010 | 禁止无限重试循环包裹 Redis 调用 | 🟡 风险 | [JEDIS-010.md](./JEDIS-010.md) |
| JEDIS-011 | 禁止业务层重试循环包裹 jedisCluster 调用 | 🟡 风险 | [JEDIS-011.md](./JEDIS-011.md) |
| JEDIS-012 | 必须设置 commandTimeout 命令超时时间 | 🟡 风险 | [JEDIS-012.md](./JEDIS-012.md) |
| JEDIS-013 | 建议开启 setTestOnBorrow(true) 连接借用检测 | 🔵 提示 | [JEDIS-013.md](./JEDIS-013.md) |
| JEDIS-014 | Lua 脚本必须使用 SCRIPT LOAD + EVALSHA | 🔵 提示 | [JEDIS-014.md](./JEDIS-014.md) |

## 集群通用规则

| 规则ID | 规则描述 | 风险等级 | 详细文档 |
|--------|---------|---------|---------|
| CLUSTER-001 | maxAttempts 应设置 3-5，禁止过大值 | 🔴 严重 | [CLUSTER-001.md](./CLUSTER-001.md) |
| CLUSTER-002 | 集群总连接数 = 节点数 × maxTotal，必须评估 | 🟡 风险 | [CLUSTER-002.md](./CLUSTER-002.md) |
| CLUSTER-003 | 禁止业务层重试循环包裹集群调用 | 🟡 风险 | [CLUSTER-003.md](./CLUSTER-003.md) |

## 风险等级统计

- 🔴 **严重**: 7 条（JEDIS-001~006, CLUSTER-001）
- 🟡 **风险**: 9 条（JEDIS-007~012, CLUSTER-002~003）
- 🔵 **提示**: 2 条（JEDIS-013, JEDIS-014）

## 检查流程

1. 确认扫描路径
2. 运行 `python scripts/check_all.py <项目根目录>` 执行全部检查
3. 或运行单项检查，如 `python scripts/check_jedis_001.py <项目根目录>`
4. 生成结构化审计报告，按风险等级排序（🔴 → 🟡 → 🔵）
