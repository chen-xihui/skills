# Redis 常见故障场景与处理建议

## 场景 1：Redis 响应慢

**症状**：Redis 读写延迟明显增加

**诊断步骤**：
1. 经 paas-cli Skill 执行 `$PAAS_CLI redis info` 查看基本状态
2. 扁鹊诊断检查 slowlog 和 CPU

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 慢命令（keys *、sort 等） | 优化代码，使用 scan 替代 keys |
| 大 Key 操作 | 拆分大 Key，使用 hscan/sscan/zscan |
| 内存满触发淘汰 | 扩容或优化缓存策略 |
| 网络延迟 | 检查网络连通性和带宽 |
| 持久化阻塞 | 检查 RDB/AOF 配置，考虑调整 fsync 策略 |
| 连接数过多 | 检查连接池配置，排除连接泄漏 |

## 场景 2：Redis 内存满

**症状**：Redis 报 OOM 或内存使用率接近 maxmemory

**诊断步骤**：
1. 经 paas-cli Skill 执行 `$PAAS_CLI redis memory` 查看内存详情
2. 扁鹊诊断检查内存和淘汰策略

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 未设置过期时间 | 为 Key 设置合理的 TTL（REDIS-007） |
| 淘汰策略不合理 | 调整 maxmemory-policy（如 allkeys-lru） |
| 数据量增长 | 扩容或清理不再需要的数据 |
| 内存碎片率高 | 开启 activedefrag 或重启实例 |

## 场景 3：Redis 连接超时

**症状**：客户端连接 Redis 超时

**诊断步骤**：
1. 经 paas-cli Skill 执行 `$PAAS_CLI redis info` 查看连接数
2. 扁鹊诊断检查网络

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 连接数达上限 | 增加 maxclients 或优化连接池 |
| 网络不通 | 检查防火墙和安全组规则 |
| Redis 阻塞 | 检查是否有慢命令阻塞（如 keys *） |
| 客户端连接池配置不合理 | 调整 maxTotal/maxIdle（REDIS-004） |

## 场景 4：主从数据不一致

**症状**：从节点数据与主节点不一致

**诊断步骤**：
1. 经 paas-cli Skill 执行 `$PAAS_CLI redis nodes` 查看主从状态
2. 扁鹊诊断检查 replication

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 网络延迟导致同步慢 | 检查主从节点间网络 |
| 主节点写入量过大 | 考虑分片或读写分离 |
| 从节点断开后重连 | 等待全量同步完成 |
| 从节点只读配置异常 | 确认从节点为只读模式 |

## 场景 5：Redis 服务租期过期

**症状**：应用启动或运行时无法连接 Redis 服务，报连接超时、拒绝连接或认证失败

**诊断步骤**：
1. 经 paas-cli Skill 执行 `$PAAS_CLI redis lease status --project {project_id} --env {env}` 检查租期状态
2. 如租期已过期，这是连接失败的根本原因

**常见原因与处理**：

| 原因 | 处理建议 |
|------|----------|
| 服务租期已过期 | 经 paas-cli Skill 执行 `$PAAS_CLI redis lease renew --project {project_id} --env {env} --duration 3` 续期（默认 3 个月） |
| 租期即将过期 | 提前续期，避免服务中断 |
| 续期后仍无法连接 | 确认续期生效后重启应用，检查网络连通性 |

**完整处理流程**：
1. 检查租期状态：`$PAAS_CLI redis lease status --project {project_id} --env {env}`
2. 确认租期过期后，向用户交互确认续期时长（默认 3 个月）
3. 执行续期：`$PAAS_CLI redis lease renew --project {project_id} --env {env} --duration {months}`
4. 续期成功后重启应用，验证连接恢复正常