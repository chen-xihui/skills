# ES 客户端代码模板

本文件包含 Elasticsearch 客户端的代码模板，供智能体在执行客户端创建时参考。

---

## 1. Java + new（ElasticsearchClient，适用于 ES 8.x+）

### 1.1 ElasticsearchConfig.java

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

### 1.2 EsDocumentService.java（新版 API）

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
import java.util.stream.Collectors;

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

### 1.3 application.yml（新版）

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

### 1.4 Maven 依赖（新版 8.x）

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

---

## 2. Java + old（RestHighLevelClient，适用于 ES 7.x）

### 2.1 EsRestHighLevelConfig.java

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

### 2.2 EsDocumentService.java（旧版 API）

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

### 2.3 application.yml（旧版）

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

### 2.4 Maven 依赖（旧版 7.x）

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

---

## 3. Go 客户端模板

### 3.1 es_client.go

```go
package es

import (
	"crypto/tls"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/elastic/go-elasticsearch/v8"
)

// Config ES 连接配置
type Config struct {
	Hosts         []string `yaml:"hosts"`
	Username      string   `yaml:"username"`
	Password      string   `yaml:"password"` // 通过环境变量注入
	Scheme        string   `yaml:"scheme"`
	MaxRetries    int      `yaml:"max_retries"`
	RetryOnStatus []int    `yaml:"retry_on_status"`
	ConnectTimeout int     `yaml:"connect_timeout_ms"`
}

// NewESClient 创建 ES 客户端
func NewESClient(cfg Config) (*elasticsearch.Client, error) {
	password := cfg.Password
	if password == "" {
		password = os.Getenv("ES_PASSWORD")
	}

	retryStatuses := cfg.RetryOnStatus
	if len(retryStatuses) == 0 {
		retryStatuses = []int{502, 503, 504}
	}

	maxRetries := cfg.MaxRetries
	if maxRetries == 0 {
		maxRetries = 3
	}

	esCfg := elasticsearch.Config{
		Addresses: cfg.Hosts,
		Username:  cfg.Username,
		Password:  password,
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: cfg.Scheme == "https", // 按需配置
			},
		},
		MaxRetries:    maxRetries,
		RetryOnStatus: retryStatuses,
	}

	if cfg.ConnectTimeout > 0 {
		esCfg.Transport.(*http.Transport).MaxIdleConnsPerHost = 10
	}

	client, err := elasticsearch.NewClient(esCfg)
	if err != nil {
		return nil, fmt.Errorf("创建 ES 客户端失败: %w", err)
	}

	// 验证连接
	res, err := client.Info()
	if err != nil {
		return nil, fmt.Errorf("ES 连接验证失败: %w", err)
	}
	defer res.Body.Close()

	log.Println("ES 客户端连接成功")
	return client, nil
}
```

### 3.2 config.yaml

```yaml
elasticsearch:
  hosts:
    - "${ES_HOST:https://localhost:9200}"
  username: "${ES_USERNAME:elastic}"
  password: "${ES_PASSWORD}"  # 通过环境变量注入，禁止明文
  scheme: "https"
  max_retries: 3
  retry_on_status:
    - 502
    - 503
    - 504
  connect_timeout_ms: 5000
```

---

## 4. Python 客户端模板

### 4.1 es_client.py

```python
"""Elasticsearch 客户端封装"""

import os
import logging
from typing import List, Dict, Any, Optional

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

logger = logging.getLogger(__name__)


class ESClient:
    """ES 客户端工具类"""

    def __init__(
        self,
        hosts: List[str],
        username: str = "elastic",
        password: str = None,
        scheme: str = "https",
        max_retries: int = 3,
        retry_on_timeout: bool = True,
        request_timeout: int = 30,
        verify_certs: bool = False,
    ):
        """
        初始化 ES 客户端

        Args:
            hosts: ES 节点地址列表
            username: 用户名
            password: 密码（优先从环境变量 ES_PASSWORD 获取）
            scheme: 协议（http/https）
            max_retries: 最大重试次数
            retry_on_timeout: 超时是否重试
            request_timeout: 请求超时时间（秒）
            verify_certs: 是否验证证书
        """
        _password = password or os.getenv("ES_PASSWORD", "")
        if not _password:
            logger.warning("ES 密码未设置，请配置 ES_PASSWORD 环境变量")

        self.client = Elasticsearch(
            hosts=hosts,
            basic_auth=(username, _password),
            scheme=scheme,
            max_retries=max_retries,
            retry_on_timeout=retry_on_timeout,
            request_timeout=request_timeout,
            verify_certs=verify_certs,
        )
        logger.info("ES 客户端初始化完成, hosts=%s", hosts)

    def create_index(self, index_name: str, mapping: Dict[str, Any] = None,
                     shards: int = 1, replicas: int = 1) -> bool:
        """创建索引（如不存在）"""
        if self.client.indices.exists(index=index_name):
            logger.info("索引 %s 已存在", index_name)
            return False

        body = {
            "settings": {
                "number_of_shards": shards,
                "number_of_replicas": replicas,
            }
        }
        if mapping:
            body["mappings"] = mapping

        self.client.indices.create(index=index_name, body=body)
        logger.info("索引 %s 创建成功", index_name)
        return True

    def index_document(self, index_name: str, doc_id: str, body: Dict) -> Dict:
        """索引单条文档"""
        return self.client.index(index=index_name, id=doc_id, body=body)

    def bulk_index(self, index_name: str, documents: List[Dict]) -> tuple:
        """
        批量索引文档（推荐使用）

        Returns:
            (success_count, error_count)
        """
        actions = [
            {
                "_index": index_name,
                "_id": doc.get("_id"),
                "_source": {k: v for k, v in doc.items() if k != "_id"},
            }
            for doc in documents
        ]
        success, errors = bulk(self.client, actions, raise_on_error=False)
        if errors:
            logger.error("批量索引部分失败，错误数: %d", len(errors) if isinstance(errors, list) else errors)
        return success, errors

    def search_after(
        self,
        index_name: str,
        query: Dict,
        sort_values: Optional[List] = None,
        size: int = 100,
    ) -> Dict:
        """
        使用 search_after 深分页查询（推荐方式）

        Args:
            index_name: 索引名
            query: 查询条件
            sort_values: 上一页最后一条的排序值
            size: 每页大小
        """
        body = {
            "query": query,
            "size": size,
            "sort": [{"_id": "asc"}],
        }
        if sort_values:
            body["search_after"] = sort_values

        return self.client.search(index=index_name, body=body)

    def get_document(self, index_name: str, doc_id: str) -> Optional[Dict]:
        """根据 ID 获取文档"""
        try:
            return self.client.get(index=index_name, id=doc_id)["_source"]
        except Exception:
            return None

    def delete_document(self, index_name: str, doc_id: str) -> Dict:
        """删除文档"""
        return self.client.delete(index=index_name, id=doc_id)

    def close(self):
        """关闭连接"""
        self.client.close()
```

### 4.2 config.yaml

```yaml
elasticsearch:
  hosts:
    - "https://localhost:9200"
  username: "elastic"
  password: "${ES_PASSWORD}"  # 通过环境变量注入，禁止明文
  scheme: "https"
  max_retries: 3
  retry_on_timeout: true
  request_timeout: 30
  verify_certs: false
```

### 4.3 Pip 依赖

```
elasticsearch>=8.12.0
```
