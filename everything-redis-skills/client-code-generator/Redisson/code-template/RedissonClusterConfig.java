package com.example.redis.config;

import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import org.redisson.config.ClusterServersConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Redisson Cluster 模式配置
 */
@Configuration
public class RedissonClusterConfig {

    @Value("${spring.redis.cluster.nodes}")
    private String clusterNodes;

    @Value("${spring.redis.cluster.max-redirects:3}")
    private int maxRedirects;

    @Value("${spring.redis.password:}")
    private String password;

    @Value("${spring.redis.timeout:3000}")
    private int timeout;

    @Bean(destroyMethod = "shutdown")
    public RedissonClient redissonClusterClient() {
        Config config = new Config();
        
        List<String> nodes = Arrays.stream(clusterNodes.split(","))
            .map(String::trim)
            .collect(Collectors.toList());
        
        ClusterServersConfig clusterConfig = config.useClusterServers()
            .addNodeAddress(nodes.toArray(new String[0]))
            .setMaxConnectionPoolSize(64)
            .setMasterConnectionPoolSize(64)
            .setSlaveConnectionPoolSize(64)
            .setConnectTimeout(10000)
            .setTimeout(timeout)
            .setRetryAttempts(3)
            .setRetryInterval(1500)
            .setMaxRedirects(maxRedirects);
        
        if (password != null && !password.isEmpty()) {
            clusterConfig.setPassword(password);
        }
        
        return Redisson.create(config);
    }
}
