# 操作 7：升级版本

| 属性 | 说明 |
|------|------|
| 操作类型 | 升级版本 |
| 风险等级 | 🔴 高风险 |
| 需确认 | 是 |
| 命令 | `paas-cli nacos upgrade --project {project_id} --env {env} --version {version}` |

## 额外参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| version | string | 是 | 目标版本号（语义化版本格式） |

## 命令示例

```bash
paas-cli nacos upgrade --project j036x0 --env DEV --version 2.3.0
```

## 确认流程

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
