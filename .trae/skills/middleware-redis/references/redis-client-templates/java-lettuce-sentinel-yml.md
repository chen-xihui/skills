# Java 模板：Lettuce + Sentinel - application.yml

Sentinel 应用配置，含 Sentinel 节点列表和连接池参数。

生成目标文件：`application.yml`

```yaml
spring:
  data:
    redis:
      password: ${REDIS_PASSWORD}
      timeout: 3000ms
      sentinel:
        master: mymaster
        nodes: ${REDIS_SENTINEL_NODES:sentinel1:26379,sentinel2:26379,sentinel3:26379}
      lettuce:
        pool:
          max-active: 20
          max-idle: 10
          min-idle: 5
          max-wait: 3000ms
```
