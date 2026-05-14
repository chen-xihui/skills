# Nacos 代码优化检查规则详细说明

本文件包含 NACOS-001 ~ NACOS-007 共 7 条检查规则的详细说明和检查方法。

---

## NACOS-001：服务订阅是否启用本地快照

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-001 |
| 风险等级 | 🔵 建议 |
| 规则描述 | 服务订阅是否启用本地快照（enableLocalSnapshot） |

### 问题说明

启用本地快照后，Nacos 客户端会将获取的配置缓存到本地文件。当 Nacos 服务端不可用时，客户端可以从本地快照加载配置，提高系统容灾能力。

### 检查方法

1. 搜索 Nacos 配置中是否设置 `enableLocalSnapshot=true`
2. 搜索 Properties / YAML 配置文件中的 `enableLocalSnapshot` 字段
3. 如未找到该配置，标记为问题

搜索模式：
- `grep_code` 搜索 `enableLocalSnapshot`、`enable-local-snapshot`
- `search_codebase` 搜索 "local snapshot" 或 "本地快照" 相关配置

### 违规示例

```java
// ❌ 未启用本地快照
Properties properties = new Properties();
properties.put("serverAddr", serverAddr);
// 没有 enableLocalSnapshot 设置（默认为 false）
ConfigService configService = ConfigFactory.createConfigService(properties);
```

### 合规示例

```java
// ✅ 启用本地快照
Properties properties = new Properties();
properties.put("serverAddr", serverAddr);
properties.put("enableLocalSnapshot", "true");
ConfigService configService = ConfigFactory.createConfigService(properties);
```

---

## NACOS-002：长轮询超时是否合理

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-002 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 长轮询超时是否合理（configLongPollTimeout 建议 ≤ 30s） |

### 问题说明

`configLongPollTimeout` 控制客户端等待配置变更通知的超时时间。值过大会导致客户端感知配置变更延迟，值过小会增加服务端压力。建议设置为 30s 以内。

### 检查方法

1. 搜索 `configLongPollTimeout` 配置值
2. 检查值是否超过 30000ms（30s）
3. 如未设置，使用默认值不算问题（默认 30s）

搜索模式：
- `grep_code` 搜索 `configLongPollTimeout`、`config-long-poll-timeout`
- 检查配置值是否 > 30000

### 违规示例

```yaml
# ❌ 长轮询超时过大
nacos:
  config-long-poll-timeout: 60000  # 60s，超过建议值
```

### 合规示例

```yaml
# ✅ 长轮询超时合理
nacos:
  config-long-poll-timeout: 30000  # 30s
```

---

## NACOS-003：是否循环调用 getConfig 而未使用 Listener

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-003 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 是否循环调用 getConfig 而未使用 Listener |

### 问题说明

在循环中反复调用 `getConfig` 轮询配置变更，会浪费大量网络资源和 Nacos 服务端处理能力。应使用 Nacos 的 Listener 机制订阅配置变更，实现推送而非轮询。

### 检查方法

1. 搜索循环体内的 `getConfig` 调用
2. 检查是否有对应的 `addListener` 调用
3. 排除初始化阶段的一次性调用（如 `@PostConstruct` 中）

搜索模式：
- `grep_code` 搜索循环体（`while`、`for`）内的 `getConfig` 调用
- `search_codebase` 搜索 "getConfig" 相关代码，检查上下文是否在循环中

### 违规示例

```java
// ❌ 循环中轮询配置
while (running) {
    String config = configService.getConfig(dataId, group, 5000);
    // 处理配置...
    Thread.sleep(10000);
}
```

### 合规示例

```java
// ✅ 使用 Listener 订阅配置变更
configService.addListener(dataId, group, new Listener() {
    @Override
    public Executor getExecutor() {
        return Executors.newSingleThreadExecutor();
    }

    @Override
    public void receiveConfigInfo(String configInfo) {
        // 处理配置变更
    }
});
```

---

## NACOS-004：密码是否硬编码

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-004 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 密码是否硬编码在源码中 |

### 问题说明

将 Nacos 密码硬编码在 Java/Go/Python 源码中存在严重安全隐患。应通过环境变量、Spring Cloud Config、Vault 等方式注入。

### 检查方法

