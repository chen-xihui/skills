# 操作 8：删除服务

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除服务 |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli nacos delete --project {project_id} --env {env} --service {service_name}` |

## 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| service_name | string | 是 | 服务名称 |

## 命令示例

```bash
paas-cli nacos delete --project j036x0 --env DEV --service order-service
```

## 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli nacos delete --project j036x0 --env DEV --service order-service
  说明：删除 Nacos 服务 order-service
  影响范围：
    - 该服务下的所有实例将被注销
    - 依赖此服务的调用方将无法发现实例
    - 此操作不可逆

请输入"确认"以执行此操作：
```
