# 操作 2：查询服务注册实例

| 属性 | 说明 |
|------|------|
| 操作类型 | 查询服务注册实例 |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli nacos instances --project {project_id} --env {env} --service {service_name}` |

## 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| service_name | string | 是 | 服务名称（字母、数字、下划线、短横线） |

## 命令示例

```bash
paas-cli nacos instances --project j036x0 --env DEV --service order-service
```

## 返回信息

- 实例 IP 和端口
- 健康状态
- 权重
- 集群名
