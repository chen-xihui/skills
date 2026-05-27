# JEDIS-013：建议开启 testOnBorrow

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-013 |
| 风险等级 | 提示 |
| 规则描述 | 建议开启连接借用检测（testOnBorrow），防止获取到半关闭连接导致业务首次命令失败 |

## 问题说明

连接池中的空闲连接可能因 Redis 端主动断开（如 maxclients 淘汰、restart）、网络设备超时回收等原因变为半关闭状态。若未开启 testOnBorrow，应用从池中借出的连接可能已失效，首次执行命令时抛出 JedisConnectionException 或 EOFException。开启 testOnBorrow 后，每次借出连接前会先执行 PING 命令验证连接可用性，牺牲极少量性能换取更高可靠性。对于高并发低延迟场景，若已开启 testWhileIdle，可酌情关闭 testOnBorrow 以减少 PING 开销。

## 检查方法

- 静态分析：检查 JedisPoolConfig 中是否调用 `setTestOnBorrow(true)`
- 检查 Spring Boot 配置中是否配置了相关参数
- 脚本化检查：`python scripts/check_jedis_013.py <项目根目录>`

## 违规示例

```java
// 未开启 testOnBorrow，可能借到半关闭连接
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(200);
config.setMaxIdle(50);
config.setMinIdle(10);
config.setTestWhileIdle(true);  // 仅开启空闲检测，但借用时仍可能拿到刚失效的连接
// 缺少 config.setTestOnBorrow(true);
JedisPool pool = new JedisPool(config, "127.0.0.1", 6379, 300);
```

```yaml
# application.yml - 未配置 testOnBorrow
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    jedis:
      pool:
        max-active: 200
        max-idle: 50
        min-idle: 10
        # 缺少 test-on-borrow: true
```

## 合规示例

```java
// 开启 testOnBorrow，借用前 PING 检测连接可用性
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(200);
config.setMaxIdle(50);
config.setMinIdle(10);
config.setTestOnBorrow(true);   // 借用时检测
config.setTestWhileIdle(true);  // 空闲时检测（双重保障）
config.setMinEvictableIdleTimeMillis(60000);
config.setTimeBetweenEvictionRunsMillis(30000);
JedisPool pool = new JedisPool(config, "127.0.0.1", 6379, 300);
```

```java
// 高并发场景下，若已开启 testWhileIdle 且驱逐间隔足够短，可关闭 testOnBorrow 以减少 PING 开销
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(500);
config.setMaxIdle(100);
config.setMinIdle(20);
config.setTestOnBorrow(false);  // 高并发下关闭以减少延迟
config.setTestWhileIdle(true);
config.setTimeBetweenEvictionRunsMillis(10000);  // 缩短驱逐间隔到 10s
config.setNumTestsPerEvictionRun(50);            // 增加每次检测数
JedisPool pool = new JedisPool(config, "127.0.0.1", 6379, 300);
```

```yaml
# application.yml - 开启 testOnBorrow
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    jedis:
      pool:
        max-active: 200
        max-idle: 50
        min-idle: 10
        test-on-borrow: true
```
