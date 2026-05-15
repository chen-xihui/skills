# Java 模板：Lettuce + Cluster - application.yml

Cluster 应用配置，含集群节点和连接池参数。

生成目标文件：`application.yml`

```yaml
spring:
  data:
    redis:
      password: ${REDIS_PASSWORD}
      timeout: 3000ms
      cluster:
        nodes: ${REDIS_CLUSTER_NODES:node1:6379,node2:6379,node3:6379}
        max-redirects: 3
      lettuce:
        pool:
          max-active: 20
          max-idle: 10
          min-idle: 5
          max-wait: 3000ms
```
