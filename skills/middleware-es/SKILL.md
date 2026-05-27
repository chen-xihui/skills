---
name: "middleware-es"
version: "1.5.0"
description: "Elasticsearch中间件技能，提供客户端创建、代码优化检查、集群操作、故障排查和服务接入指引能力。触发词：ES、Elasticsearch、搜索引擎、索引、搜索、Elastic"
---

# Elasticsearch 中间件

## 功能概述

本 Skill 为 Elasticsearch 中间件提供五项标准化能力：

1. **客户端创建与配置**：经 **paas-cli Skill** 执行 `$PAAS_CLI es config` 拉取连接信息后，生成 Java（新版 ElasticsearchClient 8.x+ / 旧版 RestHighLevelClient 7.x）、Go、Python 客户端与配置
2. **代码优化检查**：扫描项目代码，按 8 条规则清单逐项检查 ES 使用规范性
3. **集群交互**：经 **paas-cli Skill** 编排 `$PAAS_CLI` 执行 ES 集群查询和运维操作，含风险分级确认机制
4. **故障排查**：通过 **bianque Skill** 与 **paas-cli Skill** 诊断 ES 集群异常，支持降级方案
5. **服务接入指引**：提供设计、开发、测试、上线全生命周期的 ES 服务接入指导

## 通用规范

### 参数收集原则

1. **优先从上下文推断**：如用户已打开项目，从项目配置文件中提取 `project_id`、`language` 等
2. **主动询问缺失参数**：对必要参数逐一询问，提供可选值提示
3. **使用合理默认值**：对有明确默认值的参数（如 `language` 默认 Java），可先使用默认值，在输出中注明

### paas-cli Skill 委托

> 详见 `_shared-references/paas-cli-skill-delegation.md`

凡涉及 PaaS 平台命令，**须先遵循 paas-cli Skill**（`skills/paas-cli/SKILL.md`）。`bianque` 诊断须遵循 **bianque Skill**（`skills/bianque/SKILL.md`）。正文 `paas-cli …` / `bianque …` 指 **`$PAAS_CLI …` / `$BIANQUE …`**。

### 安全约束

> 详细安全规则参见 `_shared-references/cli-security-rules.md`

- **参数白名单校验**：经 paas-cli Skill / bianque Skill 执行的命令参数必须经过白名单校验
- **危险字符过滤**：参数值中不得包含 `;`、`|`、`&`、`$`、`` ` ``、`(`、`)`、`{`、`}` 等 shell 元字符。如检测到，拒绝执行并提示用户
- **高风险操作确认**：🟡 中风险操作展示命令后询问；🔴 高风险操作需用户明确回复"确认"
- **敏感信息处理**：密码以占位符形式（如 `${ES_PASSWORD}`）写入配置文件，引导用户通过环境变量或密钥管理系统注入
- **操作审计**：每次经 paas-cli Skill / bianque Skill 执行的命令及结果应在对话中完整展示

### 参数白名单规则

| 参数 | 合法值规则 | 示例 |
|------|-----------|------|
| project_id | 仅允许小写字母、数字，格式如 j036x0 | `j036x0` ✅ `; rm -rf` ❌ |
| env | 枚举值：DEV / SIT / SRV | `DEV` ✅ `DEV; ls` ❌ |
| index_name | 小写字母、数字、短横线 | `log-2026` ✅ `log"; rm -rf /` ❌ |
| version | 语义化版本号格式 | `8.12.0` ✅ `8.12.0 && cat /etc/passwd` ❌ |
| count / nodes / shards / replicas / max-segments | 正整数 | `3` ✅ `3 || echo hack` ❌ |
| alias | 字母、数字、短横线、下划线 | `log-alias` ✅ `$(whoami)` ❌ |
| namespace | 仅允许小写字母、数字、短横线 | `myns` ✅ `myns; ls` ❌ |
| instance | 仅允许字母、数字、短横线 | `myes` ✅ `myes && cat` ❌ |

### 操作风险分级与确认

| 风险等级 | 操作类型 | 确认要求 |
|---------|---------|---------|
| 🟢 低风险 | 查询、状态检查 | 无需确认，直接执行 |
| 🟡 中风险 | 创建索引、索引滚动、Force merge、扩缩容 | 向用户展示即将执行的命令，等待用户确认后执行 |
| 🔴 高风险 | 升级版本、删除集群 | 向用户展示命令及影响范围，必须获得明确确认（用户回复"确认"）后方可执行 |

