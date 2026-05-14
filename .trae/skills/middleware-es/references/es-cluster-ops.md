# ES 集群交互操作详细说明

本文件包含 ES 集群交互的 9 项操作详细说明、额外参数、命令模板和注意事项，供智能体在执行集群操作时参考。

---

## 通用前置条件

执行任何集群操作前，必须完成以下前置检查：

```bash
# 1. 检查 paas-cli 是否可用
paas-cli --version
# 失败 → 提示用户安装 paas-cli

# 2. 检查网络连通性
paas-cli ping
# 失败 → 提示用户检查网络连接
```

---

## 操作 1：查看集群状态

| 属性 | 说明 |
|------|------|
| 操作类型 | 查看集群状态 |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令模板 | `paas-cli es info --project {project_id} --env {env}` |

### 额外参数

无需额外参数。

### 命令示例

```bash
paas-cli es info --project j036x0 --env DEV
```

### 返回信息

- 集群名称和 UUID
- 集群状态（Green / Yellow / Red）
- 节点数量和数据节点数量
- 分片统计（主分片、副本分片、未分配分片）
- 集群版本

### 注意事项

- 这是只读操作，可直接执行
- 如集群状态为 Red 或 Yellow，建议进一步执行索引状态查询和故障排查

---

## 操作 2：查看节点磁盘使用率

| 属性 | 说明 |
|------|------|
| 操作类型 | 查看节点磁盘使用率 |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令模板 | `paas-cli es disk-usage --project {project_id} --env {env}` |

### 额外参数

无需额外参数。

### 命令示例

```bash
paas-cli es disk-usage --project j036x0 --env DEV
```

### 返回信息

- 各节点磁盘使用率
- 磁盘水位线状态（正常 / 接近水位线 / 超过水位线）
- 磁盘总量和可用空间

### 注意事项

- 这是只读操作，可直接执行
- 当节点磁盘使用率超过 85% 时需要注意，超过 90% 可能触发只读模式
- 磁盘水位线阈值：
  - `cluster.routing.allocation.disk.watermark.low`：默认 85%，不分配新分片
  - `cluster.routing.allocation.disk.watermark.high`：默认 90%，开始迁移分片
  - `cluster.routing.allocation.disk.watermark.flood_stage`：默认 95%，索引设为只读

---

## 操作 3：查看索引状态

| 属性 | 说明 |
|------|------|
| 操作类型 | 查看索引状态 |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令模板 | `paas-cli es indices --project {project_id} --env {env}` |

### 额外参数

无需额外参数。

### 命令示例

```bash
paas-cli es indices --project j036x0 --env DEV
```

### 返回信息

- 索引列表
- 各索引的健康状态
- 主分片和副本分片数量
- 文档数量和存储大小

### 注意事项

- 这是只读操作，可直接执行
- 如发现索引状态为 Red，建议进一步排查未分配分片原因

---

## 操作 4：创建索引

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建索引 |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令模板 | `paas-cli es create-index --project {project_id} --env {env} --name {index_name} --shards {n} --replicas {n}` |

### 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| index_name | string | 是 | — | 索引名称（小写字母、数字、短横线） |
| shards | int | 否 | 1 | 主分片数 |
| replicas | int | 否 | 1 | 副本分片数 |

### 参数校验

- `index_name`：必须符合 ES 索引命名规范（小写字母开头，仅含小写字母、数字、短横线、下划线），不含 shell 元字符
- `shards`：正整数，建议根据数据量和节点数设置（一般 1-10）
- `replicas`：非负整数，生产环境建议 ≥ 1

### 命令示例

```bash
paas-cli es create-index --project j036x0 --env DEV --name log-2026-05 --shards 3 --replicas 1
```

### 确认流程

向用户展示：
```
即将执行以下操作：
  命令：paas-cli es create-index --project j036x0 --env DEV --name log-2026-05 --shards 3 --replicas 1
  说明：创建索引 log-2026-05，3 个主分片，1 个副本
  影响：新增索引，不会影响现有数据

是否继续执行？
```

### 注意事项

- 主分片数创建后不可修改，请根据数据量合理设置
- 副本分片数可后续动态调整
- 建议创建时显式定义 mapping，避免 dynamic mapping 导致类型混乱

---

## 操作 5：索引滚动

| 属性 | 说明 |
|------|------|
| 操作类型 | 索引滚动（Rollover） |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令模板 | `paas-cli es rollover --project {project_id} --env {env} --alias {alias}` |

### 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| alias | string | 是 | — | 索引别名（字母、数字、短横线、下划线） |

### 参数校验

- `alias`：仅允许字母、数字、短横线、下划线，不含 shell 元字符

### 命令示例

```bash
paas-cli es rollover --project j036x0 --env DEV --alias logs-write
```

### 确认流程

向用户展示：
```
即将执行以下操作：
  命令：paas-cli es rollover --project j036x0 --env DEV --alias logs-write
  说明：对别名 logs-write 执行滚动操作
  影响：如果当前索引满足滚动条件，将创建新索引并将别名指向新索引

是否继续执行？
```

