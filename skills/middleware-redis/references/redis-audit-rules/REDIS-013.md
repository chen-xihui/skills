# REDIS-013：大 Key 集合对象检查

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-013 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 集合对象（hash/list/set/zset）存储数据量建议控制在 5000 项以内 |

## 问题说明

大集合对象会导致单次操作耗时过长，阻塞 Redis 服务。

**建议限制**：
- String 对象：存储数据量建议控制在 10KB 以内
- 集合对象（hash、list、set、zset）：存储数据量建议控制在 5000 项以内

## 检查方法

- 评估业务场景中可能产生大集合的代码路径
- 检查 `LPUSH`/`RPUSH`/`SADD`/`HSET` 等命令的累积使用模式

## 合规建议

- 如存储数据量超过 5000 项，应均匀拆分至多个集合
- 推荐选择合适的数据压缩算法（JSON、XML、binary-data 压缩后存入）

## 违规示例

```java
// ❌ 向单个 Hash 写入大量数据
for (int i = 0; i < 100000; i++) {
    redisTemplate.opsForHash().put("large:hash", "field:" + i, value);
}
```

## 合规示例

```java
// ✅ 拆分为多个 Hash
int shard = i % 10;
String key = "hash:shard" + shard;
redisTemplate.opsForHash().put(key, "field:" + i, value);
```