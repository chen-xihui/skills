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
| auth_user | string | 是 | — | ES 用户名 |
| auth_pass | string | 是 | — | ES 密码 |
| target_path | string | 是 | — | 代码生成目标路径 |
| client_version | enum | 否 | new | 客户端版本：new（ElasticsearchClient / 8.x+）/ old（RestHighLevelClient / 7.x） |
| language | enum | 否 | Java | 项目语言：Java / Go / Python / Node.js |

### 处理流程

1. **参数收集**：确认所有必要参数，缺失项主动询问用户。特别确认 `client_version`（影响生成的 API 风格）：
   - 询问方式："请确认 ES 客户端版本：new（ElasticsearchClient，适用于 ES 8.x+）还是 old（RestHighLevelClient，适用于 ES 7.x）？"
   - 如用户不确定，提示："如果 ES 版本 ≥ 8.0，建议使用 new；如 ES 版本为 7.x，使用 old"
2. **环境信息查询**：按 **paas-cli Skill** 在终端执行 `$PAAS_CLI` 命令获取 ES 连接信息
   ```
   $PAAS_CLI es config --project {project_id} --env {env}
   ```
   - 如 paas-cli Skill 下 `$PAAS_CLI` 执行失败，提示用户检查安装及网络连通性，改为手动输入 ES 地址
3. **代码生成**：根据 `language` + `client_version` 选择对应模板，生成文件
   > 详细代码模板参见 `references/es-client-templates/` 目录
   
   | 组合 | 生成文件 |
   |------|---------|
   | Java + new | ElasticsearchConfig.java、EsDocumentService.java、application.yml |
   | Java + old | EsRestHighLevelConfig.java、EsDocumentService.java、application.yml |
   | Go | es_client.go、config.yaml |
   | Python | es_client.py、config.py |
   | Node.js | elasticsearch_client.js、config.js |

4. **文件写入**：将生成的代码写入 `target_path` 指定目录
5. **依赖提示**：列出需要添加的依赖
   - **Java + new**：`co.elastic.clients:elasticsearch-java:8.x.x`、`com.fasterxml.jackson.core:jackson-databind`、`org.elasticsearch.client:elasticsearch-rest-client`
   - **Java + old**：`org.elasticsearch.client:elasticsearch-rest-high-level-client:7.x.x`
   - **Go**：`go get github.com/elastic/go-elasticsearch/v8` 或 `v7`
   - **Python**：`pip install elasticsearch`
   - **Node.js**：`npm install @elastic/elasticsearch`

### 输出格式

```
✅ 客户端代码已生成

📁 生成文件列表：
  - {文件路径1} — {文件说明}
  - {文件路径2} — {文件说明}

📝 后续步骤：
  1. 添加依赖：{依赖信息}
  2. 配置环境变量：ES_PASSWORD={实际密码}
  3. 根据业务需求修改索引映射定义

⚠️ 注意事项：
  - 密码以 ${ES_PASSWORD} 占位符形式写入，请通过环境变量或密钥管理系统注入实际值
  - {其他注意事项，如版本兼容性提示}
```

### 异常处理

- paas-cli 命令执行失败 → 提示用户检查 paas-cli 是否安装及网络连通性，改为手动输入 ES 地址
- 目标路径不存在 → 询问用户是否创建目录
- 文件已存在 → 询问用户是否覆盖

---
