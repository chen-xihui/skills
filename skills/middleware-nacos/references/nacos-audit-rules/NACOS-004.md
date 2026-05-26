# NACOS-004: 密码是否硬编码

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-004 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 密码是否硬编码在源码中 |

## 问题说明

将 Nacos 密码硬编码在 Java/Go/Python 源码中存在严重安全隐患。应通过环境变量、Spring Cloud Config、Vault 等方式注入。

## 检查方法

1. 搜索源码中 `password` 字段的直接赋值
2. 排除配置文件（bootstrap.yml 等）中的 `${...}` 占位符形式
3. 搜索 `Properties.put("password", ...)` 中的硬编码值

搜索模式：
- `grep_code` 搜索 `.java` 文件中的 `password\s*=\s*"[^${]`
- 排除 `@Value("${...}")` 形式的安全用法

## 违规示例

```java
// 密码硬编码
properties.put("password", "MySecretPassword123");
```

## 合规示例

```java
// 密码通过配置注入
@Value("${nacos.password}")
private String password;

// bootstrap.yml 中：
// password: ${NACOS_PASSWORD}
```