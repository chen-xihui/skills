# Redis Python 客户端代码模板

本文件包含 Python 语言 Redis 客户端的代码模板。

---

## 1. Python + redis-py + Standalone

### 1.1 redis_client.py

```python
import os
import redis
from redis.connection import ConnectionPool
from typing import Optional, Any, List


class RedisClient:
    """Redis 客户端封装"""

    def __init__(self):
        self.pool = self._create_pool()
        self.client = redis.Redis(connection_pool=self.pool)

    def _create_pool(self) -> ConnectionPool:
        """创建连接池（REDIS-004）"""
        return ConnectionPool(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            password=os.getenv("REDIS_PASSWORD"),
            db=0,
            max_connections=20,        # maxTotal
            socket_connect_timeout=5,  # 连接超时 5s
            socket_timeout=3,          # 命令超时 3s
            decode_responses=True,
        )

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """设置值（含过期时间，REDIS-007）"""
        if expire:
            return self.client.set(key, value, ex=expire)
        return self.client.set(key, value)

    def get(self, key: str) -> Optional[str]:
        """获取值"""
        return self.client.get(key)

    def delete(self, key: str) -> int:
        """删除 Key"""
        return self.client.delete(key)

    def expire(self, key: str, seconds: int) -> bool:
        """设置过期时间"""
        return self.client.expire(key, seconds)

    def scan_keys(self, pattern: str, count: int = 100) -> List[str]:
        """使用 scan 替代 keys（REDIS-001）"""
        keys = []
        cursor = 0
        while True:
            cursor, batch = self.client.scan(cursor=cursor, match=pattern, count=count)
            keys.extend(batch)
            if cursor == 0:
                break
        return keys

    def pipeline_exec(self, commands: List[tuple]) -> List[Any]:
        """使用 Pipeline 批量执行（REDIS-005）"""
        pipe = self.client.pipeline()
        for cmd in commands:
            getattr(pipe, cmd[0])(*cmd[1:])
        return pipe.execute()

    def close(self):
        """关闭连接池"""
        self.pool.disconnect()
```

### 1.2 service.py

```python
from redis_client import RedisClient
from typing import Any, Optional


class RedisService:
    """Redis 业务服务层"""

    def __init__(self):
        self.redis = RedisClient()

    def set_with_expiry(self, key: str, value: Any, ttl_seconds: int) -> bool:
        """设置带过期时间的值"""
        return self.redis.set(key, value, expire=ttl_seconds)

    def get_value(self, key: str) -> Optional[str]:
        """获取值"""
        return self.redis.get(key)

    def delete_key(self, key: str) -> bool:
        """删除 Key"""
        return self.redis.delete(key) > 0

    def find_keys(self, pattern: str) -> list:
        """查找匹配 Key（使用 scan，REDIS-001）"""
        return self.redis.scan_keys(pattern)

    def batch_set(self, key_value_pairs: list, expire: Optional[int] = None) -> list:
        """批量设置值（使用 Pipeline，REDIS-005）"""
        commands = []
        for key, value in key_value_pairs:
            if expire:
                commands.append(("set", key, value, ex=expire))
            else:
                commands.append(("set", key, value))
        return self.redis.pipeline_exec(commands)
```

### 1.3 main.py（示例）

```python
import time
from service import RedisService

def main():
    service = RedisService()

    # 设置值
    key = "example:key"
    service.set_with_expiry(key, "hello, redis", ttl_seconds=600)

    # 获取值
    result = service.get_value(key)
    print(f"Value: {result}")

    # 批量设置
    pairs = [
        ("batch:key1", "value1"),
        ("batch:key2", "value2"),
        ("batch:key3", "value3"),
    ]
    service.batch_set(pairs, expire=300)

    # 查找 Key
    keys = service.find_keys("batch:*")
    print(f"Found keys: {keys}")

    # 删除
    service.delete_key(key)

if __name__ == "__main__":
    main()
```

