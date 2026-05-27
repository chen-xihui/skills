# Java — 官方 elasticsearch-java（Elastic Java API Client）

适用于 **Elasticsearch 8.x+**。基于 `co.elastic.clients:elasticsearch-java` + `elasticsearch-rest-client`，为 Elastic 官方推荐 Java 客户端。

> 与 [java-new.md](java-new.md) 内容等价；新建项目请优先使用本文件命名。

## 选型说明

| 项 | 说明 |
|----|------|
| Maven 主 artifact | `co.elastic.clients:elasticsearch-java` |
| 传输层 | `org.elasticsearch.client:elasticsearch-rest-client` |
| Spring 集成 | 可注册 `@Bean ElasticsearchClient`，或选用 [java-spring-data.md](java-spring-data.md) |

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

import java.net.URI;
import java.util.ArrayList;
import java.util.List;

@Configuration
public class ElasticsearchConfig {

    /** 平台 CLI 返回的 Hosts，如 https://es-j036x0-dev.paas.internal:9200；多节点逗号分隔 */
    @Value("${elasticsearch.hosts:${ES_HOSTS}}")
    private String hosts;

    @Value("${elasticsearch.username:${ES_USERNAME}}")
    private String username;

    @Value("${elasticsearch.password:${ES_PASSWORD}}")
    private String password;

    @Value("${elasticsearch.connect-timeout:5000}")
    private int connectTimeout;

    @Value("${elasticsearch.socket-timeout:60000}")
    private int socketTimeout;

    @Bean(destroyMethod = "close")
    public RestClient restClient() {
        CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(
            AuthScope.ANY,
            new UsernamePasswordCredentials(username, password)
        );

        HttpHost[] httpHosts = parseHosts(hosts);
        RestClientBuilder builder = RestClient.builder(httpHosts)
            .setHttpClientConfigCallback(http ->
                http.setDefaultCredentialsProvider(credentialsProvider))
            .setRequestConfigCallback(req ->
                req.setConnectTimeout(connectTimeout)
                   .setSocketTimeout(socketTimeout));

        return builder.build();
    }

    @Bean
    public ElasticsearchClient elasticsearchClient(RestClient restClient) {
        return new ElasticsearchClient(
            new RestClientTransport(restClient, new JacksonJsonpMapper()));
    }

    private static HttpHost[] parseHosts(String hostsCsv) {
        String[] parts = hostsCsv.split(",");
        List<HttpHost> list = new ArrayList<>();
        for (String part : parts) {
            String trimmed = part.trim();
            if (trimmed.isEmpty()) continue;
            URI uri = URI.create(trimmed.contains("://") ? trimmed : "https://" + trimmed);
            list.add(new HttpHost(uri.getHost(), uri.getPort() > 0 ? uri.getPort() : 9200, uri.getScheme()));
        }
        return list.toArray(new HttpHost[0]);
    }
}
```

## EsDocumentService.java（官方 API 示例）

```java
package com.example.es.service;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch.core.*;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.elasticsearch.indices.ExistsRequest;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;
import java.util.Map;

@Service
public class EsDocumentService {

    private final ElasticsearchClient client;

    public EsDocumentService(ElasticsearchClient client) {
        this.client = client;
    }

    public <T> String index(String index, String id, T doc) throws IOException {
        return client.index(i -> i.index(index).id(id).document(doc)).result().jsonValue();
    }

    public <T> BulkResponse bulkIndex(String index, List<Map.Entry<String, T>> docs) throws IOException {
        BulkRequest.Builder b = new BulkRequest.Builder();
        for (Map.Entry<String, T> e : docs) {
            b.operations(op -> op.index(idx -> idx.index(index).id(e.getKey()).document(e.getValue())));
        }
        return client.bulk(b.build());
    }

    public <T> T get(String index, String id, Class<T> clazz) throws IOException {
        GetResponse<T> r = client.get(g -> g.index(index).id(id), clazz);
        return r.found() ? r.source() : null;
    }

    /** 深分页：search_after */
    public <T> List<Hit<T>> searchAfter(String index, List<String> searchAfter, int size, Class<T> clazz)
            throws IOException {
        var builder = new co.elastic.clients.elasticsearch.core.SearchRequest.Builder()
            .index(index)
            .size(size)
            .sort(s -> s.field(f -> f.field("_id").order(
                co.elastic.clients.elasticsearch._types.SortOrder.Asc)));
        if (searchAfter != null && !searchAfter.isEmpty()) {
            builder.searchAfter(searchAfter);
        }
        return client.search(builder.build(), clazz).hits().hits();
    }
}
```

## application.yml

```yaml
elasticsearch:
  hosts: ${ES_HOSTS}          # 来自 paas-cli es config 的 Hosts
  username: ${ES_USERNAME}    # 来自 CLI Username，禁止用户覆盖
  password: ${ES_PASSWORD}    # 占位符，环境变量注入
  connect-timeout: 5000
  socket-timeout: 60000
```

## Maven（版本与集群 es_version 对齐，示例 8.12）

```xml
<properties>
  <elasticsearch.version>8.12.2</elasticsearch.version>
</properties>
<dependencies>
  <dependency>
    <groupId>co.elastic.clients</groupId>
    <artifactId>elasticsearch-java</artifactId>
    <version>${elasticsearch.version}</version>
  </dependency>
  <dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch-rest-client</artifactId>
    <version>${elasticsearch.version}</version>
  </dependency>
  <dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
  </dependency>
</dependencies>
```

## Gradle（Kotlin DSL 片段）

```kotlin
dependencies {
    implementation("co.elastic.clients:elasticsearch-java:8.12.2")
    implementation("org.elasticsearch.client:elasticsearch-rest-client:8.12.2")
}
```
