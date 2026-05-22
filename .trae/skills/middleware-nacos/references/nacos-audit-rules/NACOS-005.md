# NACOS-005: 心跳间隔、权重等是否符合最佳实践

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-005 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 心跳间隔、权重等是否符合最佳实践 |

## 问题说明

心跳间隔过短会增加 Nacos 服务端负担，过长则服务下线感知延迟大。权重设置不合理会影响负载均衡效果。

## 检查方法

1. 搜索 `heartBeatInterval`、`heart-beat-interval` 配置值
2. 搜索 `weight` 配置值
3. 检查值是否在合理范围内

推荐值：
- 心跳间隔：3-5 秒（默认 5s）
- 权重：1.0（默认值），根据实例性能调整

搜索模式：
- `grep_code` 搜索 `heartBeatInterval`、`heart-beat-interval`、`weight`

## 违规示例

```yaml
# 心跳间隔过短
nacos:
  discovery:
    heart-beat-interval: 500  # 0.5s，频率过高
    weight: 0.01              # 权重过低，几乎不分流
```

## 合规示例

```yaml
# 心跳间隔和权重合理
nacos:
  discovery:
    heart-beat-interval: 5000  # 5s
    weight: 1.0
```