# Java 模板：Lettuce + Standalone - application.yml

Spring Boot 应用配置，含 Lettuce 连接池参数。

生成目标文件：`application.yml`

```yaml
spring:
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD}  # 通过环境变量注入，禁止明文
      timeout: 3000ms
      lettuce:
        pool:
          max-active: 20      # maxTotal（REDIS-004）
          max-idle: 10        # maxIdle
          min-idle: 5         # minIdle
          max-wait: 3000ms    # maxWaitMillis
        shutdown-timeout: 100ms
```
