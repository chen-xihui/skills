# Redis 客户端代码模板

本文件包含 Redis 客户端的代码模板，覆盖 Java（Lettuce/Jedis × Standalone/Sentinel/Cluster）、Go、Python。

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

## 5. Go 客户端模板

### 5.1 redis_client.go

```go
package redis

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/redis/go-redis/v9"
)

// Config Redis 连接配置
type Config struct {
	Addr         string `yaml:"addr"`
	Password     string `yaml:"password"` // 通过环境变量注入
	DB           int    `yaml:"db"`
	MaxRetries   int    `yaml:"max_retries"`
	DialTimeout  int    `yaml:"dial_timeout_ms"`
	ReadTimeout  int    `yaml:"read_timeout_ms"`
	WriteTimeout int    `yaml:"write_timeout_ms"`
	PoolSize     int    `yaml:"pool_size"`
	MinIdleConns int    `yaml:"min_idle_conns"`
}

// NewRedisClient 创建 Redis 客户端
func NewRedisClient(cfg Config) (*redis.Client, error) {
	password := cfg.Password
	if password == "" {
		password = os.Getenv("REDIS_PASSWORD")
	}

	rdb := redis.NewClient(&redis.Options{
		Addr:         cfg.Addr,
		Password:     password,
		DB:           cfg.DB,
		MaxRetries:   cfg.MaxRetries,
		DialTimeout:  time.Duration(cfg.DialTimeout) * time.Millisecond,
		ReadTimeout:  time.Duration(cfg.ReadTimeout) * time.Millisecond,
		WriteTimeout: time.Duration(cfg.WriteTimeout) * time.Millisecond,
		PoolSize:     cfg.PoolSize,
		MinIdleConns: cfg.MinIdleConns,
	})

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := rdb.Ping(ctx).Err(); err != nil {
		return nil, fmt.Errorf("Redis 连接失败: %w", err)
	}

	return rdb, nil
}
```

### 5.2 config.yaml

```yaml
redis:
  addr: "${REDIS_ADDR:localhost:6379}"
  password: "${REDIS_PASSWORD}"  # 通过环境变量注入
  db: 0
  max_retries: 3
  dial_timeout_ms: 5000
  read_timeout_ms: 3000
  write_timeout_ms: 3000
  pool_size: 20        # REDIS-004：连接池大小
  min_idle_conns: 5
```

---

## 6. Python 客户端模板

### 6.1 redis_client.py

```python
"""Redis 客户端封装"""

import os
import logging
from typing import List, Optional, Any

import redis
from redis.commands.core import Script

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis 客户端工具类"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: str = None,
        db: int = 0,
        max_connections: int = 20,
        socket_timeout: float = 3.0,
        socket_connect_timeout: float = 5.0,
        retry_on_timeout: bool = True,
    ):
        """
        初始化 Redis 客户端

        Args:
            host: Redis 主机地址
            port: Redis 端口
            password: 密码（优先从环境变量 REDIS_PASSWORD 获取）
            db: 数据库编号
            max_connections: 最大连接数（REDIS-004）
            socket_timeout: 读写超时（秒）
            socket_connect_timeout: 连接超时（秒）
            retry_on_timeout: 超时是否重试
        """
        _password = password or os.getenv("REDIS_PASSWORD", "")
        if not _password:
            logger.warning("Redis 密码未设置，请配置 REDIS_PASSWORD 环境变量")

        self.client = redis.Redis(
            host=host,
            port=port,
            password=_password,
            db=db,
            max_connections=max_connections,
            socket_timeout=socket_timeout,
            socket_connect_timeout=socket_connect_timeout,
            retry_on_timeout=retry_on_timeout,
            decode_responses=True,
        )
        logger.info("Redis 客户端初始化完成, host=%s:%d", host, port)

    def set(self, key: str, value: str, ex: int = None, px: int = None) -> bool:
        """
        设置值

        Args:
            key: 键
            value: 值
            ex: 过期时间（秒）（REDIS-007：建议始终设置）
            px: 过期时间（毫秒）
        """
        return self.client.set(key, value, ex=ex, px=px)

    def get(self, key: str) -> Optional[str]:
        """获取值"""
        return self.client.get(key)

    def delete(self, *keys: str) -> int:
        """删除 Key"""
        return self.client.delete(*keys)

    def scan(self, match: str = "*", count: int = 100) -> List[str]:
        """使用 scan 替代 keys（REDIS-001）"""
        keys = []
        cursor = 0
        while True:
            cursor, batch = self.client.scan(cursor=cursor, match=match, count=count)
            keys.extend(batch)
            if cursor == 0:
                break
        return keys

    def pipeline(self):
        """获取 Pipeline 对象（REDIS-005：批量操作使用 Pipeline）"""
        return self.client.pipeline()

    def script_load(self, script: str) -> str:
        """预加载 Lua 脚本（REDIS-006：使用 EVALSHA）"""
        return self.client.script_load(script)

    def evalsha(self, sha: str, numkeys: int, *keys_and_args) -> Any:
        """使用 EVALSHA 执行预加载的 Lua 脚本"""
        return self.client.evalsha(sha, numkeys, *keys_and_args)

    def expire(self, key: str, time_seconds: int) -> bool:
        """设置过期时间"""
        return self.client.expire(key, time_seconds)

    def close(self):
        """关闭连接"""
        self.client.close()
```

### 6.2 config.yaml

```yaml
redis:
  host: "${REDIS_HOST:localhost}"
  port: 6379
  password: "${REDIS_PASSWORD}"  # 通过环境变量注入
  db: 0
  max_connections: 20
  socket_timeout: 3.0
  socket_connect_timeout: 5.0
```

### 6.3 Pip 依赖

```
redis>=5.0.0
```
