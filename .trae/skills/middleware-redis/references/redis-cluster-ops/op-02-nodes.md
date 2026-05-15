# 操作 2：查看节点信息

| 属性 | 说明 |
|------|------|
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli redis nodes --project {project_id} --env {env}` |

```bash
paas-cli redis nodes --project j036x0 --env DEV
```

返回：各节点角色（Master/Slave）、地址、Slot 范围、连接状态。
