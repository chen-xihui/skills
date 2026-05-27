# JEDIS-006：禁止使用 CONFIG SET/REWRITE

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-006 |
| 风险等级 | 严重 |
| 规则描述 | 运行时禁止执行 CONFIG SET、CONFIG REWRITE 命令 |

## 问题说明

`CONFIG SET` 和 `CONFIG REWRITE` 可在运行时修改 Redis 服务端配置，属于高危操作。业务代码中若调用这些命令，可能导致：修改 `requirepass` 导致所有客户端认证失败；修改 `maxmemory` 触发大规模 key 淘汰甚至数据丢失；修改 `save` 配置导致 RDB 持久化异常引发 Redis 卡死；修改 `slaveof/replicaof` 导致主从切换。此类操作应仅限于运维平台、DBA 工具等受控场景，严禁在业务代码中使用。

## 检查方法

- 静态分析：搜索 `configSet`、`configRewrite`、`config_set`、`config_rewrite` 调用
- 脚本化检查：`python scripts/check_jedis_006.py <项目根目录>`

## 违规示例

```java
// 业务代码中运行时修改 Redis 配置
public void adjustMemory(String maxMemory) {
    try (Jedis jedis = pool.getResource()) {
        jedis.configSet("maxmemory", maxMemory);  // 危险：可能导致数据淘汰
        jedis.configRewrite();  // 危险：持久化配置变更到磁盘
    }
}
```

```java
// 动态关闭持久化
public void disablePersistence() {
    try (Jedis jedis = pool.getResource()) {
        jedis.configSet("save", "");  // 危险：关闭 RDB 持久化，宕机数据丢失
        jedis.configRewrite();
    }
}
```

```java
// Spring Data Redis 中使用 CONFIG SET
@Autowired
private RedisTemplate<String, String> redisTemplate;

public void updateRedisConfig(String param, String value) {
    RedisConnection connection = redisTemplate.getConnectionFactory().getConnection();
    connection.setConfig(param, value);  // 等价于 CONFIG SET，同样危险
}
```

```java
// 通过 Jedis Cluster 执行 CONFIG SET
public void clusterConfigSet(String param, String value) {
    jedisCluster.configSet(param, value);  // Cluster 模式下影响更广
    jedisCluster.configRewrite();
}
```

## 合规示例

```java
// 业务代码仅通过正常 API 操作数据，不修改配置
public void safeSetWithTTL(String key, String value, int seconds) {
    try (Jedis jedis = pool.getResource()) {
        jedis.setex(key, seconds, value);  // 使用业务 API，不触碰配置
    }
}
```

```java
// 运维平台场景：CONFIG 操作需要审批和审计
@Service
@ConditionalOnProperty(name = "redis.admin.enabled", havingValue = "true")
public class RedisAdminService {
    private static final Logger auditLog = LoggerFactory.getLogger("REDIS_AUDIT");

    public void configSetWithApproval(String param, String value, String operator) {
        // 记录审计日志
        auditLog.info("CONFIG SET by={}, param={}, value={}", operator, param, value);
        try (Jedis jedis = pool.getResource()) {
            jedis.configSet(param, value);
            jedis.configRewrite();
        }
    }
}
```

```java
// 通过配置文件管理 Redis 参数，而非运行时修改
// application.yml
// spring:
//   redis:
//     timeout: 3000
//     lettuce:
//       pool:
//         max-active: 100

// 启动时参数通过部署配置注入，运行时不再变更
@Configuration
public class RedisConfig {
    @Value("${redis.maxmemory-policy:allkeys-lru}")
    private String maxMemoryPolicy;

    // 仅在启动日志中记录预期配置，不做运行时修改
    @PostConstruct
    public void logConfig() {
        log.info("Redis maxmemory-policy expected: {}", maxMemoryPolicy);
    }
}
```
