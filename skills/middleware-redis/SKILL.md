---
name: "middleware-redis"
version: "1.5.0"
description: "Redis中间件技能，提供客户端创建、代码优化检查、集群操作和故障排查能力。触发词：Redis、缓存、缓存数据库、哨兵、sentinel、集群缓存"
---

# Redis 中间件

## 功能概述

本 Skill 为 Redis 中间件提供五项标准化能力：

1. **客户端创建与配置**：经 **paas-cli Skill** 执行 `$PAAS_CLI redis config` 拉取连接信息后，生成 Java（Lettuce/Jedis × Standalone/Sentinel/Cluster）、Go、Python 客户端与配置
2. **代码优化检查**：扫描项目代码，按 14 条规则清单逐项检查 Redis 使用规范性
3. **集群交互**：经 **paas-cli Skill** 编排 `$PAAS_CLI` 执行 Redis 集群查询和运维操作，含风险分级确认机制
4. **故障排查**：通过 **bianque Skill** 与 **paas-cli Skill** 诊断 Redis 集群异常，支持降级方案
5. **服务接入指引**：提供设计、开发、测试、上线全生命周期的 Redis 服务接入指导

## 通用规范

### 参数收集原则

1. **优先从上下文推断**：如用户已打开项目，从项目配置文件中提取 `project_id`、`language` 等
2. **主动询问缺失参数**：对必要参数逐一询问，提供可选值提示
3. **使用合理默认值**：对有明确默认值的参数可先使用默认值，在输出中注明

### paas-cli Skill 委托

> 详见 `_shared-references/paas-cli-skill-delegation.md`

凡涉及 PaaS 平台命令，**须先遵循 paas-cli Skill**（`skills/paas-cli/SKILL.md`）。`bianque` 诊断须遵循 **bianque Skill**（`skills/bianque/SKILL.md`）。正文 `paas-cli …` / `bianque …` 指 **`$PAAS_CLI …` / `$BIANQUE …`**。

### 安全约束

> 详细安全规则参见 `_shared-references/cli-security-rules.md`

