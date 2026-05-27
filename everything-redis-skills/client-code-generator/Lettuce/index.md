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

### Lettuce 专属规则

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| LETTUCE-001 | 阻塞命令（BLPOP、SUBSCRIBE、XREAD）必须使用独立连接 | 🔴 严重 |
| LETTUCE-002 | Cluster 模式必须配置 ClusterTopologyRefreshOptions | 🔴 严重 |
| LETTUCE-003 | 应用退出时必须调用 RedisClient.shutdown() 释放 Netty 线程 | 🔴 严重 |
| LETTUCE-004 | 必须配置 SocketOptions.keepAlive(true) | 🟡 风险 |
| LETTUCE-005 | 建议开启 pingBeforeActivateConnection(true) | 🟡 风险 |
| LETTUCE-006 | 必须显式设置 commandTimeout | 🟡 风险 |
| LETTUCE-007 | shareNativeConnection=true 需明确配置连接模式 | 🔵 提示 |

### 集群通用规则

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| CLUSTER-001 | maxAttempts 应设置 3-5，禁止过大值 | 🔴 严重 |
| CLUSTER-002 | 集群总连接数 = 节点数 × maxTotal，必须评估 | 🟡 风险 |
| CLUSTER-003 | 禁止业务层重试循环包裹集群调用 | 🟡 风险 |

详细规则：[rules/index.md](./rules/index.md)

## 使用示例

### 生成 Lettuce 客户端代码

1. 收集参数：project_id、env、redis_password、target_path、mode
2. 根据 mode 选择对应模板
3. 生成代码文件

### 检查代码

```bash
# 运行全部检查
python scripts/check_all.py ./src

# 运行单项检查
python scripts/check_lettuce_001.py ./src
python scripts/check_cluster_001.py ./src
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
