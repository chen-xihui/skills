# ES 客户端代码模板索引

本目录包含 Elasticsearch 客户端的代码模板，供智能体在执行客户端创建时参考。

**平台字段（能力一）**：生成前须 `$PAAS_CLI auth check`，再 `$PAAS_CLI es config`；`Hosts`、`Scheme`、`Username` 以 CLI 为准；密码仅用 `${ES_PASSWORD}`。

## Java 技术栈选型（`java_stack`）

用户未指定时，按下列规则默认：

| 条件 | 推荐 `java_stack` |
|------|-------------------|
| ES 7.x（`client_version=old`） | `rhlc` → [java-old.md](java-old.md) |
| ES 8.x + 已有 Spring Boot 3.2+ | `spring-data` → [java-spring-data.md](java-spring-data.md) |
| ES 8.x + 团队使用 BBoss / 需 DSL 批量 | `bboss` → [java-bboss.md](java-bboss.md) |
| ES 8.x + 需完整官方 API / 非 Spring 或细粒度控制 | `elasticsearch-java`（**默认**）→ [java-elasticsearch-java.md](java-elasticsearch-java.md) |

| `java_stack` | 说明 | 详情 |
|--------------|------|------|
| **elasticsearch-java** | 官方 Elastic Java API Client（`co.elastic.clients`） | [java-elasticsearch-java.md](java-elasticsearch-java.md) |
| **spring-data** | `spring-boot-starter-data-elasticsearch` + Repository | [java-spring-data.md](java-spring-data.md) |
| **bboss** | `bboss-elasticsearch-spring-boot-starter` + DSL | [java-bboss.md](java-bboss.md) |
| **rhlc** | RestHighLevelClient（7.x 遗留） | [java-old.md](java-old.md) |

> [java-new.md](java-new.md) 为 `elasticsearch-java` 的兼容别名。

## 其他语言

| 语言 | 详情 |
|------|------|
| Go | [go.md](go.md) |
| Python | [python.md](python.md) |
| Node.js | [nodejs.md](nodejs.md) |

## 生成文件对照

| 组合 | 生成文件 |
|------|---------|
| Java + elasticsearch-java | `ElasticsearchConfig.java`、`EsDocumentService.java`、`application.yml` |
| Java + spring-data | `ElasticsearchSpringConfig.java`、`Product.java`、`ProductRepository.java`、`application.yml`（+ 可选 `ProductSearchService.java`） |
| Java + bboss | `application.yml`、`BbossDemoService.java`、`resources/esmapper/demo.xml`、实体类 |
| Java + rhlc (old) | `EsRestHighLevelConfig.java`、`EsDocumentService.java`、`application.yml` |
| Go | `es_client.go`、`config.yaml` |
| Python | `es_client.py`、`config.py` |
| Node.js | `elasticsearch_client.js`、`config.js` |

## 依赖速查

| java_stack | 主要依赖 |
|------------|----------|
| elasticsearch-java | `co.elastic.clients:elasticsearch-java`、`elasticsearch-rest-client` |
| spring-data | `spring-boot-starter-data-elasticsearch` |
| bboss | `com.bbossgroups.plugins:bboss-elasticsearch-spring-boot-starter` |
| rhlc | `elasticsearch-rest-high-level-client` 7.x |

版本号须与 CLI `Version`（`es_version`）对齐。
