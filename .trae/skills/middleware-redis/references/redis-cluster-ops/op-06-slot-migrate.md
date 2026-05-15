# 操作 6：Slot 迁移

| 属性 | 说明 |
|------|------|
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli redis slot-migrate --project {project_id} --env {env} --from {node} --to {node} --slots {range}` |

## 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| from | string | 是 | 源节点标识 |
| to | string | 是 | 目标节点标识 |
| slots | string | 是 | Slot 范围（如 0-1000 或 0,1,2） |

## 参数校验

- `from` / `to`：仅允许字母、数字、短横线、冒号、点号
- `slots`：数字和短横线、逗号组合

```bash
paas-cli redis slot-migrate --project j036x0 --env DEV --from redis-node-1 --to redis-node-4 --slots 0-5460
```

## 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli redis slot-migrate --project j036x0 --env DEV --from redis-node-1 --to redis-node-4 --slots 0-5460
  说明：将 Slot 0-5460 从 redis-node-1 迁移到 redis-node-4
  影响范围：
    - 迁移期间相关 Slot 的读写可能受影响
    - 迁移过程中源节点和目标节点负载增加
    - 如迁移中断，需要手动处理未完成的迁移状态

请输入"确认"以执行此操作：
```

## 注意事项

- 建议在业务低峰期执行
- 迁移前确认源节点和目标节点状态正常
- 迁移过程中避免对涉及的 Key 进行大批量操作
