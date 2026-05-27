# Redis PaaS Tools

本目录提供 Redis 连接信息获取工具。

## 目录结构

```
client-redis-paas-tools/
├── README.md          # 本文件
├── paas-cli.py        # 命令行工具
├── paas-cli.cmd       # Windows 入口
└── config/            # 配置文件
    └── redis/         # Redis 相关配置
```

## 使用方式

### 前置准备

将工具目录加入 PATH（PowerShell）：

```powershell
$env:PATH = "path\to\client-redis-paas-tools;" + $env:PATH
$env:PATHEXT = ".CMD;.PY;" + $env:PATHEXT
```

### 获取 Redis 连接信息

```bash
# 查看 Redis 集群信息
paas-cli redis info --project <project_id> --env <DEV|SIT|SRV>

# 查看 Redis 节点列表
paas-cli redis nodes --project <project_id> --env <DEV|SIT|SRV>

# 查看 Redis 内存详情
paas-cli redis memory --project <project_id> --env <DEV|SIT|SRV>

# 查看 Redis 连接配置
paas-cli redis config --project <project_id> --env <DEV|SIT|SRV> --mode <standalone|sentinel|cluster>
```

### Mock 返回值说明

本工具为 mock 版本，返回示例数据：

```
Redis Cluster Info — project=j036x0  env=DEV
  Cluster Name   : redis-j036x0-dev
  Status         : Running
  Version        : 7.0.0
  Mode           : standalone
  Nodes          : 1
  Connections    : 42
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| --project | 是 | 项目组编号，如 j036x0 |
| --env | 是 | 环境：DEV / SIT / SRV |
| --mode | 否 | 部署模式：standalone / sentinel / cluster |

## 注意事项

- 本工具为 mock 版本，返回示例数据
- 实际使用时需替换为真实 PaaS 平台 API
- 获取的 Redis 地址为 127.0.0.1:6379，密码为 A12345*
- 生产环境请勿直接使用此 mock 工具
