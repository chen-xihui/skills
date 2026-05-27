package com.example.redis.config;

import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import org.redisson.config.SentinelServersConfig;
import org.redisson.config.ClusterServersConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.util.StringUtils;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Redisson Sentinel 模式配置
 */
@Configuration
public class RedissonSentinelConfig {

    @Value("${spring.redis.sentinel.master}")
    private String masterName;

    @Value("${spring.redis.sentinel.nodes}")
    private String sentinelNodes;

    @Value("${spring.redis.password:}")
    private String password;

    @Value("${spring.redis.database:0}")
    private int database;

    @Value("${spring.redis.sentinel.read-mode:slave}")
    private String readMode;

    @Bean(destroyMethod = "shutdown")
    public RedissonClient redissonSentinelClient() {
        Config config = new Config();
        
        List<String> nodes = Arrays.stream(sentinelNodes.split(","))
            .map(String::trim)
            .collect(Collectors.toList());
        
        SentinelServersConfig sentinelConfig = config.useSentinelServers()
            .setMasterName(masterName)
            .addSentinelAddress(nodes.toArray(new String[0]))
            .setDatabase(database)
            .setMasterConnectionPoolSize(64)
            .setSlaveConnectionPoolSize(64)
            .setConnectTimeout(10000)
            .setTimeout(3000)
            .setRetryAttempts(3)
            .setRetryInterval(1500);
        
        // 设置密码
        if (StringUtils.hasText(password)) {
            sentinelConfig.setPassword(password);
        }
        
        // 设置读模式
        if ("slave".equalsIgnoreCase(readMode)) {
            sentinelConfig.setReadMode(org.redisson.api.ReadMode.READ_SLAVE);
        } else {
            sentinelConfig.setReadMode(org.redisson.api.ReadMode.READ_ONLY);
        }
        
        return Redisson.create(config);
    }
}
