# Java — Spring Boot Starter（spring-boot-starter-data-elasticsearch）

适用于 **Spring Boot 3.2+** + **Elasticsearch 8.x**。底层使用官方 **elasticsearch-java** 客户端，通过 Spring Data Elasticsearch 提供 `ElasticsearchRepository`、Template 等能力。

## 选型说明

| 项 | 说明 |
|----|------|
| Starter | `spring-boot-starter-data-elasticsearch` |
| 配置类 | 继承 `ElasticsearchConfiguration` 自定义 `ClientConfiguration` |
| 与官方客户端关系 | Spring Data 5.x 内置 elasticsearch-java，无需单独声明 `ElasticsearchClient` Bean（除非要混用低级 API） |

## ElasticsearchSpringConfig.java

```java
package com.example.es.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.elasticsearch.client.ClientConfiguration;
import org.springframework.data.elasticsearch.client.elc.ElasticsearchConfiguration;
import org.springframework.data.elasticsearch.repository.config.EnableElasticsearchRepositories;

import java.time.Duration;

@Configuration
@EnableElasticsearchRepositories(basePackages = "com.example.es.repository")
public class ElasticsearchSpringConfig extends ElasticsearchConfiguration {

    @Value("${spring.elasticsearch.uris:${ES_HOSTS}}")
    private String uris;

    @Value("${spring.elasticsearch.username:${ES_USERNAME}}")
    private String username;

    @Value("${spring.elasticsearch.password:${ES_PASSWORD}}")
    private String password;

    @Override
    public ClientConfiguration clientConfiguration() {
        // uris 示例: https://es-j036x0-dev.paas.internal:9200（与 CLI Hosts 一致）
        String[] nodes = uris.split(",");
        return ClientConfiguration.builder()
            .connectedTo(nodes)
            .usingSsl(uris.contains("https"))
            .withBasicAuth(username, password)
            .withConnectTimeout(Duration.ofSeconds(5))
            .withSocketTimeout(Duration.ofSeconds(60))
            .build();
    }
}
```

## 实体与 Repository 示例

```java
package com.example.es.document;

import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;

@Document(indexName = "product")
public class Product {

    @Id
    private String id;

    @Field(type = FieldType.Text)
    private String name;

    // getters / setters
}
```

```java
package com.example.es.repository;

import com.example.es.document.Product;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

import java.util.List;

public interface ProductRepository extends ElasticsearchRepository<Product, String> {

    List<Product> findByName(String name);
}
```

## ProductSearchService.java（ElasticsearchOperations 可选）

```java
package com.example.es.service;

import com.example.es.document.Product;
import org.springframework.data.elasticsearch.core.ElasticsearchOperations;
import org.springframework.data.elasticsearch.core.SearchHit;
import org.springframework.data.elasticsearch.core.query.Criteria;
import org.springframework.data.elasticsearch.core.query.CriteriaQuery;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class ProductSearchService {

    private final ElasticsearchOperations operations;

    public ProductSearchService(ElasticsearchOperations operations) {
        this.operations = operations;
    }

    public List<Product> searchByName(String keyword) {
        CriteriaQuery query = new CriteriaQuery(
            new Criteria("name").contains(keyword));
        return operations.search(query, Product.class).stream()
            .map(SearchHit::getContent)
            .collect(Collectors.toList());
    }
}
```

## application.yml

```yaml
spring:
  elasticsearch:
    uris: ${ES_HOSTS}           # 来自 paas-cli；多节点逗号分隔
    username: ${ES_USERNAME}
    password: ${ES_PASSWORD}
    connection-timeout: 5s
    socket-timeout: 60s
```

## Maven（Spring Boot 3.2+ BOM）

```xml
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.2.5</version>
</parent>
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
  </dependency>
</dependencies>
```

## 版本对照（生成时按 CLI `Version` 选用）

| 集群版本 | Spring Boot | Spring Data Elasticsearch |
|----------|-------------|---------------------------|
| 8.12.x | 3.2.x / 3.3.x | 5.3.x / 5.4.x |
| 7.17.x | 2.7.x | 4.4.x（建议用 [java-old.md](java-old.md) 或 BBoss） |

## 注意事项

- Boot 2.x + ES 8 组合不在本模板范围，需降级集群或升级 Boot。
- 需要直接使用低级 `ElasticsearchClient` 时，可额外引入 [java-elasticsearch-java.md](java-elasticsearch-java.md) 并 `@Autowired` 共存。
