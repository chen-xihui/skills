# Java 模板：Lettuce + Sentinel - RedisSentinelConfig.java

Sentinel 连接配置，含自动发现 Sentinel 节点和主从切换。

生成目标文件：`RedisSentinelConfig.java`

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
