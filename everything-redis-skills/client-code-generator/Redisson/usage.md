# Redis 客户端代码生成 - 目录用途说明

本目录为 Redisson 客户端提供以下能力：

## 目录结构

```
Redisson/
├── index.md          # 子能力说明
├── rules/            # 审计规则（REDISSON-001 ~ REDISSON-005, CLUSTER-001 ~ CLUSTER-003）
├── code-template/    # 代码模板
├── scripts/          # 代码检查工具
└── usage.md          # 本文件
```

## 规则说明

[rules/](rules/) 目录包含 Redisson 专属审计规则和集群通用规则：

| 规则ID | 风险等级 | 说明 |
|--------|---------|------|
| REDISSON-001 | 🔴 严重 | lock() 必须设置 leaseTime |
| REDISSON-002 | 🔴 严重 | RedissonClient 必须单例 |
| REDISSON-003 | 🔴 严重 | 必须调用 redisson.shutdown() |
| REDISSON-004 | 🟡 风险 | 必须设置 keepAlive: true |
| REDISSON-005 | 🟡 风险 | tryLock 必须设置 waitTime 和 leaseTime |
| CLUSTER-001 | 🔴 严重 | maxAttempts 应设置 3-5 |
| CLUSTER-002 | 🟡 风险 | 集群总连接数必须评估 |
| CLUSTER-003 | 🟡 风险 | 禁止业务层重试集群调用 |

## 代码模板说明

[code-template/](code-template/) 目录包含：

- `RedissonConfig.java` - Redisson 配置模板
- `DistributedLockService.java` - 分布式锁服务模板
- `application.yml` - 配置文件模板

## 脚本说明

[scripts/](scripts/) 目录包含：

- `check_all.py` - 汇总检查脚本（运行所有规则）
- `check_redisson_001.py` ~ `check_redisson_005.py` - Redisson 专属检查脚本
- `check_cluster_001.py` ~ `check_cluster_003.py` - 集群通用检查脚本

使用方式：
```bash
# 运行全部检查
python scripts/check_all.py ./src

# 运行单项检查
python scripts/check_redisson_001.py ./src
```

## 注意事项

Redisson 为第三方库，非 Spring 技术目录官方推荐。使用前请评估是否满足项目需求。
