# REDISSON-002：禁止循环创建 RedissonClient

| 属性 | 说明 |
|------|------|
| 规则ID | REDISSON-002 |
| 风险等级 | 严重 |
| 规则描述 | RedissonClient 必须单例，禁止循环内创建 |

## 问题说明

`RedissonClient` 内部维护了 Netty 的 `EventLoopGroup`、连接池、线程池等重型资源。每次调用 `Redisson.create()` 都会创建一套独立的 Netty 线程组和连接池。如果在循环内创建 RedissonClient，将导致连接风暴：大量 TCP 连接瞬间涌向 Redis 服务端，耗尽 Redis 的最大连接数（maxclients），同时本地也会因线程数暴增而 OOM。即使不在循环中，多次创建 RedissonClient 而不 shutdown 同样会逐步耗尽资源。

## 检查方法

- 静态分析：搜索所有 `Redisson.create()` 调用，检查是否出现在循环体内
- 静态分析：检查 RedissonClient 是否通过 Spring Bean 或单例模式管理
- 检查是否存在方法内局部变量反复创建 RedissonClient 的模式
- 脚本化检查：`python scripts/check_redisson_002.py <项目根目录>`

## 违规示例

```java
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;

@Service
public class InventoryService {

    public void batchUpdateStock(List<String> productIds) {
        // 违规：在循环内每次创建新的 RedissonClient
        // 每次迭代都建立新的 TCP 连接池和 Netty 线程组
        for (String productId : productIds) {
            Config config = new Config();
            config.useClusterServers()
                  .addNodeAddress("redis://127.0.0.1:6379");
            RedissonClient client = Redisson.create(config);
            try {
                RMap<String, Integer> stockMap = client.getMap("stock:" + productId);
                stockMap.put("quantity", 100);
            } finally {
                // 即使调用了 shutdown，循环内反复创建/销毁开销极大
                client.shutdown();
            }
        }
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

@Configuration
public class RedissonConfig {

    @Bean(destroyMethod = "shutdown")
    public RedissonClient redissonClient() {
        Config config = new Config();
        config.useClusterServers()
              .addNodeAddress("redis://127.0.0.1:7000",
                              "redis://127.0.0.1:7001",
                              "redis://127.0.0.1:7002")
              .setConnectTimeout(3000)
              .setTimeout(3000);
        return Redisson.create(config);
    }
}

@Service
public class InventoryService {

    @Autowired
    private RedissonClient redissonClient; // 合规：注入全局单例 RedissonClient

    public void batchUpdateStock(List<String> productIds) {
        for (String productId : productIds) {
            // 合规：复用同一个 RedissonClient 实例
            RMap<String, Integer> stockMap = redissonClient.getMap("stock:" + productId);
            stockMap.put("quantity", 100);
        }
    }
}
```
