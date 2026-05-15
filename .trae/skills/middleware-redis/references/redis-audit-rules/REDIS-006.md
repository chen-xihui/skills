# REDIS-006：Lua 脚本是否使用 EVALSHA

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-006 |
| 风险等级 | 🔵 建议 |
| 规则描述 | Lua 脚本是否使用 EVALSHA 预加载（而非每次 EVAL） |

## 问题说明

每次使用 `EVAL` 都会发送完整脚本内容到 Redis，浪费网络带宽。应先使用 `SCRIPT LOAD` 预加载脚本，后续使用 `EVALSHA` 仅发送脚本 SHA1 值。

## 检查方法

1. 搜索 `eval` 调用
2. 检查是否有对应的 `scriptLoad` 或 `SCRIPT LOAD`
3. 搜索 `DefaultRedisScript` 是否缓存了 SHA

搜索模式：
- `grep_code` 搜索 `eval(`、`EVAL`、`execute(RedisScript)`
- `search_codebase` 搜索 "script" + "redis" 相关代码

## 违规示例

```java
// ❌ 每次都发送完整脚本
String script = "local current = redis.call('GET', KEYS[1]) ...";
redisTemplate.execute(new DefaultRedisScript<>(script, Long.class), keys, args);
```

## 合规示例

```java
// ✅ 预加载脚本，使用 EVALSHA
DefaultRedisScript<Long> redisScript = new DefaultRedisScript<>();
redisScript.setScriptText("local current = redis.call('GET', KEYS[1]) ...");
redisScript.setResultType(Long.class);
// DefaultRedisScript 会自动缓存 SHA，后续调用使用 EVALSHA
redisTemplate.execute(redisScript, keys, args);
```
