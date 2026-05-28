# JEDIS-009：禁止超大 Pipeline

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-009 |
| 风险等级 | 风险 |
| 规则描述 | 单次 Pipeline 命令数建议控制在 100-1000 以内，禁止一次 Pipeline 提交上万条命令 |

## 问题说明

Pipeline 将多条命令打包一次发送，服务端依次执行后将结果缓冲在输出缓冲区中，最后一次性返回。若单次 Pipeline 包含数万条命令，会导致：1）Redis 输出缓冲区暴涨，触发 client-output-buffer-limit 甚至连接被强制断开；2）JVM 堆内存暴涨，大量 Response 对象同时驻留内存引发 GC 压力甚至 OOM；3）Pipeline 执行期间阻塞其他客户端请求，导致延迟毛刺。

## 检查方法

- 静态分析：检查 Pipeline 循环边界，若循环上限超过 1000 且无分批逻辑则违规
- 检查是否存在 `pipeline.sync()` / `pipeline.exec()` 前的无限循环或超大循环
- 脚本化检查：`python scripts/check_jedis_009.py <项目根目录>`

## 违规示例

```java
// 一次性提交 10 万条命令，Redis 输出缓冲区爆炸
Jedis jedis = jedisPool.getResource();
Pipeline pipeline = jedis.pipelined();
for (int i = 0; i < 100000; i++) {
    pipeline.set("key:" + i, "value:" + i);
}
pipeline.sync();
jedis.close();
```

```java
// List 批量写入未做分片，列表可能包含数万条数据
public void batchSet(List<KeyValuePair> pairs) {
    Jedis jedis = jedisPool.getResource();
    Pipeline pipeline = jedis.pipelined();
    for (KeyValuePair pair : pairs) {  // pairs 可能有 50000+ 条
        pipeline.set(pair.getKey(), pair.getValue());
    }
    pipeline.sync();
    jedis.close();
}
```

## 合规示例

```java
// 分批发送，每批 500 条
private static final int PIPELINE_BATCH_SIZE = 500;

public void batchSet(List<KeyValuePair> pairs) {
    Jedis jedis = jedisPool.getResource();
    try {
        Pipeline pipeline = jedis.pipelined();
        int count = 0;
        for (KeyValuePair pair : pairs) {
            pipeline.set(pair.getKey(), pair.getValue());
            count++;
            if (count % PIPELINE_BATCH_SIZE == 0) {
                pipeline.sync();
                pipeline = jedis.pipelined();  // 开启新一批
            }
        }
        if (count % PIPELINE_BATCH_SIZE != 0) {
            pipeline.sync();  // 处理剩余不足一批的数据
        }
    } finally {
        jedis.close();
    }
}
```

```java
// 使用 Stream 分批处理
private static final int PIPELINE_BATCH_SIZE = 500;

public void batchHSet(Map<String, Map<String, String>> keyFieldValues) {
    List<String> keys = new ArrayList<>(keyFieldValues.keySet());
    for (int from = 0; from < keys.size(); from += PIPELINE_BATCH_SIZE) {
        int to = Math.min(from + PIPELINE_BATCH_SIZE, keys.size());
        List<String> batch = keys.subList(from, to);
        try (Jedis jedis = jedisPool.getResource()) {
            Pipeline pipeline = jedis.pipelined();
            for (String key : batch) {
                Map<String, String> fields = keyFieldValues.get(key);
                pipeline.hset(key, fields);
            }
            pipeline.sync();
        }
    }
}
```
