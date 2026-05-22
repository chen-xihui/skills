# Redis Java 客户端代码模板

本文件包含 Java 客户端的所有代码模板：Lettuce/Jedis × Standalone/Sentinel/Cluster。

---

## 1. Java + Lettuce + Standalone

### 1.1 RedisConfig.java

```java
package com.example.redis.config;

import io.lettuce.core.ClientOptions;
import io.lettuce.core.SocketOptions;
import org.springframework.boot.autoconfigure.data.redis.RedisProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.connection.RedisStandaloneConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceClientConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

import java.time.Duration;

@Configuration
public class RedisConfig {

    @Bean
    public LettuceConnectionFactory redisConnectionFactory(RedisProperties props) {
        RedisStandaloneConfiguration config = new RedisStandaloneConfiguration();
        config.setHostName(props.getHost());
        config.setPort(props.getPort());
        config.setPassword(props.getPassword());

        SocketOptions socketOptions = SocketOptions.builder()
            .connectTimeout(Duration.ofMillis(5000))  // 连接超时 5s
            .keepAlive(true)
            .build();

        ClientOptions clientOptions = ClientOptions.builder()
            .socketOptions(socketOptions)
            .autoReconnect(true)
            .build();

        LettuceClientConfiguration clientConfig = LettuceClientConfiguration.builder()
            .commandTimeout(Duration.ofMillis(props.getTimeout().toMillis()))
            .clientOptions(clientOptions)
            .build();

        return new LettuceConnectionFactory(config, clientConfig);
    }

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.setHashKeySerializer(new StringRedisSerializer());
        template.setHashValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.afterPropertiesSet();
        return template;
    }
}
```

### 1.2 RedisService.java

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

### 1.3 application.yml

```yaml
spring:
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD}  # 通过环境变量注入，禁止明文
      timeout: 3000ms
      lettuce:
        pool:
          max-active: 20      # maxTotal（REDIS-004）
          max-idle: 10        # maxIdle
          min-idle: 5         # minIdle
          max-wait: 3000ms    # maxWaitMillis
        shutdown-timeout: 100ms
```

---

## 2. Java + Jedis + Standalone

### 2.1 JedisConfig.java

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

### 2.2 application.yml（Jedis）

```yaml
spring:
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD}
      timeout: 3000ms
      jedis:
        pool:
          max-active: 20
          max-idle: 10
          min-idle: 5
          max-wait: 3000ms
```

---

## 3. Java + Lettuce + Sentinel

### 3.1 RedisSentinelConfig.java

```java
package com.example.redis.config;

import io.lettuce.core.ClientOptions;
import io.lettuce.core.SocketOptions;
import org.springframework.boot.autoconfigure.data.redis.RedisProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.connection.RedisSentinelConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceClientConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

import java.time.Duration;
import java.util.Set;

@Configuration
public class RedisSentinelConfig {

    @Bean
    public RedisConnectionFactory redisConnectionFactory(RedisProperties props) {
        Set<String> sentinelHosts = props.getSentinel().getNodes();
        String masterName = props.getSentinel().getMaster();

        RedisSentinelConfiguration sentinelConfig = new RedisSentinelConfiguration()
            .master(masterName);
        for (String node : sentinelHosts) {
            String[] parts = node.split(":");
            sentinelConfig.sentinel(parts[0], Integer.parseInt(parts[1]));
        }
        sentinelConfig.setPassword(props.getPassword());

        SocketOptions socketOptions = SocketOptions.builder()
            .connectTimeout(Duration.ofMillis(5000))
            .keepAlive(true)
            .build();

        ClientOptions clientOptions = ClientOptions.builder()
            .socketOptions(socketOptions)
            .autoReconnect(true)
            .build();

        LettuceClientConfiguration clientConfig = LettuceClientConfiguration.builder()
            .commandTimeout(Duration.ofMillis(props.getTimeout().toMillis()))
            .clientOptions(clientOptions)
            .build();

        return new LettuceConnectionFactory(sentinelConfig, clientConfig);
    }

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.afterPropertiesSet();
        return template;
    }
}
```

