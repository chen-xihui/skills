# 操作 8：升级版本

| 属性 | 说明 |
|------|------|
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli redis upgrade --project {project_id} --env {env} --version {version}` |

```bash
paas-cli redis upgrade --project j036x0 --env DEV --version 7.2.0
```

## 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli redis upgrade --project j036x0 --env DEV --version 7.2.0
  说明：将 Redis 集群升级到版本 7.2.0
  影响范围：
    - 升级期间集群可能短暂不可用
    - 升级过程中节点逐个重启
    - 升级前请确保已备份数据
    - 跨大版本升级需先升级到最近的中间版本

请输入"确认"以执行此操作：
```
