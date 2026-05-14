# Nacos 故障排查详细指南

本文件包含 Nacos 故障排查的详细诊断流程、常见故障场景和扁鹊诊断命令。

---

## 1. 诊断流程详解

### 完整流程

```
信息收集 → 集群状态检查 → 扁鹊诊断 → 补充信息收集 → 结果分析与建议
```

### 步骤详解

#### 步骤 1：信息收集

- 记录用户描述的异常现象（symptom）
- 确认必要参数：`project_id`、`env`
- 常见现象分类：
  - 连接异常：连接超时、拒绝连接
  - 注册异常：服务注册不上、实例下线
  - 配置异常：配置不生效、配置获取失败
  - 性能异常：响应慢、CPU 高

#### 步骤 2：集群状态检查

```bash
paas-cli nacos info --project {project_id} --env {env}
```

关注信息：
- 节点在线数量
- Leader 节点状态
- Raft 一致性状态

#### 步骤 3：扁鹊诊断

```bash
bianque diagnose --middleware nacos --project {project_id} --env {env} --check health,raft,log
```

默认超时 60 秒，如不可达降级为仅 paas-cli。

#### 步骤 4：补充信息收集

根据结果选择性执行：

```bash
# 查询服务注册实例
paas-cli nacos instances --project {project_id} --env {env} --service {service_name}

# 查看配置列表
paas-cli nacos config-list --project {project_id} --env {env}
```

#### 步骤 5：结果分析与建议

综合诊断数据生成处理建议，按优先级排序。

---

## 2. 诊断能力详细说明

### 2.1 集群健康度

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware nacos --check health` |
| 检查内容 | 节点状态、Raft 一致性 |

### 2.2 日志分析

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware nacos --check log` |
| 检查内容 | 错误日志、异常堆栈 |

### 2.3 主备状态

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 + paas-cli |
| 检查命令 | `bianque diagnose --middleware nacos --check raft` |
| 检查内容 | Leader 选举状态、同步延迟 |

### 2.4 客户端连通性

| 项目 | 说明 |
|------|------|
| 数据来源 | 扁鹊 |
| 检查命令 | `bianque diagnose --middleware nacos --check health` |
| 检查内容 | 从客户端节点到 Nacos 的网络可达性 |

---

## 3. 常见故障场景与处理建议

### 场景 1：Nacos 连接超时

**症状**：客户端连接 Nacos 超时，服务注册/配置获取失败

**诊断步骤**：
1. 执行 `paas-cli nacos info` 确认集群状态
2. 扁鹊诊断检查网络连通性

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 网络策略变更 | 检查防火墙/安全组规则，开放 8848/9848 端口 |
| Nacos 服务端宕机 | 重启 Nacos 节点 |
| 客户端配置地址错误 | 核对 server-addr 配置 |
| DNS 解析失败 | 检查 DNS 配置或使用 IP 直连 |

### 场景 2：服务注册不上

**症状**：服务实例注册后立刻下线，或注册失败

**诊断步骤**：
1. 执行 `paas-cli nacos instances` 查看实例状态
2. 检查心跳配置是否合理

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 心跳超时 | 检查 heart-beat-interval 和 heart-beat-timeout 配置 |
| 命名空间不匹配 | 确认客户端和服务端 namespace 一致 |
| 权限不足 | 检查用户名密码是否正确 |
| 实例权重为 0 | 调整 weight > 0 |

### 场景 3：配置不生效

**症状**：修改了 Nacos 配置但应用未感知到变更

**诊断步骤**：
1. 执行 `paas-cli nacos config-list` 确认配置存在
2. 检查客户端是否使用了 Listener 监听

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 未使用 Listener | 改用 Listener 监听配置变更（NACOS-003） |
| Data ID / Group 不匹配 | 确认客户端和服务端配置一致 |
| refresh-enabled 未开启 | 设置 spring.cloud.nacos.config.refresh-enabled=true |
| 配置格式不匹配 | 确认 file-extension 与实际格式一致 |

### 场景 4：Raft 选举异常

**症状**：集群 Leader 频繁切换，服务注册不稳定

**诊断步骤**：
1. 执行 `paas-cli nacos info` 查看 Leader 状态
2. 扁鹊诊断检查 Raft 状态

**常见原因与处理**：

| 原因 | 处理建议 |
|------|---------|
| 网络分区 | 检查节点间网络连通性 |
| 节点负载不均 | 检查 CPU/内存/磁盘使用率 |
| 节点数不足 | 确保 3 个以上节点，奇数个 |
| 磁盘写入延迟 | 检查磁盘 I/O 性能 |

---

## 4. 扁鹊诊断命令参考

### 4.1 完整诊断命令

```bash
bianque diagnose --middleware nacos --project {project_id} --env {env} --check health,raft,log
```

### 4.2 单项诊断

```bash
# 仅检查集群健康状态
bianque diagnose --middleware nacos --project {project_id} --env {env} --check health

# 仅检查 Raft 状态
bianque diagnose --middleware nacos --project {project_id} --env {env} --check raft

# 仅检查日志
bianque diagnose --middleware nacos --project {project_id} --env {env} --check log
```

### 4.3 返回格式

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

---

## 5. 降级诊断方案

扁鹊不可达时，使用 paas-cli 基本诊断：

```bash
# 1. 查看集群信息
paas-cli nacos info --project {project_id} --env {env}

# 2. 查询服务实例
paas-cli nacos instances --project {project_id} --env {env} --service {service_name}

# 3. 查看配置列表
paas-cli nacos config-list --project {project_id} --env {env}
```

**降级局限**：无法获取 Raft 详细状态、日志分析和客户端连通性检查。建议在报告中注明降级。

---

## 6. 诊断报告输出模板

```
🔍 故障诊断报告

🩺 诊断目标：Nacos / {env} / {project_id}
📡 诊断来源：扁鹊平台 / paas-cli{如降级则注明"（降级模式）"}

📊 诊断结论：{一句话结论}

📋 详细发现：
  1. {发现1}
  2. {发现2}

💡 处理建议：
  1. {建议1}（优先级：高）
  2. {建议2}（优先级：中）

📎 相关日志/数据：
{诊断脚本返回的关键数据摘要}
```
