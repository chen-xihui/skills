# Redisson 客户端代码生成

## 能力说明

Redisson 是 Redis 的高级 Java 客户端，基于 Netty 实现，提供分布式数据结构、分布式锁、远程服务调用等特性。Redisson 将 Redis 数据结构映射为 Java 对象，提供更符合 Java 开发者习惯的 API。

## 支持模式

| 模式 | 触发关键词 | 说明 |
|------|-----------|------|
| Standalone | standalone、单机 | 单节点部署 |
| Sentinel | sentinel、哨兵 | 高可用哨兵模式 |
| Cluster | cluster、集群 | 分片集群模式 |
| Replicated | replicated、复制 | 主从复制模式 |

## 代码模板

| 文件 | 路径 | 说明 |
|------|------|------|
| RedissonConfig.java | [code-template/RedissonConfig.java](./code-template/RedissonConfig.java) | 客户端配置 |
| DistributedLockService.java | [code-template/DistributedLockService.java](./code-template/DistributedLockService.java) | 分布式锁服务 |
| application.yml | [code-template/application.yml](./code-template/application.yml) | 配置文件 |

## 审计规则

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| REDIS-001 | 禁止在循环中使用 keys * | 🔴 严重 |
| REDIS-002 | 大 Key 风险检查（>10KB） | 🟡 警告 |
| REDIS-003 | 热 Key 风险检查 | 🟡 警告 |
| REDIS-007 | 合理设置过期时间 | 🟡 警告 |
| REDIS-008 | 禁止密码硬编码 | 🔴 严重 |
| REDIS-009 | 禁止高危命令 | 🔴 严重 |
| REDIS-010 | 禁止 Keys 全库匹配 | 🔴 严重 |
| REDIS-012 | Key 命名规范 | 🔵 建议 |

详细规则：[rules/index.md](./rules/index.md)

## 使用示例

### 生成 Redisson 客户端代码

1. 收集参数：project_id、env、redis_password、target_path、mode
2. 根据 mode 选择对应模板
3. 生成代码文件

### 使用分布式锁

```java
RLock lock = redissonClient.getLock("myLock");
try {
    if (lock.tryLock(10, 30, TimeUnit.SECONDS)) {
        // 业务逻辑
    }
} finally {
    lock.unlock();
}
```

## 依赖说明

```xml
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson-spring-boot-starter</artifactId>
    <version>3.25.0</version>
</dependency>
```

## 注意事项

- Redisson 非 Spring 技术目录官方推荐，请评估后使用
- 分布式锁使用建议设置合理的看门狗超时时间
- 建议使用 RBatch 进行批量操作
- 避免存储过大的对象到 Redis
