# 操作 4：创建索引

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建索引 |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令模板 | `paas-cli es create-index --project {project_id} --env {env} --name {index_name} --shards {n} --replicas {n}` |

## 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| index_name | string | 是 | — | 索引名称（小写字母、数字、短横线） |
| shards | int | 否 | 1 | 主分片数 |
| replicas | int | 否 | 1 | 副本分片数 |

## 参数校验

- `index_name`：必须符合 ES 索引命名规范（小写字母开头，仅含小写字母、数字、短横线、下划线），不含 shell 元字符
- `shards`：正整数，建议根据数据量和节点数设置（一般 1-10）
- `replicas`：非负整数，生产环境建议 ≥ 1

## 命令示例

```bash
paas-cli es create-index --project j036x0 --env DEV --name log-2026-05 --shards 3 --replicas 1
```

## 确认流程

向用户展示：
```
即将执行以下操作：
  命令：paas-cli es create-index --project j036x0 --env DEV --name log-2026-05 --shards 3 --replicas 1
  说明：创建索引 log-2026-05，3 个主分片，1 个副本
  影响：新增索引，不会影响现有数据

是否继续执行？
```

## 注意事项

- 主分片数创建后不可修改，请根据数据量合理设置
- 副本分片数可后续动态调整
- 建议创建时显式定义 mapping，避免 dynamic mapping 导致类型混乱
