# 操作 6：Force Merge（强制段合并）

| 属性 | 说明 |
|------|------|
| 操作类型 | Force Merge（强制段合并） |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令模板 | `paas-cli es force-merge --project {project_id} --env {env} --index {index_name} --max-segments {n}` |

## 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| index_name | string | 是 | — | 索引名称 |
| max-segments | int | 否 | 1 | 目标段数量 |

## 参数校验

- `index_name`：符合 ES 索引命名规范，不含 shell 元字符
- `max-segments`：正整数，通常设为 1（完全合并）

## 命令示例

```bash
paas-cli es force-merge --project j036x0 --env DEV --index log-2026-04 --max-segments 1
```

## 确认流程

向用户展示：
```
即将执行以下操作：
  命令：paas-cli es force-merge --project j036x0 --env DEV --index log-2026-04 --max-segments 1
  说明：对索引 log-2026-04 执行强制段合并，目标段数 1
  影响：Force Merge 会消耗大量 I/O 和 CPU 资源，建议仅在只读索引上执行
  ⚠️ 警告：对读写中的索引执行 Force Merge 可能导致性能严重下降

是否继续执行？
```

## 注意事项

- **强烈建议只在只读索引上执行 Force Merge**
- 对活跃索引执行 Force Merge 可能产生更大的段，适得其反
- Force Merge 会消耗大量 I/O 和 CPU，建议在业务低峰期执行
- 合并完成后索引存储空间会减少，查询性能可能提升
