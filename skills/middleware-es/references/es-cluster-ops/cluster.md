# ES 集群管理

## 操作 1：创建 ES 集群

| 属性 | 说明 |
|------|------|
| 操作类型 | 创建 ES 集群 |
| resource | `escluster` |
| action | `create` |
| 风险等级 | 🟡 中风险 |
| 需确认 | 是 |

```bash
paas-cli create escluster --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster.yaml
```

**YAML 配置示例** (`iteration-elasticsearch-cluster.yaml`)：
```yaml
resource: escluster
action: create
params:
  namespace: project1-paas       # [必选] k8s 空间
  cluster: qa-ci-cluster1        # [必选] k8s 集群
  name: my-es-cluster            # [必选] ES 集群名称
  self:
    password: '123456'           # [选填] 自定义密码
    clusterMode: mix             # [必选] 部署模式: mix / detach
    configTemplate: default      # [选填] 参数模板
    mix:                         # 混合部署配置
      resources:
        limits:
          cpu: 4
          memory: 8Gi
        requests:
          cpu: 100m
          memory: 200Mi
      count: 3                   # 节点数量
      storage: 4Gi               # 持久化存储
      storageClass: localstorage # 存储类型
  atomic: true                   # [选填] 创建失败自动删除
  waitSeconds: 600               # [选填] 最大等待秒数
```

**确认流程**：
```
即将执行以下操作：
  命令：paas-cli create escluster --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster.yaml
  说明：创建 ES 集群 my-es-cluster
  影响：新增 ES 集群实例，分配计算和存储资源

是否继续执行？
```

---

## 操作 2：获取 ES 集群信息

| 属性 | 说明 |
|------|------|
| 操作类型 | 获取 ES 集群信息 |
| resource | `escluster` |
| action | `get` |
| 风险等级 | 🟢 低风险 |
| 需确认 | 否 |

```bash
paas-cli get escluster --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster.yaml
```

**返回信息**：
- 集群名称和 UUID
- 集群状态（Green / Yellow / Red）
- 节点数量和数据节点数量
- 分片统计（主分片、副本分片、未分配分片）
- 集群版本

---

## 操作 3：删除 ES 集群

| 属性 | 说明 |
|------|------|
| 操作类型 | 删除 ES 集群 |
| resource | `escluster` |
| action | `delete` |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |

```bash
paas-cli delete escluster --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster.yaml
```

**确认流程**：
```
⚠️ 高风险操作 ⚠️

即将执行以下操作：
  命令：paas-cli delete escluster --gateway-config=config/gateway.yaml -f config/es/iteration-elasticsearch-cluster.yaml
  说明：删除 ES 集群
  影响范围：
    - 集群中所有索引和数据将被永久删除，不可恢复
    - 所有依赖此集群的应用将无法访问
    - 此操作不可逆

请输入"确认"以执行此操作：
```