# JEDIS-012：必须设置 commandTimeout

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-012 |
| 风险等级 | 风险 |
| 规则描述 | 必须设置命令超时时间，禁止默认无限等待，防止线程堆积导致服务不可用 |

## 问题说明

Jedis 客户端默认的 timeout 取决于构造函数版本，部分重载未指定 timeout 时默认为 0（无限等待）或 2000ms。若未显式设置合理的命令超时时间，当 Redis 出现慢查询、网络抖动或主从切换时，业务线程将长时间阻塞在 Redis 调用上，导致 Tomcat 线程池打满、服务整体不可用。不同操作应设置不同超时：普通 KV 操作 100-500ms，Scan/聚合操作 1-3s。

## 检查方法

- 静态分析：检查 JedisPool/JedisCluster 构造函数是否指定 timeout 参数
- 检查 Spring Boot 配置中 `spring.redis.timeout` 是否设置
- 检查是否存在 `new JedisPool(config, host, port)` 等未指定 timeout 的构造方式
- 脚本化检查：`python scripts/check_jedis_012.py <项目根目录>`

## 违规示例

```java
// 未指定 timeout，可能使用默认值 0（无限等待）或 2000ms
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(200);
JedisPool pool = new JedisPool(config, "127.0.0.1", 6379);
//                                                 ^^ 缺少 timeout 参数
```

```java
// JedisCluster 未指定 timeout
Set<HostAndPort> nodes = new HashSet<>();
nodes.add(new HostAndPort("127.0.0.1", 7001));
JedisCluster cluster = new JedisCluster(nodes, poolConfig);
// 未指定 connectionTimeout 和 soTimeout
```

```java
// 直接创建 Jedis 未设置超时
Jedis jedis = new Jedis("127.0.0.1", 6379);
jedis.connect();  // 使用默认超时
```

```yaml
# application.yml - 未配置超时
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    # 缺少 timeout 配置
```

## 合规示例

```java
// 普通 KV 操作：设置 200ms 超时
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(200);
JedisPool pool = new JedisPool(config, "127.0.0.1", 6379, 200);
//                                                                ^^^ 200ms commandTimeout
```

```java
// JedisCluster 显式设置 connectionTimeout 和 soTimeout
Set<HostAndPort> nodes = new HashSet<>();
nodes.add(new HostAndPort("127.0.0.1", 7001));
nodes.add(new HostAndPort("127.0.0.1", 7002));
nodes.add(new HostAndPort("127.0.0.1", 7003));
int connectionTimeout = 200;  // 连接超时 200ms
int soTimeout = 300;          // 读取超时 300ms
JedisCluster cluster = new JedisCluster(nodes, connectionTimeout, soTimeout, 3, "password", poolConfig);
```

```java
// Scan 等耗时操作使用独立连接池，设置较长超时
JedisPoolConfig scanConfig = new JedisPoolConfig();
scanConfig.setMaxTotal(10);
JedisPool scanPool = new JedisPool(scanConfig, "127.0.0.1", 6379, 3000);
//                                                                ^^^^ Scan 操作 3s 超时
```

```yaml
# application.yml - 按场景配置超时
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    timeout: 300ms  # 命令超时 300ms
```
