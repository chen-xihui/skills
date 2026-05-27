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
| target_path | string | 是 | — | 代码生成目标路径 |
| client_version | enum | 否 | — | new（ElasticsearchClient 8.x+）/ old（RestHighLevelClient 7.x）；**可参考 CLI `Version` 推断** |
| language | enum | 否 | Java | 项目语言：Java / Go / Python / Node.js |

**平台拉取字段（禁止向用户索要或覆盖）**：

| 字段 | 来源 | 说明 |
|------|------|------|
| hosts | `$PAAS_CLI es config` 输出 `Hosts` | 写入配置或 `${ES_HOSTS}` |
| scheme | `$PAAS_CLI es config` 输出 `Scheme` | https/http |
| auth_user | `$PAAS_CLI es config` 输出 `Username` | **一律以平台输出为准**；用户提供的用户名不得覆盖 |
| es_version | `$PAAS_CLI es config` 输出 `Version` | 用于选择 client_version（≥8.0 建议 new） |

**密码**：`$PAAS_CLI es config` 仅返回脱敏密码（如 `********`），**不得**向用户索要明文密码写入代码；生成物统一使用 `${ES_PASSWORD}`，由用户通过环境变量或密钥系统注入。

### 处理流程

1. **参数收集**：确认 `project_id`、`env`、`target_path`、`language`；`client_version` 未指定时，在步骤 3 根据 CLI `Version` 建议 new/old
2. **前置检查（阻塞，须全部成功后才可继续）**：
   - **遵循 paas-cli Skill**：按 `skills/paas-cli/SKILL.md` 完成 `$PAAS_CLI` 解析
   - `$PAAS_CLI version`、`$PAAS_CLI ping`
   - **校验项目组授权（必须）**：
     ```
     $PAAS_CLI auth check --project {project_id}
     ```
     - 授权失败 → **终止流程**，不生成客户端代码
3. **平台连接信息拉取（阻塞）**：
   ```
   $PAAS_CLI es config --project {project_id} --env {env}
   ```
   - 解析：`Hosts` → `hosts`，`Scheme` → `scheme`，`Username` → `auth_user`，`Version` → `es_version`
   - 在对话中完整展示 CLI 命令及解析结果
   - **不得以用户口述或项目内旧配置覆盖 CLI 返回的 `Username`**
4. **确定 client_version**：若用户未指定，按 `es_version`：主版本 ≥8 → `new`，7.x → `old`，并在输出中说明
5. **代码生成**：按 `language` + `client_version` 选择模板
   > 详细代码模板参见 `references/es-client-templates/` 目录

   | 组合 | 生成文件 |
   |------|---------|
   | Java + new | ElasticsearchConfig.java、EsDocumentService.java、application.yml |
   | Java + old | EsRestHighLevelConfig.java、EsDocumentService.java、application.yml |
   | Go | es_client.go、config.yaml |
   | Python | es_client.py、config.py |
   | Node.js | elasticsearch_client.js、config.js |

6. **文件写入**：将生成的代码写入 `target_path`
7. **依赖提示**：列出需要添加的依赖（版本与 `es_version` 对齐）

### 输出格式

```
✅ 客户端代码已生成

🔐 平台信息（来源：paas-cli Skill）：
  - 授权检查：`$PAAS_CLI auth check` --project {project_id} — ✅ 通过
  - 连接配置：`$PAAS_CLI es config` --project {project_id} --env {env}
  - Hosts / Scheme / Username / Version：{hosts} / {scheme} / {auth_user} / {es_version}

📁 生成文件列表：
  - {文件路径1} — {文件说明}

📝 后续步骤：
  1. 添加依赖：{依赖信息}
  2. 配置环境变量：ES_HOSTS、ES_USERNAME（与 CLI 一致）、ES_PASSWORD
  3. 按业务调整索引映射

⚠️ 注意事项：
  - 用户名以平台 CLI 返回为准
  - 密码以 ${ES_PASSWORD} 占位符写入，勿写入明文
  - client_version 与集群 Version 保持一致
```

### 异常处理

- `$PAAS_CLI auth check` 失败或未授权 → **终止**，不生成代码
- `$PAAS_CLI es config` 失败 → 提示遵循 **paas-cli Skill**；**降级**：用户手动提供 `hosts`/`scheme`；`auth_user` 仅在 CLI 不可用时询问，并标注「非平台标准流程」；仍不得索要明文密码
- `$PAAS_CLI version` / `$PAAS_CLI ping` 失败 → 先修复 CLI/网络再执行 `auth check` 与 `es config`
- 目标路径不存在 → 询问是否创建目录
- 文件已存在 → 询问是否覆盖

---
