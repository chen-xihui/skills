# 操作 4：创建服务

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建服务 |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli nacos create --project {project_id} --env {env} --service {service_name} --group {group}` |

## 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| service_name | string | 是 | — | 服务名称 |
| group | string | 否 | DEFAULT_GROUP | 服务分组 |

## 命令示例

```bash
paas-cli nacos create --project j036x0 --env DEV --service order-service --group DEFAULT_GROUP
```

## 确认流程

```
即将执行以下操作：
  命令：paas-cli nacos create --project j036x0 --env DEV --service order-service --group DEFAULT_GROUP
  说明：创建 Nacos 服务 order-service
  影响：新增服务注册条目

是否继续执行？
```
