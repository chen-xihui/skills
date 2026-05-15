# NACOS-001：服务订阅是否启用本地快照

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-001 |
| 风险等级 | 🔵 建议 |
| 规则描述 | 服务订阅是否启用本地快照（enableLocalSnapshot） |

## 问题说明

启用本地快照后，Nacos 客户端会将获取的配置缓存到本地文件。当 Nacos 服务端不可用时，客户端可以从本地快照加载配置，提高系统容灾能力。

## 检查方法

1. 搜索 Nacos 配置中是否设置 `enableLocalSnapshot=true`
2. 搜索 Properties / YAML 配置文件中的 `enableLocalSnapshot` 字段
3. 如未找到该配置，标记为问题

搜索模式：
- `grep_code` 搜索 `enableLocalSnapshot`、`enable-local-snapshot`
- `search_codebase` 搜索 "local snapshot" 或 "本地快照" 相关配置

## 违规示例

```java
// ❌ 未启用本地快照
Properties properties = new Properties();
properties.put("serverAddr", serverAddr);
// 没有 enableLocalSnapshot 设置（默认为 false）
ConfigService configService = ConfigFactory.createConfigService(properties);
```

## 合规示例

```java
// ✅ 启用本地快照
Properties properties = new Properties();
properties.put("serverAddr", serverAddr);
properties.put("enableLocalSnapshot", "true");
ConfigService configService = ConfigFactory.createConfigService(properties);
```
