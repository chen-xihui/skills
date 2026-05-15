# 场景 2：Redis 内存满

**症状**：Redis 报 OOM 或内存使用率接近 maxmemory

**诊断步骤**：
1. 执行 `paas-cli redis memory` 查看内存详情
2. 扁鹊诊断检查内存和淘汰策略

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 未设置过期时间 | 为 Key 设置合理的 TTL（REDIS-007） |
| 淘汰策略不合理 | 调整 maxmemory-policy（如 allkeys-lru） |
| 数据量增长 | 扩容或清理不再需要的数据 |
| 内存碎片率高 | 开启 activedefrag 或重启实例 |
