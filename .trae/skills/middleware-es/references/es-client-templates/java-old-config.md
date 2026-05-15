# Java + old：EsRestHighLevelConfig.java

适用于 ES 7.x 的 RestHighLevelClient 配置类。

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
