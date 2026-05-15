# Go 模板：config.yaml

Go 项目 Redis 连接配置文件。

生成目标文件：`config.yaml`

```yaml
redis:
  addr: "${REDIS_ADDR:localhost:6379}"
  password: "${REDIS_PASSWORD}"  # 通过环境变量注入
  db: 0
  max_retries: 3
  dial_timeout_ms: 5000
  read_timeout_ms: 3000
  write_timeout_ms: 3000
  pool_size: 20        # REDIS-004：连接池大小
  min_idle_conns: 5
```
