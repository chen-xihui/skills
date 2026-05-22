# REDIS-004：连接池参数合理性

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-004 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 连接池参数合理性（maxTotal、maxIdle、maxWaitMillis） |

## 问题说明

连接池参数设置不合理会导致连接泄漏或资源浪费。使用默认值时可能导致高并发下连接不足。

## 检查方法

1. 搜索 `maxTotal`、`maxIdle`、`maxWaitMillis` 配置
2. 搜索 `max-active`、`max-idle`、`max-wait` YAML 配置
3. 检查是否使用 Spring Boot 默认值（通常偏小）

搜索模式：
- `grep_code` 搜索 `max-active`、`max-idle`、`max-wait`、`maxTotal`、`maxIdle`
- 检查连接池配置是否存在且合理

## 推荐值

- max-active：20-50（根据并发量调整）
- max-idle：10-20
- min-idle：5-10
- max-wait：3000ms

## Jedis 连接配置

| 配置参数 | 默认值 | 配置要求 |
|---------|--------|---------|
| maxTotal | 8 | 无特殊需求应小于 200 |
| maxIdle | 8 | 无特殊需求配置为 maxTotal/2 |
| minIdle | 0 | 高并发可配为 maxIdle 预热连接池 |
| maxWaitMillis | -1 | **禁止配置为默认值**；常见区间 50ms~5s |
| testOnBorrow | false | 建议配置为 true |
| testWhileIdle | false | 无特殊需求时配置为 true |
| timeBetweenEvictionRunsMillis | -1 | **禁止配置为默认值**；常见区间 20s~300s |

## Lettuce 连接配置

| 配置参数 | 默认值 | 配置要求 |
|---------|--------|---------|
| lettuce.pool.max-active | 8 | 无特殊需求应小于 200 |
| lettuce.pool.max-idle | 8 | 无特殊需求配置为 max-active/2 |
| lettuce.pool.min-idle | 0 | 高并发可配为 max-idle 预热 |
| lettuce.pool.max-wait | -1 | **禁止配置为默认值**；常见区间 50ms~5s |
| lettuce.cluster.refresh.adaptive | false | **禁止配置为默认值** |