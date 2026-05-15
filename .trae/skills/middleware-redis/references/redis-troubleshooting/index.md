# Redis 故障排查索引

本目录包含 Redis 故障排查的详细诊断流程、常见故障场景和扁鹊诊断命令。

**使用方式**：先在本索引中定位需要的诊断内容，再读取对应文件获取详细信息。

---

## 诊断流程与能力

| 内容 | 说明 | 详细文件 |
|------|------|---------|
| 诊断流程详解 | 5 步诊断完整流程和步骤说明 | [diagnostic-flow.md](./diagnostic-flow.md) |
| 诊断能力说明 | 慢查询、内存碎片、主从延迟、持久化、故障转移 | [diagnostic-capabilities.md](./diagnostic-capabilities.md) |
| 扁鹊诊断命令参考 | 完整诊断、单项诊断、返回格式 | [bianque-commands.md](./bianque-commands.md) |
| 降级诊断方案 | 扁鹊不可达时的 paas-cli 基本诊断 | [fallback-diagnosis.md](./fallback-diagnosis.md) |
| 诊断报告输出模板 | 故障诊断报告格式模板 | [report-template.md](./report-template.md) |

## 常见故障场景

| 场景 | 症状 | 详细文件 |
|------|------|---------|
| Redis 响应慢 | 读写延迟明显增加 | [scenario-01-slow-response.md](./scenario-01-slow-response.md) |
| Redis 内存满 | OOM 或内存使用率接近 maxmemory | [scenario-02-memory-full.md](./scenario-02-memory-full.md) |
| Redis 连接超时 | 客户端连接 Redis 超时 | [scenario-03-connection-timeout.md](./scenario-03-connection-timeout.md) |
| 主从数据不一致 | 从节点数据与主节点不一致 | [scenario-04-replication-lag.md](./scenario-04-replication-lag.md) |
