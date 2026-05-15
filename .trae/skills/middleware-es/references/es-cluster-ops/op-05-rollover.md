# 操作 5：索引滚动（Rollover）

| 属性 | 说明 |
|------|------|
| 操作类型 | 索引滚动（Rollover） |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令模板 | `paas-cli es rollover --project {project_id} --env {env} --alias {alias}` |

## 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| alias | string | 是 | — | 索引别名（字母、数字、短横线、下划线） |

## 参数校验

- `alias`：仅允许字母、数字、短横线、下划线，不含 shell 元字符

## 命令示例

```bash
paas-cli es rollover --project j036x0 --env DEV --alias logs-write
```

## 确认流程

向用户展示：
```
即将执行以下操作：
  命令：paas-cli es rollover --project j036x0 --env DEV --alias logs-write
  说明：对别名 logs-write 执行滚动操作
  影响：如果当前索引满足滚动条件，将创建新索引并将别名指向新索引

是否继续执行？
```

## 注意事项

- 滚动操作基于别名的 is_write_index 条件
- 滚动条件可在索引模板中预定义（如文档数、大小、时间）
- 滚动后别名自动指向新索引，应用代码无需修改
