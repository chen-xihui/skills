# Redis 开发指引

## 四、开发指引

### 4.1 客户端版本要求

| 客户端类型 | 版本要求 | 是否纳入开源技术目录 | 说明 |
|-----------|---------|-------------------|------|
| Jedis | ≥4.4.0 / ≥3.10 | 是 | 4.4.0、3.10.0 版本对 DNS 解析/服务断联功能进行优化 |
| Lettuce | ≥6.3.0 | 是 | 6.3.0 版本增加 tcpTimeout 参数配置 |
| Redisson | / | 否 | 非开源技术目录软件，不推荐使用 |

### 4.2 客户端配置参数

**Jedis 连接配置**

| 配置参数 | 默认值 | 配置要求 |
|---------|--------|---------|
| maxTotal | 8 | 无特殊需求应小于 200，根据并发度和性能测试结果确认 |
| maxIdle | 8 | 无特殊需求配置为 maxTotal/2 |
| minIdle | 0 | 低并发可配 0；高并发可配为 maxIdle 预热连接池 |
| maxWaitMillis | -1 | **禁止配置为默认值**；常见区间 50ms~5s |
| testOnBorrow | false | 建议配置为 true，确保连接可用性 |
| testOnReturn | false | 建议配置为 true；testOnBorrow 为 true 时可用默认值 |
| timeout | 2000ms | 无特殊需求使用默认值 |
| connection-timeout | 2000ms | 无特殊需求使用默认值 |
| blockWhenExhausted | true | 无特殊需求使用默认值 |
| testWhileIdle | false | 无特殊需求时配置为 true |
| timeBetweenEvictionRunsMillis | -1 | **禁止配置为默认值**；常见区间 20s~300s |

**Lettuce 连接配置**

| 配置参数 | 默认值 | 配置要求 |
|---------|--------|---------|
| lettuce.pool.max-active | 8 | 无特殊需求应小于 200 |
| lettuce.pool.max-idle | 8 | 无特殊需求配置为 max-active/2 |
| lettuce.pool.min-idle | 0 | 低并发可配 0；高并发可配为 max-idle 预热 |
| lettuce.pool.max-wait | -1 | **禁止配置为默认值**；常见区间 50ms~5s |
| timeout | 2000ms | 无特殊需求使用默认值 |
| connection-timeout | 2000ms | 无特殊需求使用默认值 |
| lettuce.cluster.refresh.adaptive | false | **禁止配置为默认值** |
| lettuce.cluster.refresh.period | 30s | 无特殊需求使用默认值 |

### 4.3 连接数计算

| 客户端 | 配置参数 | 服务模式 | 总连接数公式 |
|--------|---------|---------|-------------|
| Jedis / Lettuce | maxTotal / max-active | 主从模式 | 配置连接数 × 客户端副本数 |
| Jedis / Lettuce | maxTotal / max-active | 集群模式 | (配置连接数 × 分片数) × 客户端副本数 |
| Jedis / Lettuce | maxTotal / max-active | 容灾模式 | 配置连接数 × 客户端副本数 |

**容灾模式连接预热**：客户端连接 Proxy 均匀分布，需配置 minIdle 与 maxIdle 为相同大小。

### 4.4 拓扑刷新配置

集群模式下，客户端应配置拓扑刷新，在缓存服务重启、扩容、主从切换、异常宕机时正常重连。

- **Jedis**：无需额外配置
- **Lettuce**：
  - Spring Boot 版本应大于 2.3.0
  - 配置拓扑刷新开关和检查周期参数

### 4.5 Lettuce TCP 参数配置

Lettuce 客户端应在 SocketOptions 中增加 keepalive 和 tcpUserTimeout 参数：

