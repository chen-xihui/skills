# Java 模板：Lettuce + Cluster - RedisClusterConfig.java

Cluster 连接配置，含拓扑刷新和自动重连。

生成目标文件：`RedisClusterConfig.java`

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
