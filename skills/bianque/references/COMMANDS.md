# bianque 命令参考

> Mock 诊断 CLI。可执行文件：`skills/bianque/bianque.py`。工具 Skill 见 [../SKILL.md](../SKILL.md)。

---

## 二、bianque

中间件诊断平台 CLI 工具（mock 版本）。

### 2.1 全局参数

所有 `bianque` 命令都支持全局参数：

| 参数 | 说明 |
|------|------|
| `--token-file <path>` | 指定权限验证脚本文件路径（包含 API 地址和 Token） |

### 2.2 Elasticsearch 命令

#### check 命令

**功能**：检查 Elasticsearch 集群状态、日志错误信息

```bash
bianque elasticsearch check -n <namespace> -i <instance> [-v] [-o <num>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | ES 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | ES 实例名称 |
| `--verb` | `-v` | 否 | 是否展示详情（true/false） |
| `--log-lines` | `-o` | 否 | Pod 和 Operator 错误日志输出行数（默认 0） |

**示例：**

```bash
# 检查 ES 集群状态
bianque elasticsearch check -n myns -i myes

# 检查 ES 集群并显示详细信息
bianque elasticsearch check -n myns -i myes -v

# 指定错误日志输出行数
bianque elasticsearch check -n myns -i myes -o 50
```

#### client 命令

**功能**：创建 Elasticsearch 客户端并执行读写操作

```bash
bianque elasticsearch client -n <namespace> -i <instance> -k <key> -v <value> [-u <user>] [-p <password>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | ES 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | ES 实例名称 |
| `--key` | `-k` | 是 | 要写入的 key |
| `--value` | `-v` | 是 | 要写入的 value |
| `--user` | `-u` | 否 | 验证的用户名（默认 elastic） |
| `--password` | `-p` | 否 | 验证的密码（不填则自动获取） |

**示例：**

```bash
# 连接 ES 实例并写入测试数据
bianque elasticsearch client -n myns -i myes -k testkey -v testval

# 带认证信息连接
bianque elasticsearch client -n myns -i myes -k testkey -v testval -u myuser -p mypassword
```

### 2.3 Nacos 命令

#### check 命令

**功能**：检查 Nacos 实例的连接状态和配置

```bash
bianque nacos check -n <namespace> -i <instance> [-v] [-l <num>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Nacos 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Nacos 实例名称 |
| `--verb` | `-v` | 否 | 是否展示详情（true/false） |
| `--log-lines` | `-l` | 否 | 日志检查的行数（默认 1000） |

**示例：**

```bash
# 检查 Nacos 实例连接状态
bianque nacos check -n myns -i mynacos

# 检查 Nacos 并显示详细信息
bianque nacos check -n myns -i mynacos -v

# 指定日志检查行数
bianque nacos check -n myns -i mynacos -l 2000
```

#### client 命令

**功能**：创建 Nacos 客户端并执行操作

```bash
bianque nacos client -n <namespace> -i <instance> [-u <user>] [-p <password>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Nacos 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Nacos 实例名称 |
| `--user` | `-u` | 否 | 验证的用户名（默认 admin） |
| `--password` | `-p` | 否 | 验证的密码（不填则自动获取） |

**示例：**

```bash
# 连接 Nacos 实例
bianque nacos client -n myns -i mynacos

# 带认证信息连接
bianque nacos client -n myns -i mynacos -u myuser -p mypassword
```

### 2.4 Redis 命令

#### check 命令

**功能**：检查 Redis 实例的连接状态和配置

```bash
bianque redis check -n <namespace> -i <instance> -t <type> [-v] [-l <num>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Redis 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Redis 实例名称 |
| `--type` | `-t` | 是 | Redis 类型：cluster / sentinel |
| `--verb` | `-v` | 否 | 是否展示详情（true/false） |
| `--log-lines` | `-l` | 否 | 日志检查的行数（默认 1000） |

**示例：**

```bash
# 检查 sentinel 模式的 Redis 实例
bianque redis check -n myns -i myredis -t sentinel

# 检查 cluster 模式并显示详细信息
bianque redis check -n myns -i myredis -t cluster -v

# 指定日志检查行数
bianque redis check -n myns -i myredis -t sentinel -l 2000
```

#### client 命令

**功能**：创建 Redis 客户端并执行读写操作

```bash
bianque redis client -n <namespace> -i <instance> -t <type> [-a <password>]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Redis 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Redis 实例名称 |
| `--type` | `-t` | 是 | Redis 类型：cluster / sentinel |
| `--auth` | `-a` | 否 | Redis 密码（不填则自动获取） |

**示例：**

```bash
# 连接 sentinel 模式的 Redis 实例
bianque redis client -n myns -i myredis -t sentinel

# 带认证信息连接 cluster 模式
bianque redis client -n myns -i myredis -t cluster -a "mypassword"
```

#### updateRenameConfig 命令

**功能**：更新 Redis 实例的重命名配置（rename-command）

```bash
bianque redis updateRenameConfig -n <namespace> -i <instance> -t <type> [-a]
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Redis 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Redis 实例名称 |
| `--type` | `-t` | 是 | Redis 类型：cluster / sentinel |
| `--all-namespaces` | `-a` | 否 | 是否应用到所有命名空间 |

**示例：**

```bash
# 更新单个 sentinel 模式实例的重命名配置
bianque redis updateRenameConfig -n myns -i myredis -t sentinel

# 更新所有命名空间的 cluster 模式实例配置
bianque redis updateRenameConfig -n myns -i myredis -t cluster -a
```

#### clusterUpgradeRecover 命令

**功能**：恢复 Redis 集群升级操作

```bash
bianque redis clusterUpgradeRecover -n <namespace> -i <instance> -o <operation> -t <type>
```

| 参数 | 短参数 | 必填 | 说明 |
|------|--------|------|------|
| `--namespace` | `-n` | 是 | Redis 实例所在的 K8s 命名空间 |
| `--instance` | `-i` | 是 | Redis 实例名称 |
| `--operation` | `-o` | 是 | 需要恢复的 Redis operation 升级名称 |
| `--type` | `-t` | 是 | Redis 类型：cluster / sentinel |

**示例：**

```bash
bianque redis clusterUpgradeRecover -n myns -i myredis -o operation_name -t cluster
```

### 2.5 输出格式

**check 命令**输出为 JSON 结构：

```json
{
  "status": "success",
  "timestamp": "2026-05-22T10:00:00+08:00",
  "command": "bianque <middleware> check",
  "namespace": "myns",
  "instance": "myes",
  "verbose": true,
  "log_lines": "0",
  "overall_severity": "info|warning|critical",
  "findings": [
    {
      "type": "检查项",
      "severity": "info|warning|critical",
      "message": "描述信息",
      "details": { ... }
    }
  ],
  "logs": [ ... ],
  "suggestions": [ ... ]
}
```

**client 命令**输出为 JSON 结构：

```json
{
  "status": "success",
  "timestamp": "2026-05-22T10:00:00+08:00",
  "command": "bianque <middleware> client",
  "namespace": "myns",
  "instance": "myes",
  "operation": "connect_and_verify",
  "result": { ... },
  "message": "描述信息"
}
```

### 2.6 命令速查表

| 命令 | 功能 | 是否需要参数 |
|------|------|-------------|
| `bianque elasticsearch check` | 检查 ES 集群状态 | 是 |
| `bianque elasticsearch client` | 创建 ES 客户端 | 是 |
| `bianque nacos check` | 检查 Nacos 连接状态 | 是 |
| `bianque nacos client` | 创建 Nacos 客户端 | 是 |
| `bianque redis check` | 检查 Redis 连接状态 | 是 |
| `bianque redis client` | 创建 Redis 客户端 | 是 |
| `bianque redis updateRenameConfig` | 更新重命名配置 | 是 |
| `bianque redis clusterUpgradeRecover` | 恢复集群升级 | 是 |

---