1. 搜索源码中 `password` 字段的直接赋值
2. 排除配置文件（bootstrap.yml 等）中的 `${...}` 占位符形式
3. 搜索 `Properties.put("password", ...)` 中的硬编码值

搜索模式：
- `grep_code` 搜索 `.java` 文件中的 `password\s*=\s*"[^${]`
- 排除 `@Value("${...}")` 形式的安全用法

### 违规示例

```java
// ❌ 密码硬编码
properties.put("password", "MySecretPassword123");
```

### 合规示例

```java
// ✅ 密码通过配置注入
@Value("${nacos.password}")
private String password;

// bootstrap.yml 中：
// password: ${NACOS_PASSWORD}
```

---

## NACOS-005：心跳间隔、权重等是否符合最佳实践

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-005 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 心跳间隔、权重等是否符合最佳实践 |

### 问题说明

心跳间隔过短会增加 Nacos 服务端负担，过长则服务下线感知延迟大。权重设置不合理会影响负载均衡效果。

### 检查方法

1. 搜索 `heartBeatInterval`、`heart-beat-interval` 配置值
2. 搜索 `weight` 配置值
3. 检查值是否在合理范围内

推荐值：
- 心跳间隔：3-5 秒（默认 5s）
- 权重：1.0（默认值），根据实例性能调整

搜索模式：
- `grep_code` 搜索 `heartBeatInterval`、`heart-beat-interval`、`weight`

### 违规示例

```yaml
# ❌ 心跳间隔过短
nacos:
  discovery:
    heart-beat-interval: 500  # 0.5s，频率过高
    weight: 0.01              # 权重过低，几乎不分流
```

### 合规示例

```yaml
# ✅ 心跳间隔和权重合理
nacos:
  discovery:
    heart-beat-interval: 5000  # 5s
    weight: 1.0
```

---

## NACOS-006：是否缺少异常处理和重试配置

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-006 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 是否缺少异常处理和重试配置 |

### 问题说明

Nacos 客户端调用处缺少 try-catch 和重试逻辑，在网络抖动或 Nacos 服务端不可用时可能导致应用崩溃或功能异常。

### 检查方法

1. 搜索 Nacos 客户端调用处（`getConfig`、`registerInstance`、`deregisterInstance` 等）
2. 检查是否有 try-catch 包裹
3. 检查是否有重试配置

搜索模式：
- `grep_code` 搜索 Nacos API 调用，检查上下文是否有 try-catch
- `search_codebase` 搜索 Nacos 客户端调用

### 违规示例

```java
// ❌ 无异常处理
String config = configService.getConfig(dataId, group, 5000);
return config;
```

### 合规示例

```java
// ✅ 有异常处理和重试
@Retryable(value = NacosException.class, maxAttempts = 3, backoff = @Backoff(delay = 1000))
public String getConfigWithRetry(String dataId, String group) {
    try {
        return configService.getConfig(dataId, group, 5000);
    } catch (NacosException e) {
        log.error("获取配置失败: dataId={}, group={}", dataId, group, e);
        throw new RuntimeException("配置获取失败", e);
    }
}
```

---

## NACOS-007：命名空间是否按环境隔离

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-007 |
| 风险等级 | 🔵 建议 |
| 规则描述 | 命名空间是否按环境隔离 |

### 问题说明

不同环境（DEV/SIT/SRV）应使用不同的 Nacos 命名空间进行隔离，避免配置和服务注册互相干扰。

### 检查方法

1. 搜索 `namespace` 配置
2. 检查不同环境的配置文件是否使用不同 namespace
3. 如所有环境使用同一个 namespace，标记为建议

搜索模式：
- `grep_code` 搜索 `namespace` 配置
- 检查是否存在 `bootstrap-dev.yml`、`bootstrap-sit.yml` 等多环境配置
- `search_codebase` 搜索 "namespace" 相关配置

### 违规示例

```yaml
# ❌ 所有环境使用相同 namespace（默认 public）
# bootstrap-dev.yml
nacos:
  namespace: ""

# bootstrap-sit.yml
nacos:
  namespace: ""  # 与 DEV 共用命名空间
```

### 合规示例

```yaml
# ✅ 不同环境使用不同 namespace
# bootstrap-dev.yml
nacos:
  namespace: "dev-namespace-id"

# bootstrap-sit.yml
nacos:
  namespace: "sit-namespace-id"
```
