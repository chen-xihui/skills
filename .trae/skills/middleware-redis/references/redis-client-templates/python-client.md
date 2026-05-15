# Python 模板：redis_client.py

Redis 客户端工具类，含 scan 替代 keys、Pipeline、EVALSHA、过期时间设置。

生成目标文件：`redis_client.py`

```python
"""Redis 客户端封装"""

import os
import logging
from typing import List, Optional, Any

import redis
from redis.commands.core import Script

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis 客户端工具类"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: str = None,
        db: int = 0,
        max_connections: int = 20,
        socket_timeout: float = 3.0,
        socket_connect_timeout: float = 5.0,
        retry_on_timeout: bool = True,
    ):
        _password = password or os.getenv("REDIS_PASSWORD", "")
        if not _password:
            logger.warning("Redis 密码未设置，请配置 REDIS_PASSWORD 环境变量")

        self.client = redis.Redis(
            host=host,
            port=port,
            password=_password,
            db=db,
            max_connections=max_connections,
            socket_timeout=socket_timeout,
            socket_connect_timeout=socket_connect_timeout,
            retry_on_timeout=retry_on_timeout,
            decode_responses=True,
        )
        logger.info("Redis 客户端初始化完成, host=%s:%d", host, port)

    def set(self, key: str, value: str, ex: int = None, px: int = None) -> bool:
        """设置值（REDIS-007：建议始终设置过期时间）"""
        return self.client.set(key, value, ex=ex, px=px)

    def get(self, key: str) -> Optional[str]:
        """获取值"""
        return self.client.get(key)

    def delete(self, *keys: str) -> int:
        """删除 Key"""
        return self.client.delete(*keys)

    def scan(self, match: str = "*", count: int = 100) -> List[str]:
        """使用 scan 替代 keys（REDIS-001）"""
        keys = []
        cursor = 0
        while True:
            cursor, batch = self.client.scan(cursor=cursor, match=match, count=count)
            keys.extend(batch)
            if cursor == 0:
                break
        return keys

    def pipeline(self):
        """获取 Pipeline 对象（REDIS-005：批量操作使用 Pipeline）"""
        return self.client.pipeline()

    def script_load(self, script: str) -> str:
        """预加载 Lua 脚本（REDIS-006：使用 EVALSHA）"""
        return self.client.script_load(script)

    def evalsha(self, sha: str, numkeys: int, *keys_and_args) -> Any:
        """使用 EVALSHA 执行预加载的 Lua 脚本"""
        return self.client.evalsha(sha, numkeys, *keys_and_args)

    def expire(self, key: str, time_seconds: int) -> bool:
        """设置过期时间"""
        return self.client.expire(key, time_seconds)

    def close(self):
        """关闭连接"""
        self.client.close()
```
