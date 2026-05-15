# Java + new：application.yml

适用于 ES 8.x+ 的 Spring Boot 配置文件。

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
