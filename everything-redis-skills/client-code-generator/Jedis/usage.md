# Redis 客户端代码生成 - 目录用途说明

本目录为 Jedis 客户端提供以下能力：

## 目录结构

```
Jedis/
├── index.md          # 子能力说明
├── rules/            # 审计规则（JEDIS-001 ~ JEDIS-014, CLUSTER-001 ~ CLUSTER-003）
├── code-template/    # 代码模板
├── scripts/          # 代码检查工具
└── usage.md          # 本文件
```

## 规则说明

[rules/](rules/) 目录包含 Jedis 专属审计规则和集群通用规则：

| 规则ID | 风险等级 | 说明 |
|--------|---------|------|
| JEDIS-001 | 🔴 严重 | 禁止使用 KEYS 命令，应使用 SCAN |
| JEDIS-002 | 🔴 严重 | getResource() 必须使用 try-with-resources |
| JEDIS-003 | 🔴 严重 | 禁止在循环中创建连接 |
| JEDIS-004 | 🔴 严重 | Pipeline 必须调用 close() |
| JEDIS-005 | 🔴 严重 | MULTI/EXEC 异常后必须调用 discard() |
| JEDIS-006 | 🔴 严重 | 禁止运行时 CONFIG SET / CONFIG REWRITE |
| JEDIS-007 | 🟡 风险 | JedisPoolConfig 必须配置四项核心参数 |
| JEDIS-008 | 🟡 风险 | 必须开启 setTestWhileIdle(true) |
| JEDIS-009 | 🟡 风险 | Pipeline 批量命令数应控制在 100-1000 |
| JEDIS-010 | 🟡 风险 | 禁止无限重试循环 |
| JEDIS-011 | 🟡 风险 | 禁止业务层重试 jedisCluster 调用 |
| JEDIS-012 | 🟡 风险 | 必须设置 commandTimeout |
| JEDIS-013 | 🔵 提示 | 建议开启 setTestOnBorrow(true) |
| JEDIS-014 | 🔵 提示 | Lua 脚本必须使用 SCRIPT LOAD + EVALSHA |
| CLUSTER-001 | 🔴 严重 | maxAttempts 应设置 3-5 |
| CLUSTER-002 | 🟡 风险 | 集群总连接数必须评估 |
| CLUSTER-003 | 🟡 风险 | 禁止业务层重试集群调用 |

## 代码模板说明

[code-template/](code-template/) 目录包含：

- `JedisConfig.java` - 连接池配置模板
- `JedisService.java` - 服务层封装模板
- `application.yml` - 配置文件模板
- `index.md` - 模板索引

## 脚本说明

[scripts/](scripts/) 目录包含：

- `check_all.py` - 汇总检查脚本（运行所有规则）
- `check_jedis_001.py` ~ `check_jedis_014.py` - Jedis 专属检查脚本
- `check_cluster_001.py` ~ `check_cluster_003.py` - 集群通用检查脚本

使用方式：
```bash
# 运行全部检查
python scripts/check_all.py ./src

# 运行单项检查
python scripts/check_jedis_001.py ./src
```
