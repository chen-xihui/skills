# Nacos 故障排查索引

本目录包含 Nacos 故障排查的详细诊断流程、常见故障场景和扁鹊诊断命令。

**使用方式**：先在本索引中定位需要的诊断内容，再读取对应文件获取详细信息。

---

## 诊断流程与能力

| 内容 | 说明 | 详细文件 |
|------|------|---------|
| 诊断流程详解 | 5 步诊断完整流程和步骤说明 | [diagnostic-flow.md](./diagnostic-flow.md) |
| 诊断能力说明 | 集群健康度、日志分析、主备状态、客户端连通性 | [diagnostic-capabilities.md](./diagnostic-capabilities.md) |
| 扁鹊诊断命令参考 | 完整诊断、单项诊断、返回格式 | [bianque-commands.md](./bianque-commands.md) |
| 降级诊断方案 | 扁鹊不可达时的 paas-cli 基本诊断 | [fallback-diagnosis.md](./fallback-diagnosis.md) |
| 诊断报告输出模板 | 故障诊断报告格式模板 | [report-template.md](./report-template.md) |

## 常见故障场景

| 场景 | 症状 | 详细文件 |
|------|------|---------|
| Nacos 连接超时 | 客户端连接超时，服务注册/配置获取失败 | [scenario-01-connection-timeout.md](./scenario-01-connection-timeout.md) |
| 服务注册不上 | 服务实例注册后立刻下线，或注册失败 | [scenario-02-registration-failure.md](./scenario-02-registration-failure.md) |
| 配置不生效 | 修改了 Nacos 配置但应用未感知到变更 | [scenario-03-config-not-effective.md](./scenario-03-config-not-effective.md) |
| Raft 选举异常 | 集群 Leader 频繁切换，服务注册不稳定 | [scenario-04-raft-election-error.md](./scenario-04-raft-election-error.md) |