---

## 能力一：客户端创建与配置

### 触发条件

用户请求创建 ES 客户端并生成配置，如：
- "创建 ES 客户端"
- "生成 Elasticsearch 连接代码"
- "帮我配置 ES 连接"
- "创建搜索客户端"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号，如 j036x0 |
| env | enum | 是 | — | 环境：DEV / SIT / SRV |
| auth_user | string | 是 | — | ES 用户名 |
| auth_pass | string | 是 | — | ES 密码 |
| target_path | string | 是 | — | 代码生成目标路径 |
| client_version | enum | 否 | new | 客户端版本：new（ElasticsearchClient / 8.x+）/ old（RestHighLevelClient / 7.x） |
| language | enum | 否 | Java | 项目语言：Java / Go / Python / Node.js |

### 处理流程

1. **参数收集**：确认所有必要参数，缺失项主动询问用户。特别确认 `client_version`（影响生成的 API 风格）：
   - 询问方式："请确认 ES 客户端版本：new（ElasticsearchClient，适用于 ES 8.x+）还是 old（RestHighLevelClient，适用于 ES 7.x）？"
   - 如用户不确定，提示："如果 ES 版本 ≥ 8.0，建议使用 new；如 ES 版本为 7.x，使用 old"
2. **环境信息查询**：按 **paas-cli Skill** 在终端执行 `$PAAS_CLI` 命令获取 ES 连接信息
   ```
   $PAAS_CLI es config --project {project_id} --env {env}
   ```
   - 如 paas-cli Skill 下 `$PAAS_CLI` 执行失败，提示用户检查安装及网络连通性，改为手动输入 ES 地址
3. **代码生成**：根据 `language` + `client_version` 选择对应模板，生成文件
   > 详细代码模板参见 `references/es-client-templates/` 目录
   
   | 组合 | 生成文件 |
   |------|---------|
   | Java + new | ElasticsearchConfig.java、EsDocumentService.java、application.yml |
   | Java + old | EsRestHighLevelConfig.java、EsDocumentService.java、application.yml |
   | Go | es_client.go、config.yaml |
   | Python | es_client.py、config.py |
   | Node.js | elasticsearch_client.js、config.js |

4. **文件写入**：将生成的代码写入 `target_path` 指定目录
5. **依赖提示**：列出需要添加的依赖
   - **Java + new**：`co.elastic.clients:elasticsearch-java:8.x.x`、`com.fasterxml.jackson.core:jackson-databind`、`org.elasticsearch.client:elasticsearch-rest-client`
   - **Java + old**：`org.elasticsearch.client:elasticsearch-rest-high-level-client:7.x.x`
   - **Go**：`go get github.com/elastic/go-elasticsearch/v8` 或 `v7`
   - **Python**：`pip install elasticsearch`
   - **Node.js**：`npm install @elastic/elasticsearch`

### 输出格式

```
✅ 客户端代码已生成

📁 生成文件列表：
  - {文件路径1} — {文件说明}
  - {文件路径2} — {文件说明}

📝 后续步骤：
  1. 添加依赖：{依赖信息}
  2. 配置环境变量：ES_PASSWORD={实际密码}
  3. 根据业务需求修改索引映射定义

⚠️ 注意事项：
  - 密码以 ${ES_PASSWORD} 占位符形式写入，请通过环境变量或密钥管理系统注入实际值
  - {其他注意事项，如版本兼容性提示}
```

### 异常处理

- paas-cli 命令执行失败 → 提示用户检查 paas-cli 是否安装及网络连通性，改为手动输入 ES 地址
- 目标路径不存在 → 询问用户是否创建目录
- 文件已存在 → 询问用户是否覆盖

---

## 能力二：代码优化检查

### 触发条件

用户请求检查 ES 代码优化，如：
- "检查 ES 代码"
- "Elasticsearch 代码审计"
- "ES 代码优化"
- "检查搜索代码规范"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| scan_path | string | 是 | — | 需扫描的项目根目录 |

### 检查规则清单

