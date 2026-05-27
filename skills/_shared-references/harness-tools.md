# Harness 工具名映射（共享）

Skill 编写时使用**能力名**；Agent 在 Cursor 中按下表调用等价工具。

| Skill / 文档中的名称 | Cursor | 说明 |
|---------------------|--------|------|
| `grep_code` | **Grep** | 按正则搜索代码 |
| `search_codebase` | **SemanticSearch** | 语义搜索代码库 |
| `read_file` | **Read** | 读取文件 |
| 终端执行 | **Shell** | 运行 `$PAAS_CLI` / `$BIANQUE` |

Qoder / Trae 等 harness 若仍暴露旧名称，以该平台文档为准；本仓库 Skill 正文统一写 Cursor 列名称。
