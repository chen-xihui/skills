# 降级诊断方案

扁鹊不可达时，使用 paas-cli 基本诊断：

```bash
# 1. 查看集群状态
paas-cli redis info --project {project_id} --env {env}

# 2. 查看节点信息
paas-cli redis nodes --project {project_id} --env {env}

# 3. 查看内存使用
paas-cli redis memory --project {project_id} --env {env}
```

**降级局限**：无法获取慢查询详情、内存碎片率分析、主从延迟详情和故障转移日志。建议在报告中注明降级。
