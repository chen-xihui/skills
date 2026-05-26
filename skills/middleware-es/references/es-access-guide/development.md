# 开发指引

## 4.1 服务端版本要求

应符合开源技术目录的 ES 服务端版本使用：

| 版本 | 说明 |
|------|------|
| 7.17+ | 根据最新开源技术目录选择 ES 服务端版本 |
| 8.12+ | 根据最新开源技术目录选择 ES 服务端版本 |

## 4.2 客户端版本要求

推荐使用 `co.elastic.client:elasticsearch-java` 客户端，客户端版本需选择和服务端版本一致：

| 客户端类型 | 版本要求 | 说明 |
|-----------|---------|------|
| elasticsearch-java | 与服务端版本保持一致 | ES 7 推荐使用 7.17+ 版本 |
| elasticsearch-java | 与服务端版本保持一致 | ES 8 推荐使用 8.12+ 版本 |

**Spring Boot 兼容性**：
- Spring Boot 3.x 对应 Spring Data Elasticsearch 5.x，支持 ES 8.x
- Spring Boot 2.x 对应 Spring Data Elasticsearch 4.x，支持 ES 7.x

## 4.3 服务端关键配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| JVM 配置 | 根据服务资源动态配置 | Xms=Xmx=最大内存/2, MaxDirectMemorySize=最大内存/4 |
| cluster.routing.allocation.enable | all | 自动分片分配策略所有分片开启 |
| bootstrap.memory_lock | false | 开启后启动时锁定内存 |
| index.number_of_shards | 1 | 索引创建默认分片数 |
| index.number_of_replicas | 1 | 索引创建默认副本数 |
| index.refresh_interval | 1s | 索引创建默认刷新时间 |

## 4.4 客户端关键配置参数

| 参数 | 默认值 | 配置建议 |
|------|--------|---------|
| maxConnTotal | 10 | 不建议使用默认值；建议根据并发度及性能测试配置为 50~200 |
| maxConnPerRoute | 10 | 不建议使用默认值；建议配置为 maxConnTotal/2 |
| connectTimeout | 1000ms | 根据业务需求确认 |
| socketTimeout | 30000ms | 根据业务需求确认；写多读少场景可调整为 60000ms |
| maxRetryTimeoutMillis | 30000ms | 配置为 socketTimeout 一致 |
| CompressionEnabled | false | 大批量写入或大文档时开启 |

## 4.5 安全编码

- **强制认证**：应开启客户端认证，根据密码规范配置接入密码
- **禁止无认证**：禁止使用无认证的 ES 服务

## 4.6 容错开发

**健康检查**
- 推荐在设计健康检查接口时，从客户端侧增加 ES 服务的可观测指标
- 根据对 ES 服务的依赖程度，设计 ES 检查接口（Info 定时检查），并加入应用健康检查接口
- 将该接口增加至可观测采集，并增加告警
- 应用启动禁止强依赖 ES 服务，健康探测接口异常时不应触发应用自动重启

**异常处置**

| 措施 | 说明 |
|------|------|
| 服务重试 | 接口配置自动重试，应对网络抖动等场景 |
| 服务降级 | 合理设计服务降级，超过重试次数后通过指数回避，降级访问接口 |
| 服务熔断 | 合理配置失败率，防止 ES 调用异常导致线程池耗尽，避免级联故障 |
| 错误处理 | 合理捕获异常，根据错误类型打印关键日志 |

**核心交易接口要求**
- 交易接口禁止强依赖 ES 服务
- 使用 ES 接口时应考虑应用层重试、服务降级和熔断