### 3.2 application.yml（Sentinel）

```yaml
spring:
  data:
    redis:
      password: ${REDIS_PASSWORD}
      timeout: 3000ms
      sentinel:
        master: mymaster
        nodes: ${REDIS_SENTINEL_NODES:sentinel1:26379,sentinel2:26379,sentinel3:26379}
      lettuce:
        pool:
          max-active: 20
          max-idle: 10
          min-idle: 5
          max-wait: 3000ms
```

---

## 4. Java + Lettuce + Cluster

### 4.1 RedisClusterConfig.java

```java
package com.example.redis.config;

import io.lettuce.core.ClientOptions;
import io.lettuce.core.SocketOptions;
import io.lettuce.core.cluster.ClusterClientOptions;
import io.lettuce.core.cluster.ClusterTopologyRefreshOptions;
import org.springframework.boot.autoconfigure.data.redis.RedisProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisClusterConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceClientConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

import java.time.Duration;
import java.util.List;

@Configuration
public class RedisClusterConfig {

    @Bean
    public LettuceConnectionFactory redisConnectionFactory(RedisProperties props) {
        List<String> clusterNodes = props.getCluster().getNodes();
        RedisClusterConfiguration clusterConfig = new RedisClusterConfiguration(clusterNodes);
        clusterConfig.setPassword(props.getPassword());

        SocketOptions socketOptions = SocketOptions.builder()
            .connectTimeout(Duration.ofMillis(5000))
            .keepAlive(true)
            .build();

        ClusterTopologyRefreshOptions topologyRefreshOptions = ClusterTopologyRefreshOptions.builder()
            .enablePeriodicRefresh(Duration.ofMinutes(5))
            .enableAllAdaptiveRefreshTriggers()
            .build();

        ClusterClientOptions clusterClientOptions = ClusterClientOptions.builder()
            .socketOptions(socketOptions)
            .topologyRefreshOptions(topologyRefreshOptions)
            .autoReconnect(true)
            .build();

        LettuceClientConfiguration clientConfig = LettuceClientConfiguration.builder()
            .commandTimeout(Duration.ofMillis(props.getTimeout().toMillis()))
            .clientOptions(clusterClientOptions)
            .build();

        return new LettuceConnectionFactory(clusterConfig, clientConfig);
    }

    @Bean
    public RedisTemplate<String, Object> redisTemplate(LettuceConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.afterPropertiesSet();
        return template;
    }
}
```

### 4.2 application.yml（Cluster）

```yaml
spring:
  data:
    redis:
      password: ${REDIS_PASSWORD}
      timeout: 3000ms
      cluster:
        nodes: ${REDIS_CLUSTER_NODES:node1:6379,node2:6379,node3:6379}
        max-redirects: 3
      lettuce:
        pool:
          max-active: 20
          max-idle: 10
          min-idle: 5
          max-wait: 3000ms
```

---

## 7. Java + Lettuce 集群模式完整配置（含 TCP 参数）

> 此模板基于《公共技术服务接入操作程序》手册要求，包含 TCP keepalive 和 tcpUserTimeout 标准配置。

### 7.1 RedisConfig.java（Lettuce 集群 + TCP 参数 + 连接池）

