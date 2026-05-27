# Java — BBoss Elasticsearch（bboss-elasticsearch-spring-boot-starter）

适用于企业内广泛使用 **BBoss** 封装层的项目，支持 **Elasticsearch 7.x / 8.x** 集群，提供 DSL、ORM 风格 API、批量导入导出等能力。

> 官方站点与文档：https://esdoc.bbossgroups.com/

## 选型说明

| 项 | 说明 |
|----|------|
| Starter | `bboss-elasticsearch-spring-boot-starter` |
| 核心 API | `ClientInterface`（`ElasticSearchHelper.getRestClientUtil()`） |
| 适用场景 | 已有 BBoss 规范、复杂批量同步、需要内置 DSL 模板 |

## application.yml（Spring Boot）

```yaml
spring:
  elasticsearch:
    bboss:
      elasticUser: ${ES_USERNAME}
      elasticPassword: ${ES_PASSWORD}
      elasticsearch:
        rest:
          # 来自 paas-cli Hosts；多节点逗号分隔，可写 ip:port 或 https://host:9200
          hostNames: ${ES_HOSTS}
        # 生产建议关闭模板 SQL 打印
        showTemplate: false
        # 连接池与超时（可按平台规范调整）
        http:
          timeoutConnection: 5000
          timeoutSocket: 60000
          connectionRequestTimeout: 5000
          maxTotal: 200
          defaultMaxPerRoute: 100
```

等效 `application.properties` 片段：

```properties
spring.elasticsearch.bboss.elasticUser=${ES_USERNAME}
spring.elasticsearch.bboss.elasticPassword=${ES_PASSWORD}
spring.elasticsearch.bboss.elasticsearch.rest.hostNames=${ES_HOSTS}
spring.elasticsearch.bboss.elasticsearch.showTemplate=false
```

## BbossDemoService.java

```java
package com.example.es.service;

import org.frameworkset.elasticsearch.client.ClientInterface;
import org.frameworkset.elasticsearch.entity.ESDatas;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class BbossDemoService {

  /** 默认 DSL 配置文件：resources/esmapper/demo.xml */
  private final ClientInterface clientUtil;

  public BbossDemoService() {
    this.clientUtil = org.frameworkset.elasticsearch.ElasticSearchHelper.getRestClientUtil();
  }

  /**
   * 单文档写入（索引需已存在或通过 DSL 创建）
   */
  public String addDocument(String index, Object document) {
    return clientUtil.addDocument(index, document);
  }

  /**
   * 按 ID 查询
   */
  public <T> T getDocument(String index, String id, Class<T> clazz) {
    return clientUtil.getDocument(index, id, clazz);
  }

  /**
   * DSL 查询示例：demo.xml 中定义 searchDocuments
   */
  public <T> List<T> searchByDsl(String index, String keyword, Class<T> clazz) {
    Map<String, Object> params = new HashMap<>();
    params.put("keyword", keyword);
    params.put("index", index);
    ESDatas<T> datas = clientUtil.searchList(
        "esmapper/demo.xml",
        "searchDocuments",
        params,
        clazz);
    return datas.getDatas();
  }
}
```

## resources/esmapper/demo.xml（DSL 映射示例）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<properties>
  <property name="searchDocuments">
    <![CDATA[
    {
      "query": {
        "match": {
          "name": #[keyword]
        }
      },
      "size": 20
    }
    ]]>
  </property>
</properties>
```

## DemoDocument.java（文档实体示例）

```java
package com.example.es.model;

public class DemoDocument {
  private String id;
  private String name;

  public String getId() { return id; }
  public void setId(String id) { this.id = id; }
  public String getName() { return name; }
  public void setName(String name) { this.name = name; }
}
```

## Maven

```xml
<properties>
  <bboss.elasticsearch.version>7.1.6</bboss.elasticsearch.version>
</properties>
<dependencies>
  <dependency>
    <groupId>com.bbossgroups.plugins</groupId>
    <artifactId>bboss-elasticsearch-spring-boot-starter</artifactId>
    <version>${bboss.elasticsearch.version}</version>
  </dependency>
</dependencies>
```

## Gradle

```kotlin
implementation("com.bbossgroups.plugins:bboss-elasticsearch-spring-boot-starter:7.1.6")
```

## 生成文件建议

| 文件 | 说明 |
|------|------|
| `application.yml` | BBoss 连接与账号（占位符） |
| `BbossDemoService.java` | 业务封装 |
| `resources/esmapper/*.xml` | DSL 查询（按需） |
| `model/*.java` | 文档实体 |

## 注意事项

- `hostNames` 须与平台 CLI 返回的 `Hosts` 一致；HTTPS 集群确保 BBoss 版本支持 TLS。
- 用户名以 CLI 为准；密码仅 `${ES_PASSWORD}` 环境变量注入。
- 与官方 [java-elasticsearch-java.md](java-elasticsearch-java.md) 勿在同一模块混用两套客户端 Bean，除非明确隔离。