### 注意事项

- 滚动操作基于别名的 is_write_index 条件
- 滚动条件可在索引模板中预定义（如文档数、大小、时间）
- 滚动后别名自动指向新索引，应用代码无需修改

---

## 操作 6：Force Merge

| 属性 | 说明 |
|------|------|
| 操作类型 | Force Merge（强制段合并） |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令模板 | `paas-cli es force-merge --project {project_id} --env {env} --index {index_name} --max-segments {n}` |

### 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| index_name | string | 是 | — | 索引名称 |
| max-segments | int | 否 | 1 | 目标段数量 |

### 参数校验

- `index_name`：符合 ES 索引命名规范，不含 shell 元字符
- `max-segments`：正整数，通常设为 1（完全合并）

### 命令示例

```bash
paas-cli es force-merge --project j036x0 --env DEV --index log-2026-04 --max-segments 1
```

### 确认流程

向用户展示：
```
即将执行以下操作：
  命令：paas-cli es force-merge --project j036x0 --env DEV --index log-2026-04 --max-segments 1
  说明：对索引 log-2026-04 执行强制段合并，目标段数 1
  影响：Force Merge 会消耗大量 I/O 和 CPU 资源，建议仅在只读索引上执行
  ⚠️ 警告：对读写中的索引执行 Force Merge 可能导致性能严重下降

是否继续执行？
```

### 注意事项

- **强烈建议只在只读索引上执行 Force Merge**
- 对活跃索引执行 Force Merge 可能产生更大的段，适得其反
- Force Merge 会消耗大量 I/O 和 CPU，建议在业务低峰期执行
- 合并完成后索引存储空间会减少，查询性能可能提升

---

## 操作 7：扩缩容

| 属性 | 说明 |
|------|------|
| 操作类型 | 扩缩容 |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令模板 | `paas-cli es scale --project {project_id} --env {env} --nodes {count}` |

### 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| nodes | int | 是 | — | 目标节点数量（正整数） |

### 参数校验

- `nodes`：正整数，建议根据数据量和负载合理设置

### 命令示例

```bash
paas-cli es scale --project j036x0 --env DEV --nodes 5
```

### 确认流程

向用户展示：
```
即将执行以下操作：
  命令：paas-cli es scale --project j036x0 --env DEV --nodes 5
  说明：将 ES 集群节点数调整为 5
  影响：扩容时需等待新节点加入集群并完成分片分配；缩容时需先迁移分片

是否继续执行？
```

### 注意事项

- 扩容时新节点加入集群后，分片会自动重新分配（rebalance）
- 缩容时需确保节点上的分片能迁移到其他节点
- 建议逐步扩缩容（每次 1-2 个节点），观察集群状态
- 扩缩容期间集群性能可能受影响

---

## 操作 8：升级版本

| 属性 | 说明 |
|------|------|
| 操作类型 | 升级版本 |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令模板 | `paas-cli es upgrade --project {project_id} --env {env} --version {version}` |

### 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| version | string | 是 | — | 目标版本号（语义化版本格式，如 8.12.0） |

### 参数校验

- `version`：必须符合语义化版本号格式（如 `8.12.0`、`7.17.15`），不含 shell 元字符

### 命令示例

```bash
paas-cli es upgrade --project j036x0 --env DEV --version 8.12.0
```

### 确认流程

向用户展示：
```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli es upgrade --project j036x0 --env DEV --version 8.12.0
  说明：将 ES 集群升级到版本 8.12.0
  影响范围：
    - 升级期间集群可能短暂不可用
    - 升级过程中部分节点需要重启
    - 跨大版本升级（如 7.x → 8.x）需要先升级到 7.17.x
    - 升级前请确保已备份数据
    - 升级后客户端代码可能需要适配新 API

请输入"确认"以执行此操作：
```

### 注意事项

- **升级前必须备份数据**
- 建议在 DEV 环境先验证升级流程
- 跨大版本升级需遵循 ES 官方升级路径
- 升级期间建议停止写入操作
- 升级后验证集群状态和数据完整性

---

## 操作 9：删除集群

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除集群 |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令模板 | `paas-cli es delete --project {project_id} --env {env}` |

### 额外参数

无需额外参数。

### 命令示例

```bash
paas-cli es delete --project j036x0 --env DEV
```

### 确认流程

向用户展示：
```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli es delete --project j036x0 --env DEV
  说明：删除 ES 集群（DEV 环境，项目组 j036x0）
  影响范围：
    - 集群中所有索引和数据将被永久删除，不可恢复
    - 所有依赖此集群的应用将无法访问
    - 此操作不可逆

请输入"确认"以执行此操作：
```

### 注意事项

- **此操作不可逆，删除后数据无法恢复**
- 删除前务必确认数据已备份或不再需要
- 删除前建议先检查集群中是否有重要索引
- 确认影响范围后才能执行
