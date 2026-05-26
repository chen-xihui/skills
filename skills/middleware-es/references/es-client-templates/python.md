# Python + elasticsearch 模板

## es_client.py

```python
import json
import logging
from typing import Dict, List, Optional, Any, Tuple

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

logger = logging.getLogger(__name__)


class EsClient:
    """Elasticsearch 客户端封装"""

    def __init__(self, hosts: List[str], username: str, password: str,
                 timeout: int = 30, max_retries: int = 3):
        self.es = Elasticsearch(
            hosts=hosts,
            basic_auth=(username, password),
            timeout=timeout,
            max_retries=max_retries,
            retry_on_timeout=True,
            request_timeout=timeout,
        )
        # 测试连接
        info = self.es.info()
        logger.info(f\"Connected to Elasticsearch {info['version']['number']}\")

    def index_exists(self, index: str) -> bool:
        \"\"\"检查索引是否存在\"\"\"
        return self.es.indices.exists(index=index)

    def create_index(self, index: str, mapping: Dict[str, Any]) -> bool:
        \"\"\"创建索引\"\"\"
        if self.index_exists(index):
            logger.info(f\"Index {index} already exists\")
            return False
        self.es.indices.create(index=index, body=mapping)
        logger.info(f\"Index {index} created successfully\")
        return True

    def index_document(self, index: str, doc_id: str, document: Dict) -> str:
        \"\"\"索引单条文档\"\"\"
        response = self.es.index(
            index=index,
            id=doc_id,
            document=document,
            refresh=True,
        )
        return response['result']

    def get_document(self, index: str, doc_id: str) -> Optional[Dict]:
        \"\"\"根据 ID 获取文档\"\"\"
        response = self.es.get(index=index, id=doc_id)
        if response['found']:
            return response['_source']
        return None

    def search_after(self, index: str, search_after: Optional[List] = None,
                     size: int = 100) -> Tuple[List[Dict], Optional[List]]:
        \"\"\"使用 search_after 深分页查询\"\"\"
        body = {
            \"query\": {\"match_all\": {}},
            \"size\": size,
            \"sort\": [{\"_id\": {\"order\": \"asc\"}}],
        }
        if search_after:
            body[\"search_after\"] = search_after

        response = self.es.search(index=index, body=body)
        hits = response['hits']['hits']
        documents = [hit['_source'] for hit in hits]
        last_sort = hits[-1]['sort'] if hits else None
        return documents, last_sort

    def delete_document(self, index: str, doc_id: str) -> str:
        \"\"\"删除文档\"\"\"
        response = self.es.delete(index=index, id=doc_id, refresh=True)
        return response['result']

    def bulk_index(self, index: str, documents: List[Dict]) -> Tuple[int, List]:
        \"\"\"批量索引文档\"\"\"
        actions = []
        for doc in documents:
            action = {
                \"_index\": index,
                \"_op_type\": \"index\",
                \"_id\": doc.get(\"_id\"),
                \"_source\": doc.get(\"_source\", doc),
            }
            actions.append(action)

        success, errors = bulk(self.es, actions, raise_on_error=False)
        logger.info(f\"Bulk indexed {success} documents with {len(errors)} errors\")
        return success, errors


# 工厂函数
def create_es_client(hosts: List[str], username: str, password: str,
                     timeout: int = 30, max_retries: int = 3) -> EsClient:
    \"\"\"创建 ES 客户端的工厂函数\"\"\"
    return EsClient(
        hosts=hosts,
        username=username,
        password=password,
        timeout=timeout,
        max_retries=max_retries,
    )
```

## config.py

```python
import os

ES_CONFIG = {
    \"hosts\": [
        f\"https://{os.getenv('ES_HOST', 'localhost')}:{os.getenv('ES_PORT', '9200')}\"
    ],
    \"username\": os.getenv(\"ES_USERNAME\", \"elastic\"),
    \"password\": os.getenv(\"ES_PASSWORD\"),  # 通过环境变量注入
    \"timeout\": int(os.getenv(\"ES_TIMEOUT\", \"30\")),
    \"max_retries\": int(os.getenv(\"ES_MAX_RETRIES\", \"3\")),
}
```

## requirements.txt

```
elasticsearch>=8.12.0
```