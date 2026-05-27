# REDIS-007：是否设置合理的过期时间

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-007 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 是否设置合理的过期时间（避免 Key 永不过期导致内存泄漏） |

## 问题说明

Key 不设置过期时间会导致内存持续增长，最终可能触发 maxmemory 策略或 OOM。

## 检查方法

1. 搜索 `set` 或 `setex` 调用，检查是否有过期时间
2. 搜索 `set(key, value)` 两个参数的调用（未设置过期时间）
3. 排除确实需要永久存在的 Key（如配置类数据）

搜索模式：
- `grep_code` 搜索 `\.set\(` 调用，检查是否有过期时间参数
- `search_codebase` 搜索 "set" + "expire" 相关代码

## 违规示例

```java
// ❌ 未设置过期时间
redisTemplate.opsForValue().set("session:" + sessionId, userData);
```

## 合规示例

```java
// ✅ 设置过期时间
redisTemplate.opsForValue().set("session:" + sessionId, userData, 30, TimeUnit.MINUTES);
```