# Java 模板：NacosDiscoveryService.java

服务发现类，含注册/注销/查询实例方法。

生成目标文件：`NacosDiscoveryService.java`

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
