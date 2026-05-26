# REDIS-009：禁止使用高危命令

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-009 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 禁止使用 CONFIG、FLUSHALL、FLUSHDB 等修改服务端的命令 |

## 问题说明

高危命令可能导致服务配置变更、数据异常丢失，影响所有接入系统的可用性。

**禁止使用的高危命令**：
- `CONFIG`：修改服务端配置
- `FLUSHALL`：清空所有数据库所有键
- `FLUSHDB`：清空当前数据库所有键

## 检查方法

搜索代码中的高危命令调用。

搜索模式：
- `grep_code` 搜索 `.config(`、`.flushall(`、`.flushdb(`、`CONFIG `、`FLUSHALL`、`FLUSHDB`

## 违规示例

```java
// ❌ 使用高危命令
jedis.flushAll();
jedis.configSet("maxmemory", "1gb");
```

## 合规示例

```java
// ✅ 通过运维平台调整配置，不在代码中直接操作
// 数据清理应使用 scan + del 逐个删除，或使用 expire 设置过期时间
```