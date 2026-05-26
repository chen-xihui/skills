# NACOS-006: 是否缺少异常处理和重试配置

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-006 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 是否缺少异常处理和重试配置 |

## 问题说明

Nacos 客户端调用处缺少 try-catch 和重试逻辑，在网络抖动或 Nacos 服务端不可用时可能导致应用崩溃或功能异常。

## 检查方法

1. 搜索 Nacos 客户端调用处（`getConfig`、`registerInstance`、`deregisterInstance` 等）
2. 检查是否有 try-catch 包裹
3. 检查是否有重试配置

搜索模式：
- `grep_code` 搜索 Nacos API 调用，检查上下文是否有 try-catch
- `search_codebase` 搜索 Nacos 客户端调用

## 违规示例

```java
// 无异常处理
String config = configService.getConfig(dataId, group, 5000);
return config;
```

## 合规示例

```java
// 有异常处理和重试
@Retryable(value = NacosException.class, maxAttempts = 3, backoff = @Backoff(delay = 1000))
public String getConfigWithRetry(String dataId, String group) {
    try {
        return configService.getConfig(dataId, group, 5000);
    } catch (NacosException e) {
        log.error("获取配置失败: dataId={}, group={}", dataId, group, e);
        throw new RuntimeException("配置获取失败", e);
    }
}
```