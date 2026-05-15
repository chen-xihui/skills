# 降级诊断方案

扁鹊不可达时，使用 paas-cli 基本诊断：

```bash
# 1. 查看集群信息
paas-cli nacos info --project {project_id} --env {env}

# 2. 查询服务实例
paas-cli nacos instances --project {project_id} --env {env} --service {service_name}

# 3. 查看配置列表
paas-cli nacos config-list --project {project_id} --env {env}
```

**降级局限**：无法获取 Raft 详细状态、日志分析和客户端连通性检查。建议在报告中注明降级。
