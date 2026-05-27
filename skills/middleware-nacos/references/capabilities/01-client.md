## 能力一：客户端创建与配置

### 触发条件

用户请求创建 Nacos 客户端并生成配置，如：
- "创建 Nacos 客户端"
- "生成注册中心连接代码"
- "帮我配置 Nacos"
- "使用 Nacos 作为注册中心"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号，如 j036x0 |
| env | enum | 是 | — | 环境：DEV / SIT / SRV |
| target_path | string | 是 | — | 代码生成目标路径 |
| language | enum | 否 | Java | 项目语言：Java / Go / Python |

**平台拉取字段（禁止向用户索要或覆盖）**：

| 字段 | 来源 | 说明 |
|------|------|------|
| server_addr | paas-cli Skill：`$PAAS_CLI nacos config` 输出 `Server Addr` | 写入配置或 `${NACOS_SERVER_ADDR}` 默认值 |
| namespace | paas-cli Skill：`$PAAS_CLI nacos config` 输出 `Namespace` | 写入配置或 `${NACOS_NAMESPACE}` 默认值 |
| auth_user | paas-cli Skill：`$PAAS_CLI nacos config` 输出 `Username` | **一律以平台输出为准**；用户提供的用户名不得覆盖 |

**密码**：`$PAAS_CLI nacos config` 仅返回脱敏密码（如 `********`），**不得**向用户索要明文密码写入代码；生成物统一使用 `${NACOS_PASSWORD}`，由用户通过环境变量或密钥系统注入。

### 处理流程

1. **参数收集**：确认 `project_id`、`env`、`target_path` 及 `language`（缺省为 Java），缺失项主动询问用户
2. **前置检查（阻塞，须全部成功后才可继续）**：
   - **遵循 paas-cli Skill**：按 `skills/paas-cli/SKILL.md` 完成 `$PAAS_CLI` 解析（及后续需要的 `bianque Skill` → `$BIANQUE`）
   - 检查 CLI 可用：`$PAAS_CLI version`
   - 检查网络连通：`$PAAS_CLI ping`
   - **校验项目组授权（必须）**：
     ```
     $PAAS_CLI auth check --project {project_id}
     ```
     - 授权失败 → **终止流程**，不生成客户端代码，按 `_shared-references/cli-security-rules.md` 提示联系管理员授权
3. **平台连接信息拉取（阻塞）**：
   ```
   $PAAS_CLI nacos config --project {project_id} --env {env}
   ```
   - 从输出解析并锁定：`Server Addr` → `server_addr`，`Namespace` → `namespace`，`Username` → `auth_user`
   - 在对话中完整展示上述 CLI 命令及解析结果，供用户核对
   - **不得以用户口述或项目内旧配置覆盖 CLI 返回的 `Username`**
4. **代码生成**：将步骤 3 的 `server_addr`、`namespace`、`auth_user` 填入模板，根据 `language` 选择对应模板，生成文件
   > 详细代码模板参见 `references/nacos-client-templates/` 目录

   | 语言 | 生成文件 |
   |------|---------|
   | Java | NacosConfigService.java、NacosDiscoveryService.java、bootstrap.yml |
   | Go | nacos_client.go、config.yaml |
   | Python | nacos_client.py、config.yaml |

5. **文件写入**：将生成的代码写入 `target_path` 指定目录
6. **依赖提示**：列出需要添加的依赖
   - **Java**：Spring Cloud Alibaba Nacos Discovery + Config
   - **Go**：`github.com/nacos-group/nacos-sdk-go/v2`
   - **Python**：`nacos-sdk-python`

### 输出格式

```
✅ 客户端代码已生成

🔐 平台信息（来源：paas-cli Skill）：
  - 授权检查：`$PAAS_CLI auth check` --project {project_id} — ✅ 通过
  - 连接配置：`$PAAS_CLI nacos config` --project {project_id} --env {env}
  - Server Addr / Namespace / Username：{server_addr} / {namespace} / {auth_user}

📁 生成文件列表：
  - {文件路径1} — {文件说明}
  - {文件路径2} — {文件说明}

📝 后续步骤：
  1. 添加依赖：{依赖信息}
  2. 配置环境变量：NACOS_SERVER_ADDR、NACOS_NAMESPACE、NACOS_USERNAME（与 CLI 一致）、NACOS_PASSWORD
  3. 启动应用验证注册

⚠️ 注意事项：
  - 用户名以平台 CLI 返回为准，已写入配置或对应环境变量占位符
  - 密码以 ${NACOS_PASSWORD} 占位符形式写入，请通过环境变量或密钥管理系统注入实际值（CLI 不返回明文）
  - 请确保 Nacos 服务端已开启鉴权
```

### 异常处理

- **paas-cli Skill** 下 `$PAAS_CLI auth check` 失败或返回未授权 → **终止**，不生成代码；提示 `$PAAS_CLI auth check` 排查及联系项目管理员授权
- **paas-cli Skill** 下 `$PAAS_CLI nacos config` 失败 → 提示查阅 **paas-cli Skill**（`skills/paas-cli/SKILL.md`）并完成 `$PAAS_CLI` 解析与网络；可进入**降级流程**：由用户手动提供 `server_addr`、`namespace`；`auth_user` 仅在 CLI 不可用时询问，并在输出中标注「非平台标准流程，用户名未走 CLI」
- paas-cli Skill 下 `$PAAS_CLI version` 或 `$PAAS_CLI ping` 失败 → 同 `nacos config` 失败，优先修复 CLI/网络后再执行 `auth check` 与 `nacos config`
- 目标路径不存在 → 询问用户是否创建目录
- 文件已存在 → 询问用户是否覆盖

---
