# Redis 集群交互操作详细说明

本文件包含 Redis 集群交互的 9 项操作详细说明。

---

## 通用前置条件

```bash
paas-cli --version
paas-cli ping
```

---

## 操作 1：查看集群状态

| 风险等级 | 🟢 低风险 |
|---------|----------|
| 需确认 | 否 |
| 命令 | `paas-cli redis info --project {project_id} --env {env}` |

```bash
paas-cli redis info --project j036x0 --env DEV
```

返回：集群模式、节点数量、运行状态、连接数等。

---

## 操作 2：查看节点信息

| 风险等级 | 🟢 低风险 |
|---------|----------|
| 需确认 | 否 |
| 命令 | `paas-cli redis nodes --project {project_id} --env {env}` |

```bash
paas-cli redis nodes --project j036x0 --env DEV
```

返回：各节点角色（Master/Slave）、地址、Slot 范围、连接状态。

---

## 操作 3：查看内存使用

| 风险等级 | 🟢 低风险 |
|---------|----------|
| 需确认 | 否 |
| 命令 | `paas-cli redis memory --project {project_id} --env {env}` |

```bash
paas-cli redis memory --project j036x0 --env DEV
```

返回：已用内存、最大内存、内存碎片率、淘汰策略。

---

## 操作 4：创建实例

| 风险等级 | 🟡 中风险 |
|---------|----------|
| 需确认 | 是 |
| 命令 | `paas-cli redis create --project {project_id} --env {env} --mode {mode}` |

### 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| mode | enum | 否 | standalone | standalone / sentinel / cluster |

```bash
paas-cli redis create --project j036x0 --env DEV --mode cluster
```

### 确认流程

```
即将执行以下操作：
  命令：paas-cli redis create --project j036x0 --env DEV --mode cluster
  说明：创建 Redis 集群模式实例
  影响：创建新的 Redis 实例，分配资源

是否继续执行？
```

---

## 操作 5：扩缩容

| 风险等级 | 🟡 中风险 |
|---------|----------|
| 需确认 | 是 |
| 命令 | `paas-cli redis scale --project {project_id} --env {env} --replicas {count}` |

### 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| count | int | 是 | 目标副本数（正整数） |

```bash
paas-cli redis scale --project j036x0 --env DEV --replicas 6
```

### 确认流程

```
即将执行以下操作：
  命令：paas-cli redis scale --project j036x0 --env DEV --replicas 6
  说明：将 Redis 集群副本数调整为 6
  影响：扩容时需等待新节点加入集群并完成 Slot 分配

是否继续执行？
```

---

## 操作 6：Slot 迁移

| 风险等级 | 🔴 高风险 |
|---------|----------|
| 需确认 | 是 |
| 命令 | `paas-cli redis slot-migrate --project {project_id} --env {env} --from {node} --to {node} --slots {range}` |

### 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| from | string | 是 | 源节点标识 |
| to | string | 是 | 目标节点标识 |
| slots | string | 是 | Slot 范围（如 0-1000 或 0,1,2） |

### 参数校验

- `from` / `to`：仅允许字母、数字、短横线、冒号、点号
- `slots`：数字和短横线、逗号组合

```bash
paas-cli redis slot-migrate --project j036x0 --env DEV --from redis-node-1 --to redis-node-4 --slots 0-5460
```

### 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli redis slot-migrate --project j036x0 --env DEV --from redis-node-1 --to redis-node-4 --slots 0-5460
  说明：将 Slot 0-5460 从 redis-node-1 迁移到 redis-node-4
  影响范围：
    - 迁移期间相关 Slot 的读写可能受影响
    - 迁移过程中源节点和目标节点负载增加
    - 如迁移中断，需要手动处理未完成的迁移状态

请输入"确认"以执行此操作：
```

### 注意事项
- 建议在业务低峰期执行
- 迁移前确认源节点和目标节点状态正常
- 迁移过程中避免对涉及的 Key 进行大批量操作

---

## 操作 7：内存策略调整

| 风险等级 | 🟡 中风险 |
|---------|----------|
| 需确认 | 是 |
| 命令 | `paas-cli redis config --project {project_id} --env {env} --maxmemory-policy {policy}` |

### 额外参数

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

### 确认流程

```
即将执行以下操作：
  命令：paas-cli redis config --project j036x0 --env DEV --maxmemory-policy allkeys-lru
  说明：将内存淘汰策略调整为 allkeys-lru
  影响：当内存满时，将从所有 Key 中淘汰最近最少使用的 Key

是否继续执行？
```

---

## 操作 8：升级版本

| 风险等级 | 🔴 高风险 |
|---------|----------|
| 需确认 | 是 |
| 命令 | `paas-cli redis upgrade --project {project_id} --env {env} --version {version}` |

```bash
paas-cli redis upgrade --project j036x0 --env DEV --version 7.2.0
```

### 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli redis upgrade --project j036x0 --env DEV --version 7.2.0
  说明：将 Redis 集群升级到版本 7.2.0
  影响范围：
    - 升级期间集群可能短暂不可用
    - 升级过程中节点逐个重启
    - 升级前请确保已备份数据
    - 跨大版本升级需先升级到最近的中间版本

请输入"确认"以执行此操作：
```

---

## 操作 9：删除集群

| 风险等级 | 🔴 高风险 |
|---------|----------|
| 需确认 | 是 |
| 命令 | `paas-cli redis delete --project {project_id} --env {env}` |

```bash
paas-cli redis delete --project j036x0 --env DEV
```

### 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli redis delete --project j036x0 --env DEV
  说明：删除 Redis 集群（DEV 环境，项目组 j036x0）
  影响范围：
    - 集群中所有数据将被永久删除，不可恢复
    - 所有依赖此集群的应用将无法访问
    - 此操作不可逆

请输入"确认"以执行此操作：
```
