# Spring Data Redis 规则集
本文档包含 3 条规则
---
# SDR-001：禁止使用默认序列化器

| 属性 | 说明 |
|------|------|
| 规则ID | SDR-001 |
| 风险等级 | 严重 |
| 规则描述 | 必须配置 RedisTemplate 序列化方式 |

## 问题说明

Java 序列化无法跨语言、内存开销大

## 检查方法

静态分析：检查 RedisTemplate 配置

## 违规示例

// 使用默认 JdkSerializationRedisSerializer

## 合规示例

template.setKeySerializer(new StringRedisSerializer());<br>template.setValueSerializer(new GenericJackson2JsonRedisSerializer());

# SDR-002：禁止 RedisTemplate.keys()

| 属性 | 说明 |
|------|------|
| 规则ID | SDR-002 |
| 风险等级 | 风险 |
| 规则描述 | 禁止使用 opsForKeys().keys() |

## 问题说明

keys() 阻塞主线程

## 检查方法

静态分析：搜索 keys() 调用

## 违规示例

redisTemplate.opsForKeys().keys("*")

## 合规示例

redisTemplate.scan(scanOptions)

# SDR-003：必须配置 commandTimeout

| 属性 | 说明 |
|------|------|
| 规则ID | SDR-003 |
| 风险等级 | 风险 |
| 规则描述 | RedisTemplateFactory 必须配置超时 |

## 问题说明

无限等待导致线程堆积

## 检查方法

静态分析：检查超时配置

## 违规示例

// 未配置超时

## 合规示例

factory.setCommandTimeout(Duration.ofMillis(500));

