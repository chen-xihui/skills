# Everything Redis Skills 设计文档

## 1. 项目概述

### 1.1 项目定位

**everything-redis-skills** 是 Redis Java 客户端开发专家 Skill，聚焦于根据规范提供 Redis 接入实践。

### 1.2 核心能力

| 能力 | 说明 |
|------|------|
| 代码生成 | 生成符合规范的 Jedis、Lettuce、Redisson、Spring Data Redis 接入代码 |
| 配置生成 | 生成符合规范的连接配置（Standalone/Sentinel/Cluster 模式） |
| 代码审计 | 14 条审计规则（REDIS-001~REDIS-014），识别常用错误并给出修改建议 |
| 连接信息获取 | 通过 paas-cli 获取 Redis 地址和密码（mock） |

## 2. 目录结构

```
everything-redis-skills/
├── SKILL.md                           # 统一入口
├── design.md                          # 设计文档（本文件）
├── client-code-generator/              # 客户端代码生成
│   ├── index.md                       # 能力索引与触发规则
│   ├── Jedis/                        # Jedis 客户端
│   │   ├── index.md                  # 子能力说明
│   │   ├── rules/                    # 审计规则（REDIS-001~014）
│   │   ├── code-template/            # 代码模板
│   │   │   ├── JedisConfig.java     # 连接池配置
│   │   │   ├── JedisConnectionConfig.java
│   │   │   ├── JedisService.java    # 服务层封装
│   │   │   ├── application.yml       # 配置文件
│   │   │   └── index.md             # 模板索引
│   │   ├── scripts/                  # 检查脚本
│   │   │   └── check_code.py        # 代码审计脚本
│   │   └── usage.md                 # 目录用途说明
│   ├── Lettuce/                      # Lettuce 客户端
│   │   ├── index.md
│   │   ├── rules/
│   │   ├── code-template/
│   │   │   ├── RedisConfig.java     # 连接配置（含 TCP 优化）
│   │   │   ├── RedisService.java
│   │   │   ├── RedisClusterConfig.java  # 集群完整配置
│   │   │   ├── application.yml
│   │   │   └── index.md
│   │   ├── scripts/
│   │   │   └── check_code.py
│   │   └── usage.md
│   ├── Redisson/                     # Redisson 客户端
│   │   ├── index.md
│   │   ├── rules/
│   │   ├── code-template/
│   │   │   ├── RedissonConfig.java      # Standalone 配置
│   │   │   ├── RedissonSentinelConfig.java
│   │   │   ├── RedissonClusterConfig.java
│   │   │   ├── DistributedLockService.java  # 分布式锁服务
│   │   │   └── application.yml
│   │   ├── scripts/
│   │   │   └── check_code.py
│   │   └── usage.md
│   └── SpringDataRedis/              # Spring Data Redis 客户端
│       ├── index.md
│       ├── rules/
│       ├── code-template/
│       │   ├── RedisConfig.java
│       │   ├── RedisService.java
│       │   ├── application.yml
│       │   └── index.md
│       ├── scripts/
│       │   └── check_code.py
│       └── usage.md
└── client-redis-paas-tools/          # Redis 连接工具
    ├── README.md
    ├── paas-cli.py                   # 命令行工具（mock）
    ├── paas-cli.cmd                  # Windows 入口
    └── config/                       # 配置文件
        └── redis/                    # Redis 相关配置
```

## 3. 客户端推荐规则

### 3.1 推荐决策树

```
                    是否需要分布式锁/集合？
                            │
            ┌───────────────┴───────────────┐
            │                               │
           是                               否
            │                               │
            ▼                               ▼
    ┌───────────────┐              是否使用 Spring？
    │ Redisson      │                      │
    │ 分布式锁/集合  │              ┌───────┴───────┐
    └───────────────┘              │               │
                                   │               │
                                  是               否
                                   │               │
                                   ▼               ▼
                           ┌───────────────┐ ┌───────────────┐
                           │ Spring Data   │ │ Jedis         │
                           │ Redis         │ │ (默认推荐)    │
                           │ 底层使用Lettuce│ └───────────────┘
                           └───────────────┘
```

