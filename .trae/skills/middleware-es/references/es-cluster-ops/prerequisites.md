# 通用前置条件

执行任何 ES 集群操作前，必须完成以下前置检查：

```bash
# 1. 检查 paas-cli 是否可用
paas-cli --version
# 失败 → 提示用户安装 paas-cli

# 2. 检查网络连通性
paas-cli ping
# 失败 → 提示用户检查网络连接
```