```java
package com.example.redis.config;

import io.lettuce.core.ClientOptions;
import io.lettuce.core.SocketOptions;
import io.lettuce.core.cluster.ClusterClientOptions;
import io.lettuce.core.cluster.ClusterTopologyRefreshOptions;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.cache.annotation.CachingConfigurerSupport;
import org.springframework.data.redis.connection.RedisClusterConfiguration;
import org.springframework.data.redis.connection.RedisPassword;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.connection.lettuce.LettucePoolingClientConfiguration;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.StringRedisSerializer;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

import java.time.Duration;
import java.util.Arrays;

@Configuration
@EnableCaching
@ConfigurationProperties(prefix = "spring.redis")
public class RedisConfig extends CachingConfigurerSupport {

    /**
     * TCP_KEEPALIVE 标准值（参考《RedHat 7操作系统安装配置标准作业程序》）
     */
    private static final int TCP_KEEPALIVE_IDLE  = 150;
    private static final int TCP_KEEPALIVE_INTVL = 5;
    private static final int TCP_KEEPALIVE_CNT   = 6;

    /**
     * TCP_USER_TIMEOUT = TCP_KEEPIDLE + TCP_KEEPINTVL * TCP_KEEPCNT
     * 对于网络异常容忍度较低可配置为 30（避免过小无法容忍网络抖动）
     */
    private static final int TCP_USER_TIMEOUT = 180;

    @Value("${spring.redis.cluster.nodes}")
    private String clusterNodes;

    @Value("${spring.redis.cluster.max-redirects:3}")
    private int clusterMaxRedirects;

    @Value("${spring.redis.password}")
    private String password;

    @Value("${spring.redis.timeout:2000}")
    private Integer timeout;

    @Value("${spring.redis.lettuce.pool.max-active:20}")
    private Integer maxTotal;

    @Value("${spring.redis.lettuce.pool.max-wait:3000}")
    private Integer maxWait;

    @Value("${spring.redis.lettuce.pool.max-idle:10}")
    private Integer maxIdle;

    @Value("${spring.redis.lettuce.pool.min-idle:5}")
    private Integer minIdle;

    @Value("${spring.redis.lettuce.cluster.refresh.adaptive:true}")
    private boolean refreshAdaptive;

    @Value("${spring.redis.lettuce.cluster.refresh.period:30000}")
    private long refreshPeriod;

    /**
     * 获取缓存操作助手对象
     */
    @Bean
    public RedisTemplate<String, Object> redisTemplate() {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(getConnectionFactory());
        StringRedisSerializer serializer = new StringRedisSerializer();
        template.setKeySerializer(serializer);
        template.setHashKeySerializer(serializer);
        template.setValueSerializer(serializer);
        template.setHashValueSerializer(serializer);
        template.afterPropertiesSet();
        return template;
    }

    /**
     * 获取缓存工厂对象
     */
    @Bean
    public LettuceConnectionFactory getConnectionFactory() {
        RedisClusterConfiguration configuration = new RedisClusterConfiguration();
        String[] nodes = clusterNodes.split(",");
        for (String node : nodes) {
            String[] redisInfo = node.split(":");
            configuration.clusterNode(redisInfo[0], Integer.parseInt(redisInfo[1]));
        }
        configuration.setPassword(RedisPassword.of(password));
        configuration.setMaxRedirects(clusterMaxRedirects);

        LettuceConnectionFactory factory = new LettuceConnectionFactory(configuration, getPoolConfig());
        return factory;
    }

    /**
     * 获取缓存连接池配置对象
     */
    @Bean
    public LettucePoolingClientConfiguration getPoolConfig() {
        // 连接池配置
        GenericObjectPoolConfig<?> config = new GenericObjectPoolConfig<>();
        config.setMaxTotal(maxTotal);
        config.setMaxWaitMillis(maxWait);
        config.setMaxIdle(maxIdle);
        config.setMinIdle(minIdle);

        // 拓扑刷新配置
        ClusterTopologyRefreshOptions topologyRefreshOptions =
            ClusterTopologyRefreshOptions.builder()
                .enablePeriodicRefresh(refreshAdaptive)
                .refreshPeriod(Duration.ofMillis(refreshPeriod))
                .build();

        SocketOptions socketOptions = SocketOptions.builder()
            .keepAlive(SocketOptions.KeepAliveOptions.builder()
                .enable()
                .idle(Duration.ofSeconds(TCP_KEEPALIVE_IDLE))
                .interval(Duration.ofSeconds(TCP_KEEPALIVE_INTVL))
                .count(TCP_KEEPALIVE_CNT)
                .build())
            .tcpUserTimeout(SocketOptions.TcpUserTimeoutOptions.builder()
                .enable()
                .tcpUserTimeout(Duration.ofSeconds(TCP_USER_TIMEOUT))
                .build())
            .build();

        ClusterClientOptions clusterClientOptions = ClusterClientOptions.builder()
            .topologyRefreshOptions(topologyRefreshOptions)
            .socketOptions(socketOptions)
            .build();

        LettucePoolingClientConfiguration pool = LettucePoolingClientConfiguration.builder()
            .clientOptions(clusterClientOptions)
            .poolConfig(config)
            .commandTimeout(Duration.ofMillis(timeout))
            .build();
        return pool;
    }
}
```

