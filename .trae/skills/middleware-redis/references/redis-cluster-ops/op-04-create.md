# 操作 4：创建实例

| 属性 | 说明 |
|------|------|
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli redis create --project {project_id} --env {env} --mode {mode}` |

## 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| mode | enum | 否 | standalone | standalone / sentinel / cluster |

```bash
paas-cli redis create --project j036x0 --env DEV --mode cluster
```

## 确认流程

```
即将执行以下操作：
  命令：paas-cli redis create --project j036x0 --env DEV --mode cluster
  说明：创建 Redis 集群模式实例
  影响：创建新的 Redis 实例，分配资源

是否继续执行？
```
