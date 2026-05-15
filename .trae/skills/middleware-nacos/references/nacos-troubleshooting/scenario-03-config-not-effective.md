# 场景 3：配置不生效

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
