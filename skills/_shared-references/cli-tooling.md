# CLI 工具路径解析（共享参考）

本文件说明 **`$PAAS_CLI` / `$BIANQUE` 变量** 的含义。`$PAAS_CLI` 的**权威解析流程**在 **paas-cli Skill**（`skills/paas-cli/SKILL.md` §路径解析）；中间件 Skill 通过 `_shared-references/paas-cli-skill-delegation.md` 委托使用。

---

## 1. `$PAAS_CLI` 解析顺序（paas-cli）

| 优先级 | 条件 | `$PAAS_CLI` |
|--------|------|-------------|
| **1** | `paas-cli version` 退出码为 0 | `paas-cli` |
| **2** | 步骤 1 失败，且项目存在 `skills/paas-cli/paas-cli.py` 且 `python3 skills/paas-cli/paas-cli.py version` 成功 | `python3 skills/paas-cli/paas-cli.py`（相对工作区根） |
| — | 均失败 | 解析失败，不执行后续子命令 |

中间件 Skill 正文中的 `paas-cli …` 均表示经上述流程得到的 **`$PAAS_CLI …`**。

---

## 2. `$BIANQUE` 解析顺序（bianque）

| 优先级 | 条件 | `$BIANQUE` |
|--------|------|-------------|
| **1** | `bianque version` 退出码为 0 | `bianque` |
| **2** | 步骤 1 失败，且项目存在 `skills/bianque/bianque.py` 且 `python3 skills/bianque/bianque.py version` 成功 | `python3 skills/bianque/bianque.py`（相对工作区根） |
| — | 均失败 | 解析失败，不执行后续子命令 |

权威流程见 **bianque Skill**（`skills/bianque/SKILL.md` §路径解析）。中间件 Skill 正文中的 `bianque …` 均表示经上述流程得到的 **`$BIANQUE …`**。

---

## 3. CRD 类命令工作目录

使用步骤 2（Python 程序）时，CRD 命令建议在 `skills/paas-cli/` 下执行，详见 `skills/paas-cli/references/CONFIG.md`。

---

## 4. 目录约定

| 路径 | 说明 |
|------|------|
| `skills/paas-cli/SKILL.md` | paas-cli Skill（路径解析权威） |
| `skills/paas-cli/paas-cli.py` | 项目 Mock 入口（步骤 2 降级） |
| `skills/bianque/bianque.py` | 项目 Mock 诊断入口 |

> 历史目录 `.trae/tools/` 已移除。各 IDE 安装副本见 `scripts/install-skills.sh`（Cursor `.cursor/skills/`、Qoder `.qoder/skills/`、TRAE `.trae/skills/`）；**源码**仍在仓库根 `skills/`。
