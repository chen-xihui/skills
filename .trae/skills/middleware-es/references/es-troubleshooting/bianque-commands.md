# 扁鹊诊断命令参考

## 完整诊断命令

```bash
bianque diagnose --middleware es --project {project_id} --env {env} --check cluster-health,shard,cpu,watermark
```

## 单项诊断命令

```bash
# 仅检查集群健康状态
bianque diagnose --middleware es --project {project_id} --env {env} --check cluster-health

# 仅检查分片状态
bianque diagnose --middleware es --project {project_id} --env {env} --check shard

# 仅检查 CPU 热点
bianque diagnose --middleware es --project {project_id} --env {env} --check cpu

# 仅检查磁盘水位线和写入拒绝
bianque diagnose --middleware es --project {project_id} --env {env} --check watermark
```

## 返回格式

扁鹊返回 JSON 格式，包含以下字段：

```json
{
  "status": "success|error",
  "findings": [
    {
      "type": "cluster-health|shard|cpu|watermark",
      "severity": "critical|warning|info",
      "message": "描述信息",
      "details": {}
    }
  ],
  "logs": ["相关日志条目"],
  "suggestions": ["处理建议"]
}
```
