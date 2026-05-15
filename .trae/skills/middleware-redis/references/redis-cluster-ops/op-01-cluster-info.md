# 操作 1：查看集群状态

| 属性 | 说明 |
|------|------|
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli redis info --project {project_id} --env {env}` |

```bash
paas-cli redis info --project j036x0 --env DEV
```

返回：集群模式、节点数量、运行状态、连接数等。
