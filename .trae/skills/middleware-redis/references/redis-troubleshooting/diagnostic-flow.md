# 诊断流程详解

## 完整流程

```
信息收集 → 集群状态检查 → 扁鹊诊断 → 补充信息收集 → 结果分析与建议
```

## 步骤详解

### 步骤 1：信息收集

- 记录用户描述的异常现象（symptom）
- 确认必要参数：`project_id`、`env`
- 常见现象分类：
  - 连接异常：连接超时、拒绝连接
  - 性能异常：响应慢、延迟高
  - 内存异常：OOM、内存满
  - 数据异常：数据丢失、主从不一致
  - 持久化异常：RDB/AOF 保存失败

### 步骤 2：集群状态检查

```bash
paas-cli redis info --project {project_id} --env {env}
```

关注信息：
- 集群模式（standalone/sentinel/cluster）
- 节点在线状态
- 连接数和阻塞客户端数
- 内存使用率和淘汰策略

### 步骤 3：扁鹊诊断

```bash
bianque diagnose --middleware redis --project {project_id} --env {env} --check slowlog,memory,replication
```

默认超时 60 秒，如不可达降级为仅 paas-cli。

### 步骤 4：补充信息收集

根据结果选择性执行：

```bash
# 查看内存详情
paas-cli redis memory --project {project_id} --env {env}

# 查看节点信息
paas-cli redis nodes --project {project_id} --env {env}
```

### 步骤 5：结果分析与建议

综合诊断数据生成处理建议，按优先级排序。
