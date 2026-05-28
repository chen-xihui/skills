# LETTUCE-003：应用退出必须 shutdown

| 属性 | 说明 |
|------|------|
| 规则ID | LETTUCE-003 |
| 风险等级 | 严重 |
| 规则描述 | 应用退出时必须调用 RedisClient.shutdown() 或 RedisClusterClient.shutdown()，释放 Netty 线程与连接资源 |

## 问题说明

Lettuce 底层依赖 Netty 的 EventLoopGroup 维持线程模型。若应用退出时未调用 shutdown()，Netty 线程池（NIO线程、定时任务线程）不会自动终止，导致：1）JVM 无法正常退出，进程挂起；2）在容器化环境（Spring Boot fat jar、K8s Pod）中造成 classloader 泄漏，旧实例的类无法被 GC 回收，反复部署后 Metaspace 溢出；3）连接未优雅关闭，Redis 服务端残留 CLOSE_WAIT 连接。

## 检查方法

- 静态分析：检查 RedisClient / RedisClusterClient 的创建位置，确认在 @PreDestroy、DisposableBean.destroy()、ServletContextListener.contextDestroyed() 或 shutdown hook 中调用了 shutdown()
- 检查 Spring Boot 自动配置场景下是否依赖了 LettuceConnectionFactory 的默认销毁逻辑
- 脚本化检查：`python scripts/check_lettuce_003.py <项目根目录>`

## 违规示例

```java
// 创建 RedisClient 但未在退出时调用 shutdown
@Component
public class RedisService {

    private final RedisClient client;
    private final StatefulRedisConnection<String, String> connection;

    public RedisService() {
        this.client = RedisClient.create("redis://127.0.0.1:6379");
        this.connection = client.connect();
    }

    public String getValue(String key) {
        return connection.sync().get(key);
    }

    // 缺少 @PreDestroy 或 destroy 方法调用 client.shutdown()
    // 应用退出时 Netty 线程残留，JVM 无法正常退出
}
```

```java
// 手动创建 RedisClient 在 main 方法中，未注册 shutdown hook
public class Application {
    public static void main(String[] args) {
        RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
        StatefulRedisConnection<String, String> connection = client.connect();
        connection.sync().set("key", "value");
        // 未调用 client.shutdown()，进程退出后 Netty 线程残留
    }
}
```

## 合规示例

```java
// Spring Bean 中通过 @PreDestroy 确保 shutdown
@Component
public class RedisService implements DisposableBean {

    private final RedisClient client;
    private final StatefulRedisConnection<String, String> connection;

    public RedisService() {
        this.client = RedisClient.create("redis://127.0.0.1:6379");
        this.connection = client.connect();
    }

    public String getValue(String key) {
        return connection.sync().get(key);
    }

    @PreDestroy
    @Override
    public void destroy() {
        if (connection != null) {
            connection.close();
        }
        if (client != null) {
            client.shutdown();  // 释放 Netty 线程资源
        }
    }
}
```

```java
// 非 Spring 场景下注册 shutdown hook
public class Application {
    public static void main(String[] args) {
        RedisClient client = RedisClient.create("redis://127.0.0.1:6379");
        StatefulRedisConnection<String, String> connection = client.connect();

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            connection.close();
            client.shutdown();  // 优雅关闭，释放所有 Netty 资源
        }));

        connection.sync().set("key", "value");
    }
}
```

```java
// Spring Boot 自动配置场景，LettuceConnectionFactory 已内置 destroy 逻辑
// 只需确保不要手动创建 RedisClient 而绕过 Spring 管理
@Configuration
public class RedisConfig {

    @Bean
    public LettuceConnectionFactory redisConnectionFactory() {
        // Spring 管理的 LettuceConnectionFactory 会在销毁时自动调用 shutdown
        return new LettuceConnectionFactory(new RedisStandaloneConfiguration("127.0.0.1", 6379));
    }
}
```