### 3.2 客户端对比

| 客户端 | 推荐场景 | 特点 | 支持模式 |
|--------|---------|------|---------|
| **Jedis** | 非 Spring 项目、简单场景 | 默认推荐，轻量级同步客户端 | Standalone/Sentinel/Cluster |
| **Lettuce** | Spring Data Redis 项目 | Spring 官方推荐，异步/响应式支持，自动重连 | Standalone/Sentinel/Cluster |
| **Redisson** | 分布式锁、分布式集合 | 支持更多数据结构，Java 语义化 | Standalone/Sentinel/Cluster/Replicated |
| **Spring Data Redis** | Spring Boot 项目 | Spring 统一抽象，整合 Spring 生态（底层使用 Lettuce） | Standalone/Sentinel/Cluster |

### 3.3 触发规则

| 用户意图 | 路由目标 | 说明 |
|---------|---------|------|
| "创建 Redis 客户端"、"配置 Redis" | Jedis | 默认推荐（非 Spring 项目） |
| "Spring Data Redis"、"RedisTemplate" | Spring Data Redis | Spring 项目（底层使用 Lettuce） |
| "分布式锁"、"Redisson 锁" | Redisson | 分布式锁/集合场景 |
| "Lettuce" | Lettuce | 指定 Lettuce |
| "Jedis" | Jedis | 指定 Jedis |

## 4. 审计规则

### 4.1 规则总览

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| REDIS-001 | 禁止在循环中使用 keys *，应使用 scan | 🔴 严重 |
| REDIS-002 | 大 Key 风险检查（单次操作 Value 超过 10KB 应拆分或压缩） | 🟡 警告 |
| REDIS-003 | 热 Key 风险检查（高频读写的 Key 应考虑本地缓存） | 🟡 警告 |
| REDIS-004 | 连接池参数合理性（maxTotal、maxIdle、maxWaitMillis） | 🟡 警告 |
| REDIS-005 | Pipeline 批量使用情况（多次独立命令应使用 Pipeline） | 🔵 建议 |
| REDIS-006 | Lua 脚本是否使用 EVALSHA 预加载（而非每次 EVAL） | 🔵 建议 |
| REDIS-007 | 是否设置合理的过期时间（避免 Key 永不过期导致内存泄漏） | 🟡 警告 |
| REDIS-008 | 密码是否硬编码 | 🔴 严重 |
| REDIS-009 | 禁止使用 CONFIG、FLUSHALL、FLUSHDB 等高危命令 | 🔴 严重 |
| REDIS-010 | 禁止使用 Keys 全库匹配命令 | 🔴 严重 |
| REDIS-011 | 避免使用集合整存整取与高时间复杂度命令 | 🟡 警告 |
| REDIS-012 | Key 命名规范检查 | 🔵 建议 |
| REDIS-013 | 大 Key 集合对象检查（建议控制在 5000 项以内） | 🟡 警告 |
| REDIS-014 | 事务命令使用检查 | 🟡 警告 |

### 4.2 风险统计

- 🔴 **严重**：REDIS-001、REDIS-008、REDIS-009、REDIS-010（4 条）
- 🟡 **警告**：REDIS-002、REDIS-003、REDIS-004、REDIS-007、REDIS-011、REDIS-013、REDIS-014（7 条）
- 🔵 **建议**：REDIS-005、REDIS-006、REDIS-012（3 条）

## 5. 代码模板设计

### 5.1 Jedis 模板

| 文件 | 说明 |
|------|------|
| JedisConfig.java | JedisPool 连接池配置 |
| JedisConnectionConfig.java | Spring Data Redis + Jedis 连接配置 |
| JedisService.java | 服务层封装（含 scan 替代 keys） |
| application.yml | 配置文件（含连接池参数） |

