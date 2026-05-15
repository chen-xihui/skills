# 操作 5：扩缩容

| 属性 | 说明 |
|------|------|
| 操作类型 | 扩缩容 |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli nacos scale --project {project_id} --env {env} --replicas {count}` |

## 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| count | int | 是 | 目标副本数（正整数） |

## 命令示例

```bash
paas-cli nacos scale --project j036x0 --env DEV --replicas 3
```

## 确认流程

```
即将执行以下操作：
  命令：paas-cli nacos scale --project j036x0 --env DEV --replicas 3
  说明：将 Nacos 集群副本数调整为 3
  影响：扩容时需等待新节点加入集群；缩容时需迁移 Raft 角色

是否继续执行？
```

## 注意事项

- Nacos 集群建议奇数节点（1/3/5），确保 Raft 选举过半
- 缩容时需确保剩余节点数满足 Raft 多数派
