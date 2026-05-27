## 能力一：客户端创建与配置

### 触发条件

用户请求创建 Redis 客户端并生成配置，如：
- "创建 Redis 客户端"
- "生成缓存连接代码"
- "帮我配置 Redis"
- "创建 Redis Sentinel 客户端"

### 必要参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| project_id | string | 是 | — | 项目组编号 |
| env | enum | 是 | — | 环境：DEV / SIT / SRV |
| password | string | 是 | — | Redis 密码 |
| target_path | string | 是 | — | 代码生成目标路径 |
| mode | enum | 否 | standalone | 部署模式：standalone / sentinel / cluster |
| client_type | enum | 否 | lettuce | 客户端库：jedis / lettuce（仅 Java） |
| language | enum | 否 | Java | 项目语言：Java / Go / Python |

### 处理流程

1. **参数收集**：确认所有必要参数，缺失项主动询问用户。特别注意 `mode` 参数：
   - standalone：单机模式
   - sentinel：哨兵模式（高可用）
   - cluster：集群模式（分片）
   - 如用户不确定，提示："如果 Redis 只有一个节点选 standalone；有哨兵选 sentinel；有多分片选 cluster"
2. **环境信息查询**：按 **paas-cli Skill** 在终端执行 `$PAAS_CLI` 命令获取 Redis 连接信息
   ```
   $PAAS_CLI redis config --project {project_id} --env {env}
   ```
   - 如 paas-cli Skill 下 `$PAAS_CLI` 执行失败，提示用户检查安装及网络连通性，改为手动输入 Redis 地址
3. **代码生成**：根据参数组合选择对应模板
    > 详细代码模板参见 `references/redis-client-templates/` 目录

   | 组合 | 生成文件 |
   |------|---------|
   | Java + Lettuce + Standalone | RedisConfig.java、RedisService.java、application.yml |
   | Java + Jedis + Standalone | JedisConfig.java、JedisService.java、application.yml |
   | Java + Lettuce + Sentinel | RedisSentinelConfig.java、RedisService.java、application.yml |
   | Java + Lettuce + Cluster | RedisClusterConfig.java、RedisService.java、application.yml |
   | Go | redis_client.go、config.yaml |
   | Python | redis_client.py、config.yaml |

4. **文件写入**：将生成的代码写入 `target_path` 指定目录
5. **依赖提示**：列出需要添加的依赖
   - **Java + Lettuce**：`io.lettuce:lettuce-core`、`org.springframework.boot:spring-boot-starter-data-redis`
   - **Java + Jedis**：`redis.clients:jedis`、`org.springframework.boot:spring-boot-starter-data-redis`
   - **Go**：`github.com/redis/go-redis/v9`
   - **Python**：`pip install redis`

### 输出格式

```
✅ 客户端代码已生成

📁 生成文件列表：
  - {文件路径1} — {文件说明}
  - {文件路径2} — {文件说明}

📝 后续步骤：
  1. 添加依赖：{依赖信息}
  2. 配置环境变量：REDIS_PASSWORD={实际密码}
  3. 根据实际环境调整连接池参数

⚠️ 注意事项：
  - 密码以 ${REDIS_PASSWORD} 占位符形式写入，请通过环境变量或密钥管理系统注入实际值
  - 当前生成的是 {mode} 模式客户端，请确认与实际部署模式一致
```

### 异常处理

- paas-cli Skill 命令执行失败 → 提示用户遵循 paas-cli Skill 并完成 `$PAAS_CLI` 解析及网络连通性，改为手动输入 Redis 地址
- 目标路径不存在 → 询问用户是否创建目录
- 文件已存在 → 询问用户是否覆盖

---
