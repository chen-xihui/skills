# REDIS-010：禁止使用全库匹配命令

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-010 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 不能使用 Keys 命令，推荐使用 Scan 命令和前缀关键字匹配替代 |

## 问题说明

`KEYS *` 命令会阻塞 Redis 单线程，当键数量较多时会导致严重性能问题甚至服务不可用。

## 检查方法

搜索 `keys` 命令的使用（区分大小写）。

搜索模式：
- `grep_code` 搜索 `.keys(`、`KEYS `（排除注释和 scan 相关的代码）

## 违规示例

```java
// ❌ 使用 KEYS 命令
Set<String> keys = jedis.keys("user:*");
```

## 合规示例

```java
// ✅ 使用 SCAN 命令
ScanParams scanParams = new ScanParams().match("user:*").count(100);
try (Scanner scanner = jedis.scan(scanParams)) {
    while (scanner.hasNext()) {
        String key = scanner.next();
        // 处理 key
    }
}
```