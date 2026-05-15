# Go：es_client.go

适用于 Go 语言的 ES 客户端代码模板。

```go
package es

import (
	"crypto/tls"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/elastic/go-elasticsearch/v8"
)

// Config ES 连接配置
type Config struct {
	Hosts         []string `yaml:"hosts"`
	Username      string   `yaml:"username"`
	Password      string   `yaml:"password"` // 通过环境变量注入
	Scheme        string   `yaml:"scheme"`
	MaxRetries    int      `yaml:"max_retries"`
	RetryOnStatus []int    `yaml:"retry_on_status"`
	ConnectTimeout int     `yaml:"connect_timeout_ms"`
}

// NewESClient 创建 ES 客户端
func NewESClient(cfg Config) (*elasticsearch.Client, error) {
	password := cfg.Password
	if password == "" {
		password = os.Getenv("ES_PASSWORD")
	}

	retryStatuses := cfg.RetryOnStatus
	if len(retryStatuses) == 0 {
		retryStatuses = []int{502, 503, 504}
	}

	maxRetries := cfg.MaxRetries
	if maxRetries == 0 {
		maxRetries = 3
	}

	esCfg := elasticsearch.Config{
		Addresses: cfg.Hosts,
		Username:  cfg.Username,
		Password:  password,
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: cfg.Scheme == "https", // 按需配置
			},
		},
		MaxRetries:    maxRetries,
		RetryOnStatus: retryStatuses,
	}

	if cfg.ConnectTimeout > 0 {
		esCfg.Transport.(*http.Transport).MaxIdleConnsPerHost = 10
	}

	client, err := elasticsearch.NewClient(esCfg)
	if err != nil {
		return nil, fmt.Errorf("创建 ES 客户端失败: %w", err)
	}

	// 验证连接
	res, err := client.Info()
	if err != nil {
		return nil, fmt.Errorf("ES 连接验证失败: %w", err)
	}
	defer res.Body.Close()

	log.Println("ES 客户端连接成功")
	return client, nil
}
```
