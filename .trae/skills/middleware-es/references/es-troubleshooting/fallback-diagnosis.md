# 降级诊断方案

当扁鹊平台不可达时，使用以下 paas-cli 命令进行基本诊断：

```bash
# 1. 查看集群基本信息
paas-cli es info --project {project_id} --env {env}

# 2. 查看索引状态
paas-cli es indices --project {project_id} --env {env}

# 3. 查看磁盘使用率
paas-cli es disk-usage --project {project_id} --env {env}
```

**降级诊断的局限**：
- 无法获取 CPU 热点和热线程信息
- 无法获取详细的分片分配失败原因
- 无法获取线程池队列拒绝情况
- 建议在报告中注明"本次诊断因扁鹊不可达而降级，部分检查项未能覆盖"
