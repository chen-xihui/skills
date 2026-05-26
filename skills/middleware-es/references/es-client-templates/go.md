# Go + elastic/go-elasticsearch 模板

## elasticsearch_client.go

```go
package elasticsearch

import (
    "context"
    "encoding/json"
    "fmt"
    "log"

    "github.com/elastic/go-elasticsearch/v8"
    "github.com/elastic/go-elasticsearch/v8/esapi"
)

type Client struct {
    es *elasticsearch.Client
}

type Config struct {
    Addresses  []string
    Username   string
    Password   string
    Timeout    int // seconds
    MaxRetries int
}

// NewClient 创建 Elasticsearch 客户端
func NewClient(cfg Config) (*Client, error) {
    es, err := elasticsearch.NewClient(elasticsearch.Config{
        Addresses:  cfg.Addresses,
        Username:   cfg.Username,
        Password:   cfg.Password,
        MaxRetries: cfg.MaxRetries,
        RetryOnError: func(response *esapi.Response) bool {
            // 对 5xx 错误进行重试
            return response.IsServerError()
        },
    })
    if err != nil {
        return nil, fmt.Errorf("failed to create ES client: %w", err)
    }

    // 测试连接
    ctx := context.Background()
    info, err := es.Info(ctx)
    if err != nil {
        return nil, fmt.Errorf("failed to connect to ES: %w", err)
    }
    log.Printf("Connected to Elasticsearch %s", info.Version.Number)
    info.Close()

    return &Client{es: es}, nil
}

// IndexExists 检查索引是否存在
func (c *Client) IndexExists(ctx context.Context, index string) (bool, error) {
    resp, err := c.es.Indices.Exists(ctx, []string{index})
    if err != nil {
        return false, err
    }
    defer resp.Body.Close()
    return resp.IsError(), false
}

// CreateIndex 创建索引
func (c *Client) CreateIndex(ctx context.Context, index string, mapping map[string]interface{}) error {
    body, err := json.Marshal(mapping)
    if err != nil {
        return err
    }

    resp, err := c.es.Indices.Create(ctx, index, c.es.Indices.Create.WithBody(body))
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    if resp.IsError() {
        return fmt.Errorf("failed to create index: %s", resp.String())
    }
    return nil
}

// IndexDocument 索引单条文档
func (c *Client) IndexDocument(ctx context.Context, index string, id string, document interface{}) error {
    body, err := json.Marshal(document)
    if err != nil {
        return err
    }

    resp, err := c.es.Index(index, bytes.NewReader(body),
        c.es.Index.WithDocumentID(id),
        c.es.Index.WithRefresh("true"),
    )
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    if resp.IsError() {
        return fmt.Errorf("failed to index document: %s", resp.String())
    }
    return nil
}

// GetDocument 根据 ID 获取文档
func (c *Client) GetDocument(ctx context.Context, index string, id string) ([]byte, error) {
    resp, err := c.es.Get(ctx, index, id)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    if resp.IsError() {
        return nil, fmt.Errorf("failed to get document: %s", resp.String())
    }

    var result map[string]interface{}
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return nil, err
    }

    source, ok := result["_source"].(map[string]interface{})
    if !ok {
        return nil, fmt.Errorf("no source found")
    }

    return json.Marshal(source)
}

// SearchAfter 使用 search_after 深分页查询
func (c *Client) SearchAfter(ctx context.Context, index string,
    searchAfter []interface{}, size int) ([]map[string]interface{}, []interface{}, error) {

    body := map[string]interface{}{
        "query": map[string]interface{}{
            "match_all": {},
        },
        "size": size,
        "sort": []map[string]interface{}{
            {"_id": {"order": "asc"}},
        },
    }

    if searchAfter != nil {
        body["search_after"] = searchAfter
    }

    bodyBytes, err := json.Marshal(body)
    if err != nil {
        return nil, nil, err
    }

    resp, err := c.es.Search(c.es.Search.WithContext(ctx), c.es.Search.WithIndex(index),
        c.es.Search.WithBody(bytes.NewReader(bodyBytes)))
    if err != nil {
        return nil, nil, err
    }
    defer resp.Body.Close()

    if resp.IsError() {
        return nil, nil, fmt.Errorf("search failed: %s", resp.String())
    }

    var result map[string]interface{}
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return nil, nil, err
    }

    hits := result["hits"].(map[string]interface{})["hits"].([]interface{})
    var documents []map[string]interface{}
    var lastSort []interface{}

    for _, hit := range hits {
        h := hit.(map[string]interface{})
        source := h["_source"].(map[string]interface{})
        documents = append(documents, source)
        lastSort = h["sort"].([]interface{})
    }

    return documents, lastSort, nil
}

// DeleteDocument 删除文档
func (c *Client) DeleteDocument(ctx context.Context, index string, id string) error {
    resp, err := c.es.Delete(ctx, index, id, c.es.Delete.WithRefresh("true"))
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    if resp.IsError() {
        return fmt.Errorf("failed to delete document: %s", resp.String())
    }
    return nil
}

// BulkIndex 批量索引文档
func (c *Client) BulkIndex(ctx context.Context, index string, documents []map[string]interface{}) error {
    var buf bytes.Buffer
    for _, doc := range documents {
        action := `{"index":{"_index":"` + index + `"}}`
        buf.WriteString(action)
        buf.WriteByte('\n')
        data, _ := json.Marshal(doc)
        buf.Write(data)
        buf.WriteByte('\n')
    }

    resp, err := c.es.Bulk(ctx, bytes.NewReader(buf.Bytes()),
        c.es.Bulk.WithIndex(index),
        c.es.Bulk.WithRefresh("true"),
    )
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    if resp.IsError() {
        return fmt.Errorf("bulk index failed: %s", resp.String())
    }
    return nil
}
```

## config.yaml

```yaml
elasticsearch:
  addresses:
    - "https://es-node1:9200"
    - "https://es-node2:9200"
  username: "${ES_USERNAME}"
  password: "${ES_PASSWORD}"
  timeout: 30
  max_retries: 3
```

## go.mod 依赖

```go
require (
    github.com/elastic/go-elasticsearch/v8 v8.12.0
)
```