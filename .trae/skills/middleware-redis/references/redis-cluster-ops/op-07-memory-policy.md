# 操作 7：内存策略调整

| 属性 | 说明 |
|------|------|
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli redis config --project {project_id} --env {env} --maxmemory-policy {policy}` |

## 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| policy | enum | 是 | 淘汰策略 |

**可选策略**：
- `noeviction`：不淘汰，内存满时拒绝写入（默认）
- `allkeys-lru`：从所有 Key 中淘汰最近最少使用的
- `volatile-lru`：从设了过期时间的 Key 中淘汰最近最少使用的
- `allkeys-lfu`：从所有 Key 中淘汰最不常用的
- `volatile-lfu`：从设了过期时间的 Key 中淘汰最不常用的
- `allkeys-random`：从所有 Key 中随机淘汰
- `volatile-random`：从设了过期时间的 Key 中随机淘汰
- `volatile-ttl`：从设了过期时间的 Key 中淘汰 TTL 最短的

```bash
paas-cli redis config --project j036x0 --env DEV --maxmemory-policy allkeys-lru
```

## 确认流程

```
即将执行以下操作：
  命令：paas-cli redis config --project j036x0 --env DEV --maxmemory-policy allkeys-lru
  说明：将内存淘汰策略调整为 allkeys-lru
  影响：当内存满时，将从所有 Key 中淘汰最近最少使用的 Key

是否继续执行？
```
