# Nacos 代码优化检查规则索引

本目录包含 NACOS-001 ~ NACOS-007 共 7 条检查规则。

| 规则ID | 规则描述 | 风险等级 | 详情 |
|--------|---------|---------|------|
| NACOS-001 | 服务订阅是否启用本地快照 | 🔵 建议 | [NACOS-001.md](./NACOS-001.md) |
| NACOS-002 | 长轮询超时是否合理 | 🟡 警告 | [NACOS-002.md](./NACOS-002.md) |
| NACOS-003 | 是否循环调用 getConfig 而未使用 Listener | 🔴 严重 | [NACOS-003.md](./NACOS-003.md) |
| NACOS-004 | 密码是否硬编码在源码中 | 🔴 严重 | [NACOS-004.md](./NACOS-004.md) |
| NACOS-005 | 心跳间隔、权重等是否符合最佳实践 | 🟡 警告 | [NACOS-005.md](./NACOS-005.md) |
| NACOS-006 | 是否缺少异常处理和重试配置 | 🟡 警告 | [NACOS-006.md](./NACOS-006.md) |
| NACOS-007 | 命名空间是否按环境隔离 | 🔵 建议 | [NACOS-007.md](./NACOS-007.md) |

## 检查流程

1. 使用 `search_codebase` 和 `grep_code` 工具按规则逐项搜索
2. 搜索关键词: `NacosConfigService`、`NacosDiscoveryService`、`enableLocalSnapshot`、`configLongPollTimeout`、`getConfig`、`password`、`heartBeatInterval`、`namespace` 等
3. 按 NACOS-001 ~ NACOS-007 逐项检查,记录发现的问题
4. 生成审计报告,按风险等级排序(🔴 → 🟡 → 🔵)