### 7.2 application.yml（集群模式完整配置）

```yaml
spring:
  redis:
    password: ${REDIS_PASSWORD}
    timeout: 2000ms
    cluster:
      nodes: ${REDIS_CLUSTER_NODES:node1:6379,node2:6379,node3:6379}
      max-redirects: 3
    lettuce:
      pool:
        max-active: 20       # 最大连接数，应小于 200
        max-idle: 10         # 最大空闲连接，建议为 max-active/2
        min-idle: 5          # 最小空闲连接，高并发时可配为 max-idle 预热
        max-wait: 3000ms     # 最大阻塞等待时间，禁止使用默认值 -1
      cluster:
        refresh:
          adaptive: true     # 拓扑刷新开关，禁止配置为默认值 false
          period: 30000ms    # 拓扑刷新检查周期
```

### 7.3 Maven 依赖（含 netty-transport-native-epoll）

```xml
<!-- Lettuce 核心依赖 -->
<dependency>
    <groupId>io.lettuce</groupId>
    <artifactId>lettuce-core</artifactId>
    <version>6.3.0</version>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>

<!-- netty-transport-native-epoll：根据应用系统架构动态编译 -->
<profiles>
  <profile>
    <id>x86</id>
    <activation>
      <os>
        <arch>amd64</arch>
      </os>
    </activation>
    <dependencies>
      <dependency>
        <groupId>io.netty</groupId>
        <artifactId>netty-transport-native-epoll</artifactId>
        <version>4.1.100.Final</version>
        <classifier>linux-x86_64</classifier>
      </dependency>
    </dependencies>
  </profile>
  <profile>
    <id>arm64</id>
    <activation>
      <os>
        <arch>aarch64</arch>
      </os>
    </activation>
    <dependencies>
      <dependency>
        <groupId>io.netty</groupId>
        <artifactId>netty-transport-native-epoll</artifactId>
        <version>4.1.100.Final</version>
        <classifier>linux-arm64</classifier>
      </dependency>
    </dependencies>
  </profile>
</profiles>
```

### 7.4 Jedis 配置示例（含推荐参数）

```java
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
```

### 7.5 客户端配置参数对照表

**Jedis 连接配置**

| 配置参数 | 默认值 | 配置要求 |
|---------|--------|---------|
| maxTotal | 8 | 无特殊需求应小于 200 |
| maxIdle | 8 | 无特殊需求配置为 maxTotal/2 |
| minIdle | 0 | 高并发可配为 maxIdle 预热连接池 |
| maxWaitMillis | -1 | **禁止配置为默认值**；常见区间 50ms~5s |
| testOnBorrow | false | 建议配置为 true |
| testWhileIdle | false | 无特殊需求时配置为 true |
| timeBetweenEvictionRunsMillis | -1 | **禁止配置为默认值**；常见区间 20s~300s |

**Lettuce 连接配置**

| 配置参数 | 默认值 | 配置要求 |
|---------|--------|---------|
| lettuce.pool.max-active | 8 | 无特殊需求应小于 200 |
| lettuce.pool.max-idle | 8 | 无特殊需求配置为 max-active/2 |
| lettuce.pool.min-idle | 0 | 高并发可配为 max-idle 预热 |
| lettuce.pool.max-wait | -1 | **禁止配置为默认值**；常见区间 50ms~5s |
| lettuce.cluster.refresh.adaptive | false | **禁止配置为默认值** |

### 7.6 客户端版本要求

| 客户端 | 推荐版本 | 说明 |
|--------|---------|------|
| Jedis | ≥4.4.0 / ≥3.10 | 4.4.0、3.10.0 版本对 DNS 解析/服务断联功能进行优化 |
| Lettuce | ≥6.3.0 | 6.3.0 版本增加 tcpTimeout 参数配置 |
| Redisson | 不推荐 | 非开源技术目录软件 |