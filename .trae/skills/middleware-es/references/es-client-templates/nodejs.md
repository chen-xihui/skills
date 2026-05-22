# Node.js + @elastic/elasticsearch 模板

## elasticsearch_client.js

```javascript
const { Client } = require('@elastic/elasticsearch');
const logger = require('./logger'); // 假设使用 winston 或 pino

class EsClient {

    constructor(config) {
        this.es = new Client({
            node: config.node,
            auth: {
                username: config.username,
                password: config.password,
            },
            maxRetries: config.maxRetries || 3,
            requestTimeout: config.timeout || 30000,
        });

        // 测试连接
        this.es.info()
            .then(info => {
                logger.info(`Connected to Elasticsearch ${info.version.number}`);
            })
            .catch(err => {
                logger.error('Failed to connect to ES:', err);
            });
    }

    /**
     * 检查索引是否存在
     */
    async indexExists(index) {
        return this.es.indices.exists({ index });
    }

    /**
     * 创建索引
     */
    async createIndex(index, mapping) {
        const exists = await this.indexExists(index);
        if (exists) {
            logger.info(`Index ${index} already exists`);
            return false;
        }
        await this.es.indices.create({ index, body: mapping });
        logger.info(`Index ${index} created successfully`);
        return true;
    }

    /**
     * 索引单条文档
     */
    async indexDocument(index, id, document) {
        const response = await this.es.index({
            index,
            id,
            refresh: true,
            body: document,
        });
        return response.result;
    }

    /**
     * 根据 ID 获取文档
     */
    async getDocument(index, id) {
        const response = await this.es.get({ index, id });
        if (response.found) {
            return response._source;
        }
        return null;
    }

    /**
     * 使用 search_after 深分页查询
     */
    async searchAfter(index, searchAfter = null, size = 100) {
        const body = {
            query: { match_all: {} },
            size,
            sort: [{ _id: { order: 'asc' } }],
        };
        if (searchAfter) {
            body.search_after = searchAfter;
        }

        const response = await this.es.search({ index, body });
        const hits = response.hits.hits;
        const documents = hits.map(hit => hit._source);
        const lastSort = hits.length > 0 ? hits[hits.length - 1].sort : null;
        return { documents, lastSort };
    }

    /**
     * 删除文档
     */
    async deleteDocument(index, id) {
        const response = await this.es.delete({ index, id, refresh: true });
        return response.result;
    }

    /**
     * 批量索引文档
     */
    async bulkIndex(index, documents) {
        const ops = [];
        for (const doc of documents) {
            ops.push({
                index: { _index: index, _id: doc._id },
            });
            ops.push(doc._source || doc);
        }

        const response = await this.es.bulk({ refresh: true, body: ops });
        if (response.errors) {
            logger.warn(`Bulk indexed with ${response.items.filter(i => i.index.error).length} errors`);
        }
        return response;
    }
}

// 工厂函数
function createEsClient(config) {
    return new EsClient(config);
}

module.exports = { EsClient, createEsClient };
```

## config.js

```javascript
const ES_CONFIG = {
    node: process.env.ES_NODE || 'https://localhost:9200',
    username: process.env.ES_USERNAME || 'elastic',
    password: process.env.ES_PASSWORD,  // 通过环境变量注入
    timeout: parseInt(process.env.ES_TIMEOUT, 10) || 30000,
    maxRetries: parseInt(process.env.ES_MAX_RETRIES, 10) || 3,
};

module.exports = ES_CONFIG;
```

## package.json 依赖

```json
{
  "dependencies": {
    "@elastic/elasticsearch": "^8.12.0"
  }
}
```