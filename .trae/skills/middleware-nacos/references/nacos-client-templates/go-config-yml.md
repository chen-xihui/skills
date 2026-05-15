# Go 模板：config.yaml

Go 项目 Nacos 连接配置文件。

生成目标文件：`config.yaml`

```yaml
nacos:
  server_addr: "${NACOS_SERVER_ADDR:localhost}"
  namespace: "${NACOS_NAMESPACE:}"
  username: "${NACOS_USERNAME:nacos}"
  password: "${NACOS_PASSWORD}"  # 通过环境变量注入，禁止明文
```
