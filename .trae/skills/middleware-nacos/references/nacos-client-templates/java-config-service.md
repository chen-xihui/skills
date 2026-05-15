# Java 模板：NacosConfigService.java

配置服务类，含本地快照启用、Listener 配置变更监听、长轮询超时设置。

生成目标文件：`NacosConfigService.java`

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
