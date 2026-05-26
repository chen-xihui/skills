# REDIS-001：禁止在循环中使用 keys *

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-001 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 禁止在循环中使用 `keys *`，应使用 `scan` |

## 问题说明

`keys *` 命令会遍历 Redis 中所有 Key，时间复杂度 O(N)，在 Key 数量多时会导致 Redis 阻塞，影响所有客户端请求。应使用 `scan` 命令增量遍历。

## 检查方法

1. 搜索循环体内的 `keys(` 调用
2. 搜索 `KEYS *` 命令
3. 即使不在循环中，生产环境也不建议使用 `keys *`

搜索模式：
- `grep_code` 搜索 `keys(`、`.keys(`
- `search_codebase` 搜索 "keys *" 相关代码

## 违规示例

```java
// ❌ 循环中使用 keys
Set<String> keys = redisTemplate.keys("user:*");
for (String key : keys) {
    // 处理每个 key...
}
```

## 合规示例

```java
// ✅ 使用 scan 替代 keys
Set<String> keys = new HashSet<>();
ScanOptions options = ScanOptions.scanOptions().match("user:*").count(100).build();
try (var cursor = redisTemplate.scan(options)) {
    while (cursor.hasNext()) {
        keys.add(cursor.next());
    }
}
```