# Jedis 客户端代码生成

## 能力说明

Jedis 是 Redis 的轻量级 Java 客户端，提供同步阻塞的 API 风格。本能力提供 Jedis 客户端的代码生成、配置生成和代码审计。

## 支持模式

| 模式 | 触发关键词 | 说明 |
|------|-----------|------|
| Standalone | standalone、单机 | 单节点部署 |
| Sentinel | sentinel、哨兵 | 高可用哨兵模式 |
| Cluster | cluster、集群 | 分片集群模式 |

## 代码模板

| 文件 | 路径 | 说明 |
|------|------|------|
| JedisConfig.java | [code-template/JedisConfig.java](./code-template/JedisConfig.java) | 连接池配置 |
| JedisService.java | [code-template/JedisService.java](./code-template/JedisService.java) | 服务层封装 |
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

### 生成 Jedis 客户端代码

1. 收集参数：project_id、env、redis_password、target_path、mode
2. 根据 mode 选择对应模板
3. 生成代码文件

### 检查代码

```bash
python scripts/check_code.py --path ./src --client jedis
```

## 依赖说明

```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>4.4.0</version>
</dependency>
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
</dependency>
```

## 注意事项

- Jedis 4.4.0+ 版本对 DNS 解析和服务断联进行了优化
- 连接池 maxTotal 建议小于 200
- maxWaitMillis 禁止使用默认值 -1
