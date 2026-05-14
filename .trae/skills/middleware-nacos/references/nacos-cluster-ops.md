# Nacos 集群交互操作详细说明

本文件包含 Nacos 集群交互的 8 项操作详细说明。

---

## 通用前置条件

```bash
# 1. 检查 paas-cli 是否可用
paas-cli --version
# 2. 检查网络连通性
paas-cli ping
```

---

## 操作 1：查询集群信息

| 操作类型 | 查询集群信息 |
|---------|------------|
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli nacos info --project {project_id} --env {env}` |

```bash
paas-cli nacos info --project j036x0 --env DEV
```

### 返回信息
- 集群节点列表和状态
- Leader 节点信息
- Raft 一致性状态
- 配置数量

---

## 操作 2：查询服务注册实例

| 操作类型 | 查询服务注册实例 |
|---------|---------------|
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli nacos instances --project {project_id} --env {env} --service {service_name}` |

### 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| service_name | string | 是 | 服务名称（字母、数字、下划线、短横线） |

```bash
paas-cli nacos instances --project j036x0 --env DEV --service order-service
```

### 返回信息
- 实例 IP 和端口
- 健康状态
- 权重
- 集群名

---

## 操作 3：查询配置列表

| 操作类型 | 查询配置列表 |
|---------|------------|
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `paas-cli nacos config-list --project {project_id} --env {env}` |

```bash
paas-cli nacos config-list --project j036x0 --env DEV
```

### 返回信息
- 配置 Data ID 列表
- 所属 Group
- 最后修改时间

---

## 操作 4：创建服务

| 操作类型 | 创建服务 |
|---------|---------|
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli nacos create --project {project_id} --env {env} --service {service_name} --group {group}` |

### 额外参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| service_name | string | 是 | — | 服务名称 |
| group | string | 否 | DEFAULT_GROUP | 服务分组 |

```bash
paas-cli nacos create --project j036x0 --env DEV --service order-service --group DEFAULT_GROUP
```

### 确认流程

```
即将执行以下操作：
  命令：paas-cli nacos create --project j036x0 --env DEV --service order-service --group DEFAULT_GROUP
  说明：创建 Nacos 服务 order-service
  影响：新增服务注册条目

是否继续执行？
```

---

## 操作 5：扩缩容

| 操作类型 | 扩缩容 |
|---------|-------|
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli nacos scale --project {project_id} --env {env} --replicas {count}` |

### 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| count | int | 是 | 目标副本数（正整数） |

```bash
paas-cli nacos scale --project j036x0 --env DEV --replicas 3
```

### 确认流程

```
即将执行以下操作：
  命令：paas-cli nacos scale --project j036x0 --env DEV --replicas 3
  说明：将 Nacos 集群副本数调整为 3
  影响：扩容时需等待新节点加入集群；缩容时需迁移 Raft 角色

是否继续执行？
```

### 注意事项
- Nacos 集群建议奇数节点（1/3/5），确保 Raft 选举过半
- 缩容时需确保剩余节点数满足 Raft 多数派

---

## 操作 6：配置灰度发布

| 操作类型 | 配置灰度发布 |
|---------|-----------|
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `paas-cli nacos gray-publish --project {project_id} --env {env} --config {config_id}` |

### 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| config_id | string | 是 | 配置 ID（字母、数字、下划线、短横线、点号） |

```bash
paas-cli nacos gray-publish --project j036x0 --env DEV --config application.yml
```

### 确认流程

```
即将执行以下操作：
  命令：paas-cli nacos gray-publish --project j036x0 --env DEV --config application.yml
  说明：对配置 application.yml 执行灰度发布
  影响：灰度配置将推送到灰度规则的实例，不影响全量实例

是否继续执行？
```

---

## 操作 7：升级版本

| 操作类型 | 升级版本 |
|---------|---------|
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli nacos upgrade --project {project_id} --env {env} --version {version}` |

### 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| version | string | 是 | 目标版本号（语义化版本格式） |

```bash
paas-cli nacos upgrade --project j036x0 --env DEV --version 2.3.0
```

### 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli nacos upgrade --project j036x0 --env DEV --version 2.3.0
  说明：将 Nacos 集群升级到版本 2.3.0
  影响范围：
    - 升级期间集群可能短暂不可用
    - 升级过程中节点逐个重启
    - 升级前请确保已备份数据和配置
    - 跨大版本升级需遵循官方升级路径

请输入"确认"以执行此操作：
```

---

## 操作 8：删除服务

| 操作类型 | 删除服务 |
|---------|---------|
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli nacos delete --project {project_id} --env {env} --service {service_name}` |

### 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| service_name | string | 是 | 服务名称 |

```bash
paas-cli nacos delete --project j036x0 --env DEV --service order-service
```

### 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli nacos delete --project j036x0 --env DEV --service order-service
  说明：删除 Nacos 服务 order-service
  影响范围：
    - 该服务下的所有实例将被注销
    - 依赖此服务的调用方将无法发现实例
    - 此操作不可逆

请输入"确认"以执行此操作：
```
