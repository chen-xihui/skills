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

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| REDIS-001 | 禁止在循环中使用 keys * | 🔴 严重 |
| REDIS-002 | 大 Key 风险检查（>10KB） | 🟡 警告 |
| REDIS-003 | 热 Key 风险检查 | 🟡 警告 |
| REDIS-004 | 连接池参数合理性 | 🟡 警告 |
| REDIS-005 | Pipeline 批量使用 | 🔵 建议 |
| REDIS-006 | Lua 脚本使用 EVALSHA | 🔵 建议 |
| REDIS-007 | 合理设置过期时间 | 🟡 警告 |
| REDIS-008 | 禁止密码硬编码 | 🔴 严重 |
| REDIS-009 | 禁止高危命令 | 🔴 严重 |
| REDIS-010 | 禁止 Keys 全库匹配 | 🔴 严重 |
| REDIS-011 | 高时间复杂度命令 | 🟡 警告 |
| REDIS-012 | Key 命名规范 | 🔵 建议 |
| REDIS-013 | 大 Key 集合检查 | 🟡 警告 |
| REDIS-014 | 事务命令使用检查 | 🟡 警告 |

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
