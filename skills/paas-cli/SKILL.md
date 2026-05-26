---
name: "paas-cli"
version: "1.4.1"
description: "PaaS 中间件运维 CLI（Mock）。执行集群查询、授权检查、连接配置拉取及 CRD 运维。触发词：paas-cli、PaaS CLI、集群运维、auth check、nacos config、redis config、es config"
---

# paas-cli

## 功能概述

本 Skill 是 **PaaS 命令行的唯一入口**：描述仓库内 Mock 版 paas-cli（v2.4.1）的路径解析、调用方式与命令全集。

`middleware-nacos`、`middleware-redis`、`middleware-es` 等专项 Skill **不得绕过本 Skill 直接执行 paas-cli 可执行文件**；须先遵循本 Skill 完成 `$PAAS_CLI` 解析，再按 `references/COMMANDS.md` 构造子命令。

**可执行文件位置**（相对项目根）：

| 文件 | 路径 |
|------|------|
| Python 入口 | `skills/paas-cli/paas-cli.py` |
| Windows 入口 | `skills/paas-cli/paas-cli.cmd` |
| 网关配置 | `skills/paas-cli/config/gateway.yaml` |
| CRD YAML | `skills/paas-cli/config/{nacos,redis,es}/` |

## 路径解析（与中间件 Skill 共用）

> 详见 `_shared-references/cli-tooling.md`

**优先级：`paas-cli` 命令 → 项目 Python 程序**。解析结果存入 `$PAAS_CLI`，后续子命令均写作 `$PAAS_CLI <subcommand> ...`。

### 1. 优先：判定 `paas-cli` 命令

直接执行（用于探测 PATH 中是否存在可用 `paas-cli`）：

```bash
paas-cli version    # 须退出码为 0
```

- 成功 → `PAAS_CLI="paas-cli"`，**采用 `paas-cli` 命令**（系统或 PATH 安装），本步结束
- 命令不存在（如 `command not found`）或 `version` 失败 → 进入步骤 2

### 2. 降级：当前项目内的 Python 程序

在**工作区根目录**检查项目 Mock：

```bash
test -f skills/paas-cli/paas-cli.py
```

若存在，则：

```bash
PAAS_CLI="python3 skills/paas-cli/paas-cli.py"
$PAAS_CLI version    # 须退出码为 0
```

- 文件存在且 `version` 成功 → 使用项目内 `paas-cli.py`
- 文件不存在，或 `version` 仍失败 → **解析失败**，提示安装 `paas-cli` 或确认项目含 `skills/paas-cli/paas-cli.py`

### 3. 解析完成后

- 在对话中写明最终 `$PAAS_CLI` 的完整形式及 `version` 输出摘要
- 使用步骤 2（Python 程序）且执行 CRD 类命令时，建议在 `skills/paas-cli/` 目录下执行（见下文）

CRD 类命令（`create/get/update/delete` + 资源名）须在 **paas-cli 目录**下执行，或保证 `config/` 相对路径正确：

```bash
cd skills/paas-cli && python3 paas-cli.py get nacosclusterbackup \
  --gateway-config=config/gateway.yaml -f config/nacos/iteration-nacos-cluster-backup-get.yaml
```

## 能力清单

| 类别 | 说明 | 详细文档 |
|------|------|----------|
| 通用 | `--version`、`ping`、`auth check` | `references/COMMANDS.md` §1.1 |
| Nacos | `nacos info/instances/config/...` | `references/COMMANDS.md` §1.2 |
| Redis | `redis info/nodes/config/...` | `references/COMMANDS.md` §1.3 |
| Elasticsearch | `es info/indices/config/...` | `references/COMMANDS.md` §1.4 |
| CRD 运维 | `create/get/update/delete` + 资源类型 | `references/COMMANDS.md` §1.5 |
| 配置说明 | gateway.yaml、YAML 参数 | `references/CONFIG.md` |

## 与中间件 Skill 的关系

| 中间件 Skill | 典型 paas-cli 用法 |
|-------------|-------------------|
| middleware-nacos | `auth check` → `nacos config`（客户端创建）；`nacos info`（集群/排障） |
| middleware-redis | `redis config`（客户端创建）；`redis info`（集群/排障） |
| middleware-es | `es config`（客户端创建）；`es info`（集群/排障） |

执行前须遵守 `_shared-references/cli-security-rules.md`（参数白名单、风险确认）。

## 可选：加入 PATH

```bash
export PATH="$(pwd)/skills/paas-cli:$PATH"
export PATHEXT=".CMD;.PY;$PATHEXT"   # Windows
```

可将项目 `skills/paas-cli` 加入 PATH，使步骤 1 的 `paas-cli version` 能直接命中。中间件 Skill 通过 `_shared-references/paas-cli-skill-delegation.md` 引用本流程。

## 变更记录

- v1.4.1 (2026-05-26): 步骤 1 改为 `paas-cli version` 探测（不再使用 `command -v`）；Mock 支持 `version` 子命令
- v1.4.0 (2026-05-26): 路径解析改为优先 `paas-cli` 命令，失败再降级 Python 程序
- v1.3.0 (2026-05-26): 路径解析改为优先当前项目 Mock，失败再降级系统（已调整，见 v1.4.0）
- v1.2.0 (2026-05-26): 明确为中间件 Skill 唯一 PaaS CLI 入口；中间件须委托本 Skill 而非直接调工具
- v1.1.0 (2026-05-26): 路径统一为项目根 `skills/paas-cli/`（移除 `.trae` 目录）
- v1.0.0 (2026-05-26): 初始版本，Mock CLI 与命令参考