> 详细规则说明、检查方法和代码示例参见 `references/es-audit-rules/` 目录

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| ES-001 | 深分页应使用 search_after 替代 from/size | 🔴 严重 |
| ES-002 | bulk 操作的批次大小应合理（建议 5-15MB） | 🟡 警告 |
| ES-003 | 索引映射设计是否合理（避免 dynamic mapping 导致类型混乱） | 🟡 警告 |
| ES-004 | 高消耗脚本查询检测（script_query、painless 脚本） | 🔴 严重 |
| ES-005 | 是否使用批量操作替代单条操作（批量索引/批量更新） | 🔵 建议 |
| ES-006 | 连接超时和重试配置是否合理 | 🟡 警告 |
| ES-007 | 密码是否硬编码 | 🔴 严重 |
| ES-008 | 是否合理使用索引别名（而非直接操作索引名） | 🔵 建议 |

### 检查流程

1. **确认扫描路径**：确认 `scan_path` 参数，缺失时主动询问
2. **识别 ES 客户端类型**：通过搜索代码判断项目使用的是新版还是旧版 ES 客户端
   - 搜索 `ElasticsearchClient` → 新版
   - 搜索 `RestHighLevelClient` → 旧版
3. **扫描 ES 相关代码**：使用 `search_codebase` 和 `grep_code` 工具按规则逐项搜索
   - 搜索关键词：`SearchRequest`、`IndexRequest`、`BulkRequest`、`script`、`from`、`size`、`password`、`alias`、`mapping`、`timeout`、`retry` 等
4. **逐规则检查**：按 ES-001 ~ ES-008 逐项检查，记录发现的问题
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
- 未找到 ES 相关代码 → 告知用户未检测到 Elasticsearch 客户端代码

---

## 能力三：集群交互

### 触发条件

用户请求与 ES 集群进行交互，如：
- "查看 ES 集群状态"
- "ES 索引列表"
- "创建 ES 索引"
- "ES 扩缩容"
- "ES 节点磁盘"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境：DEV / SIT / SRV |
| action | enum | 是 | — | 操作类型（见操作矩阵） |

### 操作矩阵

> 详细操作说明、额外参数和命令模板参见 `references/es-cluster-ops/` 目录

| 操作类型 | 命令模板（paas-cli Skill，`$PAAS_CLI`） | 风险等级 | 需确认 |
|---------|-------------------|---------|--------|
| 查看集群状态 | `$PAAS_CLI es info --project {project_id} --env {env}` | 🟢 | 否 |
| 查看节点磁盘使用率 | `$PAAS_CLI es disk-usage --project {project_id} --env {env}` | 🟢 | 否 |
| 查看索引状态 | `$PAAS_CLI es indices --project {project_id} --env {env}` | 🟢 | 否 |
| 创建索引 | `$PAAS_CLI es create-index --project {project_id} --env {env} --name {index_name} --shards {n} --replicas {n}` | 🟡 | 是 |
| 索引滚动 | `$PAAS_CLI es rollover --project {project_id} --env {env} --alias {alias}` | 🟡 | 是 |
| Force merge | `$PAAS_CLI es force-merge --project {project_id} --env {env} --index {index_name} --max-segments {n}` | 🟡 | 是 |
| 扩缩容 | `$PAAS_CLI es scale --project {project_id} --env {env} --nodes {count}` | 🟡 | 是 |
| 查看服务租期 | `$PAAS_CLI es lease status --project {project_id} --env {env}` | 🟢 | 否 |
| 续期服务租期 | `$PAAS_CLI es lease renew --project {project_id} --env {env} --duration {months}` | 🟡 | 是 |
| 升级版本 | `$PAAS_CLI es upgrade --project {project_id} --env {env} --version {version}` | 🔴 | 是 |
| 删除集群 | `$PAAS_CLI es delete --project {project_id} --env {env}` | 🔴 | 是 |

### 前置条件检查

执行集群操作前，先检查：
1. **解析 CLI 路径**：按 `_shared-references/cli-tooling.md` 设置 `PAAS_CLI`
2. 按 **paas-cli Skill** 检查 `$PAAS_CLI` 是否可用：执行 `$PAAS_CLI version`
   - 失败 → 提示遵循 paas-cli Skill 或确认 `skills/paas-cli/paas-cli.py` 存在（见 **paas-cli Skill**（`skills/paas-cli/SKILL.md`））
