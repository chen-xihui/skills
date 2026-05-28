# REDISSON-003：应用退出必须 shutdown

| 属性 | 说明 |
|------|------|
| 规则ID | REDISSON-003 |
| 风险等级 | 严重 |
| 规则描述 | 必须调用 redisson.shutdown() |

## 问题说明

RedissonClient 内部维护了 Netty 的 `EventLoopGroup`（默认包含 CPU 核数 * 2 个线程）、定时任务线程池、连接池等资源。如果应用退出时未调用 `shutdown()`，这些非守护线程将阻止 JVM 正常退出，导致进程挂起。在 Spring Boot 热部署或容器重启场景中，未 shutdown 的 RedissonClient 会造成 ClassLoader 泄漏：旧 ClassLoader 引用的 Netty 线程仍在运行，持有对旧类的引用，导致 PermGen/Metaspace 无法回收，反复部署后最终 OOM。

## 检查方法

- 静态分析：检查所有 `Redisson.create()` 调用，确认对应的 shutdown 逻辑是否存在
- 静态分析：在 Spring 项目中检查是否存在 `@PreDestroy` 或 `@Bean(destroyMethod = "shutdown")`
- 检查是否通过 `DisposableBean` 接口实现销毁回调
- 脚本化检查：`python scripts/check_redisson_003.py <项目根目录>`

## 违规示例

```java
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RedissonConfig {

    @Bean
    // 违规：未指定 destroyMethod，Spring 容器关闭时不会调用 shutdown()
    // Netty 线程池残留，JVM 无法正常退出，ClassLoader 泄漏
    public RedissonClient redissonClient() {
        Config config = new Config();
        config.useClusterServers()
              .addNodeAddress("redis://127.0.0.1:7000",
                              "redis://127.0.0.1:7001",
                              "redis://127.0.0.1:7002");
        return Redisson.create(config);
    }
}
```

## 合规示例

```java
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import javax.annotation.PreDestroy;

// 方式一：通过 @Bean(destroyMethod) 声明销毁方法（推荐）
@Configuration
public class RedissonConfig {

    @Bean(destroyMethod = "shutdown")
    public RedissonClient redissonClient() {
        Config config = new Config();
        config.useClusterServers()
              .addNodeAddress("redis://127.0.0.1:7000",
                              "redis://127.0.0.1:7001",
                              "redis://127.0.0.1:7002");
        return Redisson.create(config);
    }
}

// 方式二：通过 @PreDestroy 手动调用 shutdown
@Configuration
public class RedissonConfigV2 {

    private RedissonClient redissonClient;

    @Bean
    public RedissonClient redissonClient() {
        Config config = new Config();
        config.useClusterServers()
              .addNodeAddress("redis://127.0.0.1:7000",
                              "redis://127.0.0.1:7001",
                              "redis://127.0.0.1:7002");
        this.redissonClient = Redisson.create(config);
        return this.redissonClient;
    }

    @PreDestroy
    public void destroy() {
        if (redissonClient != null && !redissonClient.isShutdown()) {
            redissonClient.shutdown();
        }
    }
}

// 方式三：实现 DisposableBean 接口
@Configuration
public class RedissonConfigV3 implements DisposableBean {

    private RedissonClient redissonClient;

    @Bean
    public RedissonClient redissonClient() {
        Config config = new Config();
        config.useClusterServers()
              .addNodeAddress("redis://127.0.0.1:7000",
                              "redis://127.0.0.1:7001",
                              "redis://127.0.0.1:7002");
        this.redissonClient = Redisson.create(config);
        return this.redissonClient;
    }

    @Override
    public void destroy() {
        if (redissonClient != null && !redissonClient.isShutdown()) {
            redissonClient.shutdown();
        }
    }
}
```
