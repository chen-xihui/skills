# ES 代码优化检查规则详细说明

本文件包含 ES-001 ~ ES-008 共 8 条检查规则的详细说明、检查方法和代码示例，供智能体在执行代码优化检查时参考。

---

## ES-001：深分页应使用 search_after 替代 from/size

| 属性 | 说明 |
|------|------|
| 规则ID | ES-001 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 深分页应使用 search_after 替代 from/size，当 from 值 > 10000 时性能严重下降 |

### 问题说明

Elasticsearch 的 `from` + `size` 分页方式在深分页时性能极差。ES 需要在每个分片上取 `from + size` 条数据，再在协调节点上合并排序。当 `from` 值很大时（如 10000+），每个分片需要返回大量数据，导致内存和 CPU 消耗急剧增加。

### 检查方法

1. 搜索 `SearchRequest` 或 `SearchSourceBuilder` 中使用 `from()` 方法设置偏移量的代码
2. 搜索代码中的 `from` 和 `size` 组合使用
3. 重点关注 `from` 值是否可能超过 10000（硬编码大值、动态计算、用户输入未限制）

搜索模式：
- `grep_code` 搜索 `.from(` 或 `setFrom(` 或 `"from"` + `"size"` 组合
- `search_codebase` 搜索 "deep pagination" 或 "from size" 相关代码

### 违规示例（Java 新版）

```java
// ❌ 深分页：from 值过大
SearchResponse<Map> response = esClient.search(s -> s
    .index("logs")
    .from(50000)  // 危险：深分页
    .size(100)
    .query(q -> q.matchAll(m -> m)),
    Map.class
);
```

### 合规示例（Java 新版）

```java
// ✅ 使用 search_after 实现深分页
List<Hit<Map>> hits = esClient.search(s -> s
    .index("logs")
    .size(100)
    .sort(so -> so.field(f -> f.field("_id").order(SortOrder.Asc)))
    .searchAfter(lastSortValues),  // 上一页最后一条的排序值
    Map.class
).hits().hits();
```

---

## ES-002：bulk 操作的批次大小应合理

| 属性 | 说明 |
|------|------|
| 规则ID | ES-002 |
| 风险等级 | 🟡 警告 |
| 规则描述 | bulk 操作的批次大小应合理（建议 5-15MB），过大会导致内存压力，过小则效率低 |

### 问题说明

Bulk 请求的批次大小直接影响写入性能和集群稳定性。批次过大会占用过多 JVM 堆内存，可能触发熔断器；批次过小则网络往返次数多，吞吐量低。建议每个 bulk 请求大小控制在 5-15MB 之间。

### 检查方法

1. 搜索 `BulkRequest`、`bulk` 相关代码
2. 检查是否有批次大小限制（如固定条数或大小）
3. 检查是否在循环中逐条调用 bulk（每条一个 bulk 请求，效率极低）

搜索模式：
- `grep_code` 搜索 `BulkRequest`、`bulk(`、`bulkIndex`、`bulk_index`
- `search_codebase` 搜索 "bulk" 相关代码

### 违规示例

```java
// ❌ 没有批次大小控制，一次性提交所有数据
BulkRequest.Builder bulkBuilder = new BulkRequest.Builder();
for (Map.Entry<String, Object> entry : allDocuments.entrySet()) {
    bulkBuilder.operations(op -> op.index(idx -> idx
        .index("logs")
        .id(entry.getKey())
        .document(entry.getValue())
    ));
}
// 如果 allDocuments 有几十万条，这个 bulk 请求会极大
esClient.bulk(bulkBuilder.build());
```

### 合规示例

```java
// ✅ 分批提交，每批 1000 条或 10MB
int batchSize = 1000;
List<Map.Entry<String, Object>> batch = new ArrayList<>();

for (Map.Entry<String, Object> entry : allDocuments.entrySet()) {
    batch.add(entry);
    if (batch.size() >= batchSize) {
        executeBatch(batch);
        batch.clear();
    }
}
if (!batch.isEmpty()) {
    executeBatch(batch);
}
```

---

## ES-003：索引映射设计是否合理

| 属性 | 说明 |
|------|------|
| 规则ID | ES-003 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 索引映射设计是否合理，避免 dynamic mapping 导致类型混乱 |

### 问题说明

ES 默认启用 dynamic mapping，自动推断字段类型。当同一字段名被不同类型的数据写入时（如先写入数字再写入字符串），可能导致映射冲突和查询异常。建议在创建索引时显式定义 mapping，或在生产环境中设置 `dynamic: strict`。

### 检查方法

