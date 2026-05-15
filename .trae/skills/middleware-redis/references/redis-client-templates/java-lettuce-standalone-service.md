# Java 模板：Lettuce + Standalone - RedisService.java

RedisService 服务类，含 scan 替代 keys、Pipeline 批量执行、过期时间设置。

生成目标文件：`RedisService.java`

```java
package com.example.redis.service;

import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ScanOptions;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.TimeUnit;

@Service
public class RedisService {

    private final RedisTemplate<String, Object> redisTemplate;

    public RedisService(RedisTemplate<String, Object> redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    /** 设置值（含过期时间，REDIS-007） */
    public void set(String key, Object value, long timeout, TimeUnit unit) {
        redisTemplate.opsForValue().set(key, value, timeout, unit);
    }

    /** 获取值 */
    public Object get(String key) {
        return redisTemplate.opsForValue().get(key);
    }

    /** 删除 Key */
    public Boolean delete(String key) {
        return redisTemplate.delete(key);
    }

    /** 使用 scan 替代 keys（REDIS-001） */
    public Set<String> scan(String pattern, int count) {
        Set<String> keys = new HashSet<>();
        ScanOptions options = ScanOptions.scanOptions()
            .match(pattern)
            .count(count)
            .build();
        try (var cursor = redisTemplate.scan(options)) {
            while (cursor.hasNext()) {
                keys.add(cursor.next());
            }
        }
        return keys;
    }

    /** 使用 Pipeline 批量执行（REDIS-005） */
    public List<Object> executePipeline(List<Runnable> operations) {
        return redisTemplate.executePipelined((connection) -> {
            for (Runnable op : operations) {
                op.run();
            }
            return null;
        });
    }

    /** 设置过期时间 */
    public Boolean expire(String key, long timeout, TimeUnit unit) {
        return redisTemplate.expire(key, timeout, unit);
    }
}
```
