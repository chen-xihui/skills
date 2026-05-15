# REDIS-002：大 Key 风险检查

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-002 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 大 Key 风险检查（单次操作 Value 超过 10KB 应拆分或压缩） |

## 问题说明

大 Key（Value 超过 10KB）会导致 Redis 在读写时阻塞较长时间，影响其他请求。常见场景：将大对象序列化后存入 Redis。

## 检查方法

1. 搜索大字符串直接 `set` 或大对象序列化写入
2. 搜索 `JSON.toJSONString` + `set` 组合
3. 搜索 `ObjectMapper.writeValueAsString` + Redis 操作

搜索模式：
- `grep_code` 搜索序列化操作后紧跟 Redis 写入

## 违规示例

```java
// ❌ 大对象直接写入 Redis
String json = objectMapper.writeValueAsString(largeOrderList); // 可能几十MB
redisTemplate.opsForValue().set("orders:all", json);
```

## 合规示例

```java
// ✅ 拆分为小 Key 或使用 Hash 分片
for (Order order : largeOrderList) {
    String key = "order:" + order.getId();
    redisTemplate.opsForValue().set(key, objectMapper.writeValueAsString(order), 1, TimeUnit.HOURS);
}
```
