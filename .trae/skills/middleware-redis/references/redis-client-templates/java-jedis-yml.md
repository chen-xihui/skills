# Java 模板：Jedis + Standalone - application.yml

Spring Boot 应用配置（Jedis 客户端），含连接池参数。

生成目标文件：`application.yml`

```yaml
spring:
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD}
      timeout: 3000ms
      jedis:
        pool:
          max-active: 20
          max-idle: 10
          min-idle: 5
          max-wait: 3000ms
```
