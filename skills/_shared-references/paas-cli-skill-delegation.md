# paas-cli Skill 委托（共享参考）

中间件专项 Skill（`middleware-nacos`、`middleware-redis`、`middleware-es`）及入口 Skill 凡涉及 PaaS 平台命令行操作时，**须先遵循 paas-cli Skill**，不得绕过该 Skill 直接拼凑或执行命令。

## 必须加载的 Skill

| Skill | 路径 | 职责 |
|-------|------|------|
| **paas-cli** | `skills/paas-cli/SKILL.md` | `$PAAS_CLI` 路径解析、子命令选型、CRD 工作目录 |
| 命令全集 | `skills/paas-cli/references/COMMANDS.md` | 各中间件子命令参数与示例 |
| 配置说明 | `skills/paas-cli/references/CONFIG.md` | gateway.yaml、CRD YAML |

## 执行顺序（阻塞）

1. **遵循 paas-cli Skill**：按其中「路径解析」完成 `$PAAS_CLI` 设置——**先** `paas-cli version` 成功则 `PAAS_CLI=paas-cli`，**否则**降级 `python3 skills/paas-cli/paas-cli.py` 并执行 `version` 校验；再按需执行 `$PAAS_CLI ping` 等
2. **选取子命令**：从 paas-cli Skill 的 `references/COMMANDS.md` 确认完整命令格式（如 `nacos config`、`redis info`）
3. **安全校验**：参数符合 `_shared-references/cli-security-rules.md` 白名单
4. **终端执行**：运行 `$PAAS_CLI <subcommand> ...`，在对话中展示**实际完整命令**与输出

## 表述约定

- 中间件 Skill 正文中的「`paas-cli …`」均指经 **paas-cli Skill** 编排后的 **`$PAAS_CLI …`**
- 输出中的「来源：paas-cli」应写为 **「来源：paas-cli Skill（`$PAAS_CLI`）」**
- 安装/失败提示：引导用户阅读 **paas-cli Skill**，而非仅说「安装 paas-cli 工具」

## 与 bianque Skill 的关系

故障排查中如需诊断 CLI，先 **paas-cli Skill**（集群状态、配置列表等），再 **bianque Skill**（`skills/bianque/SKILL.md`）。扁鹊不可达时，降级为仅通过 paas-cli Skill 执行基础 `$PAAS_CLI` 查询。