- **参数白名单校验**：经 paas-cli Skill / bianque Skill 执行的命令参数必须经过白名单校验
- **危险字符过滤**：参数值中不得包含 `;`、`|`、`&`、`$`、`` ` ``、`(`、`)`、`{`、`}` 等 shell 元字符。如检测到，拒绝执行并提示用户
- **高风险操作确认**：🟡 中风险操作展示命令后询问；🔴 高风险操作需用户明确回复"确认"
- **敏感信息处理**：密码以占位符形式（如 `${REDIS_PASSWORD}`）写入配置文件，引导用户通过环境变量或密钥管理系统注入
- **操作审计**：每次经 paas-cli Skill / bianque Skill 执行的命令及结果应在对话中完整展示

### 参数白名单规则

| 参数 | 合法值规则 | 示例 |
|------|-----------|------|
| project_id | 仅允许小写字母、数字 | `j036x0` ✅ |
| env | 枚举值：DEV / SIT / SRV | `DEV` ✅ |
| mode | 枚举值：standalone / sentinel / cluster | `cluster` ✅ |
| client_type | 枚举值：jedis / lettuce | `lettuce` ✅ |
| node | 仅允许字母、数字、短横线、冒号、点号 | `redis-node-1` ✅ |
| version | 语义化版本号格式 | `7.2.0` ✅ |
| count / replicas | 正整数 | `3` ✅ |
| policy | 枚举值：noeviction / allkeys-lru / volatile-lru / allkeys-lfu / volatile-lfu / allkeys-random / volatile-random / volatile-ttl | `allkeys-lru` ✅ |
| namespace | 仅允许小写字母、数字、短横线 | `myns` ✅ |
| instance | 仅允许字母、数字、短横线 | `myredis` ✅ |
| type | 枚举值：cluster / sentinel | `cluster` ✅ |

### 操作风险分级与确认

| 风险等级 | 操作类型 | 确认要求 |
|---------|---------|---------|
| 🟢 低风险 | 查询、状态检查 | 无需确认，直接执行 |
| 🟡 中风险 | 创建实例、扩缩容、内存策略调整 | 向用户展示即将执行的命令，等待用户确认后执行 |
| 🔴 高风险 | Slot 迁移、升级版本、删除集群 | 向用户展示命令及影响范围，必须获得明确确认（用户回复"确认"）后方可执行 |

---

## 能力一：客户端创建与配置

### 触发条件

用户请求创建 Redis 客户端并生成配置，如：
- "创建 Redis 客户端"
- "生成缓存连接代码"
- "帮我配置 Redis"
- "创建 Redis Sentinel 客户端"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境：DEV / SIT / SRV |
| password | string | 是 | — | Redis 密码 |
| target_path | string | 是 | — | 代码生成目标路径 |
| mode | enum | 否 | standalone | 部署模式：standalone / sentinel / cluster |
| client_type | enum | 否 | lettuce | 客户端库：jedis / lettuce（仅 Java） |
| language | enum | 否 | Java | 项目语言：Java / Go / Python |

### 处理流程

1. **参数收集**：确认所有必要参数，缺失项主动询问用户。特别注意 `mode` 参数：
   - standalone：单机模式
   - sentinel：哨兵模式（高可用）
   - cluster：集群模式（分片）
   - 如用户不确定，提示："如果 Redis 只有一个节点选 standalone；有哨兵选 sentinel；有多分片选 cluster"
2. **环境信息查询**：按 **paas-cli Skill** 在终端执行 `$PAAS_CLI` 命令获取 Redis 连接信息
   ```
   $PAAS_CLI redis config --project {project_id} --env {env}
   ```
   - 如 paas-cli Skill 下 `$PAAS_CLI` 执行失败，提示用户检查安装及网络连通性，改为手动输入 Redis 地址
3. **代码生成**：根据参数组合选择对应模板
    > 详细代码模板参见 `references/redis-client-templates/` 目录

   | 组合 | 生成文件 |
   |------|---------|
   | Java + Lettuce + Standalone | RedisConfig.java、RedisService.java、application.yml |
   | Java + Jedis + Standalone | JedisConfig.java、JedisService.java、application.yml |
   | Java + Lettuce + Sentinel | RedisSentinelConfig.java、RedisService.java、application.yml |
   | Java + Lettuce + Cluster | RedisClusterConfig.java、RedisService.java、application.yml |
   | Go | redis_client.go、config.yaml |
   | Python | redis_client.py、config.yaml |

4. **文件写入**：将生成的代码写入 `target_path` 指定目录
5. **依赖提示**：列出需要添加的依赖
   - **Java + Lettuce**：`io.lettuce:lettuce-core`、`org.springframework.boot:spring-boot-starter-data-redis`
   - **Java + Jedis**：`redis.clients:jedis`、`org.springframework.boot:spring-boot-starter-data-redis`
   - **Go**：`github.com/redis/go-redis/v9`
   - **Python**：`pip install redis`

### 输出格式

```
✅ 客户端代码已生成

📁 生成文件列表：
  - {文件路径1} — {文件说明}
  - {文件路径2} — {文件说明}

📝 后续步骤：
  1. 添加依赖：{依赖信息}
  2. 配置环境变量：REDIS_PASSWORD={实际密码}
  3. 根据实际环境调整连接池参数

⚠️ 注意事项：
  - 密码以 ${REDIS_PASSWORD} 占位符形式写入，请通过环境变量或密钥管理系统注入实际值
  - 当前生成的是 {mode} 模式客户端，请确认与实际部署模式一致
