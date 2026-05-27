## 能力二：代码优化检查

> 代码扫描：`_shared-references/harness-tools.md`（Cursor 使用 **Grep**、**SemanticSearch**）。

### 触发条件

用户请求检查 Redis 代码优化，如：
- "检查 Redis 代码"
- "缓存代码审计"
- "Redis 代码优化"
- "检查缓存代码规范"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| scan_path | string | 是 | — | 需扫描的项目根目录 |

### 检查规则清单

> 详细规则说明和检查方法参见 `references/redis-audit-rules/` 目录

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| REDIS-001 | 禁止在循环中使用 `keys *`，应使用 `scan` | 🔴 严重 |
| REDIS-002 | 大 Key 风险检查（单次操作 Value 超过 10KB 应拆分或压缩） | 🟡 警告 |
| REDIS-003 | 热 Key 风险检查（高频读写的 Key 应考虑本地缓存） | 🟡 警告 |
| REDIS-004 | 连接池参数合理性（maxTotal、maxIdle、maxWaitMillis） | 🟡 警告 |
| REDIS-005 | Pipeline 批量使用情况（多次独立命令应使用 Pipeline） | 🔵 建议 |
| REDIS-006 | Lua 脚本是否使用 EVALSHA 预加载（而非每次 EVAL） | 🔵 建议 |
| REDIS-007 | 是否设置合理的过期时间（避免 Key 永不过期导致内存泄漏） | 🟡 警告 |
| REDIS-008 | 密码是否硬编码 | 🔴 严重 |
| REDIS-009 | 禁止使用 CONFIG、FLUSHALL、FLUSHDB 等高危命令 | 🔴 严重 |
| REDIS-010 | 禁止使用 Keys 全库匹配命令 | 🔴 严重 |
| REDIS-011 | 避免使用集合整存整取与高时间复杂度命令 | 🟡 警告 |
| REDIS-012 | Key 命名规范检查 | 🔵 建议 |
| REDIS-013 | 大 Key 集合对象检查（建议控制在 5000 项以内） | 🟡 警告 |
| REDIS-014 | 事务命令使用检查 | 🟡 警告 |

### 检查流程

1. **确认扫描路径**：确认 `scan_path` 参数，缺失时主动询问
2. **识别 Redis 客户端类型**：判断使用的是 Lettuce 还是 Jedis
   - 搜索 `LettuceConnectionFactory` / `RedisClient` → Lettuce
   - 搜索 `JedisPool` / `JedisCluster` → Jedis
3. **扫描 Redis 相关代码**：使用 `SemanticSearch` 与 `Grep` 按规则逐项搜索
   - 搜索关键词：`keys(`、`scan`、`set`、`get`、`pipeline`、`eval`、`password`、`maxTotal` 等
4. **逐规则检查**：按 REDIS-001 ~ REDIS-014 逐项检查，记录发现的问题
5. **生成审计报告**：按输出格式生成结构化报告，按风险等级排序（🔴 → 🟡 → 🔵）

### 输出格式

```
📋 代码审计报告

📊 概要：共扫描 {N} 个文件，发现 {M} 个问题（🔴 严重 {x} | 🟡 警告 {y} | 🔵 建议 {z}）

| # | 文件路径 | 行号 | 规则ID | 问题描述 | 风险等级 | 改进建议 |
|---|---------|------|--------|---------|---------|---------|
| 1 | ... | ... | ... | ... | 🔴 严重 | ... |

💡 优先修复建议：{按风险等级排序的 Top 3 修复建议}
```

### 异常处理

- 扫描路径不存在 → 提示用户确认路径
- 未找到 Redis 相关代码 → 告知用户未检测到 Redis 客户端代码

---
