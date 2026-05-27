# LETTUCE-007：shareNativeConnection 需明确配置

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-007 |
| 风险等级 | 提示 |
| 规则描述 | LettuceConnectionFactory 默认 shareNativeConnection=true（共享单连接），需明确配置连接模式，避免误引入 commons-pool2 但未正确启用 |

## 问题说明

Spring Data Redis 的 LettuceConnectionFactory 默认 shareNativeConnection=true，即所有操作共享一个 Netty 连接（Lettuce 天然多路复用，单连接即可支撑高并发）。但很多开发者误以为需要连接池，引入了 commons-pool2 依赖并将 shareNativeConnection 设为 false，却未正确配置 pool 参数（maxActive、maxIdle 等），导致连接池使用默认值（maxActive=8），反而降低了吞吐量。另一种常见误区是引入了 commons-pool2 依赖但未将 shareNativeConnection 设为 false，连接池实际未生效。

## 检查方法

- 静态分析：检查 pom.xml / build.gradle 中是否引入了 commons-pool2 依赖
- 若引入了 commons-pool2，检查 LettuceConnectionFactory 是否配置了 `setShareNativeConnection(false)` 和合理的 pool 参数
- 若未引入 commons-pool2，确认 shareNativeConnection=true（默认值）即可满足需求
- 脚本化检查：`python scripts/check_lettuce_007.py <项目根目录>`

## 违规示例

```java
// 引入了 commons-pool2 但未关闭 shareNativeConnection，连接池未生效
@Configuration
public class RedisConfig {

    @Bean
    public LettuceConnectionFactory redisConnectionFactory() {
        RedisStandaloneConfiguration config = new RedisStandaloneConfiguration("127.0.0.1", 6379);
        LettuceConnectionFactory factory = new LettuceConnectionFactory(config);
        // shareNativeConnection 默认 true，连接池不会生效
        // commons-pool2 依赖被引入但白费
        return factory;
    }
}
```

```java
// 关闭了 shareNativeConnection 但未配置连接池参数，使用默认极小值
@Configuration
public class RedisConfig {

    @Bean
    public LettuceConnectionFactory redisConnectionFactory() {
        RedisStandaloneConfiguration config = new RedisStandaloneConfiguration("127.0.0.1", 6379);

        LettuceClientConfiguration clientConfig = LettuceClientConfiguration.builder()
            .poolConfig(new GenericObjectPoolConfig<>())  // 使用默认 pool 配置，maxTotal=8
            .build();

        LettuceConnectionFactory factory = new LettuceConnectionFactory(config, clientConfig);
        factory.setShareNativeConnection(false);  // 关闭共享但池参数过小
        return factory;
    }
}
```

## 合规示例

```java
// 大多数场景：保持默认 shareNativeConnection=true，无需连接池
@Configuration
public class RedisConfig {

    @Bean
    public LettuceConnectionFactory redisConnectionFactory() {
        RedisStandaloneConfiguration config = new RedisStandaloneConfiguration("127.0.0.1", 6379);
        // Lettuce 天然多路复用，单连接即可高并发
        // 不需要 commons-pool2 依赖
        return new LettuceConnectionFactory(config);
    }
}
```

```java
// 需要阻塞命令等场景确实需要连接池时：明确配置所有参数
@Configuration
public class RedisConfig {

    @Bean
    public LettuceConnectionFactory redisConnectionFactory() {
        RedisStandaloneConfiguration config = new RedisStandaloneConfiguration("127.0.0.1", 6379);

        GenericObjectPoolConfig poolConfig = new GenericObjectPoolConfig();
        poolConfig.setMaxTotal(20);      // 最大连接数
        poolConfig.setMaxIdle(10);       // 最大空闲连接
        poolConfig.setMinIdle(5);        // 最小空闲连接
        poolConfig.setMaxWaitMillis(1000); // 获取连接最大等待时间

        LettuceClientConfiguration clientConfig = LettuceClientConfiguration.builder()
            .poolConfig(poolConfig)
            .commandTimeout(Duration.ofMillis(500))
            .build();

        LettuceConnectionFactory factory = new LettuceConnectionFactory(config, clientConfig);
        factory.setShareNativeConnection(false);  // 关闭共享，启用连接池
        return factory;
    }
}
```

```yaml
# application.yml - Spring Boot 明确配置连接池
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    lettuce:
      pool:
        max-active: 20    # 最大连接数
        max-idle: 10      # 最大空闲
        min-idle: 5       # 最小空闲
        max-wait: 1000ms  # 获取连接等待时间
      shutdown-timeout: 200ms
```
