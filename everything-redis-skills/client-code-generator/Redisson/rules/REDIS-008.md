# REDIS-008：密码是否硬编码

| 属性 | 说明 |
|------|------|
| 规则ID | REDIS-008 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 密码是否硬编码 |

## 问题说明

将 Redis 密码硬编码在源码中存在严重安全隐患。应通过环境变量或密钥管理系统注入。

## 检查方法

1. 搜索源码中 `password` 字段的直接赋值
2. 排除配置文件中的 `${...}` 占位符形式
3. 搜索 `JedisPool`、`RedisStandaloneConfiguration` 中的硬编码密码

搜索模式：
- `grep_code` 搜索 `.java` 文件中的 `password\s*=\s*"[^${]`
- 排除 `@Value("${...}")` 形式

## 违规示例

```java
// ❌ 密码硬编码
JedisPool pool = new JedisPool(config, host, port, timeout, "MyRedisPassword123");
```

## 合规示例

```java
// ✅ 密码通过配置注入
@Value("${spring.data.redis.password}")
private String password;

// application.yml 中：
// password: ${REDIS_PASSWORD}
```