1. 搜索索引创建代码，检查是否有显式 mapping 定义
2. 搜索 `CreateIndexRequest`、`mapping`、`mappings` 关键词
3. 检查是否设置了 `dynamic` 策略

搜索模式：
- `grep_code` 搜索 `CreateIndexRequest`、`mapping`、`mappings`、`dynamic`
- `search_codebase` 搜索 "index mapping" 相关代码

### 违规示例

```java
// ❌ 创建索引时没有定义 mapping，依赖 dynamic mapping
CreateIndexRequest request = new CreateIndexRequest("logs");
// 没有 .mapping(...) 调用
esClient.indices().create(request);
```

### 合规示例

```java
// ✅ 显式定义 mapping，设置 dynamic: strict
esClient.indices().create(c -> c
    .index("logs")
    .mappings(m -> m
        .dynamic("strict")
        .properties("timestamp", p -> p.date(d -> d))
        .properties("level", p -> p.keyword(k -> k))
        .properties("message", p -> p.text(t -> t))
    )
);
```

---

## ES-004：高消耗脚本查询检测

| 属性 | 说明 |
|------|------|
| 规则ID | ES-004 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 高消耗脚本查询检测（script_query、painless 脚本），脚本查询可能导致 CPU 飙升和集群不稳定 |

### 问题说明

在查询中使用 Painless 脚本（`script_query`、`script_score`、`runtime_fields` 中的脚本）会导致每个文档都需要执行脚本计算，CPU 消耗极大，严重影响查询性能和集群稳定性。应尽量避免在查询中使用脚本，改用数据建模（如写入时预计算）或 filter 查询。

### 检查方法

1. 搜索 `script` 相关查询代码
2. 搜索 `painless`、`script_score`、`script_query` 关键词
3. 搜索 `runtimeFields` 或 `runtime` + `script` 组合

搜索模式：
- `grep_code` 搜索 `"script"`、`painless`、`scriptScore`、`scriptQuery`、`runtime`
- `search_codebase` 搜索 "script query" 或 "painless" 相关代码

### 违规示例

```java
// ❌ 使用 script_score 进行计算
SearchResponse<Map> response = esClient.search(s -> s
    .index("products")
    .query(q -> q
        .scriptScore(ss -> ss
            .query(sq -> sq.matchAll(m -> m))
            .script(sc -> sc.inline(i -> i
                .source("doc['popularity'].value * params.boost")
                .params("boost", JsonData.of(2.0))
            ))
        )
    ),
    Map.class
);
```

### 合规示例

```java
// ✅ 使用写入时预计算的字段替代运行时脚本
// 在索引 mapping 中添加 popularity_score 字段
// 写入时计算：popularity_score = popularity * 2.0
SearchResponse<Map> response = esClient.search(s -> s
    .index("products")
    .query(q -> q
        .functionScore(fs -> fs
            .query(sq -> sq.matchAll(m -> m))
            .functions(f -> f
                .fieldValueFactor(fvf -> fvf
                    .field("popularity_score")
                    .factor(1.0f)
                )
            )
        )
    ),
    Map.class
);
```

---

## ES-005：是否使用批量操作替代单条操作

| 属性 | 说明 |
|------|------|
| 规则ID | ES-005 |
| 风险等级 | 🔵 建议 |
| 规则描述 | 是否使用批量操作替代单条操作（批量索引/批量更新），循环中的单条操作应改为批量操作 |

### 问题说明

在循环中逐条执行 index/update/delete 操作会产生大量网络请求，效率极低。应使用 Bulk API 将多个操作合并为一次请求，大幅提升吞吐量。

### 检查方法

1. 搜索循环体内的 `index`、`update`、`delete` 单条操作
2. 检查是否有对应的 `bulk` 或 `BulkRequest` 调用
3. 关注 `for` / `while` 循环中的 ES 客户端调用

搜索模式：
- `grep_code` 搜索循环体内的 `esClient.index(`、`esClient.update(`、`esClient.delete(`
- `search_codebase` 搜索 "bulk" 相关代码，检查是否缺失

### 违规示例

```java
// ❌ 循环中逐条索引
for (Document doc : documents) {
    esClient.index(i -> i
        .index("logs")
        .id(doc.getId())
        .document(doc)
    );
}
```

### 合规示例

```java
// ✅ 使用 BulkRequest 批量索引
BulkRequest.Builder bulkBuilder = new BulkRequest.Builder();
for (Document doc : documents) {
    bulkBuilder.operations(op -> op
        .index(idx -> idx
            .index("logs")
            .id(doc.getId())
            .document(doc)
        )
    );
}
esClient.bulk(bulkBuilder.build());
```

---

## ES-006：连接超时和重试配置是否合理

