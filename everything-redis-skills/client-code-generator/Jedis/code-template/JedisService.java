package com.example.redis.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.ScanParams;
import redis.clients.jedis.ScanResult;

import java.util.*;

/**
 * Jedis 服务层封装
 */
@Service
public class JedisService {

    private final JedisPool jedisPool;

    @Autowired
    public JedisService(JedisPool jedisPool) {
        this.jedisPool = jedisPool;
    }

    /**
     * 设置值（含过期时间，REDIS-007）
     */
    public void set(String key, String value, int expireSeconds) {
        try (Jedis jedis = jedisPool.getResource()) {
            jedis.setex(key, expireSeconds, value);
        }
    }

    /**
     * 获取值
     */
    public String get(String key) {
        try (Jedis jedis = jedisPool.getResource()) {
            return jedis.get(key);
        }
    }

    /**
     * 删除 Key
     */
    public Long delete(String key) {
        try (Jedis jedis = jedisPool.getResource()) {
            return jedis.del(key);
        }
    }

    /**
     * 使用 scan 替代 keys（REDIS-001）
     */
    public Set<String> scan(String pattern, int count) {
        Set<String> keys = new HashSet<>();
        try (Jedis jedis = jedisPool.getResource()) {
            ScanParams params = new ScanParams().match(pattern).count(count);
            String cursor = "0";
            do {
                ScanResult<String> result = jedis.scan(cursor, params);
                keys.addAll(result.getResult());
                cursor = result.getCursor();
            } while (!cursor.equals("0"));
        }
        return keys;
    }

    /**
     * 设置过期时间
     */
    public Boolean expire(String key, int seconds) {
        try (Jedis jedis = jedisPool.getResource()) {
            return jedis.expire(key, seconds);
        }
    }

    /**
     * 检查 Key 是否存在
     */
    public Boolean exists(String key) {
        try (Jedis jedis = jedisPool.getResource()) {
            return jedis.exists(key) > 0;
        }
    }

    /**
     * 递增
     */
    public Long incr(String key) {
        try (Jedis jedis = jedisPool.getResource()) {
            return jedis.incr(key);
        }
    }

    /**
     * Hash 操作 - 设置字段
     */
    public void hset(String key, String field, String value) {
        try (Jedis jedis = jedisPool.getResource()) {
            jedis.hset(key, field, value);
        }
    }

    /**
     * Hash 操作 - 获取字段值
     */
    public String hget(String key, String field) {
        try (Jedis jedis = jedisPool.getResource()) {
            return jedis.hget(key, field);
        }
    }

    /**
     * Hash 操作 - 获取所有字段
     */
    public Map<String, String> hgetAll(String key) {
        try (Jedis jedis = jedisPool.getResource()) {
            return jedis.hgetAll(key);
        }
    }

    /**
     * List 操作 - 右侧添加
     */
    public Long rpush(String key, String... values) {
        try (Jedis jedis = jedisPool.getResource()) {
            return jedis.rpush(key, values);
        }
    }

    /**
     * List 操作 - 左侧获取并移除
     */
    public String lpop(String key) {
        try (Jedis jedis = jedisPool.getResource()) {
            return jedis.lpop(key);
        }
    }
}
