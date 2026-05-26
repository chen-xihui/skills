# Go 客户端模板

## nacos_client.go

```go
package nacos

import (
    "fmt"
    "os"

    "github.com/nacos-group/nacos-sdk-go/v2/clients"
    "github.com/nacos-group/nacos-sdk-go/v2/clients/config_client"
    "github.com/nacos-group/nacos-sdk-go/v2/clients/naming_client"
    "github.com/nacos-group/nacos-sdk-go/v2/common/constant"
    "github.com/nacos-group/nacos-sdk-go/v2/model"
    "github.com/nacos-group/nacos-sdk-go/v2/vo"
)

// Config Nacos 连接配置
type Config struct {
    ServerAddr string `yaml:"server_addr"`
    Namespace  string `yaml:"namespace"`
    Username   string `yaml:"username"`
    Password   string `yaml:"password"` // 通过环境变量注入
}

// Client Nacos 客户端封装
type Client struct {
    configClient  config_client.IConfigClient
    namingClient  naming_client.INamingClient
    namespace     string
}

// NewClient 创建 Nacos 客户端
func NewClient(cfg Config) (*Client, error) {
    password := cfg.Password
    if password == "" {
        password = os.Getenv("NACOS_PASSWORD")
    }

    serverConfigs := []constant.ServerConfig{
        {
            IpAddr: cfg.ServerAddr,
            Port:   8848,
        },
    }

    clientConfig := constant.ClientConfig{
        NamespaceId:         cfg.Namespace,
        Username:            cfg.Username,
        Password:            password,
        EnableLocalSnapshot: true, // NACOS-001：启用本地快照
    }

    // 创建配置客户端
    configClient, err := clients.NewConfigClient(
        vo.NacosClientParam{
            ClientConfig:  &clientConfig,
            ServerConfigs: serverConfigs,
        },
    )
    if err != nil {
        return nil, fmt.Errorf("创建 Nacos 配置客户端失败: %w", err)
    }

    // 创建命名客户端
    namingClient, err := clients.NewNamingClient(
        vo.NacosClientParam{
            ClientConfig:  &clientConfig,
            ServerConfigs: serverConfigs,
        },
    )
    if err != nil {
        return nil, fmt.Errorf("创建 Nacos 命名客户端失败: %w", err)
    }

    return &Client{
        configClient: configClient,
        namingClient: namingClient,
        namespace:    cfg.Namespace,
    }, nil
}

// RegisterService 注册服务实例
func (c *Client) RegisterService(serviceName, ip string, port uint64) error {
    _, err := c.namingClient.RegisterInstance(vo.RegisterInstanceParam{
        ServiceName: serviceName,
        Ip:          ip,
        Port:        port,
        Weight:      1.0, // NACOS-005：默认权重
        Enable:      true,
        Healthy:     true,
    })
    return err
}

// DeregisterService 注销服务实例
func (c *Client) DeregisterService(serviceName, ip string, port uint64) error {
    _, err := c.namingClient.DeregisterInstance(vo.DeregisterInstanceParam{
        ServiceName: serviceName,
        Ip:          ip,
        Port:        port,
    })
    return err
}

// GetInstances 获取服务实例列表
func (c *Client) GetInstances(serviceName string) ([]model.Instance, error) {
    instances, err := c.namingClient.SelectInstances(vo.SelectInstancesParam{
        ServiceName: serviceName,
        HealthyOnly: true,
    })
    return instances, err
}

// GetConfig 获取配置（NACOS-003：建议使用 Listener 监听而非循环调用）
func (c *Client) GetConfig(dataId, group string) (string, error) {
    return c.configClient.GetConfig(vo.ConfigParam{
        DataId: dataId,
        Group:  group,
    })
}

// ListenConfig 监听配置变更（推荐方式）
func (c *Client) ListenConfig(dataId, group string, onChange func(content string)) error {
    return c.configClient.ListenConfig(vo.ConfigParam{
        DataId:   dataId,
        Group:    group,
        OnChange: func(namespace, group, dataId, content string) {
            onChange(content)
        },
    })
}
```

## config.yaml

```yaml
nacos:
  server_addr: "${NACOS_SERVER_ADDR:localhost}"
  namespace: "${NACOS_NAMESPACE:}"
  username: "${NACOS_USERNAME:nacos}"
  password: "${NACOS_PASSWORD}"  # 通过环境变量注入，禁止明文
```