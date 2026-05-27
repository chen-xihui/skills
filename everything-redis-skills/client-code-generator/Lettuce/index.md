# Lettuce 客户端代码生成

## 能力说明

Lettuce 是 Redis 的高级 Java 客户端，支持同步、异步和响应式 API，基于 Netty 实现，提供更好的性能和连接管理。本能力提供 Lettuce 客户端的代码生成、配置生成和代码审计。

## 支持模式

| 模式 | 触发关键词 | 说明 |
|------|-----------|------|
| Standalone | standalone、单机 | 单节点部署 |
| Sentinel | sentinel、哨兵 | 高可用哨兵模式 |
| Cluster | cluster、集群 | 分片集群模式（含 TCP 参数优化） |

## 代码模板

| 文件 | 路径 | 说明 |
|------|------|------|
| RedisConfig.java | [code-template/RedisConfig.java](./code-template/RedisConfig.java) | 连接配置（含 TCP 优化） |
| RedisService.java | [code-template/RedisService.java](./code-template/RedisService.java) | 服务层封装 |
| application.yml | [code-template/application.yml](./code-template/application.yml) | 配置文件 |
| RedisClusterConfig.java | [code-template/RedisClusterConfig.java](./code-template/RedisClusterConfig.java) | 集群完整配置 |

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

### 生成 Lettuce 客户端代码

1. 收集参数：project_id、env、redis_password、target_path、mode
2. 根据 mode 选择对应模板
3. 生成代码文件

### 检查代码

```bash
python scripts/check_code.py --path ./src --client lettuce
```

## 依赖说明

```xml
<dependency>
    <groupId>io.lettuce</groupId>
    <artifactId>lettuce-core</artifactId>
    <version>6.3.0</version>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
<!-- Linux 环境推荐添加 -->
<dependency>
    <groupId>io.netty</groupId>
    <artifactId>netty-transport-native-epoll</artifactId>
    <version>4.1.100.Final</version>
    <classifier>linux-x86_64</classifier>
</dependency>
```

## 注意事项

- Lettuce 6.3.0+ 支持 tcpUserTimeout 参数配置
- 集群模式必须开启拓扑刷新（adaptive: true）
- TCP keepalive 参数：idle=150s, interval=5s, cnt=6
- TCP user timeout：建议 180s（容忍网络抖动）