### 1.4 requirements.txt

```
redis>=4.5.0
```

---

## 2. Python + redis-py + Cluster

### 2.1 redis_cluster.py

```python
import os
import redis
from redis.cluster import RedisCluster, ClusterNode


class RedisClusterClient:
    """Redis 集群客户端封装"""

    def __init__(self):
        self.client = self._create_cluster_client()

    def _create_cluster_client(self) -> RedisCluster:
        """创建集群连接"""
        nodes_str = os.getenv("REDIS_CLUSTER_NODES", "node1:6379,node2:6379,node3:6379")
        nodes = [n.strip() for n in nodes_str.split(",")]

        startup_nodes = [ClusterNode(host, port) for host, port in [n.split(":") for n in nodes]]

        return RedisCluster(
            startup_nodes=startup_nodes,
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=3,
            max_connections=20,
        )

    def set(self, key: str, value, expire: int = None):
        """设置值"""
        if expire:
            return self.client.set(key, value, ex=expire)
        return self.client.set(key, value)

    def get(self, key: str):
        """获取值"""
        return self.client.get(key)

    def delete(self, key: str):
        """删除 Key"""
        return self.client.delete(key)

    def close(self):
        """关闭连接"""
        self.client.close()
```

### 2.2 环境变量配置

```bash
# 集群节点地址（逗号分隔）
export REDIS_CLUSTER_NODES="node1:6379,node2:6379,node3:6379"
# 密码
export REDIS_PASSWORD="your_password_here"
```

---

## 3. Python + redis-py + Sentinel

### 3.1 redis_sentinel.py

```python
import os
import redis
from redis.sentinel import Sentinel


class RedisSentinelClient:
    """Redis Sentinel 客户端封装"""

    def __init__(self):
        self.client = self._create_sentinel_client()

    def _create_sentinel_client(self):
        """创建 Sentinel 连接"""
        sentinel_nodes_str = os.getenv("REDIS_SENTINEL_NODES", "sentinel1:26379,sentinel2:26379,sentinel3:26379")
        sentinel_nodes = [n.strip() for n in sentinel_nodes_str.split(",")]

        master_name = os.getenv("REDIS_SENTINEL_MASTER", "mymaster")

        sentinel = Sentinel(
            [(n.split(":")[0], int(n.split(":")[1])) for n in sentinel_nodes],
            socket_timeout=3,
        )

        return sentinel.master_for(
            master_name,
            password=os.getenv("REDIS_PASSWORD"),
            socket_connect_timeout=5,
            socket_timeout=3,
            decode_responses=True,
        )

    def set(self, key: str, value, expire: int = None):
        """设置值"""
        if expire:
            return self.client.set(key, value, ex=expire)
        return self.client.set(key, value)

    def get(self, key: str):
        """获取值"""
        return self.client.get(key)

    def delete(self, key: str):
        """删除 Key"""
        return self.client.delete(key)

    def close(self):
        """关闭连接"""
        self.client.close()
```

### 3.2 环境变量配置

```bash
# Sentinel 节点地址（逗号分隔）
export REDIS_SENTINEL_NODES="sentinel1:26379,sentinel2:26379,sentinel3:26379"
# Master 名称
export REDIS_SENTINEL_MASTER="mymaster"
# 密码
export REDIS_PASSWORD="your_password_here"
```

---

## 4. 安全注意事项

- **密码注入**：通过环境变量注入密码，禁止在代码中硬编码（REDIS-008）
- **连接池参数**：`max_connections` 应小于 200（REDIS-004）
- **Key 命名**：使用 `项目名:业务模块:Key` 格式（REDIS-012）
- **过期时间**：所有 Key 必须设置过期时间（REDIS-007）
- **禁止命令**：不在生产环境使用 `KEYS`、`FLUSHALL`、`FLUSHDB` 等高危险命令（REDIS-001、REDIS-009、REDIS-010）