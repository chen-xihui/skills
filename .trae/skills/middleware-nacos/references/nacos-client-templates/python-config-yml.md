# Python 模板：config.yaml

Python 项目 Nacos 连接配置文件。

生成目标文件：`config.yaml`

```yaml
nacos:
  server_addresses: "localhost:8848"
  namespace: ""
  username: "nacos"
  password: "${NACOS_PASSWORD}"  # 通过环境变量注入，禁止明文
```
