# Redis 客户端代码生成 - 目录用途说明

本目录为 Spring Data Redis 客户端提供以下能力：

## 目录结构

```
SpringDataRedis/
├── index.md          # 子能力说明
├── rules/            # 审计规则（SDR-001 ~ SDR-003, CLUSTER-001 ~ CLUSTER-003）
├── code-template/    # 代码模板
├── scripts/          # 代码检查工具
└── usage.md          # 本文件
```

## 规则说明

[rules/](rules/) 目录包含 Spring Data Redis 专属审计规则和集群通用规则：

| 规则ID | 风险等级 | 说明 |
|--------|---------|------|
| SDR-001 | 🔴 严重 | RedisTemplate 必须配置序列化方式 |
| SDR-002 | 🟡 风险 | 禁止使用 keys()，应使用 SCAN |
| SDR-003 | 🟡 风险 | LettuceConnectionFactory 必须配置 commandTimeout |
| CLUSTER-001 | 🔴 严重 | maxAttempts 应设置 3-5 |
| CLUSTER-002 | 🟡 风险 | 集群总连接数必须评估 |
| CLUSTER-003 | 🟡 风险 | 禁止业务层重试集群调用 |

## 代码模板说明

[code-template/](code-template/) 目录包含：

- `RedisConfig.java` - Redis 配置类模板
- `RedisTemplateConfig.java` - 序列化配置模板
- `application.yml` - 配置文件模板
- `index.md` - 模板索引

## 脚本说明

[scripts/](scripts/) 目录包含：

- `check_all.py` - 汇总检查脚本（运行所有规则）
- `check_sdr_001.py` ~ `check_sdr_003.py` - Spring Data Redis 专属检查脚本
- `check_cluster_001.py` ~ `check_cluster_003.py` - 集群通用检查脚本

使用方式：
```bash
# 运行全部检查
python scripts/check_all.py ./src

# 运行单项检查
python scripts/check_sdr_001.py ./src
```

## 依赖说明

Spring Boot 2.x 默认使用 Lettuce 作为底层客户端。Spring Data Redis 提供统一的抽象层。
