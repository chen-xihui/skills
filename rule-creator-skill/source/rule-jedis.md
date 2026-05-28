# Jedis 规则集
本文档包含 14 条规则
---
# JEDIS-001：禁止使用 KEYS 命令

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-001 |
| 风险等级 | 严重 |
| 规则描述 | KEYS 命令会阻塞 Redis 主线程，在大数据集下导致服务不可用 |

## 问题说明

KEYS 命令时间复杂度 O(N)，会遍历所有键，导致生产事故

## 检查方法

静态分析：搜索 .keys( 调用，禁止使用 redisTemplate.keys()、jedis.keys()、sync.keys()

## 违规示例

redisTemplate.keys("*")<br>jedis.keys("*")<br>sync.keys("*")

## 合规示例

SCAN / SSCAN / HSCAN / ZSCAN<br>必须设置 COUNT、游标循环、限流，不允许一次性加载全量

# JEDIS-002：禁止使用连接池后未释放连接

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-002 |
| 风险等级 | 严重 |
| 规则描述 | getResource() 获取的连接必须显式释放，防止连接泄漏 |

## 问题说明

连接泄漏导致 pool exhausted、Could not get a resource from the pool

## 检查方法

静态分析：检查 try-with-resources 或 finally 中是否归还连接

## 违规示例

Jedis jedis = pool.getResource();<br>jedis.get("key");<br>// 未归还连接

## 合规示例

try (Jedis jedis = pool.getResource()) {<br>    jedis.get("key");<br>} // 自动归还

# JEDIS-003：禁止循环内创建连接

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-003 |
| 风险等级 | 严重 |
| 规则描述 | 禁止在循环中创建 RedisClient、RedisClusterClient、JedisPool、RedissonClient |

## 问题说明

导致连接风暴、TIME_WAIT暴涨、FD耗尽

## 检查方法

静态分析：检查循环内是否存在 new Jedis/pool.getResource()

## 违规示例

for (...) {<br>    Jedis jedis = pool.getResource();<br>    jedis.get(key);<br>}

## 合规示例

在循环外获取连接，全局复用

# JEDIS-004：禁止未关闭 Pipeline

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-004 |
| 风险等级 | 严重 |
| 规则描述 | Pipeline 必须调用 close() 关闭，防止连接泄漏 |

## 问题说明

连接泄漏导致 pool exhausted

## 检查方法

静态分析：检查 Pipeline 使用后是否 close()

## 违规示例

Pipeline pipeline = jedis.pipelined();<br>pipeline.get(key);<br>// 未关闭

## 合规示例

try (Pipeline pipeline = jedis.pipelined()) {<br>    pipeline.get(key);<br>    pipeline.sync();<br>}

# JEDIS-005：禁止事务异常后未 Discard

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-005 |
| 风险等级 | 严重 |
| 规则描述 | MULTI/EXEC 异常后必须调用 discard() 清理连接状态 |

## 问题说明

ERR MULTI calls can not be nested 连接污染

## 检查方法

静态分析：检查事务异常处理是否包含 discard()

## 违规示例

Transaction tx = jedis.multi();<br>// 异常后未 discard

## 合规示例

try {<br>    Transaction tx = jedis.multi();<br>    tx.set(key, value);<br>    tx.exec();<br>} catch (Exception e) {<br>    jedis.discard();<br>}

# JEDIS-006：禁止使用 CONFIG SET/REWRITE

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-006 |
| 风险等级 | 严重 |
| 规则描述 | 运行时禁止执行 CONFIG SET、CONFIG REWRITE 命令 |

## 问题说明

可能导致主从切换、数据丢失、Redis卡死

## 检查方法

静态分析：搜索 configSet、configRewrite 调用

## 违规示例

jedis.configSet("maxmemory", "1gb")<br>jedis.configRewrite()

## 合规示例

仅在运维平台、DBA工具、明确审批场景下使用

# JEDIS-007：连接池参数必须完整配置

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-007 |
| 风险等级 | 风险 |
| 规则描述 | JedisPool 必须配置 maxTotal、maxIdle、minIdle、maxWaitMillis |

## 问题说明

未设置导致连接泄漏不可恢复、获取连接无限等待、FullGC

## 检查方法

静态分析：检查 JedisPoolConfig 是否包含所有必需参数

## 违规示例

JedisPool pool = new JedisPool(); // 未配置参数

## 合规示例

JedisPoolConfig config = new JedisPoolConfig();<br>config.setMaxTotal(100);<br>config.setMaxIdle(50);<br>config.setMinIdle(10);<br>config.setMaxWaitMillis(3000);

# JEDIS-008：必须开启 testWhileIdle

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-008 |
| 风险等级 | 风险 |
| 规则描述 | 连接池必须开启空闲连接检测，防止 NAT/防火墙回收导致半关闭 |

## 问题说明

长期空闲连接被回收，业务首次命令失败

## 检查方法

静态分析：检查 setTestWhileIdle(true)

## 违规示例

// 未开启 testWhileIdle

## 合规示例

config.setTestWhileIdle(true);<br>config.setMinEvictableIdleTimeMillis(60000);

# JEDIS-009：禁止超大 Pipeline

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-009 |
| 风险等级 | 风险 |
| 规则描述 | 单次 Pipeline 命令数建议控制在 100-1000 以内 |

## 问题说明

一次 10w 命令导致 Redis 输出 buffer 爆炸、JVM 堆暴涨

## 检查方法

静态分析：检查 Pipeline 循环边界

## 违规示例

Pipeline pipeline = jedis.pipelined();<br>for (int i = 0; i < 100000; i++) {<br>    pipeline.set(key + i, value);<br>}

## 合规示例

分批发送，每批 500-1000 条

# JEDIS-010：必须限制重试次数

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-010 |
| 风险等级 | 风险 |
| 规则描述 | 禁止无限重试，防止雪崩放大、自旋风暴 |

## 问题说明

Redis 故障时无限重试导致应用雪崩

## 检查方法

静态分析：检查是否存在 while(true) retry

## 违规示例

while(true) {<br>    redis.get(key);<br>}

## 合规示例

读请求重试 1-2 次，写请求重试 0-1 次，MQ 消费幂等后重试

# JEDIS-011：Cluster 模式下禁止业务层二次重试

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-011 |
| 风险等级 | 风险 |
| 规则描述 | Redis Cluster 客户端已有 MOVED/ASK 重试机制，业务禁止再次重试 |

## 问题说明

指数级放大故障

## 检查方法

静态分析：检查 Cluster 模式下是否存在外层重试逻辑

## 违规示例

for (int i = 0; i < 10; i++) {<br>    jedisCluster.get(key);<br>}

## 合规示例

依赖 JedisCluster 内置重试，maxAttempts 设置 3-5

# JEDIS-012：必须设置 commandTimeout

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-012 |
| 风险等级 | 风险 |
| 规则描述 | 必须设置命令超时时间，禁止默认无限等待 |

## 问题说明

线程堆积、Tomcat 打满

## 检查方法

静态分析：检查 JedisPool/JedisCluster 是否配置 timeout

## 违规示例

JedisPool pool = new JedisPool(config, host, port);

## 合规示例

普通 KV: 100ms-500ms, Scan: 1-3s

# JEDIS-013：建议开启 testOnBorrow

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-013 |
| 风险等级 | 提示 |
| 规则描述 | 建议开启连接借用检测，防止半关闭连接 |

## 问题说明

连接已半关闭，业务首次命令失败

## 检查方法

静态分析：检查 setTestOnBorrow

## 违规示例

// 未开启 testOnBorrow

## 合规示例

config.setTestOnBorrow(true);

# JEDIS-014：SCRIPT LOAD 必须复用 SHA

| 属性 | 说明 |
|------|------|
| 规则ID | JEDIS-014 |
| 风险等级 | 提示 |
| 规则描述 | Lua 脚本禁止每次 eval()，必须先 SCRIPT LOAD 后 EVALSHA |

## 问题说明

每次传输完整脚本增加网络开销

## 检查方法

静态分析：检查是否存在重复 eval()

## 违规示例

redis.eval(script); // 每次传输完整脚本

## 合规示例

String sha = redis.scriptLoad(script);<br>redis.evalsha(sha);

