# NACOS-007：命名空间是否按环境隔离

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-007 |
| 风险等级 | 🔵 建议 |
| 规则描述 | 命名空间是否按环境隔离 |

## 问题说明

不同环境（DEV/SIT/SRV）应使用不同的 Nacos 命名空间进行隔离，避免配置和服务注册互相干扰。

## 检查方法

1. 搜索 `namespace` 配置
2. 检查不同环境的配置文件是否使用不同 namespace
3. 如所有环境使用同一个 namespace，标记为建议

搜索模式：
- `grep_code` 搜索 `namespace` 配置
- 检查是否存在 `bootstrap-dev.yml`、`bootstrap-sit.yml` 等多环境配置
- `search_codebase` 搜索 "namespace" 相关配置

## 违规示例

```yaml
# ❌ 所有环境使用相同 namespace（默认 public）
# bootstrap-dev.yml
nacos:
  namespace: ""

# bootstrap-sit.yml
nacos:
  namespace: ""  # 与 DEV 共用命名空间
```

## 合规示例

```yaml
# ✅ 不同环境使用不同 namespace
# bootstrap-dev.yml
nacos:
  namespace: "dev-namespace-id"

# bootstrap-sit.yml
nacos:
  namespace: "sit-namespace-id"
```
