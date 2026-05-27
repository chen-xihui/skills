## 能力二：代码优化检查

> 代码扫描：`_shared-references/harness-tools.md`（Cursor 使用 **Grep**、**SemanticSearch**）。

### 触发条件

用户请求检查 Nacos 代码优化，如：
- "检查 Nacos 代码"
- "Nacos 代码审计"
- "注册中心代码优化"
- "检查配置中心代码规范"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| scan_path | string | 是 | — | 需扫描的项目根目录 |

### 检查规则清单

> 详细规则说明和检查方法参见 `references/nacos-audit-rules/` 目录

| 规则ID | 规则描述 | 风险等级 |
|--------|---------|---------|
| NACOS-001 | 服务订阅是否启用本地快照（enableLocalSnapshot） | 🔵 建议 |
| NACOS-002 | 长轮询超时是否合理（configLongPollTimeout 建议 ≤ 30s） | 🟡 警告 |
| NACOS-003 | 是否循环调用 getConfig 而未使用 Listener | 🔴 严重 |
| NACOS-004 | 密码是否硬编码在源码中 | 🔴 严重 |
| NACOS-005 | 心跳间隔、权重等是否符合最佳实践 | 🟡 警告 |
| NACOS-006 | 是否缺少异常处理和重试配置 | 🟡 警告 |
| NACOS-007 | 命名空间是否按环境隔离 | 🔵 建议 |

### 检查流程

1. **确认扫描路径**：确认 `scan_path` 参数，缺失时主动询问
2. **扫描 Nacos 相关代码**：使用 `SemanticSearch` 与 `Grep` 工具按规则逐项搜索
   - 搜索关键词：`NacosConfigService`、`NacosDiscoveryService`、`enableLocalSnapshot`、`configLongPollTimeout`、`getConfig`、`password`、`heartBeatInterval`、`namespace` 等
3. **逐规则检查**：按 NACOS-001 ~ NACOS-007 逐项检查，记录发现的问题
4. **生成审计报告**：按输出格式生成结构化报告，按风险等级排序（🔴 → 🟡 → 🔵）

### 输出格式

```
📋 代码审计报告

📊 概要：共扫描 {N} 个文件，发现 {M} 个问题（🔴 严重 {x} | 🟡 警告 {y} | 🔵 建议 {z}）

| # | 文件路径 | 行号 | 规则ID | 问题描述 | 风险等级 | 改进建议 |
|---|---------|------|--------|---------|---------|---------|
| 1 | ... | ... | ... | ... | 🔴 严重 | ... |

💡 优先修复建议：{按风险等级排序的 Top 3 修复建议}
```

### 异常处理

- 扫描路径不存在 → 提示用户确认路径
- 未找到 Nacos 相关代码 → 告知用户未检测到 Nacos 客户端代码

---