| 属性 | 说明 |
|------|------|
| 规则ID | ES-006 |
| 风险等级 | 🟡 警告 |
| 规则描述 | 连接超时和重试配置是否合理，缺少超时和重试配置可能导致请求无限等待 |

### 问题说明

ES 客户端连接需要合理的超时和重试配置。缺少超时配置可能导致线程阻塞在无响应的请求上；缺少重试配置则网络抖动时直接失败。建议配置连接超时 5s、Socket 超时 60s、重试 3 次。

### 检查方法

1. 搜索 ES 客户端配置代码中的 `timeout`、`retry` 设置
2. 检查 `RestClientBuilder` 的 `setRequestConfigCallback` 是否设置了超时
3. 检查 `ElasticsearchConfig` 中是否有 `connectTimeout`、`socketTimeout` 属性

搜索模式：
- `grep_code` 搜索 `connectTimeout`、`socketTimeout`、`setConnectTimeout`、`maxRetries`、`retry`
- `search_codebase` 搜索 "timeout" 或 "retry" 相关配置

### 违规示例

```java
// ❌ 没有配置超时和重试
RestHighLevelClient client = new RestHighLevelClient(
    RestClient.builder(new HttpHost("localhost", 9200, "http"))
);
```

### 合规示例

```java
// ✅ 配置连接超时和重试
RestClientBuilder builder = RestClient.builder(new HttpHost("localhost", 9200, "http"))
    .setRequestConfigCallback(requestConfigBuilder ->
        requestConfigBuilder
            .setConnectTimeout(5000)     // 连接超时 5s
            .setSocketTimeout(60000)     // Socket 超时 60s
            .setConnectionRequestTimeout(60000)
    );
```

---

## ES-007：密码是否硬编码

| 属性 | 说明 |
|------|------|
| 规则ID | ES-007 |
| 风险等级 | 🔴 严重 |
| 规则描述 | 密码是否硬编码在源码中，应使用环境变量或密钥管理系统注入 |

### 问题说明

将 ES 密码硬编码在 Java/Go/Python 源码中存在严重安全隐患。代码泄露即密码泄露，且密码轮换时需要修改源码重新部署。应通过环境变量、Spring Cloud Config、Vault 等密钥管理系统注入。

### 检查方法

1. 搜索源码中 `password` 字段的直接赋值
2. 排除配置文件（application.yml 等）中的 `${...}` 占位符形式
3. 搜索 `new UsernamePasswordCredentials` 或 `basicAuth` 中的硬编码密码

搜索模式：
- `grep_code` 搜索 `password\s*=\s*"[^${]`（排除占位符形式的赋值）
- `search_codebase` 搜索 "password" 相关代码
- 特别注意 Java 源码（.java 文件），排除配置文件

### 违规示例

```java
// ❌ 密码硬编码
credentialsProvider.setCredentials(
    AuthScope.ANY,
    new UsernamePasswordCredentials("elastic", "MySecretPassword123")  // 硬编码！
);
```

### 合规示例

```java
// ✅ 密码通过配置文件占位符 + 环境变量注入
@Value("${elasticsearch.password}")
private String password;

// application.yml 中：
// password: ${ES_PASSWORD}
```

---

## ES-008：是否合理使用索引别名

| 属性 | 说明 |
|------|------|
| 规则ID | ES-008 |
| 风险等级 | 🔵 建议 |
| 规则描述 | 是否合理使用索引别名（而非直接操作索引名），使用别名可实现零停机索引切换 |

### 问题说明

直接在代码中硬编码索引名，在需要重建索引或索引滚动时必须修改代码。使用索引别名可以实现零停机切换：先将别名指向旧索引，重建完成后原子性地将别名切换到新索引。

### 检查方法

1. 搜索代码中硬编码的索引名字符串
2. 检查是否通过配置文件或常量管理索引名
3. 检查是否使用了索引别名 API（`alias`、`aliases`）

搜索模式：
- `grep_code` 搜索 `.index("xxx")` 中的硬编码索引名
- `search_codebase` 搜索 "alias" 相关代码
- 检查索引名是否可配置化

### 违规示例

```java
// ❌ 硬编码索引名
esClient.search(s -> s.index("logs-2026-05"), Map.class);
```

### 合规示例

```java
// ✅ 使用索引别名
@Value("${elasticsearch.index-alias.logs}")
private String logsAlias;

esClient.search(s -> s.index(logsAlias), Map.class);

// 配置中：elasticsearch.index-alias.logs=logs-current
// 别名 "logs-current" 指向实际索引 "logs-2026-05"
// 切换时只需修改别名指向，无需改代码
```