3. 检查网络连通性：执行 `$PAAS_CLI ping`
   - 失败 → 提示用户检查网络连接

### 确认流程

1. 🟢 低风险操作：直接执行，无需确认
2. 🟡 中风险操作：
   - 向用户展示即将执行的完整命令
   - 询问"是否继续执行？"
   - 获得肯定回复后执行；拒绝则取消
3. 🔴 高风险操作：
   - 向用户展示完整命令及操作影响说明
   - 要求用户明确回复"确认"后方可执行
   - 用户拒绝或超时未确认 → 取消操作，不执行任何命令

### 输出格式

```
🔧 集群操作结果

操作：{操作类型}
目标：Elasticsearch / {环境} / {集群标识}
状态：✅ 成功 / ❌ 失败

📊 返回信息：
{paas-cli 命令输出内容}

⏱️ 执行耗时：{N}秒
```

### 异常处理

- paas-cli 未安装 → 提示安装方式
- 命令执行超时 → 提示用户检查网络，建议加 `--timeout` 参数重试
- 权限不足 → 提示用户联系管理员授权
- 参数包含危险字符 → 拒绝执行并提示用户

---

## 能力四：故障排查

### 触发条件

用户请求 ES 故障排查或描述 ES 集群/查询异常，如：
- "ES 故障排查"
- "我的 Elasticsearch 查询很慢"
- "ES 集群 Red"
- "搜索服务异常"
- "ES 写入失败"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境 |
| namespace | string | 是 | — | ES 实例所在的 K8s 命名空间 |
| instance | string | 是 | — | ES 实例名称 |
| symptom | string | 否 | — | 用户描述的异常现象 |

### 租期过期专项排查

当用户报告 ES 客户端连接失败，且错误信息涉及连接超时、拒绝连接或认证失败时，应优先检查服务租期是否过期：

1. **租期状态查询**：按 **paas-cli Skill** 在终端执行 `$PAAS_CLI` 检查租期
   ```
   $PAAS_CLI es lease status --project {project_id} --env {env}
   ```
2. **租期续期**：如租期已过期，按 **paas-cli Skill** 执行续期命令（🟡 中风险，需确认）
   ```
   $PAAS_CLI es lease renew --project {project_id} --env {env} --duration {months}
   ```
   - `--duration` 参数单位为月，默认值为 **3**（即 3 个月）
   - 需向用户交互确认续期时长，提供默认值 3 个月
3. **续期后验证**：续期成功后，引导用户重启应用以重新建立连接

### 诊断流程

> 详细诊断能力说明和诊断脚本参见 `references/es-troubleshooting/` 目录

1. **信息收集**：记录用户描述的异常现象（symptom），如集群状态异常、查询缓慢、写入拒绝等
2. **租期检查**（连接失败时优先）：如症状为连接失败/拒绝连接/认证失败，先按 **租期过期专项排查** 检查租期状态
3. **集群状态检查**：按 **paas-cli Skill** 在终端执行 `$PAAS_CLI` 查看 ES 集群基本状态
   ```
   $PAAS_CLI es info --project {project_id} --env {env}
   ```
   - 检查集群健康状态（Green / Yellow / Red）
   - 检查节点数量和状态
3. **扁鹊诊断**：通过终端调用扁鹊平台执行 ES 诊断命令
   ```
   bianque elasticsearch check -n {namespace} -i {instance} -v true -o 50
   ```
   - 扁鹊诊断命令默认超时 60 秒（部分诊断脚本执行时间较长）
   - 如扁鹊不可达，回退到仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 状态检查，在报告中注明
4. **补充信息收集**（可选）：如集群状态为 yellow/red，进一步查询：
   ```
   $PAAS_CLI es indices --project {project_id} --env {env}
   $PAAS_CLI es disk-usage --project {project_id} --env {env}
   ```
   - 查看未分配分片详情
   - 检查磁盘水位线状态
5. **结果分析与建议**：综合诊断数据，生成处理建议，按优先级排序

### 诊断能力

