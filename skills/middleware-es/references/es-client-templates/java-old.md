# Java + RestHighLevelClient (7.x) 模板

## EsRestHighLevelConfig.java

```java
package com.example.es.config;

import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestClientBuilder;
import org.elasticsearch.client.RestHighLevelClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class EsRestHighLevelConfig {

    @Value("${elasticsearch.host}")
    private String host;

    @Value("${elasticsearch.port}")
    private int port;

    @Value("${elasticsearch.scheme:http}")
    private String scheme;

    @Value("${elasticsearch.username}")
    private String username;

    @Value("${elasticsearch.password}")
    private String password;

    @Value("${elasticsearch.connect-timeout:5000}")
    private int connectTimeout;

    @Value("${elasticsearch.socket-timeout:60000}")
    private int socketTimeout;

    @Bean(destroyMethod = "close")
    public RestHighLevelClient restHighLevelClient() {
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
        );

        return new RestHighLevelClient(builder);
    }
}
```

## EsDocumentService.java（旧版 API）

```java
package com.example.es.service;

import org.elasticsearch.action.delete.DeleteRequest;
import org.elasticsearch.action.delete.DeleteResponse;
import org.elasticsearch.action.get.GetRequest;
import org.elasticsearch.action.get.GetResponse;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.client.indices.CreateIndexRequest;
import org.elasticsearch.client.indices.GetIndexRequest;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.xcontent.XContentType;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.search.sort.SortOrder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class EsDocumentService {

    private static final Logger log = LoggerFactory.getLogger(EsDocumentService.class);

    private final RestHighLevelClient esClient;

    public EsDocumentService(RestHighLevelClient esClient) {
        this.esClient = esClient;
    }

    /**
     * 创建索引
     */
    public boolean createIndexIfNotExists(String indexName, String mappingJson,
            int shards, int replicas) throws IOException {
        GetIndexRequest getIndexRequest = new GetIndexRequest(indexName);
        boolean exists = esClient.indices().exists(getIndexRequest, RequestOptions.DEFAULT);
        if (!exists) {
            CreateIndexRequest request = new CreateIndexRequest(indexName);
            request.mapping(mappingJson, XContentType.JSON);
            request.settings(Settings.builder()
                .put("index.number_of_shards", shards)
                .put("index.number_of_replicas", replicas));
            esClient.indices().create(request, RequestOptions.DEFAULT);
            log.info("索引 {} 创建成功", indexName);
            return true;
        }
        return false;
    }

    /**
     * 索引单条文档
     */
    public String indexDocument(String indexName, String id, String jsonDoc) throws IOException {
        IndexRequest request = new IndexRequest(indexName).id(id)
            .source(jsonDoc, XContentType.JSON);
        IndexResponse response = esClient.index(request, RequestOptions.DEFAULT);
        return response.getResult().name();
    }

    /**
     * 根据 ID 获取文档
     */
    public Map<String, Object> getDocument(String indexName, String id) throws IOException {
        GetRequest request = new GetRequest(indexName, id);
        GetResponse response = esClient.get(request, RequestOptions.DEFAULT);
        return response.isExists() ? response.getSourceAsMap() : null;
    }

    /**
     * 使用 search_after 深分页查询
     */
    public List<Map<String, Object>> searchAfter(String indexName,
            Object[] sortValues, int size) throws IOException {
        SearchSourceBuilder sourceBuilder = new SearchSourceBuilder()
            .query(QueryBuilders.matchAllQuery())
            .size(size)
            .sort("_id", SortOrder.ASC);
        if (sortValues != null && sortValues.length > 0) {
            sourceBuilder.searchAfter(sortValues);
        }
        SearchRequest searchRequest = new SearchRequest(indexName).source(sourceBuilder);
        SearchResponse response = esClient.search(searchRequest, RequestOptions.DEFAULT);

        List<Map<String, Object>> results = new ArrayList<>();
        for (SearchHit hit : response.getHits()) {
            results.add(hit.getSourceAsMap());
        }
        return results;
    }

    /**
     * 删除文档
     */
    public String deleteDocument(String indexName, String id) throws IOException {
        DeleteRequest request = new DeleteRequest(indexName, id);
        DeleteResponse response = esClient.delete(request, RequestOptions.DEFAULT);
        return response.getResult().name();
    }
}
```

## application.yml（旧版）

```yaml
elasticsearch:
  host: ${ES_HOST:localhost}
  port: ${ES_PORT:9200}
  scheme: ${ES_SCHEME:http}
  username: ${ES_USERNAME:elastic}
  password: ${ES_PASSWORD}  # 通过环境变量注入，禁止明文
  connect-timeout: 5000
  socket-timeout: 60000
```

## Maven 依赖（旧版 7.x）

```xml
<dependencies>
    <!-- Elasticsearch Rest High Level Client 7.x -->
    <dependency>
        <groupId>org.elasticsearch.client</groupId>
        <artifactId>elasticsearch-rest-high-level-client</artifactId>
        <version>7.17.15</version>
    </dependency>
    <dependency>
        <groupId>org.elasticsearch</groupId>
        <artifactId>elasticsearch</artifactId>
        <version>7.17.15</version>
    </dependency>
</dependencies>
```