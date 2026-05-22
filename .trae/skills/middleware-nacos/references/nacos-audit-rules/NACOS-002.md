# NACOS-002: 长轮询超时是否合理

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-002 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 长轮询超时是否合理（configLongPollTimeout 建议 ≤ 30s） |

## 问题说明

`configLongPollTimeout` 控制客户端等待配置变更通知的超时时间。值过大会导致客户端感知配置变更延迟，值过小会增加服务端压力。建议设置为 30s 以内。

## 检查方法

1. 搜索 `configLongPollTimeout` 配置值
2. 检查值是否超过 30000ms（30s）
3. 如未设置，使用默认值不算问题（默认 30s）

搜索模式：
- `grep_code` 搜索 `configLongPollTimeout`、`config-long-poll-timeout`
- 检查配置值是否 > 30000

## 违规示例

```yaml
# 长轮询超时过大
nacos:
  config-long-poll-timeout: 60000  # 60s，超过建议值
```

## 合规示例

```yaml
# 长轮询超时合理
nacos:
  config-long-poll-timeout: 30000  # 30s
```