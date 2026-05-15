# Java 模板：Maven 依赖

Maven 依赖配置片段，需添加到项目 pom.xml 中。

```xml
<dependencies>
    <!-- Spring Cloud Alibaba Nacos -->
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        <version>2023.0.1.0</version>
    </dependency>
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
        <version>2023.0.1.0</version>
    </dependency>
    <!-- Nacos Client -->
    <dependency>
        <groupId>com.alibaba.nacos</groupId>
        <artifactId>nacos-client</artifactId>
        <version>2.3.2</version>
    </dependency>
</dependencies>
```
