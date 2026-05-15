# Java + new：EsDocumentService.java

适用于 ES 8.x+ 的 ElasticsearchClient 文档操作服务类。

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
