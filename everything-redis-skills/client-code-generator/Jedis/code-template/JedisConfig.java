package com.example.redis.config;

import org.apache.commons.pool2.impl.GenericObjectPoolConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

@Configuration
public class JedisConfig {

    @Value("${spring.redis.host}")
    private String host;

    @Value("${spring.redis.port}")
    private int port;

    @Value("${spring.redis.password}")
    private String password;

    @Value("${spring.redis.timeout:2000}")
    private int timeout;

    @Value("${spring.redis.jedis.pool.max-active:20}")
    private int maxActive;

    @Value("${spring.redis.jedis.pool.max-idle:10}")
    private int maxIdle;

    @Value("${spring.redis.jedis.pool.min-idle:5}")
    private int minIdle;

    @Value("${spring.redis.jedis.pool.max-wait:3000}")
    private long maxWait;

    @Value("${spring.redis.jedis.pool.test-on-borrow:true}")
    private boolean testOnBorrow;

    @Value("${spring.redis.jedis.pool.test-while-idle:true}")
    private boolean testWhileIdle;

    @Value("${spring.redis.jedis.pool.time-between-eviction-runs-millis:30000}")
    private long timeBetweenEvictionRunsMillis;

    @Bean
    public JedisPool jedisPool() {
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(maxActive);
        poolConfig.setMaxIdle(maxIdle);
        poolConfig.setMinIdle(minIdle);
        poolConfig.setMaxWaitMillis(maxWait);
        poolConfig.setTestOnBorrow(testOnBorrow);
        poolConfig.setTestWhileIdle(testWhileIdle);
        poolConfig.setTimeBetweenEvictionRunsMillis(timeBetweenEvictionRunsMillis);

        return new JedisPool(poolConfig, host, port, timeout, password);
    }
}
