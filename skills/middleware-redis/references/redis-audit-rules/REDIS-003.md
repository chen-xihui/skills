# REDIS-003：热 Key 风险检查

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-003 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 热 Key 风险检查（高频读写的 Key 应考虑本地缓存） |

## 问题说明

热 Key（高频读写的 Key）可能导致单个 Redis 节点压力过大。建议使用本地缓存（如 Caffeine）缓存热 Key 数据，减少 Redis 访问频率。

## 检查方法

1. 分析代码中高频调用的 Redis 操作模式
2. 搜索循环中或高频方法中的 `get` 调用
3. 检查是否有本地缓存机制

搜索模式：
- `grep_code` 搜索高频方法中的 `redisTemplate.opsForValue().get`
- `search_codebase` 搜索 Redis 操作与本地缓存（Caffeine/Guava Cache）的组合

## 违规示例

```java
// ❌ 每次请求都访问 Redis
public User getUser(String userId) {
    return (User) redisTemplate.opsForValue().get("user:" + userId);
}
```

## 合规示例

```java
// ✅ 使用本地缓存 + Redis 二级缓存
@Cacheable(value = "localCache", key = "'user:' + #userId")
public User getUser(String userId) {
    return (User) redisTemplate.opsForValue().get("user:" + userId);
}
```