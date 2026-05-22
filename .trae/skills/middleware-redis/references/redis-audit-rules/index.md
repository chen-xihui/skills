# Redis 代码优化检查规则索引

本目录包含 REDIS-001 ~ REDIS-014 共 14 条检查规则的详细说明和检查方法。

## 规则总览

| 规则ID | 规则描述 | 风险等级 | 详细文档 |
|--------|---------|---------|---------|
| REDIS-001 | 禁止在循环中使用 `keys *`，应使用 `scan` | 🔴 严重 | [REDIS-001.md](./REDIS-001.md) |
| REDIS-002 | 大 Key 风险检查（单次操作 Value 超过 10KB 应拆分或压缩） | 🟡 警告 | [REDIS-002.md](./REDIS-002.md) |
| REDIS-003 | 热 Key 风险检查（高频读写的 Key 应考虑本地缓存） | 🟡 警告 | [REDIS-003.md](./REDIS-003.md) |
| REDIS-004 | 连接池参数合理性（maxTotal、maxIdle、maxWaitMillis） | 🟡 警告 | [REDIS-004.md](./REDIS-004.md) |
| REDIS-005 | Pipeline 批量使用情况（多次独立命令应使用 Pipeline） | 🔵 建议 | [REDIS-005.md](./REDIS-005.md) |
| REDIS-006 | Lua 脚本是否使用 EVALSHA 预加载（而非每次 EVAL） | 🔵 建议 | [REDIS-006.md](./REDIS-006.md) |
| REDIS-007 | 是否设置合理的过期时间（避免 Key 永不过期导致内存泄漏） | 🟡 警告 | [REDIS-007.md](./REDIS-007.md) |
| REDIS-008 | 密码是否硬编码 | 🔴 严重 | [REDIS-008.md](./REDIS-008.md) |
| REDIS-009 | 禁止使用 CONFIG、FLUSHALL、FLUSHDB 等高危命令 | 🔴 严重 | [REDIS-009.md](./REDIS-009.md) |
| REDIS-010 | 禁止使用 Keys 全库匹配命令 | 🔴 严重 | [REDIS-010.md](./REDIS-010.md) |
| REDIS-011 | 避免使用集合整存整取与高时间复杂度命令 | 🟡 警告 | [REDIS-011.md](./REDIS-011.md) |
| REDIS-012 | Key 命名规范检查 | 🔵 建议 | [REDIS-012.md](./REDIS-012.md) |
| REDIS-013 | 大 Key 集合对象检查（建议控制在 5000 项以内） | 🟡 警告 | [REDIS-013.md](./REDIS-013.md) |
| REDIS-014 | 事务命令使用检查 | 🟡 警告 | [REDIS-014.md](./REDIS-014.md) |

## 风险等级统计

- 🔴 **严重**: 4 条（REDIS-001、REDIS-008、REDIS-009、REDIS-010）
- 🟡 **警告**: 7 条（REDIS-002、REDIS-003、REDIS-004、REDIS-007、REDIS-011、REDIS-013、REDIS-014）
- 🔵 **建议**: 3 条（REDIS-005、REDIS-006、REDIS-012）

## 检查流程

1. 确认扫描路径
2. 识别 Redis 客户端类型（Lettuce / Jedis）
3. 按 REDIS-001 ~ REDIS-014 逐项搜索检查
4. 生成结构化审计报告，按风险等级排序（🔴 → 🟡 → 🔵）