```

### 异常处理

- paas-cli Skill 命令执行失败 → 提示用户遵循 paas-cli Skill 并完成 `$PAAS_CLI` 解析及网络连通性，改为手动输入 Redis 地址
- 目标路径不存在 → 询问用户是否创建目录
- 文件已存在 → 询问用户是否覆盖

---

## 能力二：代码优化检查

### 触发条件

用户请求检查 Redis 代码优化，如：
- "检查 Redis 代码"
- "缓存代码审计"
- "Redis 代码优化"
- "检查缓存代码规范"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| scan_path | string | 是 | — | 需扫描的项目根目录 |

### 检查规则清单

> 详细规则说明和检查方法参见 `references/redis-audit-rules/` 目录

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| REDIS-001 | 禁止在循环中使用 `keys *`，应使用 `scan` | 🔴 严重 |
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

### 检查流程

1. **确认扫描路径**：确认 `scan_path` 参数，缺失时主动询问
2. **识别 Redis 客户端类型**：判断使用的是 Lettuce 还是 Jedis
   - 搜索 `LettuceConnectionFactory` / `RedisClient` → Lettuce
   - 搜索 `JedisPool` / `JedisCluster` → Jedis
3. **扫描 Redis 相关代码**：使用 `search_codebase` 和 `grep_code` 按规则逐项搜索
   - 搜索关键词：`keys(`、`scan`、`set`、`get`、`pipeline`、`eval`、`password`、`maxTotal` 等
4. **逐规则检查**：按 REDIS-001 ~ REDIS-014 逐项检查，记录发现的问题
5. **生成审计报告**：按输出格式生成结构化报告，按风险等级排序（🔴 → 🟡 → 🔵）

### 输出格式

```
📋 代码审计报告

📊 概要：共扫描 {N} 个文件，发现 {M} 个问题（🔴 严重 {x} | 🟡 警告 {y} | 🔵 建议 {z}）

| # | 文件路径 | 行号 | 规则ID | 问题描述 | 风险等级 | 改进建议 |
|---|---------|------|--------|---------|---------|---------|
| 1 | ... | ... | ... | ... | 🔴 严重 | ... |

💡 优先修复建议：{按风险等级排序的 Top 3 修复建议}
```

### 异常处理

- 扫描路径不存在 → 提示用户确认路径
- 未找到 Redis 相关代码 → 告知用户未检测到 Redis 客户端代码

---

## 能力三：集群交互

### 触发条件

用户请求与 Redis 集群进行交互，如：
- "查看 Redis 集群状态"
- "Redis 内存使用"
- "Redis 扩缩容"
- "查看 Redis 节点信息"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境：DEV / SIT / SRV |
| action | enum | 是 | — | 操作类型（见操作矩阵） |

### 操作矩阵

> 详细操作说明和命令模板参见 `references/redis-cluster-ops/` 目录

| 操作类型 | 命令模板（paas-cli Skill，`$PAAS_CLI`） | 风险等级 | 需确认 |
|---------|-------------------|---------|--------|
| 查看集群状态 | `$PAAS_CLI redis info --project {project_id} --env {env}` | 🟢 | 否 |
| 查看节点信息 | `$PAAS_CLI redis nodes --project {project_id} --env {env}` | 🟢 | 否 |
| 查看内存使用 | `$PAAS_CLI redis memory --project {project_id} --env {env}` | 🟢 | 否 |
| 创建实例 | `$PAAS_CLI redis create --project {project_id} --env {env} --mode {mode}` | 🟡 | 是 |
| 扩缩容 | `$PAAS_CLI redis scale --project {project_id} --env {env} --replicas {count}` | 🟡 | 是 |
| Slot 迁移 | `$PAAS_CLI redis slot-migrate --project {project_id} --env {env} --from {node} --to {node} --slots {range}` | 🔴 | 是 |
| 内存策略调整 | `$PAAS_CLI redis config --project {project_id} --env {env} --maxmemory-policy {policy}` | 🟡 | 是 |
| 升级版本 | `$PAAS_CLI redis upgrade --project {project_id} --env {env} --version {version}` | 🔴 | 是 |
| 删除集群 | `$PAAS_CLI redis delete --project {project_id} --env {env}` | 🔴 | 是 |

### 前置条件检查

执行集群操作前，先检查：
1. **解析 CLI 路径**：按 `_shared-references/cli-tooling.md` 设置 `PAAS_CLI`
2. 按 **paas-cli Skill** 检查 `$PAAS_CLI` 是否可用：执行 `$PAAS_CLI version`
   - 失败 → 提示遵循 paas-cli Skill 或确认 `skills/paas-cli/paas-cli.py` 存在（见 **paas-cli Skill**（`skills/paas-cli/SKILL.md`））
3. 检查网络连通性：执行 `$PAAS_CLI ping`

### 确认流程

1. 🟢 低风险操作：直接执行，无需确认
2. 🟡 中风险操作：展示完整命令，询问"是否继续执行？"，获得肯定回复后执行
3. 🔴 高风险操作：展示完整命令及影响说明，要求用户明确回复"确认"后方可执行

### 输出格式

```
🔧 集群操作结果

操作：{操作类型}
目标：Redis / {环境} / {集群标识}
状态：✅ 成功 / ❌ 失败

📊 返回信息：
{paas-cli Skill / `$PAAS_CLI` 命令输出内容}

⏱️ 执行耗时：{N}秒
```

### 异常处理

- paas-cli Skill 不可用（`$PAAS_CLI` 解析失败） → 提示安装方式
- 命令执行超时 → 提示用户检查网络，建议加 `--timeout` 参数重试
- 权限不足 → 提示用户联系管理员授权
- 参数包含危险字符 → 拒绝执行并提示用户

---

## 能力四：故障排查

### 触发条件

用户请求 Redis 故障排查或描述 Redis 连接/性能异常，如：
- "Redis 故障排查"
- "缓存连不上了"
- "Redis 响应很慢"
- "内存溢出了"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境 |
| namespace | string | 是 | — | Redis 实例所在的 K8s 命名空间 |
| instance | string | 是 | — | Redis 实例名称 |
| type | enum | 是 | — | Redis 类型：cluster / sentinel |
| symptom | string | 否 | — | 用户描述的异常现象 |

### 诊断流程

> 详细诊断能力说明参见 `references/redis-troubleshooting/` 目录

1. **信息收集**：记录用户描述的异常现象（symptom），如连接超时、响应慢、内存满等
2. **集群状态检查**：按 **paas-cli Skill** 在终端执行 `$PAAS_CLI` 查看 Redis 集群基本状态
   ```
   $PAAS_CLI redis info --project {project_id} --env {env}
   ```
3. **扁鹊诊断**：通过终端调用扁鹊平台执行 Redis 诊断命令
   ```
   bianque redis check -n {namespace} -i {instance} -t {type} -v true
   ```
   - 扁鹊诊断命令默认超时 60 秒
   - 如扁鹊不可达，回退到仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 状态检查
4. **补充信息收集**（可选）：如需进一步诊断，执行内存详情或慢查询命令
   ```
   $PAAS_CLI redis memory --project {project_id} --env {env}
   $PAAS_CLI redis nodes --project {project_id} --env {env}
   ```
5. **结果分析与建议**：综合诊断数据，生成处理建议，按优先级排序

### 诊断能力

| 诊断项 | 检查内容 | 数据来源 |
|--------|---------|---------|
| 慢查询分析 | slowlog 中的高频慢命令 | 扁鹊 |
| 内存碎片率 | mem_fragmentation_ratio | bianque Skill + paas-cli Skill |
| 主从延迟 | replication offset 差异 | 扁鹊 |
| 持久化状态 | RDB/AOF 最后保存时间及状态 | 扁鹊 |
| 故障转移 | Sentinel 选举记录、Failover 日志 | 扁鹊 |
| 客户端连通性 | Redis 客户端读写验证 | 扁鹊 |

> 上述诊断项均通过 `bianque redis check` 命令执行，使用 `-v true` 展示详情，`-l` 指定日志检查行数

### 降级方案

当扁鹊平台不可达时，仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 诊断：
1. 查看集群状态：**paas-cli Skill**：`$PAAS_CLI redis info`
2. 查看节点信息：**paas-cli Skill**：`$PAAS_CLI redis nodes`
3. 查看内存使用：**paas-cli Skill**：`$PAAS_CLI redis memory`

### 输出格式

```
🔍 故障诊断报告

🩺 诊断目标：Redis / {集群标识}
📡 诊断来源：bianque Skill / paas-cli Skill

📊 诊断结论：{一句话结论}

📋 详细发现：
  1. {发现1}
  2. {发现2}

💡 处理建议：
  1. {建议1}（优先级：高）
  2. {建议2}（优先级：中）

📎 相关日志/数据：
{诊断脚本返回的关键数据摘要}
```

### 异常处理

- 扁鹊不可达 → 回退到仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 状态检查，在报告中注明诊断来源降级
- 诊断脚本返回异常 → 展示原始错误信息，建议联系扁鹊平台运维
- paas-cli Skill 不可用（`$PAAS_CLI` 解析失败） → 提示安装方式，仅提供基于代码分析和经验的一般性建议

---

## 能力五：服务接入指引

### 触发条件

用户请求 Redis 服务接入指导，如：
- "Redis 服务如何接入"
- "缓存设计指引"
- "Redis 开发规范"
- "缓存上线检查"
- "Redis 容灾设计"

### 指引内容

> 完整接入指引参见 `references/redis-access-guide/` 目录

**设计指引**
- 缓存依赖设计（熔断、降级、多级存储）
- 数据隔离规则（按安全等级/业务领域/可用性等级/访问频率拆分）
- 部署模式选型（主从 vs 集群，规格选型）
- 持久化模式选型（内存/RDB/AOF/多级存储）
- 容灾功能设计（数据同步/流量路由/容灾切换/读写策略）

**开发指引**
- 客户端版本要求（Jedis ≥4.4.0 / Lettuce ≥6.3.0）
- 连接池参数配置（含详细参数说明和推荐值）
- 连接数计算（主从/集群/容灾模式）
- 拓扑刷新配置（Jedis 自动 / Lettuce 需手动配置）
- Lettuce TCP 参数配置（keepalive + tcpUserTimeout）
- 命令使用规范（高危命令/批量命令/全库匹配/事务命令/键空间事件）
- 容错开发（健康检查/熔断/降级/重试）
- 安全编码（服务认证/数据加密）

**测试指引**
- 性能测试（全链路测试、容量评估）
- 专项测试案例（网络抖动/全量宕机/主从切换/分片故障/容灾切换）

**上线指引**
- 前置资源准备（部署模式/资源需求/持久化模式/容灾要求）
- 告警规则确认
- 接入前置检查（客户端配置/生产资源/网络连通性/连接认证）
- 应急卡片准备

### 输出格式

```
📖 Redis 服务接入指引

根据您的需求，以下是相关指引：

**{指引类别}**
{具体指引内容摘要}

📎 详细内容请参考：references/redis-access-guide/ 目录
```

---

## 变更记录

- v1.5.0 (2026-05-26): 所有 paas-cli 操作改为委托 **paas-cli Skill**
- v1.4.0 (2026-05-26): Skill 与 CLI 路径统一为项目根 `skills/`（移除 `.trae/`）
- v1.3.0 (2026-05-15): 重构 redis-troubleshooting.md 为模块化目录结构
- v1.2.0 (2026-05-15): 重构 references 目录结构，将大文件拆分为模块化小文件，优化 LLM 上下文加载效率
- v1.1.0 (2026-05-12): 新增服务接入指引能力；审计规则由 8 条扩展至 14 条（新增 REDIS-009 ~ REDIS-014）
- v1.0.0 (2026-05-11): 初始版本，包含客户端创建与配置、代码优化检查、集群交互、故障排查四项基础能力