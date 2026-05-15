# REDIS-005：Pipeline 批量使用情况

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-005 |
| 风险等级 | 🔵 建议 |
| 规则描述 | Pipeline 批量使用情况（多次独立命令应使用 Pipeline） |

## 问题说明

多次独立的 Redis 命令逐条发送会产生多次网络往返，效率低。使用 Pipeline 可以将多个命令打包发送，减少网络延迟。

## 检查方法

1. 搜索连续的 Redis 命令调用
2. 检查是否使用 `pipeline()` 或 `executePipelined`
3. 关注循环中的 Redis 操作

搜索模式：
- `grep_code` 搜索循环中的 `redisTemplate.opsForValue().set` 连续调用
- `search_codebase` 搜索 "pipeline" 相关代码

## 违规示例

```java
// ❌ 逐条执行
for (Map.Entry<String, String> entry : dataMap.entrySet()) {
    redisTemplate.opsForValue().set(entry.getKey(), entry.getValue());
}
```

## 合规示例

```java
// ✅ 使用 Pipeline
redisTemplate.executePipelined((connection) -> {
    for (Map.Entry<String, String> entry : dataMap.entrySet()) {
        connection.set(
            entry.getKey().getBytes(),
            entry.getValue().getBytes()
        );
    }
    return null;
});
```
