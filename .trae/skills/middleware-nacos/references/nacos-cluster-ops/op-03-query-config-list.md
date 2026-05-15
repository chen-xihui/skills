# 操作 3：查询配置列表

| 属性 | 说明 |
|------|------|
| 操作类型 | 查询配置列表 |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli nacos config-list --project {project_id} --env {env}` |

## 命令示例

```bash
paas-cli nacos config-list --project j036x0 --env DEV
```

## 返回信息

- 配置 Data ID 列表
- 所属 Group
- 最后修改时间
