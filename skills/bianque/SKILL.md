---
name: "bianque"
version: "1.2.0"
description: "扁鹊中间件诊断 CLI（Mock）。检查 Nacos/Redis/ES 实例健康、日志与客户端连通性。触发词：bianque、扁鹊、故障诊断、nacos check、redis check、elasticsearch check"
---

# bianque（扁鹊）

## 功能概述

本 Skill 描述仓库内 **Mock 版 bianque** 诊断 CLI 的安装位置、调用方式与命令全集。供 `middleware-nacos`、`middleware-redis`、`middleware-es` 的 **故障排查** 能力在终端执行诊断命令时引用。

**可执行文件位置**（相对项目根）：

| 文件 | 路径 |
|------|------|
| Python 入口 | `skills/bianque/bianque.py` |
| Windows 入口 | `skills/bianque/bianque.cmd` |

## 路径解析（与中间件 Skill 共用）

> 详见 `_shared-references/cli-tooling.md`

**优先级：`bianque` 命令 → 项目 Python 程序**。

### 1. 优先：判定 `bianque` 命令

```bash
bianque version    # 须退出码为 0
```

- 成功 → `BIANQUE="bianque"`，本步结束
- 失败 → 进入步骤 2

### 2. 降级：当前项目内的 Python 程序

```bash
test -f skills/bianque/bianque.py
BIANQUE="python3 skills/bianque/bianque.py"
$BIANQUE version
```

- 文件存在且 `version` 成功 → 使用项目 Mock
- 仍失败 → 解析失败

## 命令格式

```text
bianque <middleware> <subcommand> [options]
```

| middleware | 子命令 | 用途 |
|------------|--------|------|
| `nacos` | `check` | 集群健康、日志、Raft、连通性 |
| `nacos` | `client` | 客户端连接验证 |
| `redis` | `check` / `client` / `updateRenameConfig` / `clusterUpgradeRecover` | 见参考文档 |
| `elasticsearch` | `check` / `client` | 见参考文档 |

**全局参数**：`--token-file <path>` — 权限验证脚本（API 地址与 Token）

详细参数与示例见 `references/COMMANDS.md`。

## 与中间件 Skill 的关系

| 中间件 Skill | 典型命令 |
|-------------|---------|
| middleware-nacos | `bianque nacos check -n {namespace} -i {instance} -v true` |
| middleware-redis | `bianque redis check -n {namespace} -i {instance} -t {type} -v true` |
| middleware-es | `bianque elasticsearch check -n {namespace} -i {instance} -v true` |

扁鹊不可达时，各中间件 Skill 按自身 **降级方案**，回退为仅通过 **paas-cli Skill** 执行基础 `$PAAS_CLI` 检查。

## 可选：加入 PATH

```bash
export PATH="$(pwd)/skills/bianque:$PATH"
```

## 变更记录

- v1.2.0 (2026-05-26): 路径解析与 paas-cli 对齐（`bianque version` → 项目 `bianque.py version`）；Mock 支持 `version` 子命令
- v1.1.0 (2026-05-26): 路径统一为项目根 `skills/bianque/`（移除 `.trae` 目录）
- v1.0.0 (2026-05-26): 初始版本，Mock 诊断 CLI 与命令参考
