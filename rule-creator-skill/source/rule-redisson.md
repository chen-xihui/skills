# Redisson 规则集
本文档包含 5 条规则
---
# REDISSON-001：分布式锁必须设置 leaseTime

| 属性 | 说明 |
|------|------|
| 规则ID | REDISSON-001 |
| 风险等级 | 严重 |
| 规则描述 | lock() 必须设置 leaseTime 参数，防止锁永久持有 |

## 问题说明

节点宕机后锁无法自动释放

## 检查方法

静态分析：检查 lock() 调用是否包含 leaseTime

## 违规示例

RLock lock = redisson.getLock(key);<br>lock.lock(); // 无 leaseTime

## 合规示例

lock.lock(30, TimeUnit.SECONDS);<br>// 或 lock.tryLock(10, 30, TimeUnit.SECONDS);

# REDISSON-002：禁止循环创建 RedissonClient

| 属性 | 说明 |
|------|------|
| 规则ID | REDISSON-002 |
| 风险等级 | 严重 |
| 规则描述 | RedissonClient 必须单例，禁止循环内创建 |

## 问题说明

连接风暴

## 检查方法

静态分析：检查是否存在循环内 new Redisson

## 违规示例

for (...) {<br>    RedissonClient client = Redisson.create();<br>}

## 合规示例

单例 RedissonClient，Spring Bean 全局复用

# REDISSON-003：应用退出必须 shutdown

| 属性 | 说明 |
|------|------|
| 规则ID | REDISSON-003 |
| 风险等级 | 严重 |
| 规则描述 | 必须调用 redisson.shutdown() |

## 问题说明

Netty 线程残留、classloader 泄漏

## 检查方法

静态分析：检查 @PreDestroy 是否调用 shutdown

## 违规示例

// 未调用 shutdown

## 合规示例

@PreDestroy<br>public void destroy() {<br>    redisson.shutdown();<br>}

# REDISSON-004：必须开启 TCP KeepAlive

| 属性 | 说明 |
|------|------|
| 规则ID | REDISSON-004 |
| 风险等级 | 风险 |
| 规则描述 | 配置文件中必须设置 keepAlive: true |

## 问题说明

长连接假死

## 检查方法

静态分析：检查配置文件或代码中的 keepAlive 配置

## 违规示例

// 未开启 keepAlive

## 合规示例

keepAlive: true

# REDISSON-005：禁止 watch dog 场景下无限等待

| 属性 | 说明 |
|------|------|
| 规则ID | REDISSON-005 |
| 风险等级 | 风险 |
| 规则描述 | tryLock 必须设置 leaseTime 或等待时间 |

## 问题说明

永久等待导致线程堆积

## 检查方法

静态分析：检查 tryLock 参数

## 违规示例

lock.tryLock(); // 无限等待

## 合规示例

lock.tryLock(10, 30, TimeUnit.SECONDS);

