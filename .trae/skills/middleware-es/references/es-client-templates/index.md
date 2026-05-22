# ES 客户端代码模板索引

本目录包含 Elasticsearch 客户端的代码模板，供智能体在执行客户端创建时参考。

## 模板清单

| 语言/版本 | 详情文件 | 说明 |
|-----------|---------|------|
| Java (ElasticsearchClient 8.x+) | [java-new.md](./java-new.md) | 新版 API，适用于 ES 8.x+ |
| Java (RestHighLevelClient 7.x) | [java-old.md](./java-old.md) | 旧版 API，适用于 ES 7.x |
| Go | [go.md](./go.md) | go-elasticsearch 客户端 |
| Python | [python.md](./python.md) | elasticsearch-py 客户端 |
| Node.js | [nodejs.md](./nodejs.md) | @elastic/elasticsearch 客户端 |

## 生成文件对照

| 组合 | 生成文件 |
|------|---------|
| Java + new | ElasticsearchConfig.java、EsDocumentService.java、application.yml |
| Java + old | EsRestHighLevelConfig.java、EsDocumentService.java、application.yml |
| Go | es_client.go、config.yaml |
| Python | es_client.py、config.py |
| Node.js | elasticsearch_client.js、config.js |

## 依赖提示

- **Java + new**：`co.elastic.clients:elasticsearch-java:8.x.x`、`com.fasterxml.jackson.core:jackson-databind`、`org.elasticsearch.client:elasticsearch-rest-client`
- **Java + old**：`org.elasticsearch.client:elasticsearch-rest-high-level-client:7.x.x`
- **Go**：`go get github.com/elastic/go-elasticsearch/v8` 或 `v7`
- **Python**：`pip install elasticsearch`
- **Node.js**：`npm install @elastic/elasticsearch`