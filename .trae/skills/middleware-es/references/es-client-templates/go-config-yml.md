# Go：config.yaml

适用于 Go 语言的 ES 配置文件模板。

```yaml
elasticsearch:
  hosts:
    - "${ES_HOST:https://localhost:9200}"
  username: "${ES_USERNAME:elastic}"
  password: "${ES_PASSWORD}"  # 通过环境变量注入，禁止明文
  scheme: "https"
  max_retries: 3
  retry_on_status:
    - 502
    - 503
    - 504
  connect_timeout_ms: 5000
```
