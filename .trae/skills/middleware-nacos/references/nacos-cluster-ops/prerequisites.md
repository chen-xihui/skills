# 通用前置条件检查

执行任何集群操作前，必须完成以下检查：

```bash
# 1. 检查 paas-cli 是否可用
paas-cli --version

# 2. 检查网络连通性
paas-cli ping
```

**异常处理**：
- paas-cli 未安装 → 提示用户安装 paas-cli，并提供安装文档链接
- 网络不通 → 提示用户检查网络连接
