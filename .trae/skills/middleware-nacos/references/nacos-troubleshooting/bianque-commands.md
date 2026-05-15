# 扁鹊诊断命令参考

## 完整诊断命令

```bash
bianque diagnose --middleware nacos --project {project_id} --env {env} --check health,raft,log
```

## 单项诊断

```bash
# 仅检查集群健康状态
bianque diagnose --middleware nacos --project {project_id} --env {env} --check health

# 仅检查 Raft 状态
bianque diagnose --middleware nacos --project {project_id} --env {env} --check raft

# 仅检查日志
bianque diagnose --middleware nacos --project {project_id} --env {env} --check log
```

## 返回格式

```json
{
  "status": "success|error",
  "findings": [
    {
      "type": "health|raft|log",
      "severity": "critical|warning|info",
      "message": "描述信息",
      "details": {}
    }
  ],
  "logs": ["相关日志条目"],
  "suggestions": ["处理建议"]
}
```
