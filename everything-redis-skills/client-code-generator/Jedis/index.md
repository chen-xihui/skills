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

### Jedis 专属规则

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| JEDIS-001 | 禁止使用 KEYS 命令，应使用 SCAN | 🔴 严重 |
| JEDIS-002 | getResource() 必须使用 try-with-resources 防止连接泄漏 | 🔴 严重 |
| JEDIS-003 | 禁止在循环中创建连接（Jedis、JedisPool、RedissonClient） | 🔴 严重 |
| JEDIS-004 | Pipeline 必须调用 close() 或使用 try-with-resources | 🔴 严重 |
| JEDIS-005 | MULTI/EXEC 异常后必须调用 discard() 清理连接状态 | 🔴 严重 |
| JEDIS-006 | 禁止运行时执行 CONFIG SET / CONFIG REWRITE | 🔴 严重 |
| JEDIS-007 | JedisPoolConfig 必须配置四项核心参数（maxTotal、maxIdle、minIdle、maxWaitMillis） | 🟡 风险 |
| JEDIS-008 | 必须开启 setTestWhileIdle(true) 检测失效连接 | 🟡 风险 |
| JEDIS-009 | Pipeline 批量命令数应控制在 100-1000 以内 | 🟡 风险 |
| JEDIS-010 | 禁止无限重试循环包裹 Redis 调用 | 🟡 风险 |
| JEDIS-011 | 禁止业务层重试循环包裹 jedisCluster 调用 | 🟡 风险 |
| JEDIS-012 | 必须设置 commandTimeout 命令超时时间 | 🟡 风险 |
| JEDIS-013 | 建议开启 setTestOnBorrow(true) 连接借用检测 | 🔵 提示 |
| JEDIS-014 | Lua 脚本必须使用 SCRIPT LOAD + EVALSHA | 🔵 提示 |

### 集群通用规则

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| CLUSTER-001 | maxAttempts 应设置 3-5，禁止过大值 | 🔴 严重 |
| CLUSTER-002 | 集群总连接数 = 节点数 × maxTotal，必须评估 | 🟡 风险 |
| CLUSTER-003 | 禁止业务层重试循环包裹集群调用 | 🟡 风险 |

详细规则：[rules/index.md](./rules/index.md)

## 使用示例

### 生成 Jedis 客户端代码

1. 收集参数：project_id、env、redis_password、target_path、mode
2. 根据 mode 选择对应模板
3. 生成代码文件

### 检查代码

```bash
# 运行全部检查
python scripts/check_all.py ./src

# 运行单项检查
python scripts/check_jedis_001.py ./src
python scripts/check_cluster_001.py ./src
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
