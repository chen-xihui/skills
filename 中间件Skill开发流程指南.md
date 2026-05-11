# 中间件 Skill 项目开发流程指南

**版本**：V1.0
**日期**：2026-05-07
**开发平台**：Qoder AI IDE

---

## 目录

1. [开发流程总览](#1-开发流程总览)
2. [前置准备](#2-前置准备)
3. [Phase 1 开发流程：核心 Skill + 纯智能体能力（MVP）](#3-phase-1-开发流程核心-skill--纯智能体能力mvp)
4. [Phase 2 开发流程：集群操作 + paas-cli 集成](#4-phase-2-开发流程集群操作--paas-cli-集成)
5. [Phase 3 开发流程：故障排查 + 扁鹊集成](#5-phase-3-开发流程故障排查--扁鹊集成)
6. [Phase 4-6 开发流程：增强与扩展](#6-phase-4-6-开发流程增强与扩展)
7. [Skill 质量验证流程](#7-skill-质量验证流程)
8. [Skill 发布与分发流程](#8-skill-发布与分发流程)
9. [常见问题与排查](#9-常见问题与排查)

---

## 1. 开发流程总览

### 1.1 全局工作流

```
需求文档 ──→ Skill 设计 ──→ Skill 编写 ──→ 即时验证 ──→ 迭代优化 ──→ 版本发布
   │              │              │              │             │            │
   │              │              │              │             │            ▼
   │              │              │              │             │       Git Tag
   │              │              │              │             │       CHANGELOG
   │              │              │              │             │
   │              │              │              ▼             │
   │              │              │         Qoder 对话测试     │
   │              │              │         (即时反馈)         │
   │              │              │                            │
   │              │              ▼                            │
   │              │     /create-skill 或手动编写               │
   │              │     SKILL.md + references/                │
   │              │                                        │
   │              ▼                                        │
   │       参照需求文档第 4.1 节                              │
   │       Skill 文件结构模板                                 │
   │                                                     │
   ▼                                                    │
 中间件Skill需求文档.md ───────────────────────────────────┘
```

### 1.2 Qoder 驱动开发的核心原则

| 原则 | 说明 |
|------|------|
| **对话即开发** | 通过 Qoder 对话窗口描述需求，Qoder 自动生成/修改 Skill 文件 |
| **即时验证** | 保存后即可通过对话测试 Skill 效果，无需编译/部署等待 |
| **渐进式编写** | 先写核心流程（触发条件+处理步骤+输出格式），再补充细节（异常处理、边界条件） |
| **references 分离** | 规则清单、命令模板等大量内容放入 `references/`，SKILL.md 保持精简（< 500 行） |

### 1.3 Qoder 可用工具与 Skill 能力映射

| Skill 能力 | 主要使用的 Qoder 工具 | 辅助工具 |
|-----------|---------------------|---------|
| 客户端代码生成 | `create_file`（写入代码）、`search_replace`（修改配置） | `read_file`（读取项目结构）、`search_codebase`（查找已有配置） |
| 代码优化检查 | `search_codebase`（语义搜索代码模式）、`grep_code`（规则匹配） | `read_file`（读取具体文件）、`get_problems`（获取 IDE 诊断） |
| 集群交互 | `run_in_terminal`（执行 paas-cli 命令） | `read_file`（读取命令输出） |
| 故障排查 | `run_in_terminal`（执行扁鹊/paas-cli 命令） | `search_codebase`（搜索相关配置） |

---

## 2. 前置准备

### 2.1 项目目录初始化

在 Qoder 中打开项目后，通过对话请求创建目录结构：

```
对话示例：
"帮我初始化中间件 Skill 项目的目录结构，包含 middleware、middleware-nacos、middleware-redis、middleware-es 四个 Skill 目录"
```

Qoder 将创建：

```
.trae/skills/
 ├── middleware/
 │   └── SKILL.md
 ├── middleware-nacos/
 │   ├── SKILL.md
 │   └── references/
 ├── middleware-redis/
 │   ├── SKILL.md
 │   └── references/
 └── middleware-es/
     ├── SKILL.md
     └── references/
```

### 2.2 使用 /create-skill 初始化

也可通过 Qoder 的内置 Skill 创建工具初始化：

```
对话示例：
"/create-skill 创建一个 Nacos 中间件运维技能，提供客户端创建、代码优化检查、集群操作和故障排查能力"
```

Qoder 会通过交互式对话引导你完成：
1. Skill 名称（middleware-nacos）
2. 描述（用于自动触发）
3. 使用场景
4. 工作流步骤
5. 输出格式

生成初版 SKILL.md 后，再根据需求文档进行完善。

### 2.3 需求文档就绪

确保 `中间件Skill需求文档.md` 已在项目根目录，Qoder 可随时引用其中的规范。

---

## 3. Phase 1 开发流程：核心 Skill + 纯智能体能力（MVP）

**目标**：客户端代码生成 + 代码优化检查，零外部依赖

### 3.1 开发顺序

建议按以下顺序逐步完成，每完成一个 Skill 立即验证：

```
middleware（入口路由） → middleware-nacos → middleware-redis → middleware-es
```

### 3.2 通用入口 Skill 开发

**步骤 1：创建 SKILL.md**

```
对话示例：
"参照需求文档第 3.3 节和第 4.1 节，创建 middleware 通用入口 Skill。
它的职责是识别用户提到的中间件类型，然后将请求路由到对应的专项 Skill。
支持 Nacos、Redis、ES 三种中间件。"
```

**步骤 2：定义路由逻辑**

在 SKILL.md 中编写路由决策逻辑：

```markdown
## 路由规则

当用户请求涉及以下关键词时，激活对应专项 Skill：
- Nacos / 注册中心 / 配置中心 / 命名空间 → 使用 middleware-nacos Skill
- Redis / 缓存 / 缓存数据库 / 哨兵 → 使用 middleware-redis Skill
- ES / Elasticsearch / 搜索引擎 / 索引 → 使用 middleware-es Skill

如用户同时提及多个中间件，依次调用对应 Skill 并综合结果。
```

**步骤 3：即时验证**

```
对话示例：
"我的 Nacos 连不上了"
→ 期望：智能体自动路由到 middleware-nacos Skill

"检查 Redis 代码"
→ 期望：智能体自动路由到 middleware-redis Skill

"ES 集群状态怎么样"
→ 期望：智能体自动路由到 middleware-es Skill
```

### 3.3 专项 Skill 开发（以 Nacos 为例）

#### 3.3.1 客户端生成能力

**步骤 1：编写核心流程**

```
对话示例：
"参照需求文档第 5.1 节，在 middleware-nacos/SKILL.md 中添加客户端创建与配置能力。
包含参数表（project_id, env, auth_user, auth_pass, target_path, language）、
处理流程（5 步）、输出格式（按第 4.3.1 节）、异常处理（3 种场景）。"
```

**步骤 2：提取模板到 references/**

```
对话示例：
"将 Nacos 客户端的 Java 代码模板和配置文件模板提取到
middleware-nacos/references/nacos-java-template.md 中，
在 SKILL.md 中引用该文件。同时对 Go 和 Python 模板也创建对应 references 文件。"
```

生成文件结构：

```
middleware-nacos/
 ├── SKILL.md
 └── references/
     ├── nacos-java-template.md      # Java 模板（NacosConfigService、bootstrap.yml）
     ├── nacos-go-template.md        # Go 模板
     └── nacos-python-template.md    # Python 模板
```

**步骤 3：即时验证**

```
对话示例：
"使用 Nacos 作为注册中心，项目组 j036x0，用户名 admin，密码 secret123，
环境 DEV，请在 src/main/java 下创建客户端"
→ 期望：生成 NacosConfigService.java、NacosDiscoveryService.java、bootstrap.yml

"我需要 Go 语言的 Nacos 客户端，项目组 j036x0，环境 SIT"
→ 期望：生成 nacos_client.go、config.yaml
```

#### 3.3.2 代码优化检查能力

**步骤 1：编写检查规则**

```
对话示例：
"参照需求文档第 5.2 节，在 middleware-nacos/SKILL.md 中添加代码优化检查能力。
将 7 条检查规则（NACOS-001 到 NACOS-007）的详细说明提取到
middleware-nacos/references/nacos-audit-rules.md 中，
SKILL.md 中仅引用规则文件并定义检查流程和输出格式。"
```

**步骤 2：即时验证**

```
对话示例（在一个包含 Nacos 客户端代码的项目中）：
"检查 Nacos 代码优化"
→ 期望：输出结构化审计报告，按 4.3.2 格式

"帮我扫描 src/main 下 Nacos 相关的代码问题"
→ 期望：触发代码审计，输出含规则ID和风险等级的报告
```

**步骤 3：迭代优化**

如果审计结果不准确，通过对话精化规则描述：

```
对话示例：
"NACOS-003 规则误报太多了，循环中的 getConfig 调用如果在初始化阶段（如 @PostConstruct）
应该是合理的。请在 nacos-audit-rules.md 中补充排除条件：仅当循环为运行时重复调用
（如 while/for 循环体内每次请求都调用）时才判定为问题，初始化阶段的一次性调用不算。"
```

### 3.4 Redis 和 ES Skill 开发

重复 3.3 的流程，分别开发 Redis 和 ES 的客户端生成和代码审计能力。

**关键差异点**：

| Skill | 客户端生成特有参数 | 审计规则文件 |
|-------|-----------------|------------|
| Redis | `mode`（standalone/sentinel/cluster）、`client_type`（jedis/lettuce） | `redis-audit-rules.md`（8 条规则） |
| ES | `client_version`（new/old） | `es-audit-rules.md`（8 条规则） |

### 3.5 Phase 1 验收检查清单

完成所有 Skill 后，逐项验证：

```
对话示例：
"逐项验证 Phase 1 验收标准：
1. 生成 Nacos 客户端代码并写入 src/main/java
2. 生成 Redis 客户端代码（Lettuce + Sentinel 模式）
3. 生成 ES 客户端代码（新版 ElasticsearchClient）
4. 扫描项目代码输出 Nacos 审计报告
5. 扫描项目代码输出 Redis 审计报告
6. 扫描项目代码输出 ES 审计报告
7. 缺少参数时主动询问
8. 密码以占位符形式写入配置"
```

---

## 4. Phase 2 开发流程：集群操作 + paas-cli 集成

### 4.1 前置条件确认

```
对话示例：
"检查 paas-cli 是否可用：执行 paas-cli --version"
```

如不可用，Phase 2 的开发仍可进行（编写 Skill 内容），但验证需在 paas-cli 可用环境中进行。

### 4.2 开发步骤

**步骤 1：在通用规范中补充安全规则**

```
对话示例：
"参照需求文档第 9.1 节，在 middleware-nacos/SKILL.md 的集群交互章节中
添加命令注入防护规则：参数白名单校验表、危险字符过滤规则。
将这些通用安全规则提取到一个共享的 references 文件中，
三个专项 Skill 都引用它。"
```

建议创建共享 references：

```
.trae/skills/_shared-references/
 └── cli-security-rules.md     # 命令注入防护规则（三个 Skill 共用）
```

**步骤 2：编写操作矩阵**

```
对话示例：
"参照需求文档第 5.3 节，在 middleware-nacos/SKILL.md 中添加集群交互能力。
包含参数表、8 项操作矩阵（含 paas-cli 命令模板和风险分级）、
确认流程、输出格式。将操作矩阵详情放入
middleware-nacos/references/nacos-cluster-ops.md。"
```

**步骤 3：即时验证**

```
对话示例：
"查看 Nacos DEV 环境 j036x0 的集群信息"
→ 期望：执行 paas-cli 命令，返回集群信息

"删除 Nacos DEV 环境的 order-service 服务"
→ 期望：展示高危操作确认提示，等待确认后才执行
```

### 4.3 Phase 2 验收检查清单

```
1. 查询集群状态 → 直接执行，返回结果
2. 扩缩容操作 → 展示命令后要求确认
3. 删除操作 → 展示命令和影响范围，要求明确"确认"
4. 参数包含分号或管道符 → 拒绝执行并提示
5. paas-cli 未安装 → 提示安装方式
```

---

## 5. Phase 3 开发流程：故障排查 + 扁鹊集成

### 5.1 开发步骤

**步骤 1：编写诊断流程**

```
对话示例：
"参照需求文档第 5.4 节，在 middleware-nacos/SKILL.md 中添加故障排查能力。
包含诊断流程（5 步）、诊断能力表、扁鹊命令模板、降级方案。
将诊断能力详情放入 middleware-nacos/references/nacos-troubleshooting.md。"
```

**步骤 2：即时验证**

```
对话示例：
"Nacos SIT 环境连接超时，项目组 j036x0，帮我排查"
→ 期望：执行诊断流程，先查集群状态，再调扁鹊，输出诊断报告

"扁鹊平台不可达，但我的 Redis 还是连不上"
→ 期望：降级到仅 paas-cli 基本检查
```

### 5.2 Phase 3 验收检查清单

```
1. 正常诊断流程 → 输出含结论、发现、建议的诊断报告
2. 扁鹊不可达 → 自动降级到 paas-cli 基本检查
3. 诊断脚本返回异常 → 展示原始错误，建议联系扁鹊运维
```

---

## 6. Phase 4-6 开发流程：增强与扩展

### 6.1 Phase 4：知识库与智能分析

**步骤 1：创建知识库文件**

```
对话示例：
"在项目中创建 .trae/knowledge/ 目录结构，
包含 middleware-standards/、incident-records/、runbooks/ 三个子目录。
先创建一个空的 nacos-standard.md 模板文件。"
```

**步骤 2：编写规范知识库**

```
对话示例：
"将企业 Nacos 标准规范的关键要点整理到
.trae/knowledge/middleware-standards/nacos-standard.md 中，
按配置规范、服务注册规范、客户端规范三个分类组织。
每个规范条目标明编号，便于代码审计时引用。"
```

**步骤 3：更新 Skill 引用知识库**

```
对话示例：
"在 middleware-nacos/SKILL.md 的代码优化检查章节中，
添加知识库引用指引：审计时先读取 .trae/knowledge/middleware-standards/nacos-standard.md，
除了按 SKILL.md 中的规则清单检查外，还参照知识库中的完整规范进行扩展检查。
输出中增加'参考依据'字段，引用知识库中的具体编号。"
```

**步骤 4：置信度评分和推理链**

```
对话示例：
"参照需求文档第 10.2 节，在三个 Skill 的代码审计和故障排查输出格式中
增加置信度评分（高/中/低）。故障排查增加推理链展示。"
```

### 6.2 Phase 5：跨中间件关联与修复编排

```
对话示例：
"参照需求文档第 10.4 节，在 middleware 入口 Skill 中添加依赖拓扑定义和级联诊断逻辑。
参照第 10.5 节，在三个专项 Skill 中添加修复动作分级和一键修复指引。"
```

### 6.3 Phase 6：持续优化与生态扩展

此阶段为持续迭代，主要工作：
- 收集用户反馈，修正规则误报
- 新增中间件 Skill（按第 11.3 节标准流程）
- Skill 效果评估指标采集
- 定时巡检调度能力

---

## 7. Skill 质量验证流程

### 7.1 单 Skill 验证

每完成一个 Skill 的一个能力后，立即在 Qoder 对话中验证：

```
验证清单模板（以 Nacos 客户端生成为例）：

□ 正常场景：提供完整参数，验证生成正确的代码文件
□ 缺参数：省略 auth_pass，验证智能体主动询问
□ 默认值：省略 language，验证使用 Java 默认值并注明
□ 路径不存在：target_path 不存在，验证询问是否创建
□ 文件已存在：目标路径有文件，验证询问是否覆盖
□ 密码处理：验证密码以 ${NACOS_PASSWORD} 占位符写入
```

### 7.2 交叉验证

确保三个 Skill 的输出格式一致：

```
对话示例：
"分别对 Nacos、Redis、ES 执行代码优化检查，
对比三份审计报告的格式是否一致（都包含规则ID、风险等级、改进建议列）"
```

### 7.3 回归验证

Skill 修改后，验证未破坏已有功能：

```
对话示例：
"我刚刚修改了 middleware-redis 的代码审计规则，
请重新测试以下场景：
1. 正常审计输出
2. 缺少 scan_path 参数
3. 未找到 Redis 相关代码"
```

### 7.4 验证记录

建议在项目中维护一个简单的验证记录文件：

```
.trae/skills/_test-records/
 ├── nacos-client-gen.md       # Nacos 客户端生成验证记录
 ├── nacos-code-audit.md       # Nacos 代码审计验证记录
 ├── redis-client-gen.md       # ...
 └── ...
```

每条记录包含：测试时间、测试场景、输入参数、预期输出、实际输出、是否通过。

---

## 8. Skill 发布与分发流程

### 8.1 发布流程

```
1. 完成当前 Phase 所有 Skill 的开发和验证
2. 更新每个 SKILL.md 的 version 字段
3. 更新仓库 CHANGELOG.md
4. Git commit + tag（如 v1.2.0）
5. Git push（含 tag）
6. 通知用户更新
```

### 8.2 Qoder 中的版本更新操作

```
对话示例：
"帮我更新所有 Skill 的版本号到 1.2.0，
并在 CHANGELOG.md 中添加本版本变更记录：
- Added: Nacos/Redis/ES 故障排查能力
- Fixed: Redis REDIS-004 规则误报"

"创建 Git tag v1.2.0"
```

### 8.3 安装方式（参照需求文档第 12 章）

| 方式 | 命令 |
|------|------|
| 一键安装 | `npx skills add <org>/middleware-skills/middleware-nacos` |
| Git 子模块 | `git submodule add <repo-url> .trae/skills-external/middleware-skills` |
| 手动复制 | 将 SKILL.md 复制到 `.trae/skills/middleware-nacos/` |

---

## 9. 常见问题与排查

### 9.1 Skill 未被自动触发

**症状**：用户说了"检查 Nacos 代码"，但智能体没有使用 middleware-nacos Skill。

**排查**：

1. 检查 SKILL.md 的 `description` 字段是否包含触发关键词（如 "Nacos"、"代码优化检查"）
2. 确认 SKILL.md 文件位于 `.trae/skills/middleware-nacos/` 目录下
3. 尝试使用斜杠命令强制触发：`/middleware-nacos`

**修复**：

```
对话示例：
"middleware-nacos Skill 的 description 触发词不够丰富，
请补充以下触发场景：'Nacos代码检查'、'Nacos代码审计'、
'检查Nacos配置'、'Nacos代码优化'、'Nacos代码规范'"
```

### 9.2 Skill 输出格式不一致

**症状**：不同 Skill 的审计报告格式有差异。

**排查**：

1. 检查各 SKILL.md 是否引用了相同的输出格式定义（第 4.3 节）
2. 将通用输出格式提取到 `_shared-references/output-formats.md`，各 Skill 统一引用

**修复**：

```
对话示例：
"将需求文档第 4.3 节的四种输出格式模板提取到
.trae/skills/_shared-references/output-formats.md 中，
然后更新三个 Skill 的 SKILL.md，统一引用该文件"
```

### 9.3 Skill 内容过长导致效果下降

**症状**：智能体输出质量下降，遗漏 SKILL.md 中的步骤。

**排查**：

1. 检查 SKILL.md 行数是否超过 500 行
2. 如果是，将详细规则/模板拆分到 `references/` 目录

**修复**：

```
对话示例：
"middleware-redis/SKILL.md 超过了 500 行，
请将检查规则详情移到 references/redis-audit-rules.md，
将集群操作矩阵移到 references/redis-cluster-ops.md，
SKILL.md 中只保留流程指引和 references 引用"
```

### 9.4 paas-cli 命令执行失败

**症状**：终端命令执行报错。

**排查步骤**：

1. 确认 paas-cli 已安装：`paas-cli --version`
2. 确认网络连通：`paas-cli ping`
3. 确认项目组权限：`paas-cli auth check --project j036x0`
4. 检查参数是否包含特殊字符（被安全规则拦截）

---

**文档结束**
