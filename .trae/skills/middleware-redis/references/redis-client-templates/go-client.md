# Go 模板：redis_client.go

Redis 客户端封装，支持连接验证、密码环境变量回退。

生成目标文件：`redis_client.go`

```go
package redis

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/redis/go-redis/v9"
)

// Config Redis 连接配置
type Config struct {
	Addr         string `yaml:"addr"`
	Password     string `yaml:"password"` // 通过环境变量注入
	DB           int    `yaml:"db"`
	MaxRetries   int    `yaml:"max_retries"`
	DialTimeout  int    `yaml:"dial_timeout_ms"`
	ReadTimeout  int    `yaml:"read_timeout_ms"`
	WriteTimeout int    `yaml:"write_timeout_ms"`
	PoolSize     int    `yaml:"pool_size"`
	MinIdleConns int    `yaml:"min_idle_conns"`
}

// NewRedisClient 创建 Redis 客户端
func NewRedisClient(cfg Config) (*redis.Client, error) {
	password := cfg.Password
	if password == "" {
		password = os.Getenv("REDIS_PASSWORD")
	}

	rdb := redis.NewClient(&redis.Options{
		Addr:         cfg.Addr,
		Password:     password,
		DB:           cfg.DB,
		MaxRetries:   cfg.MaxRetries,
		DialTimeout:  time.Duration(cfg.DialTimeout) * time.Millisecond,
		ReadTimeout:  time.Duration(cfg.ReadTimeout) * time.Millisecond,
		WriteTimeout: time.Duration(cfg.WriteTimeout) * time.Millisecond,
		PoolSize:     cfg.PoolSize,
		MinIdleConns: cfg.MinIdleConns,
	})

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := rdb.Ping(ctx).Err(); err != nil {
		return nil, fmt.Errorf("Redis 连接失败: %w", err)
	}

	return rdb, nil
}
```
