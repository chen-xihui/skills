# Nacos 客户端代码模板

本文件包含 Nacos 客户端的代码模板，供智能体在执行客户端创建时参考。

---

## 1. Java 客户端模板

### 1.1 NacosConfigService.java（配置服务类）

```java
package com.example.nacos.config;

import com.alibaba.nacos.api.config.ConfigService;
import com.alibaba.nacos.api.config.ConfigFactory;
import com.alibaba.nacos.api.config.listener.Listener;
import com.alibaba.nacos.api.exception.NacosException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Properties;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

@Configuration
public class NacosConfigService {

    private static final Logger log = LoggerFactory.getLogger(NacosConfigService.class);

    @Value("${nacos.server-addr}")
    private String serverAddr;

    @Value("${nacos.namespace}")
    private String namespace;

    @Value("${nacos.username}")
    private String username;

    @Value("${nacos.password}")
    private String password;

    @Value("${nacos.config.data-id:application.yml}")
    private String dataId;

    @Value("${nacos.config.group:DEFAULT_GROUP}")
    private String group;

    @Value("${nacos.config.timeout:30000}")
    private long timeout;

    @Bean
    public ConfigService nacosConfigService() throws NacosException {
        Properties properties = new Properties();
        properties.put("serverAddr", serverAddr);
        properties.put("namespace", namespace);
        properties.put("username", username);
        properties.put("password", password);
        // 启用本地快照（NACOS-001）
        properties.put("enableLocalSnapshot", "true");
        // 长轮询超时（NACOS-002，建议 ≤ 30s）
        properties.put("configLongPollTimeout", "30000");

        ConfigService configService = ConfigFactory.createConfigService(properties);

        // 使用 Listener 监听配置变更（NACOS-003：避免循环调用 getConfig）
        configService.addListener(dataId, group, new Listener() {
            @Override
            public Executor getExecutor() {
                return Executors.newSingleThreadExecutor();
            }

            @Override
            public void receiveConfigInfo(String configInfo) {
                log.info("Nacos 配置变更通知: dataId={}, group={}", dataId, group);
                // 处理配置变更逻辑
            }
        });

        log.info("Nacos ConfigService 初始化完成, serverAddr={}", serverAddr);
        return configService;
    }
}
```

### 1.2 NacosDiscoveryService.java（服务发现类）

```java
package com.example.nacos.service;

import com.alibaba.nacos.api.exception.NacosException;
import com.alibaba.nacos.api.naming.NamingService;
import com.alibaba.nacos.api.naming.pojo.Instance;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NacosDiscoveryService {

    private static final Logger log = LoggerFactory.getLogger(NacosDiscoveryService.class);

    @Autowired
    private NamingService namingService;

    /**
     * 注册服务实例
     */
    public void registerInstance(String serviceName, String ip, int port) throws NacosException {
        namingService.registerInstance(serviceName, ip, port);
        log.info("服务注册成功: serviceName={}, ip={}, port={}", serviceName, ip, port);
    }

    /**
     * 注销服务实例
     */
    public void deregisterInstance(String serviceName, String ip, int port) throws NacosException {
        namingService.deregisterInstance(serviceName, ip, port);
        log.info("服务注销成功: serviceName={}, ip={}, port={}", serviceName, ip, port);
    }

    /**
     * 查询服务实例列表
     */
    public List<Instance> getAllInstances(String serviceName) throws NacosException {
        return namingService.getAllInstances(serviceName);
    }

    /**
     * 查询健康的服务实例
     */
    public List<Instance> selectInstances(String serviceName, boolean healthy) throws NacosException {
        return namingService.selectInstances(serviceName, healthy);
    }

    /**
     * 选择一个健康的服务实例（负载均衡）
     */
    public Instance selectOneHealthyInstance(String serviceName) throws NacosException {
        return namingService.selectOneHealthyInstance(serviceName);
    }
}
```

### 1.3 bootstrap.yml

```yaml
spring:
  application:
    name: ${APP_NAME:demo-service}
  cloud:
    nacos:
      server-addr: ${NACOS_SERVER_ADDR:localhost:8848}
      username: ${NACOS_USERNAME:nacos}
      password: ${NACOS_PASSWORD}  # 通过环境变量注入，禁止明文
      namespace: ${NACOS_NAMESPACE:}
      discovery:
        enabled: true
        namespace: ${NACOS_NAMESPACE:}
        group: DEFAULT_GROUP
        heart-beat-interval: 5000    # 心跳间隔（NACOS-005）
        heart-beat-timeout: 15000
        weight: 1.0                  # 权重（NACOS-005）
      config:
        enabled: true
        namespace: ${NACOS_NAMESPACE:}
        group: DEFAULT_GROUP
        data-id: application.yml
        refresh-enabled: true
        file-extension: yml
```

### 1.4 Maven 依赖

```xml
<dependencies>
    <!-- Spring Cloud Alibaba Nacos -->
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        <version>2023.0.1.0</version>
    </dependency>
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
        <version>2023.0.1.0</version>
    </dependency>
    <!-- Nacos Client -->
    <dependency>
        <groupId>com.alibaba.nacos</groupId>
        <artifactId>nacos-client</artifactId>
        <version>2.3.2</version>
    </dependency>
</dependencies>
```

---

## 2. Go 客户端模板

### 2.1 nacos_client.go

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

### 2.2 config.yaml

```yaml
nacos:
  server_addr: "${NACOS_SERVER_ADDR:localhost}"
  namespace: "${NACOS_NAMESPACE:}"
  username: "${NACOS_USERNAME:nacos}"
  password: "${NACOS_PASSWORD}"  # 通过环境变量注入，禁止明文
```

---

## 3. Python 客户端模板

### 3.1 nacos_client.py

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

### 3.2 config.yaml

```yaml
nacos:
  server_addresses: "localhost:8848"
  namespace: ""
  username: "nacos"
  password: "${NACOS_PASSWORD}"  # 通过环境变量注入，禁止明文
```

### 3.3 Pip 依赖

```
nacos-sdk-python>=1.0.0
```
