# paas-cli 配置说明

> 路径相对于 `skills/paas-cli/`。命令参考见 [COMMANDS.md](COMMANDS.md)。

## 三、配置文件说明

### 3.1 目录结构

```
skills/paas-cli/
├── SKILL.md
├── paas-cli.cmd
├── paas-cli.py
└── config/
        ├── gateway.yaml                          # API 网关连接配置
        ├── nacos/                                 # Nacos CRD 资源配置
        │   ├── iteration-nacos-cluster-backup-create.yaml
        │   ├── iteration-nacos-cluster-backup-get.yaml
        │   ├── iteration-nacos-cluster-restore.yaml
        │   ├── iteration-nacos-cluster-access-token-create.yaml
        │   ├── iteration-nacos-cluster-access-token-get.yaml
        │   ├── iteration-nacos-cluster-access-token-delete.yaml
        │   ├── iteration-nacos-cluster-monitor-get.yaml
        │   ├── iteration-nacos-cluster-monitor-update.yaml
        │   ├── iteration-nacos-cluster-network-policy-create.yaml
        │   ├── iteration-nacos-cluster-network-policy-get.yaml
        │   ├── iteration-nacos-cluster-network-policy-update.yaml
        │   └── iteration-nacos-cluster-network-policy-delete.yaml
        ├── redis/                                 # Redis CRD 资源配置
        │   ├── ncractivestrategy.yaml
        │   ├── ncrhotbackupstrategy.yaml
        │   └── ncrunitstrategy.yaml
        └── es/                                    # ES CRD 资源配置
            ├── iteration-elasticsearch-index.yaml
            ├── iteration-elasticsearch-index-template.yaml
            ├── iteration-elasticsearch-clusterIP.yaml
            ├── iteration-elasticsearch-lb.yaml
            └── iteration-elasticsearch-cluster-replicas-update.yaml
```

### 3.2 gateway.yaml

所有 CRD 风格命令都需要通过 `--gateway-config=config/gateway.yaml` 引用此文件，其中包含 API Server 地址、超时配置和认证方式。

---

## 四、公共参数说明

以下参数在多数命令中通用：

| 参数 | 格式 | 默认值 | 说明 |
|------|------|--------|------|
| `--project` | `--project <id>` 或 `--project=<id>` | `j036x0` | 项目标识 |
| `--env` | `--env <env>` 或 `--env=<env>` | `DEV` | 环境名称 |
| `--gateway-config` | `--gateway-config=<path>` | 脚本目录下 `config/gateway.yaml` | 网关配置路径（仅 CRD 命令，默认自动解析） |
| `-f` | `-f <path>` | — | 资源配置文件路径（仅 CRD 命令） |
| `--namespace` / `-n` | `-n <namespace>` | — | K8s 命名空间（bianque 命令） |
| `--instance` / `-i` | `-i <instance>` | — | 实例名称（bianque 命令） |
| `--type` / `-t` | `-t <type>` | — | Redis 类型 cluster/sentinel（bianque 命令） |
| `--verb` / `-v` | `-v` | false | 展示详情（bianque check 命令） |
| `--token-file` | `--token-file <path>` | — | 权限验证脚本文件路径（bianque 全局参数） |
