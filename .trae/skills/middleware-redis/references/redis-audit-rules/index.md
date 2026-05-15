# Redis 代码优化检查规则索引

本目录包含 REDIS-001 ~ REDIS-008 共 8 条检查规则的详细说明。

**使用方式**：先在本索引中定位需要检查的规则 ID，再读取对应文件获取详细检查方法和示例代码。

---

## 规则索引

| 规则ID | 规则描述 | 风险等级 | 详细文件 |
|--------|---------|---------|---------|
| REDIS-001 | 禁止在循环中使用 `keys *`，应使用 `scan` | 🔴 严重 | [REDIS-001.md](./REDIS-001.md) |
| REDIS-002 | 大 Key 风险检查（单次操作 Value 超过 10KB 应拆分或压缩） | 🟡 警告 | [REDIS-002.md](./REDIS-002.md) |
| REDIS-003 | 热 Key 风险检查（高频读写的 Key 应考虑本地缓存） | 🟡 警告 | [REDIS-003.md](./REDIS-003.md) |
| REDIS-004 | 连接池参数合理性（maxTotal、maxIdle、maxWaitMillis） | 🟡 警告 | [REDIS-004.md](./REDIS-004.md) |
| REDIS-005 | Pipeline 批量使用情况（多次独立命令应使用 Pipeline） | 🔵 建议 | [REDIS-005.md](./REDIS-005.md) |
| REDIS-006 | Lua 脚本是否使用 EVALSHA 预加载（而非每次 EVAL） | 🔵 建议 | [REDIS-006.md](./REDIS-006.md) |
| REDIS-007 | 是否设置合理的过期时间（避免 Key 永不过期导致内存泄漏） | 🟡 警告 | [REDIS-007.md](./REDIS-007.md) |
| REDIS-008 | 密码是否硬编码 | 🔴 严重 | [REDIS-008.md](./REDIS-008.md) |

---

## 检查通用流程

1. 确认扫描路径 `scan_path`
2. 识别 Redis 客户端类型（Lettuce / Jedis）
3. 按规则 ID 逐项检查，读取对应规则文件获取检查方法和搜索模式
4. 生成审计报告，按风险等级排序（🔴 → 🟡 → 🔵）
