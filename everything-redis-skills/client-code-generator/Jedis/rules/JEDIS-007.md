# JEDIS-007：连接池参数必须完整配置

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-007 |
| 风险等级 | 风险 |
| 规则描述 | JedisPool 必须配置 maxTotal、maxIdle、minIdle、maxWaitMillis 四项核心参数 |

## 问题说明

JedisPool 使用 Apache Commons Pool2 作为底层连接池实现，默认配置无法满足生产环境需求。未设置 `maxTotal` 时默认值为 8，高并发下连接数不足导致请求排队；未设置 `maxIdle` 时默认值为 8，连接创建后不会合理回收造成资源浪费；未设置 `minIdle` 时默认值为 0，空闲时所有连接被销毁，突发流量时需要冷启动创建连接；未设置 `maxWaitMillis` 时默认值为 -1（无限等待），连接耗尽时请求永久阻塞，导致线程池耗尽和 Full GC。

## 检查方法

- 静态分析：检查 JedisPoolConfig 或 GenericObjectPoolConfig 是否同时设置 `setMaxTotal`、`setMaxIdle`、`setMinIdle`、`setMaxWaitMillis`
- 脚本化检查：`python scripts/check_jedis_007.py <项目根目录>`

## 违规示例

```java
// 使用默认配置，所有参数均为默认值
JedisPool pool = new JedisPool("127.0.0.1", 6379);
// maxTotal=8, maxIdle=8, minIdle=0, maxWaitMillis=-1(无限等待)
```

```java
// 仅设置部分参数，遗漏关键配置
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(100);  // 仅设了 maxTotal
// 遗漏 maxIdle、minIdle、maxWaitMillis
JedisPool pool = new JedisPool(config, "127.0.0.1", 6379);
```

```java
// Spring Boot 配置遗漏关键参数
@Bean
public JedisPool jedisPool() {
    JedisPoolConfig config = new JedisPoolConfig();
    config.setMaxTotal(200);
    config.setMaxIdle(50);
    // 遗漏 minIdle 和 maxWaitMillis
    return new JedisPool(config, "127.0.0.1", 6379, 3000, "password");
}
```

```yaml
# application.yml 遗漏关键参数
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    lettuce:
      pool:
        max-active: 200
        max-idle: 50
        # 遗漏 min-idle 和 max-wait
```

## 合规示例

```java
// 完整配置所有核心参数
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(100);        // 最大连接数
config.setMaxIdle(50);          // 最大空闲连接数
config.setMinIdle(10);          // 最小空闲连接数，预热防冷启动
config.setMaxWaitMillis(3000);  // 获取连接最大等待时间 3s，超时抛异常而非无限阻塞
JedisPool pool = new JedisPool(config, "127.0.0.1", 6379, 3000, "password");
```

```java
// Spring Bean 完整配置
@Configuration
public class RedisConfig {

    @Bean
    public JedisPool jedisPool() {
        JedisPoolConfig config = new JedisPoolConfig();
        config.setMaxTotal(100);
        config.setMaxIdle(50);
        config.setMinIdle(10);
        config.setMaxWaitMillis(3000);
        config.setTestWhileIdle(true);         // 空闲检测
        config.setTimeBetweenEvictionRunsMillis(30000);  // 检测间隔 30s
        config.setMinEvictableIdleTimeMillis(60000);     // 空闲 60s 可回收
        return new JedisPool(config, "127.0.0.1", 6379, 3000, "password");
    }
}
```

```yaml
# application.yml 完整配置（Spring Boot + Lettuce）
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    password: password
    timeout: 3000ms
    lettuce:
      pool:
        max-active: 100       # 对应 maxTotal
        max-idle: 50          # 对应 maxIdle
        min-idle: 10          # 对应 minIdle
        max-wait: 3000ms      # 对应 maxWaitMillis
      shutdown-timeout: 200ms
```

```java
// JedisCluster 完整配置
@Configuration
public class RedisClusterConfig {

    @Bean
    public JedisCluster jedisCluster() {
        JedisPoolConfig config = new JedisPoolConfig();
        config.setMaxTotal(100);
        config.setMaxIdle(50);
        config.setMinIdle(10);
        config.setMaxWaitMillis(3000);
        Set<HostAndPort> nodes = new HashSet<>();
        nodes.add(new HostAndPort("127.0.0.1", 7001));
        nodes.add(new HostAndPort("127.0.0.1", 7002));
        nodes.add(new HostAndPort("127.0.0.1", 7003));
        return new JedisCluster(nodes, 3000, 3, config);
    }
}
```
