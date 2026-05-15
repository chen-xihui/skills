# Python：es_client.py

适用于 Python 语言的 ES 客户端代码模板。

```python
"""Elasticsearch 客户端封装"""

import os
import logging
from typing import List, Dict, Any, Optional

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

logger = logging.getLogger(__name__)


class ESClient:
    """ES 客户端工具类"""

    def __init__(
        self,
        hosts: List[str],
        username: str = "elastic",
        password: str = None,
        scheme: str = "https",
        max_retries: int = 3,
        retry_on_timeout: bool = True,
        request_timeout: int = 30,
        verify_certs: bool = False,
    ):
        """
        初始化 ES 客户端

        Args:
            hosts: ES 节点地址列表
            username: 用户名
            password: 密码（优先从环境变量 ES_PASSWORD 获取）
            scheme: 协议（http/https）
            max_retries: 最大重试次数
            retry_on_timeout: 超时是否重试
            request_timeout: 请求超时时间（秒）
            verify_certs: 是否验证证书
        """
        _password = password or os.getenv("ES_PASSWORD", "")
        if not _password:
            logger.warning("ES 密码未设置，请配置 ES_PASSWORD 环境变量")

        self.client = Elasticsearch(
            hosts=hosts,
            basic_auth=(username, _password),
            scheme=scheme,
            max_retries=max_retries,
            retry_on_timeout=retry_on_timeout,
            request_timeout=request_timeout,
            verify_certs=verify_certs,
        )
        logger.info("ES 客户端初始化完成, hosts=%s", hosts)

    def create_index(self, index_name: str, mapping: Dict[str, Any] = None,
                     shards: int = 1, replicas: int = 1) -> bool:
        """创建索引（如不存在）"""
        if self.client.indices.exists(index=index_name):
            logger.info("索引 %s 已存在", index_name)
            return False

        body = {
            "settings": {
                "number_of_shards": shards,
                "number_of_replicas": replicas,
            }
        }
        if mapping:
            body["mappings"] = mapping

        self.client.indices.create(index=index_name, body=body)
        logger.info("索引 %s 创建成功", index_name)
        return True

    def index_document(self, index_name: str, doc_id: str, body: Dict) -> Dict:
        """索引单条文档"""
        return self.client.index(index=index_name, id=doc_id, body=body)

    def bulk_index(self, index_name: str, documents: List[Dict]) -> tuple:
        """
        批量索引文档（推荐使用）

        Returns:
            (success_count, error_count)
        """
        actions = [
            {
                "_index": index_name,
                "_id": doc.get("_id"),
                "_source": {k: v for k, v in doc.items() if k != "_id"},
            }
            for doc in documents
        ]
        success, errors = bulk(self.client, actions, raise_on_error=False)
        if errors:
            logger.error("批量索引部分失败，错误数: %d", len(errors) if isinstance(errors, list) else errors)
        return success, errors

    def search_after(
        self,
        index_name: str,
        query: Dict,
        sort_values: Optional[List] = None,
        size: int = 100,
    ) -> Dict:
        """
        使用 search_after 深分页查询（推荐方式）

        Args:
            index_name: 索引名
            query: 查询条件
            sort_values: 上一页最后一条的排序值
            size: 每页大小
        """
        body = {
            "query": query,
            "size": size,
            "sort": [{"_id": "asc"}],
        }
        if sort_values:
            body["search_after"] = sort_values

        return self.client.search(index=index_name, body=body)

    def get_document(self, index_name: str, doc_id: str) -> Optional[Dict]:
        """根据 ID 获取文档"""
        try:
            return self.client.get(index=index_name, id=doc_id)["_source"]
        except Exception:
            return None

    def delete_document(self, index_name: str, doc_id: str) -> Dict:
        """删除文档"""
        return self.client.delete(index=index_name, id=doc_id)

    def close(self):
        """关闭连接"""
        self.client.close()
```
