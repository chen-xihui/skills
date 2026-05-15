# Java 模板：bootstrap.yml

Spring Cloud 引导配置文件，含服务发现和配置中心双模块配置。

生成目标文件：`bootstrap.yml`

```yaml
spring:
  application:
    name: ${APP_NAME:demo-service}
  cloud:
    nacos:
      server-addr: ${NACOS_SERVER_ADDR:localhost:8848}
      username: ${NACOS_USERNAME:nacos}
      password: ${NACOS_PASSWORD}  # 通过环境变量注入，禁止明文
      namespace: ${NACOS_NAMESPACE:}
      discovery:
        enabled: true
        namespace: ${NACOS_NAMESPACE:}
        group: DEFAULT_GROUP
        heart-beat-interval: 5000    # 心跳间隔（NACOS-005）
        heart-beat-timeout: 15000
        weight: 1.0                  # 权重（NACOS-005）
      config:
        enabled: true
        namespace: ${NACOS_NAMESPACE:}
        group: DEFAULT_GROUP
        data-id: application.yml
        refresh-enabled: true
        file-extension: yml
```
