# 操作 6：配置灰度发布

| 属性 | 说明 |
|------|------|
| 操作类型 | 配置灰度发布 |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli nacos gray-publish --project {project_id} --env {env} --config {config_id}` |

## 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| config_id | string | 是 | 配置 ID（字母、数字、下划线、短横线、点号） |

## 命令示例

```bash
paas-cli nacos gray-publish --project j036x0 --env DEV --config application.yml
```

## 确认流程

```
即将执行以下操作：
  命令：paas-cli nacos gray-publish --project j036x0 --env DEV --config application.yml
  说明：对配置 application.yml 执行灰度发布
  影响：灰度配置将推送到灰度规则的实例，不影响全量实例

是否继续执行？
```
