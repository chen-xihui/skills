## 能力一：客户端创建与配置

### 触发条件

用户请求创建 Redis 客户端并生成配置，如：
- "创建 Redis 客户端"
- "生成缓存连接代码"
- "帮我配置 Redis"
- "创建 Redis Sentinel 客户端"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境：DEV / SIT / SRV |
| target_path | string | 是 | — | 代码生成目标路径 |
| mode | enum | 否 | — | 部署模式提示：standalone / sentinel / cluster；**最终以 CLI 输出为准** |
| client_type | enum | 否 | lettuce | 客户端库：jedis / lettuce（仅 Java） |
| language | enum | 否 | Java | 项目语言：Java / Go / Python |

**平台拉取字段（禁止向用户索要或覆盖）**：

| 字段 | 来源 | 说明 |
|------|------|------|
| mode | `$PAAS_CLI redis config` 输出 `Mode` | 决定 Standalone/Sentinel/Cluster 模板；**不得以用户口述覆盖 CLI** |
| endpoints | `$PAAS_CLI redis config` 输出 `Endpoints` | 写入配置或 `${REDIS_ENDPOINTS}` / 各节点占位符 |
| master_name | `$PAAS_CLI redis config` 输出 `Master Name`（Sentinel） | 仅 Sentinel 模式使用 |
| database | `$PAAS_CLI redis config` 输出 `Database` | 写入配置默认值 |

**密码**：`$PAAS_CLI redis config` 仅返回脱敏密码（如 `********`），**不得**向用户索要明文密码写入代码；生成物统一使用 `${REDIS_PASSWORD}`，由用户通过环境变量或密钥系统注入。

### 处理流程

1. **参数收集**：确认 `project_id`、`env`、`target_path`、`language`、`client_type`；`mode` 可选，用于向用户澄清部署形态，缺失时不主动索要密码
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
   $PAAS_CLI redis config --project {project_id} --env {env}
   ```
   - 若用户已明确 `mode`，可在命令中附加 `--mode {mode}` 供平台查询；**生成代码时仍以 CLI 返回的 `Mode` 为准**
   - 解析并锁定：`Mode`、`Endpoints`、（Sentinel 时）`Master Name`、`Database`
   - 在对话中完整展示 CLI 命令及解析结果
4. **代码生成**：按 CLI 确定的 `mode` 与 `language`/`client_type` 选择模板
   > 详细代码模板参见 `references/redis-client-templates/` 目录

   | 组合 | 生成文件 |
   |------|---------|
   | Java + Lettuce + Standalone | RedisConfig.java、RedisService.java、application.yml |
   | Java + Jedis + Standalone | JedisConfig.java、JedisService.java、application.yml |
   | Java + Lettuce + Sentinel | RedisSentinelConfig.java、RedisService.java、application.yml |
   | Java + Lettuce + Cluster | RedisClusterConfig.java、RedisService.java、application.yml |
   | Go | redis_client.go、config.yaml |
   | Python | redis_client.py、config.yaml |

5. **文件写入**：将生成的代码写入 `target_path`
6. **依赖提示**：列出需要添加的依赖（Lettuce/Jedis/Go/Python，见模板索引）

### 输出格式

```
✅ 客户端代码已生成

🔐 平台信息（来源：paas-cli Skill）：
  - 授权检查：`$PAAS_CLI auth check` --project {project_id} — ✅ 通过
  - 连接配置：`$PAAS_CLI redis config` --project {project_id} --env {env}
  - Mode / Endpoints / Database：{mode} / {endpoints} / {database}

📁 生成文件列表：
  - {文件路径1} — {文件说明}

📝 后续步骤：
  1. 添加依赖：{依赖信息}
  2. 配置环境变量：REDIS_PASSWORD（及模板中的 REDIS_ENDPOINTS 等）
  3. 确认部署模式与平台 Mode 一致后启动验证

⚠️ 注意事项：
  - 连接信息与 Mode 以平台 CLI 返回为准
  - 密码以 ${REDIS_PASSWORD} 占位符写入，勿写入明文
```

### 异常处理

- `$PAAS_CLI auth check` 失败或未授权 → **终止**，不生成代码
- `$PAAS_CLI redis config` 失败 → 提示遵循 **paas-cli Skill**；**降级**：用户手动提供 endpoints/mode，输出标注「非平台标准流程」；仍不得索要明文密码
- `$PAAS_CLI version` / `$PAAS_CLI ping` 失败 → 先修复 CLI/网络再执行 `auth check` 与 `redis config`
- 目标路径不存在 → 询问是否创建目录
- 文件已存在 → 询问是否覆盖

---
