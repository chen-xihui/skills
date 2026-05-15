# Python：config.yaml

适用于 Python 语言的 ES 配置文件模板。

```yaml
elasticsearch:
  hosts:
    - "https://localhost:9200"
  username: "elastic"
  password: "${ES_PASSWORD}"  # 通过环境变量注入，禁止明文
  scheme: "https"
  max_retries: 3
  retry_on_timeout: true
  request_timeout: 30
  verify_certs: false
```
