# Java + ElasticsearchClient (8.x+) 模板

> **已拆分**：完整官方客户端模板见 [java-elasticsearch-java.md](java-elasticsearch-java.md)。下文保留兼容；新建请优先引用该文件。

---

## ElasticsearchConfig.java

```java
package com.example.es.config;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestClientBuilder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ElasticsearchConfig {

    @Value("${elasticsearch.host}")
    private String host;

    @Value("${elasticsearch.port}")
    private int port;

    @Value("${elasticsearch.scheme:https}")
    private String scheme;

    @Value("${elasticsearch.username}")
    private String username;

    @Value("${elasticsearch.password}")
    private String password;

    @Value("${elasticsearch.connect-timeout:5000}")
    private int connectTimeout;

    @Value("${elasticsearch.socket-timeout:60000}")
    private int socketTimeout;

    @Value("${elasticsearch.max-retry-timeout:60000}")
    private int maxRetryTimeout;

    @Bean(destroyMethod = "close")
    public RestClient restClient() {
        CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(
            AuthScope.ANY,
            new UsernamePasswordCredentials(username, password)
        );

        RestClientBuilder builder = RestClient.builder(
            new HttpHost(host, port, scheme)
        )
        .setHttpClientConfigCallback(httpClientBuilder ->
            httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider)
        )
        .setRequestConfigCallback(requestConfigBuilder ->
            requestConfigBuilder
                .setConnectTimeout(connectTimeout)
                .setSocketTimeout(socketTimeout)
                .setConnectionRequestTimeout(maxRetryTimeout)
        );

        return builder.build();
    }

    @Bean
    public ElasticsearchClient elasticsearchClient(RestClient restClient) {
        RestClientTransport transport = new RestClientTransport(
            restClient, new JacksonJsonpMapper()
        );
        return new ElasticsearchClient(transport);
    }
}
```

## EsDocumentService.java（新版 API）

```java
package com.example.es.service;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch.core.*;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.elasticsearch.indices.CreateIndexRequest;
import co.elastic.clients.elasticsearch.indices.ExistsRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;
import java.util.Map;

@Service
public class EsDocumentService {

    private static final Logger log = LoggerFactory.getLogger(EsDocumentService.class);

    private final ElasticsearchClient esClient;

    public EsDocumentService(ElasticsearchClient esClient) {
        this.esClient = esClient;
    }

    /**
     * 创建索引（如不存在）
     */
    public boolean createIndexIfNotExists(String indexName, Map<String, Object> mapping) throws IOException {
        boolean exists = esClient.indices()
            .exists(ExistsRequest.of(e -> e.index(indexName)))
            .value();
        if (!exists) {
            esClient.indices().create(CreateIndexRequest.of(c -> c
                .index(indexName)
                .mappings(m -> m.properties(mapping))
            ));
            log.info("索引 {} 创建成功", indexName);
            return true;
        }
        return false;
    }

    /**
     * 索引单条文档
     */
    public <T> String indexDocument(String indexName, String id, T document) throws IOException {
        IndexResponse response = esClient.index(i -> i
            .index(indexName)
            .id(id)
            .document(document)
        );
        return response.result().jsonValue();
    }

    /**
     * 批量索引文档（使用 BulkRequest）
     */
    public <T> BulkResponse bulkIndex(String indexName, List<Map.Entry<String, T>> documents) throws IOException {
        BulkRequest.Builder bulkBuilder = new BulkRequest.Builder();
        for (Map.Entry<String, T> entry : documents) {
            bulkBuilder.operations(op -> op
                .index(idx -> idx
                    .index(indexName)
                    .id(entry.getKey())
                    .document(entry.getValue())
                )
            );
        }
        return esClient.bulk(bulkBuilder.build());
    }

    /**
     * 根据 ID 获取文档
     */
    public <T> T getDocument(String indexName, String id, Class<T> clazz) throws IOException {
        GetResponse<T> response = esClient.get(g -> g
            .index(indexName)
            .id(id),
            clazz
        );
        return response.found() ? response.source() : null;
    }

    /**
     * 使用 search_after 深分页查询（推荐方式）
     */
    public <T> List<Hit<T>> searchAfter(String indexName, List<String> sortValues,
            int size, Class<T> clazz) throws IOException {
        SearchRequest.Builder searchBuilder = new SearchRequest.Builder()
            .index(indexName)
            .size(size)
            .sort(s -> s.field(f -> f.field("_id").order(co.elastic.clients.elasticsearch._types.SortOrder.Asc)));

        if (sortValues != null && !sortValues.isEmpty()) {
            searchBuilder.searchAfter(sortValues);
        }

        SearchResponse<T> response = esClient.search(searchBuilder.build(), clazz);
        return response.hits().hits();
    }

    /**
     * 删除文档
     */
    public String deleteDocument(String indexName, String id) throws IOException {
        DeleteResponse response = esClient.delete(d -> d
            .index(indexName)
            .id(id)
        );
        return response.result().jsonValue();
    }
}
```

## application.yml（新版）

```yaml
elasticsearch:
  host: ${ES_HOST:localhost}
  port: ${ES_PORT:9200}
  scheme: ${ES_SCHEME:https}
  username: ${ES_USERNAME:elastic}
  password: ${ES_PASSWORD}  # 通过环境变量注入，禁止明文
  connect-timeout: 5000
  socket-timeout: 60000
  max-retry-timeout: 60000

spring:
  elasticsearch:
    uris: ${ES_SCHEME:https}://${ES_HOST:localhost}:${ES_PORT:9200}
```

## Maven 依赖（新版 8.x）

```xml
<dependencies>
    <!-- Elasticsearch Java Client 8.x -->
    <dependency>
        <groupId>co.elastic.clients</groupId>
        <artifactId>elasticsearch-java</artifactId>
        <version>8.12.0</version>
    </dependency>
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.15.2</version>
    </dependency>
    <dependency>
        <groupId>org.elasticsearch.client</groupId>
        <artifactId>elasticsearch-rest-client</artifactId>
        <version>8.12.0</version>
    </dependency>
</dependencies>
```