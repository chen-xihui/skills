# REDIS-011：避免使用集合整存整取与高时间复杂度命令

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-011 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 不宜使用集合对象整存整取命令、集合高时间复杂度命令 |

## 问题说明

以下命令在数据量大时会导致慢日志问题：
- `HGETALL`：获取 Hash 所有字段和值
- `SMEMBERS`：获取 Set 所有成员
- `LRANGE 0 -1`：获取 List 所有元素
- `ZRANGE -inf +inf`：获取 ZSet 所有成员
- `LREM`：移除 List 中指定元素
- `ZUNION`：集合求并集

## 检查方法

搜索这些高复杂度命令的使用。

搜索模式：
- `grep_code` 搜索 `hgetall`、`smembers`、`lrange`、`zrange`、`lrem`、`zunion`

## 合规建议

- 使用 `HSCAN` / `SSCAN` / `ZSCAN` 增量遍历替代整存整取
- 使用范围查询替代全量获取
- 控制集合对象数据量在 5000 项以内

## 违规示例

```java
// ❌ 一次性获取所有 Hash 字段
Map<Object, Object> all = redisTemplate.opsForHash().entries("large:hash");
```

## 合规示例

```java
// ✅ 使用 HSCAN 增量遍历
ScanOptions options = ScanOptions.scanOptions().count(100).build();
Cursor<Map.Entry<Object, Object>> cursor = redisTemplate.opsForHash().scan("large:hash", options);
while (cursor.hasNext()) {
    Map.Entry<Object, Object> entry = cursor.next();
    // 处理每个字段
}
cursor.close();
```