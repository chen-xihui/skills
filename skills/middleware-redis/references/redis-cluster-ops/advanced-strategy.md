# Redis 高阶策略操作说明

## 五、Redis 高阶策略

### 5.1 多活策略

#### 操作 57：创建多活策略

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建多活策略 |
| resource | `activestrategy` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI create activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml` |

```bash
paas-cli create activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml
```

**YAML 配置示例** (`ncractivestrategy.yaml`)：
```yaml
resource: activestrategy
action: create
params:
  name: active-strategy-test001  # [必填] 策略名称
  clusterType: cluster           # [必填] 集群类型: cluster / sentinel
  clusterCnt: 2                  # [必填] 多活集群数量
  clusters:                      # [必填] 集群列表
    - 1/wxx/cluster-active-0
    - 1/wxx/cluster-active-1
  failoverRecover: auto          # [选填] 故障恢复策略
  sharedDownRecover: auto        # [选填] 分片故障恢复策略
  enableHealthCheck: true        # [选填] 是否自动切流
  proxyReadMode: preferLogicMaster # [选填] 读策略
```

---

#### 操作 58：获取多活策略

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取多活策略 |
| resource | `activestrategy` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `$PAAS_CLI get activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml` |

```bash
paas-cli get activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml
```

---

#### 操作 59：删除多活策略

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除多活策略 |
| resource | `activestrategy` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI delete activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml` |

```bash
paas-cli delete activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy.yaml
```

---

#### 操作 60：更新多活策略

| 属性 | 说明 |
|------|------|
| 操作类型 | 更新多活策略 |
| resource | `activestrategy` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI update activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy-update.yaml` |

```bash
paas-cli update activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy-update.yaml
```

---

#### 操作 61：更新 Proxy 读模式

| 属性 | 说明 |
|------|------|
| 操作类型 | 更新 Proxy 读模式 |
| resource | `activestrategy` |
| action | `update` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI update activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy-proxyReadMode-update.yaml` |

```bash
paas-cli update activestrategy --gateway-config=config/gateway.yaml -f config/redis/ncractivestrategy-proxyReadMode-update.yaml
```

---

### 5.2 多活切换操作

#### 操作 62：双集群主从切换

| 属性 | 说明 |
|------|------|
| 操作类型 | 双集群主从切换 |
| resource | `activestrategy` |
| action | `switch` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI switch activestrategy --gateway-config=config/gateway.yaml -f config/redis/redis-activestrategy.yaml` |

```bash
paas-cli switch activestrategy --gateway-config=config/gateway.yaml -f config/redis/redis-activestrategy.yaml
```

### 确认流程

```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli switch activestrategy --gateway-config=config/gateway.yaml -f config/redis/redis-activestrategy.yaml
  说明：执行双集群主从切换
  影响范围：
    - 切换期间可能产生短暂的服务中断
    - 主从角色互换，流量方向改变
    - 切换前请确保两个集群数据已同步

请输入"确认"以执行此操作：
```

---

#### 操作 63：多活降备

| 属性 | 说明 |
|------|------|
| 操作类型 | 多活降备 |
| resource | `demoteActiveMaster` |
| action | `switch` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI switch demoteActiveMaster --gateway-config=config/gateway.yaml -f config/redis/redis-demoteActiveMaster.yaml` |

```bash
paas-cli switch demoteActiveMaster --gateway-config=config/gateway.yaml -f config/redis/redis-demoteActiveMaster.yaml
```

---

#### 操作 64：多活升主

| 属性 | 说明 |
|------|------|
| 操作类型 | 多活升主 |
| resource | `promoteActiveSlave` |
| action | `switch` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI switch promoteActiveSlave --gateway-config=config/gateway.yaml -f config/redis/redis-promoteActiveSlave.yaml` |

```bash
paas-cli switch promoteActiveSlave --gateway-config=config/gateway.yaml -f config/redis/redis-promoteActiveSlave.yaml
```

---

#### 操作 65：切流恢复

| 属性 | 说明 |
|------|------|
| 操作类型 | 切流恢复 |
| resource | `activestrategy` |
| action | `switch` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI switch activestrategy --gateway-config=config/gateway.yaml -f config/redis/autoSwitchResetRecovery.yaml` |

```bash
paas-cli switch activestrategy --gateway-config=config/gateway.yaml -f config/redis/autoSwitchResetRecovery.yaml
```

---

#### 操作 66：逻辑主恢复

| 属性 | 说明 |
|------|------|
| 操作类型 | 逻辑主恢复 |
| resource | `configLogicMasterRecover` |
| action | `update` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI update configLogicMasterRecover --gateway-config=config/gateway.yaml -f config/redis/configLogicMasterRecover.yaml` |

```bash
paas-cli update configLogicMasterRecover --gateway-config=config/gateway.yaml -f config/redis/configLogicMasterRecover.yaml
```

---

### 5.3 热备策略

#### 操作 67：创建热备策略

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建热备策略 |
| resource | `hotbackupstrategy` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI create hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml` |

```bash
paas-cli create hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml
```

---

#### 操作 68：获取热备策略

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取热备策略 |
| resource | `hotbackupstrategy` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `$PAAS_CLI get hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml` |

```bash
paas-cli get hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml
```

---

#### 操作 69：删除热备策略

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除热备策略 |
| resource | `hotbackupstrategy` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI delete hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml` |

```bash
paas-cli delete hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrhotbackupstrategy.yaml
```

---

#### 操作 70：热备切换

| 属性 | 说明 |
|------|------|
| 操作类型 | 热备切换 |
| resource | `hotbackupstrategy` |
| action | `switch` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI switch hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/switchredishotback.yaml` |

```bash
paas-cli switch hotbackupstrategy --gateway-config=config/gateway.yaml -f config/redis/switchredishotback.yaml
```

---

### 5.4 单元化策略

#### 操作 71：创建单元化策略

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建单元化策略 |
| resource | `unitstrategy` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI create unitstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrunitstrategy.yaml` |

```bash
paas-cli create unitstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrunitstrategy.yaml
```

---

#### 操作 72：获取单元化策略

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取单元化策略 |
| resource | `unitstrategy` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |
| 命令 | `$PAAS_CLI get unitstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrunitstrategy.yaml` |

```bash
paas-cli get unitstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrunitstrategy.yaml
```

---

#### 操作 73：删除单元化策略

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除单元化策略 |
| resource | `unitstrategy` |
| action | `delete` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |
| 命令 | `$PAAS_CLI delete unitstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrunitstrategy.yaml` |

```bash
paas-cli delete unitstrategy --gateway-config=config/gateway.yaml -f config/redis/ncrunitstrategy.yaml
```