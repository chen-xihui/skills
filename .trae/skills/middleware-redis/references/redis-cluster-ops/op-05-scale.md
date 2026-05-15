# 操作 5：扩缩容

| 属性 | 说明 |
|------|------|
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli redis scale --project {project_id} --env {env} --replicas {count}` |

## 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| count | int | 是 | 目标副本数（正整数） |

```bash
paas-cli redis scale --project j036x0 --env DEV --replicas 6
```

## 确认流程

```
即将执行以下操作：
  命令：paas-cli redis scale --project j036x0 --env DEV --replicas 6
  说明：将 Redis 集群副本数调整为 6
  影响：扩容时需等待新节点加入集群并完成 Slot 分配

是否继续执行？
```
