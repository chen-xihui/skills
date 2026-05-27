# 中间件智能运维 Skill 知识库

面向 **Cursor / Qoder / TRAE** 等 Agent 的 **Nacos / Redis / Elasticsearch** 运维 Skill，含 Mock CLI（`paas-cli`、`bianque`）。

**源码目录（唯一事实源）**：仓库根目录 `skills/`。各 IDE 通过安装脚本**复制**到对应发现路径（不使用符号链接）。

## 目录结构

```
skills/                          # 开发与 Git 管理的源码
├── middleware/                  # 路由入口
├── middleware-{nacos,redis,es}/
│   └── references/capabilities/
├── paas-cli/
├── bianque/
└── _shared-references/
```

## 安装（复制到各 Agent 目录）

在**本仓库根目录**或**目标业务项目根目录**执行（需已包含 `skills/` 源码，或通过 `--project-dir` 指向本仓库）：

```bash
chmod +x scripts/install-skills.sh scripts/validate-skills.sh

# Cursor
./scripts/install-skills.sh cursor

# Qoder（项目级，推荐团队仓库）
./scripts/install-skills.sh qoder

# Qoder（用户级，所有项目可用）
./scripts/install-skills.sh qoder --global

# TRAE
./scripts/install-skills.sh trae

# 一次安装三种 Agent
./scripts/install-skills.sh all
```

安装到**其他业务项目**时：

```bash
./scripts/install-skills.sh all --project-dir /path/to/your-app
```

### 各 Agent 目标路径

| Agent | 项目级路径 | 用户级（可选） |
|-------|------------|----------------|
| **Cursor** | `.cursor/skills/` | — |
| **Qoder** | `.qoder/skills/` | `~/.qoder/skills/`（`qoder --global`） |
| **TRAE** | `.trae/skills/` | — |

修改 `skills/` 源码后，**重新执行**对应安装命令以覆盖副本。

本仓库**不提交** `.cursor/`、`.qoder/`、`.trae/`（已在 `.gitignore` 中忽略）；Cursor 的 hooks/commands 源码在 `integrations/cursor/`，随 `install-skills.sh cursor` 一并安装。

## 验证

```bash
./scripts/validate-skills.sh
python3 skills/paas-cli/paas-cli.py version
python3 skills/bianque/bianque.py version
```

## 加载策略（ECC Agent 模式）

| Skill | 加载方式 |
|-------|----------|
| `middleware` | 入口，识别中间件类型 |
| `middleware-*` | 由入口点名，`disable-model-invocation: true` |
| `paas-cli` / `bianque` | 专项 Skill 委托时加载 |
| `references/capabilities/*.md` | 仅加载与用户意图匹配的一篇 |

## 文档

- `中间件Skill需求精简版.md` — 需求摘要
- `中间件Skill开发流程指南.md` — 开发与验证流程