| 诊断项 | 检查内容 | 数据来源 |
|--------|---------|---------|
| 集群健康状态 | Red / Yellow / Green 及原因 | bianque Skill + paas-cli Skill |
| 未分配分片 | UNASSIGNED 分片及分配失败原因 | 扁鹊 |
| CPU 热点 | 节点 CPU 使用率及热线程 | 扁鹊 |
| 写入拒绝 | 磁盘水位线、线程池队列拒绝 | 扁鹊 |
| 索引健康 | 副本分片状态、段合并情况 | 扁鹊 |
| 客户端连通性 | ES 客户端读写验证 | 扁鹊 |
| 服务租期状态 | 服务租期是否过期 | paas-cli Skill（`$PAAS_CLI es lease status`） |

> 上述诊断项均通过 `bianque elasticsearch check` 命令执行，使用 `-v true` 展示详情，`-o` 指定错误日志输出行数

### 降级方案

当扁鹊平台不可达时，仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 诊断：
1. 查看集群状态：**paas-cli Skill**：`$PAAS_CLI es info`
2. 查看索引状态：**paas-cli Skill**：`$PAAS_CLI es indices`
3. 查看磁盘使用：**paas-cli Skill**：`$PAAS_CLI es disk-usage`
4. 基于上述信息提供有限的分析和建议

### 输出格式

```
🔍 故障诊断报告

🩺 诊断目标：Elasticsearch / {集群标识}
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

用户请求 ES 服务接入指导，如：
- "ES 服务如何接入"
- "搜索设计指引"
- "Elasticsearch 开发规范"
- "ES 上线检查"
- "索引设计原则"
- "分词器怎么选"

### 指引内容

> 完整接入指引参见 `references/es-access-guide/` 目录

**设计指引**
- ES 依赖设计（交易类/非交易类接口的熔断与降级）
- 数据隔离规则（按业务领域/可用性等级拆分）
- 部署模式选型（混合 vs 角色分离，规格选型）
- 持久化模式选型（同步刷盘/异步刷盘）
- 命名设计（索引/字段命名规范）
- 分词器选择（standard/keyword/IK/pinyin/自定义）
- 索引设计（主分片/副本分片/分片限制）
- Mapping 设计（字段类型选择/多字段配置/聚合优化）
- 查询设计（DSL 语法/性能优化/聚合查询/相关性评分）

**开发指引**
- 服务端版本要求（7.17+ / 8.12+）
- 客户端版本要求（elasticsearch-java，版本与服务端一致）
- Spring Boot 兼容性（3.x→ES 8.x / 2.x→ES 7.x）
- 服务端关键配置参数（JVM/分片/刷新间隔）
- 客户端关键配置参数（连接池/超时/重试/压缩）
- 安全编码（强制认证，禁止无认证）
- 容错开发（健康检查/重试/降级/熔断）

**测试指引**
- 性能测试（全链路测试、容量评估）
- 专项测试案例（data/master 节点宕机/网络延迟/网络丢包）

**上线指引**
- 前置资源准备（部署模式/资源需求/容灾要求/定制化需求）
- 告警原则确认
- 接入前置检查（客户端配置/生产资源/网络连通性/连接认证）
- 应急卡片准备

### 输出格式

```
📖 Elasticsearch 服务接入指引

根据您的需求，以下是相关指引：

**{指引类别}**
{具体指引内容摘要}

📎 详细内容请参考：references/es-access-guide/ 目录
```

---

## 变更记录

- v1.4.0 (2026-05-26): 所有 paas-cli 操作改为委托 **paas-cli Skill**
- v1.5.0 (2026-05-27): 新增服务租期管理（`es lease status/renew`），故障排查优先检查租期过期
- v1.3.0 (2026-05-26): Skill 与 CLI 路径统一为项目根 `skills/`（移除 `.trae/`）
- v1.2.0 (2026-05-15): 重构 references 目录结构，将大文件拆分为模块化文件夹（es-audit-rules/、es-client-templates/、es-access-guide/、es-cluster-ops/、es-troubleshooting/），优化 LLM 上下文窗口使用效率
- v1.1.0 (2026-05-12): 新增服务接入指引能力，涵盖设计、开发、测试、上线全生命周期指导
- v1.0.0 (2026-05-11): 初始版本，包含客户端创建与配置、代码优化检查、集群交互、故障排查四项基础能力