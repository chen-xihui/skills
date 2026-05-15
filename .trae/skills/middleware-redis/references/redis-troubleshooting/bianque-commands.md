# 扁鹊诊断命令参考

## 完整诊断命令

```bash
bianque diagnose --middleware redis --project {project_id} --env {env} --check slowlog,memory,replication
```

## 单项诊断

```bash
# 仅检查慢查询
bianque diagnose --middleware redis --project {project_id} --env {env} --check slowlog

# 仅检查内存
bianque diagnose --middleware redis --project {project_id} --env {env} --check memory

# 仅检查主从复制
bianque diagnose --middleware redis --project {project_id} --env {env} --check replication
```

## 返回格式

```json
{
  "status": "success|error",
  "findings": [
    {
      "type": "slowlog|memory|replication",
      "severity": "critical|warning|info",
      "message": "描述信息",
      "details": {}
    }
  ],
  "logs": ["相关日志条目"],
  "suggestions": ["处理建议"]
}
```