```java
// TCP_KEEPALIVE 标准值
private static final int TCP_KEEPALIVE_IDLE = 150;
private static final int TCP_KEEPALIVE_INTVL = 5;
private static final int TCP_KEEPALIVE_CNT = 6;
// TCP_USER_TIMEOUT = TCP_KEEPIDLE + TCP_KEEPINTVL * TCP_KEEPCNT
private static final int TCP_USER_TIMEOUT = 180;

SocketOptions socketOptions = SocketOptions.builder()
    .keepAlive(SocketOptions.KeepAliveOptions.builder()
        .enable()
        .idle(Duration.ofSeconds(TCP_KEEPALIVE_IDLE))
        .interval(Duration.ofSeconds(TCP_KEEPALIVE_INTVL))
        .count(TCP_KEEPALIVE_CNT)
        .build())
    .tcpUserTimeout(SocketOptions.TcpUserTimeoutOptions.builder()
        .enable()
        .tcpUserTimeout(Duration.ofSeconds(TCP_USER_TIMEOUT))
        .build())
    .build();
```

同时引入 netty-transport-native-epoll 依赖（根据架构动态编译 x86/arm64）。

### 4.6 命令使用规范

**高危命令（禁止使用）**
- CONFIG、FLUSHALL、FLUSHDB 等修改服务端的命令

**批量命令（合理使用）**
- 推荐合理使用 MGET、MSET 或 Pipeline 等批量命令
- 控制单次处理的数据量
- 不宜使用集合对象整存整取命令：HGETALL、SMEMBERS、LRANGE 0 -1、ZRANGE -inf +inf、LREM、ZUNION 等

**全库匹配命令（禁止使用）**
- 不能使用 Keys 命令，推荐使用 Scan 命令和前缀关键字匹配替代

**事务命令（谨慎使用）**
- 缓存服务不支持强一致性事务，仅提供乐观锁和批量操作的最终一致性
- SETNX：仅在键不存在时设置值，可用于设计锁
- WATCH：监听键值是否被修改，被修改则放弃执行事务
- MULTI/EXEC：开启和提交事务，错误命令不会回滚已执行的命令
- DISCARD：取消事务

**键空间事件**

| 参数 | 说明 |
|------|------|
| K | 监听 Keyspace 事件，订阅事件为 __keyspace@<db>__<键值> |
| E | 监听 Keyevent 事件，订阅事件为 __keyevent@<db>__<指令> |
| g/$/l/s/z/t/x/e/m | 分别监听通用/String/List/Set/SortedSet/流/过期/淘汰/未命中命令 |
| A | 监听上述所有命令 |

### 4.7 容错开发

**健康检查**
- 根据依赖程度设计缓存检查接口（Ping、Set/Get 定时检查）
- 新增应用客户端访问缓存健康指标，增加应用告警
- 设计健康探测、自动重启（仅在强依赖且无法改造时使用）

**异常处置**

| 措施 | 说明 |
|------|------|
| 服务熔断 | 合理配置超时时间，访问异常时熔断缓存请求 |
| 服务降级 | 访问异常时降级访问数据库，保障核心接口正常返回 |
| 错误处理 | 合理捕获异常，根据错误类型打印关键日志 |
| 请求重试 | 针对网络抖动等场景捕获特定异常并重试，重试接口应满足幂等性 |

### 4.8 容灾开发

**Proxy 组件兼容性**
- 客户端按主从模式配置
- 配置重连相关配置，确保容灾切换后自动重连
- 不能使用 keys 命令，应使用 scan 替代
- 不能使用 multi、exec、discard 等事务命令

**数据一致性**
- Proxy 开启读写分离后，仅支持最终一致性，存在同步时延
- 推荐在读取接口中增加重试逻辑

**容灾切换方案**

| 方案 | 说明 |
|------|------|
| 主动切换 | 控制器定时检测主机房健康状态，异常后自动切换流量 |
| 手动切换 | 控制器检测异常后，需运维人员介入手动切换 |

### 4.9 安全编码

- **服务认证**：应开启客户端认证，根据密码规范配置接入密码
- **数据加密**：业务数据应加密后存储至缓存服务