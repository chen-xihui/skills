# Java 客户端模板

## NacosConfigService.java（配置服务类）

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

## NacosDiscoveryService.java（服务发现类）

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

## bootstrap.yml

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

## Maven 依赖

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