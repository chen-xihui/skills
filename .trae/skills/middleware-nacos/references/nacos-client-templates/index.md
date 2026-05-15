# Nacos 客户端代码模板索引

本目录包含 Nacos 客户端的代码模板，供智能体在执行客户端创建时参考。

**使用方式**：先在本索引中根据目标语言定位需要的模板文件，再读取对应文件获取完整代码。

---

## Java 模板

| 模板文件 | 说明 | 生成目标文件 |
|---------|------|------------|
| [java-config-service.md](./java-config-service.md) | 配置服务类，含本地快照、Listener、长轮询配置 | NacosConfigService.java |
| [java-discovery-service.md](./java-discovery-service.md) | 服务发现类，含注册/注销/查询实例 | NacosDiscoveryService.java |
| [java-bootstrap-yml.md](./java-bootstrap-yml.md) | Spring Cloud 引导配置文件 | bootstrap.yml |
| [java-maven-deps.md](./java-maven-deps.md) | Maven 依赖配置 | pom.xml 依赖片段 |

## Go 模板

| 模板文件 | 说明 | 生成目标文件 |
|---------|------|------------|
| [go-client.md](./go-client.md) | Nacos 客户端封装，含配置客户端+命名客户端 | nacos_client.go |
| [go-config-yml.md](./go-config-yml.md) | Go 项目配置文件 | config.yaml |

## Python 模板

| 模板文件 | 说明 | 生成目标文件 |
|---------|------|------------|
| [python-client.md](./python-client.md) | Nacos 客户端工具类，含注册/配置/监听 | nacos_client.py |
| [python-config-yml.md](./python-config-yml.md) | Python 项目配置文件 | config.yaml |
| [python-pip-deps.md](./python-pip-deps.md) | Pip 依赖配置 | requirements.txt 片段 |

---

## 通用规范

- 所有密码字段均使用 `${NACOS_PASSWORD}` 占位符，引导用户通过环境变量注入
- 模板中已内嵌 NACOS-001 ~ NACOS-005 最佳实践注释
- Go 和 Python 模板的密码获取逻辑：优先使用传入值 → 回退到环境变量 `NACOS_PASSWORD`
