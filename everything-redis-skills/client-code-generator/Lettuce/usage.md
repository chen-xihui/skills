# Redis 客户端代码生成 - 目录用途说明

本目录为 Lettuce 客户端提供以下能力：

## 目录结构

```
Lettuce/
├── index.md          # 子能力说明
├── rules/            # 审计规则（LETTUCE-001 ~ LETTUCE-007, CLUSTER-001 ~ CLUSTER-003）
├── code-template/    # 代码模板
├── scripts/          # 代码检查工具
└── usage.md          # 本文件
```

## 规则说明

[rules/](rules/) 目录包含 Lettuce 专属审计规则和集群通用规则：

| 规则ID | 风险等级 | 说明 |
|--------|---------|------|
| LETTUCE-001 | 🔴 严重 | 阻塞命令必须使用独立连接 |
| LETTUCE-002 | 🔴 严重 | Cluster 模式必须配置 ClusterTopologyRefreshOptions |
| LETTUCE-003 | 🔴 严重 | 必须调用 RedisClient.shutdown() |
| LETTUCE-004 | 🟡 风险 | 必须配置 SocketOptions.keepAlive(true) |
| LETTUCE-005 | 🟡 风险 | 建议开启 pingBeforeActivateConnection(true) |
| LETTUCE-006 | 🟡 风险 | 必须显式设置 commandTimeout |
| LETTUCE-007 | 🔵 提示 | shareNativeConnection=true 需明确配置 |
| CLUSTER-001 | 🔴 严重 | maxAttempts 应设置 3-5 |
| CLUSTER-002 | 🟡 风险 | 集群总连接数必须评估 |
| CLUSTER-003 | 🟡 风险 | 禁止业务层重试集群调用 |

## 代码模板说明

[code-template/](code-template/) 目录包含：

- `RedisConfig.java` - 连接配置模板（含 TCP 优化）
- `RedisService.java` - 服务层封装模板
- `RedisClusterConfig.java` - 集群完整配置模板
- `application.yml` - 配置文件模板
- `index.md` - 模板索引

## 脚本说明

[scripts/](scripts/) 目录包含：

- `check_all.py` - 汇总检查脚本（运行所有规则）
- `check_lettuce_001.py` ~ `check_lettuce_007.py` - Lettuce 专属检查脚本
- `check_cluster_001.py` ~ `check_cluster_003.py` - 集群通用检查脚本

使用方式：
```bash
# 运行全部检查
python scripts/check_all.py ./src

# 运行单项检查
python scripts/check_lettuce_001.py ./src
```
