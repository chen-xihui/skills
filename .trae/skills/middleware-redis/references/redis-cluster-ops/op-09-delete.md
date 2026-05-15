# 操作 9：删除集群

| 属性 | 说明 |
|------|------|
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli redis delete --project {project_id} --env {env}` |

```bash
paas-cli redis delete --project j036x0 --env DEV
```

## 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli redis delete --project j036x0 --env DEV
  说明：删除 Redis 集群（DEV 环境，项目组 j036x0）
  影响范围：
    - 集群中所有数据将被永久删除，不可恢复
    - 所有依赖此集群的应用将无法访问
    - 此操作不可逆

请输入"确认"以执行此操作：
```
