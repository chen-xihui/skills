# Python 模板：config.yaml

Python 项目 Redis 连接配置文件。

生成目标文件：`config.yaml`

```yaml
redis:
  host: "${REDIS_HOST:localhost}"
  port: 6379
  password: "${REDIS_PASSWORD}"  # 通过环境变量注入
  db: 0
  max_connections: 20
  socket_timeout: 3.0
  socket_connect_timeout: 5.0
```
