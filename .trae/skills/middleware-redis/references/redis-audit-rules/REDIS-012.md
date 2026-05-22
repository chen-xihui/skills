# REDIS-012：Key 命名规范检查

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-012 |
| 风险等级 | 🔵 建议 |
| 规则描述 | 业务 Key 应遵循命名规范，不宜使用特殊字符 |

## 规范要求

- 业务 Key 不宜使用特殊字符（空格、换行符、双引号及转义字符）
- 推荐通过系统编号、模块区分，如 `J036X0:order:Key1`
- 非 Lua 场景下不宜使用 hashtag，避免出现流量倾斜

## 检查方法

搜索 Key 的拼接和定义方式。

搜索模式：
- `grep_code` 搜索包含空格、换行符等特殊字符的 Key 定义

## 合规示例

```java
// ✅ 规范的 Key 命名
String key = "J036X0:order:" + orderId;
String key = "J036X0:user:profile:" + userId;
```

## 违规示例

```java
// ❌ 使用特殊字符
String key = "J036X0 order Key1";        // 包含空格
String key = "user profile:" + userId;   // 包含空格
```