# Nacos 客户端代码模板索引

本目录包含 Nacos 客户端的代码模板，供智能体在执行客户端创建时参考。

**平台字段（能力一）**：生成前须先经 **paas-cli Skill** 执行 `$PAAS_CLI auth check`、`$PAAS_CLI nacos config`；`server_addr`、`namespace`、`username` 以 CLI 解析结果填入模板或环境变量默认值，用户名不得被用户输入覆盖；密码仅用 `${NACOS_PASSWORD}` 占位符。

| 语言 | 详情 | 生成文件 |
|------|------|---------|
| Java | [java.md](java.md) | NacosConfigService.java、NacosDiscoveryService.java、bootstrap.yml |
| Go | [go.md](go.md) | nacos_client.go、config.yaml |
| Python | [python.md](python.md) | nacos_client.py、config.yaml |

## 依赖提示

- **Java**: Spring Cloud Alibaba Nacos Discovery + Config
- **Go**: `github.com/nacos-group/nacos-sdk-go/v2`
- **Python**: `nacos-sdk-python`