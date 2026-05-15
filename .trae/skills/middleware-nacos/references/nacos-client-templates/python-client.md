# Python 模板：nacos_client.py

Nacos 客户端工具类，含服务注册/注销/查询、配置获取/监听/发布方法。

生成目标文件：`nacos_client.py`

```python
"""Nacos 客户端封装"""

import os
import logging
from typing import List, Optional, Callable

import nacos

logger = logging.getLogger(__name__)


class NacosClient:
    """Nacos 客户端工具类"""

    def __init__(
        self,
        server_addresses: str,
        namespace: str = "",
        username: str = "nacos",
        password: str = None,
    ):
        """
        初始化 Nacos 客户端

        Args:
            server_addresses: Nacos 服务地址（多个用逗号分隔）
            namespace: 命名空间 ID
            username: 用户名
            password: 密码（优先从环境变量 NACOS_PASSWORD 获取）
        """
        _password = password or os.getenv("NACOS_PASSWORD", "")
        if not _password:
            logger.warning("Nacos 密码未设置，请配置 NACOS_PASSWORD 环境变量")

        self.client = nacos.NacosClient(
            server_addresses=server_addresses,
            namespace=namespace,
            username=username,
            password=_password,
        )
        self._namespace = namespace
        logger.info("Nacos 客户端初始化完成, server_addresses=%s", server_addresses)

    def register_service(
        self, service_name: str, ip: str, port: int,
        weight: float = 1.0, cluster_name: str = "DEFAULT"
    ) -> bool:
        """注册服务实例"""
        try:
            self.client.add_naming_instance(
                service_name=service_name,
                ip=ip,
                port=port,
                weight=weight,
                cluster_name=cluster_name,
                ephemeral=True,
            )
            logger.info("服务注册成功: %s:%d", ip, port)
            return True
        except Exception as e:
            logger.error("服务注册失败: %s", e)
            return False

    def deregister_service(
        self, service_name: str, ip: str, port: int,
        cluster_name: str = "DEFAULT"
    ) -> bool:
        """注销服务实例"""
        try:
            self.client.remove_naming_instance(
                service_name=service_name,
                ip=ip,
                port=port,
                cluster_name=cluster_name,
            )
            logger.info("服务注销成功: %s:%d", ip, port)
            return True
        except Exception as e:
            logger.error("服务注销失败: %s", e)
            return False

    def get_instances(
        self, service_name: str, group_name: str = "DEFAULT_GROUP",
        healthy_only: bool = True
    ) -> List[dict]:
        """查询服务实例列表"""
        instances = self.client.list_naming_instance(
            service_name=service_name,
            group_name=group_name,
            healthy_only=healthy_only,
        )
        return instances.get("hosts", [])

    def get_config(
        self, data_id: str, group: str = "DEFAULT_GROUP"
    ) -> Optional[str]:
        """获取配置（NACOS-003：建议使用 Listener 监听而非循环调用）"""
        try:
            return self.client.get_config(data_id=data_id, group=group)
        except Exception as e:
            logger.error("获取配置失败: %s", e)
            return None

    def watch_config(
        self, data_id: str, group: str = "DEFAULT_GROUP",
        callback: Optional[Callable] = None
    ) -> None:
        """监听配置变更（推荐方式，替代循环调用 getConfig）"""
        def _on_change(event):
            logger.info("配置变更: data_id=%s, group=%s", data_id, group)
            if callback:
                callback(event)

        self.client.add_config_watcher(
            data_id=data_id,
            group=group,
            cb=_on_change,
        )
        logger.info("配置监听已注册: data_id=%s, group=%s", data_id, group)

    def publish_config(
        self, data_id: str, content: str, group: str = "DEFAULT_GROUP",
        config_type: str = "yaml"
    ) -> bool:
        """发布配置"""
        try:
            return self.client.publish_config(
                data_id=data_id,
                group=group,
                content=content,
                config_type=config_type,
            )
        except Exception as e:
            logger.error("发布配置失败: %s", e)
            return False
```
