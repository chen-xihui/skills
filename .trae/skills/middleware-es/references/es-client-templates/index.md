# ES 客户端代码模板索引

本目录包含 Elasticsearch 客户端的代码模板，按语言和版本分类。智能体执行客户端创建时，先查阅本索引确认所需模板组合，再按需加载具体模板文件。

## 模板分类

### Java + new（ElasticsearchClient，适用于 ES 8.x+）

| 文件 | 说明 |
|------|------|
| [java-new-config.md](java-new-config.md) | ElasticsearchConfig.java — 配置类（RestClient + ElasticsearchClient Bean） |
| [java-new-service.md](java-new-service.md) | EsDocumentService.java — 文档操作服务（索引、批量、查询、删除） |
| [java-new-yml.md](java-new-yml.md) | application.yml — Spring Boot 配置文件 |
| [java-new-maven.md](java-new-maven.md) | Maven 依赖 — elasticsearch-java 8.x |

生成文件：ElasticsearchConfig.java、EsDocumentService.java、application.yml

### Java + old（RestHighLevelClient，适用于 ES 7.x）

| 文件 | 说明 |
|------|------|
| [java-old-config.md](java-old-config.md) | EsRestHighLevelConfig.java — 配置类（RestHighLevelClient Bean） |
| [java-old-service.md](java-old-service.md) | EsDocumentService.java — 文档操作服务（索引、查询、删除） |
| [java-old-yml.md](java-old-yml.md) | application.yml — Spring Boot 配置文件 |
| [java-old-maven.md](java-old-maven.md) | Maven 依赖 — elasticsearch-rest-high-level-client 7.x |

生成文件：EsRestHighLevelConfig.java、EsDocumentService.java、application.yml

### Go

| 文件 | 说明 |
|------|------|
| [go-client.md](go-client.md) | es_client.go — ES 客户端封装（配置 + 连接 + 验证） |
| [go-config-yml.md](go-config-yml.md) | config.yaml — Go 项目配置文件 |

生成文件：es_client.go、config.yaml

### Python

| 文件 | 说明 |
|------|------|
| [python-client.md](python-client.md) | es_client.py — ES 客户端工具类（索引、批量、查询、删除） |
| [python-config-yml.md](python-config-yml.md) | config.yaml — Python 项目配置文件 |
| [python-pip-deps.md](python-pip-deps.md) | Pip 依赖 — elasticsearch>=8.12.0 |

生成文件：es_client.py、config.yaml
