# REDIS-004：连接池参数合理性

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-004 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 连接池参数合理性（maxTotal、maxIdle、maxWaitMillis） |

## 问题说明

连接池参数设置不合理会导致连接泄漏或资源浪费。使用默认值时可能导致高并发下连接不足。

## 推荐值

- max-active：20-50（根据并发量调整）
- max-idle：10-20
- min-idle：5-10
- max-wait：3000ms

## 检查方法

1. 搜索 `maxTotal`、`maxIdle`、`maxWaitMillis` 配置
2. 搜索 `max-active`、`max-idle`、`max-wait` YAML 配置
3. 检查是否使用 Spring Boot 默认值（通常偏小）

搜索模式：
- `grep_code` 搜索 `max-active`、`max-idle`、`max-wait`、`maxTotal`、`maxIdle`
- 检查连接池配置是否存在且合理
