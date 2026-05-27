# JEDIS-008：必须开启 testWhileIdle

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-008 |
| 风险等级 | 风险 |
| 规则描述 | 连接池必须开启空闲连接检测，防止 NAT/防火墙回收导致半关闭 |

## 问题说明

在云环境或存在 NAT/防火墙的网络拓扑中，长期空闲的 TCP 连接会被中间网络设备静默回收。若连接池未开启空闲检测（testWhileIdle），应用从池中取到的可能是一个已被对端关闭的半关闭连接，导致首次命令执行失败，抛出 JedisConnectionException 或 EOFException。此类问题在流量低谷后的首次请求时尤为明显。

## 检查方法

- 静态分析：检查 JedisPoolConfig / GenericObjectPoolConfig 中是否调用 `setTestWhileIdle(true)`
- 检查 Spring Boot 配置中 `spring.redis.lettuce.pool.time-between-eviction-runs` 或 `spring.redis.jedis.pool.time-between-eviction-runs` 是否配置
- 脚本化检查：`python scripts/check_jedis_008.py <项目根目录>`

## 违规示例

```java
// 未开启 testWhileIdle，空闲连接可能已被防火墙回收但仍留在池中
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(200);
config.setMaxIdle(50);
config.setMinIdle(10);
// 缺少 config.setTestWhileIdle(true);
JedisPool pool = new JedisPool(config, "127.0.0.1", 6379, 2000, "password");
```

```yaml
# application.yml - 未配置空闲检测相关参数
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    jedis:
      pool:
        max-active: 200
        max-idle: 50
        min-idle: 10
        # 缺少 time-between-eviction-runs 配置
```

## 合规示例

```java
// 开启 testWhileIdle 并配合驱逐参数，定期检测并清除无效连接
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(200);
config.setMaxIdle(50);
config.setMinIdle(10);
config.setTestWhileIdle(true);
config.setMinEvictableIdleTimeMillis(60000);   // 空闲 60s 的连接可被驱逐
config.setTimeBetweenEvictionRunsMillis(30000); // 每 30s 执行一次驱逐扫描
config.setNumTestsPerEvictionRun(10);           // 每次扫描检测 10 个连接
JedisPool pool = new JedisPool(config, "127.0.0.1", 6379, 2000, "password");
```

```yaml
# application.yml - 开启空闲检测
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    jedis:
      pool:
        max-active: 200
        max-idle: 50
        min-idle: 10
        time-between-eviction-runs: 30s   # 每 30s 扫描一次
        min-evictable-idle: 60s           # 空闲 60s 可驱逐
```
