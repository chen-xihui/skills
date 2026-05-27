# 中间件专项 Skill 通用规范（共享）

各 `middleware-{nacos,redis,es}` 专项 Skill 均须遵守本节；专项白名单扩展见各 Skill 正文或 `references/capabilities/`。

---

## 参数收集原则

1. **优先从上下文推断**：从项目配置、打开文件提取 `project_id`、`language` 等
2. **主动询问缺失参数**：必要参数逐一询问，提供可选值
3. **使用合理默认值**：有默认值时可在输出中注明

---

## CLI Skill 委托

> 详见 `_shared-references/paas-cli-skill-delegation.md`

| 场景 | 须加载的 Skill |
|------|----------------|
| PaaS / 集群 / 连接配置 | `skills/paas-cli/SKILL.md` → `$PAAS_CLI` |
| 故障诊断 | `skills/bianque/SKILL.md` → `$BIANQUE` |

- 不得跳过上述 Skill 直接调用可执行文件
- 正文 `paas-cli …` → **`$PAAS_CLI …`**；`bianque …` → **`$BIANQUE …`**

### 前置检查（涉及终端 CLI 时）

```bash
$PAAS_CLI version
$PAAS_CLI ping
# 诊断场景另需：
$BIANQUE version
```

失败时按对应 Skill 提示处理，勿继续执行 CRD/诊断子命令。

---

## 安全约束

> 详见 `_shared-references/cli-security-rules.md`

- **参数白名单**：CLI 参数须符合白名单
- **危险字符**：禁止 `;` `|` `&` `$` `` ` `` `(` `)` `{` `}` 等 shell 元字符
- **风险确认**：🟡 展示命令后询问；🔴 须用户回复「确认」
- **敏感信息**：密码用 `${*_PASSWORD}` 占位符，禁止明文写入代码
- **操作审计**：CLI 命令与输出须在对话中完整展示

---

## 通用参数白名单

| 参数 | 合法值规则 |
|------|-----------|
| project_id | 小写字母、数字，如 j036x0 |
| env | DEV / SIT / SRV |
| version | 语义化版本号 |
| count / replicas / nodes / shards / months / duration | 正整数（`duration` 用于租约续期，单位：月） |
| namespace | 小写字母、数字、短横线 |
| instance | 字母、数字、短横线 |

---

## 操作风险分级

| 等级 | 类型 | 确认 |
|------|------|------|
| 🟢 | 查询、状态检查 | 直接执行 |
| 🟡 | 创建、扩缩容、配置变更 | 展示命令，用户确认后执行 |
| 🔴 | 升级、删除、Slot 迁移等 | 须明确回复「确认」 |

---

## 代码扫描工具（Harness 映射）

> 详见 `_shared-references/harness-tools.md`

审计能力扫描代码时，按当前 IDE 选用 **Grep** / **SemanticSearch**（或等价工具），勿使用已废弃的 `grep_code` / `search_codebase` 名称。
