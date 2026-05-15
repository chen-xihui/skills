# Java 模板：Jedis + Standalone - JedisConfig.java

JedisPool 配置，含连接池参数和密码注入。

生成目标文件：`JedisConfig.java`

```java
package com.example.redis.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

@Configuration
public class JedisConfig {

    @Value("${spring.data.redis.host}")
    private String host;

    @Value("${spring.data.redis.port}")
    private int port;

    @Value("${spring.data.redis.password}")
    private String password;

    @Value("${spring.data.redis.timeout:3000}")
    private int timeout;

    @Value("${spring.data.redis.jedis.pool.max-active:20}")
    private int maxActive;

    @Value("${spring.data.redis.jedis.pool.max-idle:10}")
    private int maxIdle;

    @Value("${spring.data.redis.jedis.pool.min-idle:5}")
    private int minIdle;

    @Value("${spring.data.redis.jedis.pool.max-wait:3000}")
    private long maxWait;

    @Bean
    public JedisPool jedisPool() {
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(maxActive);
        poolConfig.setMaxIdle(maxIdle);
        poolConfig.setMinIdle(minIdle);
        poolConfig.setMaxWaitMillis(maxWait);
        poolConfig.setTestOnBorrow(true);
        poolConfig.setTestOnReturn(false);

        return new JedisPool(poolConfig, host, port, timeout, password);
    }
}
```
