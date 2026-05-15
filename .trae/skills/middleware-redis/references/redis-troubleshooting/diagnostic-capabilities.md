# 诊断能力详细说明

## 2.1 慢查询分析

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware redis --check slowlog` |
| 检查内容 | slowlog 中的高频慢命令 |

**关注指标**：
- 慢查询数量和频率
- 最耗时的命令类型（如 `KEYS`、`SORT`、`HGETALL` 大 Hash）
- 慢查询的 Key 模式

## 2.2 内存碎片率

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 + paas-cli |
| 检查命令 | `bianque diagnose --middleware redis --check memory` |
| 检查内容 | mem_fragmentation_ratio |

**关注指标**：
- 碎片率 < 1.0：Redis 使用了超出分配的内存（使用了 swap）
- 碎片率 1.0-1.5：正常
- 碎片率 > 1.5：内存碎片较多，可考虑重启或开启 activedefrag

## 2.3 主从延迟

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware redis --check replication` |
| 检查内容 | replication offset 差异 |

**关注指标**：
- 主从 offset 差异大 → 同步延迟
- 从节点断开连接 → 网络问题或负载高
- 主从切换频率 → 不稳定

## 2.4 持久化状态

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware redis --check replication`（含持久化检查） |
| 检查内容 | RDB/AOF 最后保存时间及状态 |

**关注指标**：
- RDB 最后保存时间距当前过久 → 持久化可能失败
- AOF fsync 延迟 → 磁盘 I/O 瓶颈
- AOF 重写是否正常执行

## 2.5 故障转移

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware redis --check replication` |
| 检查内容 | Sentinel 选举记录、Failover 日志 |

**关注指标**：
- 近期是否发生故障转移
- 故障转移耗时
- 新主节点是否正常
