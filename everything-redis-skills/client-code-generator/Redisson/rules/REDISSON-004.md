# REDISSON-004：必须开启 TCP KeepAlive

| 属性 | 说明 |
|------|------|
| 规则ID | REDISSON-004 |
| 风险等级 | 风险 |
| 规则描述 | 配置文件中必须设置 keepAlive: true |

## 问题说明

Redisson 与 Redis 之间通过长连接通信。在云环境或跨机房部署中，中间网络设备（如负载均衡器、防火墙、NAT 网关）会清理空闲连接。若未开启 TCP KeepAlive，当网络设备静默丢弃连接后，Redisson 客户端仍认为连接有效，发送请求时才发现连接已断开，导致请求超时失败。更严重的是，这种"半开连接"状态难以自动恢复，可能引发级联超时和连接池耗尽。

开启 TCP KeepAlive 后，操作系统会定期发送心跳探测包，即使应用层无数据交互也能维持连接活性，及时发现并清理已断开的连接。

## 检查方法

- 静态分析：检查 Redisson 配置文件（YAML/JSON）中是否包含 `keepAlive: true`
- 静态分析：检查 Java Config 中是否调用了 `setKeepAlive(true)`
- 检查是否在 `useClusterServers()` 或 `useSingleServer()` 配置中设置了 keepAlive
- 脚本化检查：`python scripts/check_redisson_004.py <项目根目录>`

## 违规示例

```yaml
# redisson-config.yml
# 违规：未配置 keepAlive 或 keepAlive: false
clusterServersConfig:
  nodeAddresses:
    - "redis://127.0.0.1:7000"
    - "redis://127.0.0.1:7001"
    - "redis://127.0.0.1:7002"
  connectTimeout: 3000
  timeout: 3000
  retryAttempts: 3
  retryInterval: 500
  # keepAlive 未设置，默认为 false
```

```java
// 违规：Java Config 中未设置 keepAlive
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
              .setTimeout(3000)
              .setRetryAttempts(3)
              .setRetryInterval(500);
              // 未调用 setKeepAlive(true)
        return Redisson.create(config);
    }
}
```

## 合规示例

```yaml
# redisson-config.yml
# 合规：显式设置 keepAlive: true
clusterServersConfig:
  nodeAddresses:
    - "redis://127.0.0.1:7000"
    - "redis://127.0.0.1:7001"
    - "redis://127.0.0.1:7002"
  connectTimeout: 3000
  timeout: 3000
  retryAttempts: 3
  retryInterval: 500
  keepAlive: true
```

```java
// 合规：Java Config 中显式设置 keepAlive
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
              .setTimeout(3000)
              .setRetryAttempts(3)
              .setRetryInterval(500)
              .setKeepAlive(true); // 合规：显式开启 TCP KeepAlive
        return Redisson.create(config);
    }
}
```
