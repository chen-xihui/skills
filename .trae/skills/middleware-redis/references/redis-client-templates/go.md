# Redis Go 客户端代码模板

本文件包含 Go 语言 Redis 客户端的代码模板。

---

## 1. Go + go-redis + Standalone

### 1.1 redis.go

```go
package redis

import (
    "context"
    "fmt"
    "os"
    "time"

    "github.com/redis/go-redis/v9"
)

var ctx = context.Background()

var rdb *redis.Client

// InitRedis 初始化 Redis 连接
func InitRedis() error {
    host := os.Getenv("REDIS_HOST")
    if host == "" {
        host = "localhost"
    }
    port := os.Getenv("REDIS_PORT")
    if port == "" {
        port = "6379"
    }
    password := os.Getenv("REDIS_PASSWORD")

    rdb = redis.NewClient(&redis.Options{
        Addr:         fmt.Sprintf("%s:%s", host, port),
        Password:     password,
        DB:           0,
        DialTimeout:  5 * time.Second,
        ReadTimeout:  3 * time.Second,
        WriteTimeout: 3 * time.Second,
        PoolSize:     20,       // maxTotal（REDIS-004）
        MinIdleConns: 5,        // minIdle
        MaxConnAge:   30 * time.Minute,
        PoolTimeout:  3 * time.Second,  // maxWaitMillis
        PoolFIFO:     false,
    })

    // 测试连接
    if err := rdb.Ping(ctx).Err(); err != nil {
        return fmt.Errorf("redis ping error: %w", err)
    }

    return nil
}

// GetRedisClient 获取 Redis 客户端
func GetRedisClient() *redis.Client {
    return rdb
}

// CloseRedis 关闭 Redis 连接
func CloseRedis() error {
    if rdb != nil {
        return rdb.Close()
    }
    return nil
}
```

### 1.2 service.go

```go
package redis

import (
    "context"
    "fmt"
    "time"

    "github.com/redis/go-redis/v9"
)

// Set 设置值（含过期时间，REDIS-007）
func Set(key string, value interface{}, expiration time.Duration) error {
    return rdb.Set(ctx, key, value, expiration).Err()
}

// Get 获取值
func Get(key string) (string, error) {
    return rdb.Get(ctx, key).Result()
}

// Delete 删除 Key
func Delete(key string) error {
    return rdb.Del(ctx, key).Err()
}

// SetWithExpiry 设置带过期时间的值
func SetWithExpiry(key string, value interface{}, ttl time.Duration) error {
    return rdb.Set(ctx, key, value, ttl).Err()
}

// ScanKeys 使用 scan 替代 keys（REDIS-001）
func ScanKeys(pattern string) ([]string, error) {
    var keys []string
    cursor := uint64(0)
    count := int64(100)

    for {
        var batch []string
        var err error
        batch, cursor, err = rdb.Scan(ctx, cursor, pattern, count).Result()
        if err != nil {
            return nil, fmt.Errorf("redis scan error: %w", err)
        }
        keys = append(keys, batch...)
        if cursor == 0 {
            break
        }
    }

    return keys, nil
}

// PipelineExec 使用 Pipeline 批量执行（REDIS-005）
func PipelineExec(fn func(*redis.Pipeline) error) ([]redis.Cmder, error) {
    pipe := rdb.Pipeline()
    if err := fn(pipe); err != nil {
        return nil, err
    }
    return pipe.Exec(ctx)
}

// Expire 设置过期时间
func Expire(key string, ttl time.Duration) error {
    return rdb.Expire(ctx, key, ttl).Err()
}
```

### 1.3 main.go（示例）

```go
package main

import (
    "fmt"
    "log"
    "os"
    "time"

    "your/module/redis"
)

func main() {
    // 初始化 Redis
    if err := redis.InitRedis(); err != nil {
        log.Fatalf("Failed to init Redis: %v", err)
    }
    defer redis.CloseRedis()

    // 设置值
    key := "example:key"
    value := "hello, redis"
    if err := redis.Set(key, value, 10*time.Minute); err != nil {
        log.Fatalf("Failed to set key: %v", err)
    }

    // 获取值
    result, err := redis.Get(key)
    if err != nil {
        log.Fatalf("Failed to get key: %v", err)
    }
    fmt.Printf("Value: %s\n", result)

    // 使用 Pipeline 批量设置
    cmds, err := redis.PipelineExec(func(pipe *redis.Pipeline) error {
        pipe.Set(ctx, "batch:key1", "value1", 5*time.Minute)
        pipe.Set(ctx, "batch:key2", "value2", 5*time.Minute)
        pipe.Set(ctx, "batch:key3", "value3", 5*time.Minute)
        return nil
    })
    if err != nil {
        log.Fatalf("Pipeline error: %v", err)
    }
    for _, cmd := range cmds {
        fmt.Println(cmd.Err())
    }

    // 使用 scan 查找 Key
    keys, err := redis.ScanKeys("batch:*")
    if err != nil {
        log.Fatalf("Scan error: %v", err)
    }
    fmt.Printf("Found keys: %v\n", keys)
}
```

