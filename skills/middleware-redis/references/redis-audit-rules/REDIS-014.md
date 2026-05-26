# REDIS-014：事务命令使用检查

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-014 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 缓存服务不支持强一致性事务，不宜使用缓存服务处理事务 |

## 问题说明

Redis 仅提供乐观锁和批量操作的最终一致性能力：
- `MULTI`/`EXEC`：开启和提交事务，错误命令不会回滚已执行的命令
- `DISCARD`：取消事务
- `WATCH`：监听键值是否被修改
- `SETNX`：仅在键不存在时设置值，可用于设计锁

**注意**：使用 Proxy 组件时，不支持 multi、exec、discard 等事务命令。

## 检查方法

搜索事务命令的使用。

搜索模式：
- `grep_code` 搜索 `.multi(`、`.exec(`、`.discard(`、`.watch(`

## 合规建议

- 如需使用事务功能，需充分评估一致性影响、事务异常设计、事务回滚方案
- 优先使用 SETNX 实现分布式锁，而非复杂事务

## 违规示例

```java
// ❌ 在 Proxy 环境下使用事务命令
redisTemplate.execute(new SessionCallback() {
    public Object execute(RedisOperations ops) {
        ops.multi();
        ops.opsForValue().set("k1", "v1");
        ops.opsForValue().set("k2", "v2");
        return ops.exec();
    }
});
```

## 合规示例

```java
// ✅ 使用 SETNX 实现分布式锁
Boolean acquired = redisTemplate.opsForValue()
    .setIfAbsent("lock:order:" + orderId, "locked", 10, TimeUnit.SECONDS);
if (Boolean.TRUE.equals(acquired)) {
    try {
        // 执行业务逻辑
    } finally {
        redisTemplate.delete("lock:order:" + orderId);
    }
}
```