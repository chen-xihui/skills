# ES 故障排查索引

本目录包含 Elasticsearch 故障排查的详细诊断流程、诊断能力说明、常见故障场景和扁鹊诊断命令。智能体执行故障排查时，先查阅本索引了解诊断流程和场景映射，再按需加载具体文件。

## 诊断流程

> 完整诊断流程详见 [diagnostic-flow.md](diagnostic-flow.md)

```
信息收集 → 集群状态检查 → 扁鹊诊断 → 补充信息收集 → 结果分析与建议
```

## 诊断能力

> 5 项诊断能力详见 [diagnostic-capabilities.md](diagnostic-capabilities.md)

| 诊断项 | 检查内容 | 数据来源 |
|--------|---------|---------|
| 集群健康状态 | Red / Yellow / Green 及原因 | 扁鹊 + paas-cli |
| 未分配分片 | UNASSIGNED 分片及分配失败原因 | 扁鹊 |
| CPU 热点 | 节点 CPU 使用率及热线程 | 扁鹊 |
| 写入拒绝 | 磁盘水位线、线程池队列拒绝 | 扁鹊 |
| 索引健康 | 副本分片状态、段合并情况 | 扁鹊 |

## 常见故障场景

| 场景 | 症状 | 详细文件 |
|------|------|---------|
| 场景 1 | 集群状态 Red，部分索引不可用 | [scenario-01-cluster-red.md](scenario-01-cluster-red.md) |
| 场景 2 | ES 查询响应时间明显变长 | [scenario-02-slow-query.md](scenario-02-slow-query.md) |
| 场景 3 | 写入请求被拒绝或超时 | [scenario-03-write-rejection.md](scenario-03-write-rejection.md) |
| 场景 4 | 集群状态 Yellow，部分副本未分配 | [scenario-04-cluster-yellow.md](scenario-04-cluster-yellow.md) |

## 扁鹊诊断命令

> 完整命令参考详见 [bianque-commands.md](bianque-commands.md)

```bash
bianque diagnose --middleware es --project {project_id} --env {env} --check cluster-health,shard,cpu,watermark
```

## 降级方案

> 扁鹊不可达时的降级方案详见 [fallback-diagnosis.md](fallback-diagnosis.md)

当扁鹊不可达时，使用 paas-cli 进行基本诊断（es info / es indices / es disk-usage）。

## 报告模板

> 诊断报告输出格式详见 [report-template.md](report-template.md)