### 1.4 go.mod 依赖

```go
module your/module

go 1.21

require (
    github.com/redis/go-redis/v9 v9.0.5
)
```

---

## 2. Go + go-redis + Cluster

### 2.1 redis_cluster.go

```go
package redis

import (
    "context"
    "fmt"
    "os"
    "strings"
    "time"

    "github.com/redis/go-redis/v9"
)

var clusterRdb *redis.ClusterClient

// InitRedisCluster 初始化 Redis 集群连接
func InitRedisCluster() error {
    nodesEnv := os.Getenv("REDIS_CLUSTER_NODES")
    if nodesEnv == "" {
        return fmt.Errorf("REDIS_CLUSTER_NODES environment variable is required")
    }

    nodes := strings.Split(nodesEnv, ",")
    var addrs []string
    for _, node := range nodes {
        addrs = append(addrs, strings.TrimSpace(node))
    }

    password := os.Getenv("REDIS_PASSWORD")

    clusterRdb = redis.NewClusterClient(&redis.ClusterOptions{
        Addrs:        addrs,
        Password:     password,
        DialTimeout:  5 * time.Second,
        ReadTimeout:  3 * time.Second,
        WriteTimeout: 3 * time.Second,
        PoolSize:     20,
        MinIdleConns: 5,
        PoolTimeout:  3 * time.Second,
        MaxRedirects: 3,
    })

    // 测试连接
    if err := clusterRdb.Ping(ctx).Err(); err != nil {
        return fmt.Errorf("redis cluster ping error: %w", err)
    }

    return nil
}

// GetClusterClient 获取集群客户端
func GetClusterClient() *redis.ClusterClient {
    return clusterRdb
}

// CloseCluster 关闭集群连接
func CloseCluster() error {
    if clusterRdb != nil {
        return clusterRdb.Close()
    }
    return nil
}
```

### 2.2 环境变量配置

```bash
# 集群节点地址（逗号分隔）
export REDIS_CLUSTER_NODES="node1:6379,node2:6379,node3:6379"
# 密码
export REDIS_PASSWORD="your_password_here"
```

---

## 3. Go + go-redis + Sentinel

### 3.1 redis_sentinel.go

```go
package redis

import (
    "context"
    "fmt"
    "os"
    "strings"
    "time"

    "github.com/redis/go-redis/v9"
)

var sentinelRdb *redis.Client

// InitRedisSentinel 初始化 Redis Sentinel 连接
func InitRedisSentinel() error {
    sentinelNodesEnv := os.Getenv("REDIS_SENTINEL_NODES")
    if sentinelNodesEnv == "" {
        return fmt.Errorf("REDIS_SENTINEL_NODES environment variable is required")
    }

    masterName := os.Getenv("REDIS_SENTINEL_MASTER")
    if masterName == "" {
        masterName = "mymaster"
    }

    nodes := strings.Split(sentinelNodesEnv, ",")
    var sentinelAddrs []string
    for _, node := range nodes {
        sentinelAddrs = append(sentinelAddrs, strings.TrimSpace(node))
    }

    password := os.Getenv("REDIS_PASSWORD")

    sentinelRdb = redis.NewFailoverClient(&redis.FailoverOptions{
        MasterName:     masterName,
        SentinelAddrs:  sentinelAddrs,
        Password:       password,
        DialTimeout:    5 * time.Second,
        ReadTimeout:    3 * time.Second,
        WriteTimeout:   3 * time.Second,
        PoolSize:       20,
        MinIdleConns:   5,
        PoolTimeout:    3 * time.Second,
    })

    // 测试连接
    if err := sentinelRdb.Ping(ctx).Err(); err != nil {
        return fmt.Errorf("redis sentinel ping error: %w", err)
    }

    return nil
}

// GetSentinelClient 获取 Sentinel 客户端
func GetSentinelClient() *redis.Client {
    return sentinelRdb
}

// CloseSentinel 关闭 Sentinel 连接
func CloseSentinel() error {
    if sentinelRdb != nil {
        return sentinelRdb.Close()
    }
    return nil
}
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
- **连接池参数**：`PoolSize` 应小于 200，`PoolTimeout` 禁止使用默认值 0（REDIS-004）
- **Key 命名**：使用 `项目名:业务模块:Key` 格式（REDIS-012）
- **过期时间**：所有 Key 必须设置过期时间（REDIS-007）
- **禁止命令**：不在生产环境使用 `KEYS`、`FLUSHALL`、`FLUSHDB` 等高危险命令（REDIS-001、REDIS-009、REDIS-010）