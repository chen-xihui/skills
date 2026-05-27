# JEDIS-004：禁止未关闭 Pipeline

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-004 |
| 风险等级 | 严重 |
| 规则描述 | Pipeline 必须调用 close() 关闭，防止连接泄漏 |

## 问题说明

Jedis 的 Pipeline 对象持有底层连接引用，使用完毕后必须调用 `close()` 归还资源。若 Pipeline 未关闭，底层连接无法归还连接池，导致可用连接逐渐减少，最终出现 `Could not get a resource from the pool` 错误。此问题在异常路径中尤为常见——当 Pipeline 执行中途抛出异常时跳过了 close 调用。

## 检查方法

- 静态分析：检查 `jedis.pipelined()` 调用后是否在 try-with-resources 或 finally 块中调用 `close()`
- 脚本化检查：`python scripts/check_jedis_004.py <项目根目录>`

## 违规示例

```java
// Pipeline 未关闭，连接泄漏
public void batchSet(Map<String, String> kvPairs) {
    Jedis jedis = pool.getResource();
    Pipeline pipeline = jedis.pipelined();
    for (Map.Entry<String, String> entry : kvPairs.entrySet()) {
        pipeline.set(entry.getKey(), entry.getValue());
    }
    pipeline.sync();
    jedis.close();
    // pipeline 未 close()，连接可能泄漏
}
```

```java
// 异常路径 Pipeline 未关闭
public Map<String, String> batchGet(List<String> keys) {
    Jedis jedis = pool.getResource();
    Pipeline pipeline = jedis.pipelined();
    for (String key : keys) {
        pipeline.get(key);
    }
    List<Object> results = pipeline.syncAndReturnAll();  // 若此处抛异常
    pipeline.close();  // 此行不执行
    jedis.close();     // 此行也不执行
    // 双重泄漏：pipeline 和 jedis 均未关闭
    Map<String, String> map = new HashMap<>();
    for (int i = 0; i < keys.size(); i++) {
        map.put(keys.get(i), (String) results.get(i));
    }
    return map;
}
```

```java
// Pipeline 与 Jedis 分离管理，遗漏关闭
public void updateCache(List<String> keys, String value) {
    try (Jedis jedis = pool.getResource()) {
        Pipeline pipeline = jedis.pipelined();
        for (String key : keys) {
            pipeline.setex(key, 3600, value);
        }
        pipeline.sync();
        // jedis 会自动关闭，但 pipeline 内部状态未清理
    }
}
```

## 合规示例

```java
// 使用 try-with-resources 同时管理 Jedis 和 Pipeline
public void batchSet(Map<String, String> kvPairs) {
    try (Jedis jedis = pool.getResource()) {
        try (Pipeline pipeline = jedis.pipelined()) {
            for (Map.Entry<String, String> entry : kvPairs.entrySet()) {
                pipeline.set(entry.getKey(), entry.getValue());
            }
            pipeline.sync();
        }
    }
}
```

```java
// Pipeline 批量读取，正确关闭
public Map<String, String> batchGet(List<String> keys) {
    Map<String, String> result = new HashMap<>();
    try (Jedis jedis = pool.getResource()) {
        try (Pipeline pipeline = jedis.pipelined()) {
            for (String key : keys) {
                pipeline.get(key);
            }
            List<Object> results = pipeline.syncAndReturnAll();
            for (int i = 0; i < keys.size(); i++) {
                result.put(keys.get(i), (String) results.get(i));
            }
        }
    }
    return result;
}
```

```java
// 传统 try-finally 确保关闭（兼容旧版本）
public void updateCache(List<String> keys, String value) {
    Jedis jedis = null;
    Pipeline pipeline = null;
    try {
        jedis = pool.getResource();
        pipeline = jedis.pipelined();
        for (String key : keys) {
            pipeline.setex(key, 3600, value);
        }
        pipeline.sync();
    } finally {
        if (pipeline != null) {
            pipeline.close();
        }
        if (jedis != null) {
            jedis.close();
        }
    }
}
```