### 5.2 Lettuce 模板

| 文件 | 说明 |
|------|------|
| RedisConfig.java | Lettuce 连接配置（含 TCP 优化） |
| RedisService.java | 服务层封装 |
| RedisClusterConfig.java | 集群完整配置（含 TCP keepalive/tcpUserTimeout） |
| application.yml | 配置文件 |

### 5.3 Redisson 模板

| 文件 | 说明 |
|------|------|
| RedissonConfig.java | Standalone 模式配置 |
| RedissonSentinelConfig.java | Sentinel 模式配置 |
| RedissonClusterConfig.java | Cluster 模式配置 |
| DistributedLockService.java | 分布式锁服务 |
| application.yml | 配置文件 |

### 5.4 Spring Data Redis 模板

| 文件 | 说明 |
|------|------|
| RedisConfig.java | Redis 配置类 |
| RedisService.java | 服务层封装 |
| application.yml | 配置文件 |

## 6. 脚本设计

### 6.1 代码审计脚本

**文件**：`client-code-generator/*/scripts/check_code.py`

**功能**：扫描 Java 代码，按 14 条规则检查 Redis 使用规范性

**使用方式**：
```bash
python scripts/check_code.py --path ./src --client jedis
```

**输出格式**：JSON 或 Text

## 7. Redis 连接工具

### 7.1 paas-cli

**文件**：`client-redis-paas-tools/paas-cli.py`

**功能**：获取 Redis 连接信息（mock 版本）

**支持命令**：
- `paas-cli redis info` - 查看集群信息
- `paas-cli redis nodes` - 查看节点列表
- `paas-cli redis memory` - 查看内存详情
- `paas-cli redis config` - 查看连接配置

**Mock 返回示例**：
```
Redis Cluster Info — project=j036x0  env=DEV
  Cluster Name   : redis-j036x0-dev
  Status         : Running
  Version        : 7.0.0
  Mode           : standalone
  Nodes          : 1
  Connections    : 42
```

## 8. 通用参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | - | 项目组编号 |
| env | enum | 是 | - | 环境：DEV / SIT / SRV |
| mode | enum | 否 | standalone | 部署模式：standalone / sentinel / cluster |
| target_path | string | 是 | - | 代码生成目标路径 |
| redis_password | string | 是 | - | Redis 密码（写入为占位符） |

## 9. 安全约束

### 9.1 密码处理

- 密码以 `${REDIS_PASSWORD}` 占位符形式写入配置文件
- 通过环境变量或密钥管理系统注入实际值

### 9.2 连接池配置

- maxTotal 建议小于 200
- maxWaitMillis 禁止使用默认值 -1

### 9.3 危险操作

- 生产环境禁止使用 `keys *` 命令
- 禁止使用 CONFIG、FLUSHALL、FLUSHDB 等高危命令

## 10. 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-05-26 | 初始版本创建 |
| 1.0.1 | 2026-05-26 | 更新客户端推荐规则：非 Spring 推荐 Jedis，Spring Data Redis 底层使用 Lettuce，分布式锁使用 Redisson |

## 11. 依赖说明

### 11.1 Maven 依赖

**Jedis**：
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

**Lettuce**：
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
```

**Redisson**：
```xml
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson-spring-boot-starter</artifactId>
    <version>3.25.0</version>
</dependency>
```

### 11.2 客户端版本要求

| 客户端 | 推荐版本 | 说明 |
|--------|---------|------|
| Jedis | ≥4.4.0 / ≥3.10 | 4.4.0、3.10.0 版本对 DNS 解析/服务断联功能进行优化 |
| Lettuce | ≥6.3.0 | 6.3.0 版本增加 tcpTimeout 参数配置 |
| Redisson | ≥3.25.0 | 推荐使用最新稳定版 |
