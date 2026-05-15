# 操作 1：查询集群信息

| 属性 | 说明 |
|------|------|
| 操作类型 | 查询集群信息 |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli nacos info --project {project_id} --env {env}` |

## 命令示例

```bash
paas-cli nacos info --project j036x0 --env DEV
```

## 返回信息

- 集群节点列表和状态
- Leader 节点信息
- Raft 一致性状态
- 配置数量
