# 操作 3：查看内存使用

| 属性 | 说明 |
|------|------|
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli redis memory --project {project_id} --env {env}` |

```bash
paas-cli redis memory --project j036x0 --env DEV
```

返回：已用内存、最大内存、内存碎片率、淘汰策略。
