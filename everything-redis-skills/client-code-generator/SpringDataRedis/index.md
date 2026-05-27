# Spring Data Redis 客户端代码生成

## 能力说明

Spring Data Redis 是 Spring Data 家族成员，提供统一的 Redis 访问抽象。**Spring Boot 2.x 默认使用 Lettuce 作为底层客户端**，本能力提供 Spring Data Redis 的代码生成、配置生成和代码审计。

## 适用场景

适用于已使用 Spring/Spring Boot 框架的项目，通过 Spring Data Redis 统一抽象访问 Redis。

## 支持模式

| 模式 | 触发关键词 | 说明 |
|------|-----------|------|
| Standalone | standalone、单机 | 单节点部署 |
| Sentinel | sentinel、哨兵 | 高可用哨兵模式 |
| Cluster | cluster、集群 | 分片集群模式 |

## 代码模板

| 文件 | 路径 | 说明 |
|------|------|------|
| RedisConfig.java | [code-template/RedisConfig.java](./code-template/RedisConfig.java) | Redis 配置类 |
| RedisTemplateConfig.java | [code-template/RedisTemplateConfig.java](./code-template/RedisTemplateConfig.java) | 序列化配置 |
| application.yml | [code-template/application.yml](./code-template/application.yml) | 配置文件 |

## 审计规则

### Spring Data Redis 专属规则

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| SDR-001 | RedisTemplate 必须配置 keySerializer 和 valueSerializer | 🔴 严重 |
| SDR-002 | 禁止使用 redisTemplate.keys() 和 opsForKeys().keys()，应使用 SCAN | 🟡 风险 |
| SDR-003 | LettuceConnectionFactory 必须配置 commandTimeout | 🟡 风险 |

### 集群通用规则

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| CLUSTER-001 | maxAttempts 应设置 3-5，禁止过大值 | 🔴 严重 |
| CLUSTER-002 | 集群总连接数 = 节点数 × maxTotal，必须评估 | 🟡 风险 |
| CLUSTER-003 | 禁止业务层重试循环包裹集群调用 | 🟡 风险 |

详细规则：[rules/index.md](./rules/index.md)

## 使用示例

### 生成 Spring Data Redis 配置

1. 收集参数：project_id、env、redis_password、target_path、mode
2. 根据 mode 选择对应模板
3. 生成代码文件

### 使用 RedisTemplate

```java
@Autowired
private RedisTemplate<String, Object> redisTemplate;

// 存储
redisTemplate.opsForValue().set("key", value, 1, TimeUnit.HOURS);

// 获取
Object value = redisTemplate.opsForValue().get("key");

// 删除
redisTemplate.delete("key");
```

## 依赖说明

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
</dependency>
```

## 注意事项

- Spring Boot 2.x 默认使用 Lettuce 作为客户端
- 推荐使用 StringRedisTemplate 或配置 GenericJackson2JsonRedisSerializer
- 集群模式下需要配置 cluster nodes
- 连接池配置参数需根据实际并发量调整
