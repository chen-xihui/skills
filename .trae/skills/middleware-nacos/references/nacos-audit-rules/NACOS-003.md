# NACOS-003：是否循环调用 getConfig 而未使用 Listener

| 属性 | 说明 |
|------|------|
| 规则ID | NACOS-003 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 是否循环调用 getConfig 而未使用 Listener |

## 问题说明

在循环中反复调用 `getConfig` 轮询配置变更，会浪费大量网络资源和 Nacos 服务端处理能力。应使用 Nacos 的 Listener 机制订阅配置变更，实现推送而非轮询。

## 检查方法

1. 搜索循环体内的 `getConfig` 调用
2. 检查是否有对应的 `addListener` 调用
3. 排除初始化阶段的一次性调用（如 `@PostConstruct` 中）

搜索模式：
- `grep_code` 搜索循环体（`while`、`for`）内的 `getConfig` 调用
- `search_codebase` 搜索 "getConfig" 相关代码，检查上下文是否在循环中

## 违规示例

```java
// ❌ 循环中轮询配置
while (running) {
    String config = configService.getConfig(dataId, group, 5000);
    // 处理配置...
    Thread.sleep(10000);
}
```

## 合规示例

```java
// ✅ 使用 Listener 订阅配置变更
configService.addListener(dataId, group, new Listener() {
    @Override
    public Executor getExecutor() {
        return Executors.newSingleThreadExecutor();
    }

    @Override
    public void receiveConfigInfo(String configInfo) {
        // 处理配置变更
    }
});
```
