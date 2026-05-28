# REDISSON-001：分布式锁必须设置 leaseTime

| 属性 | 说明 |
|------|------|
| 规则ID | REDISSON-001 |
| 风险等级 | 严重 |
| 规则描述 | lock() 必须设置 leaseTime 参数，防止锁永久持有 |

## 问题说明

调用 `lock.lock()` 不带 leaseTime 参数时，Redisson 会启用 watch dog 机制自动续期（默认每 10 秒续期一次，锁持有时间 30 秒）。如果持有锁的节点发生宕机、进程被 kill 或发生 OOM，watch dog 线程随之消亡，但此时锁可能尚未过期（取决于续期时机），存在短暂窗口期。更严重的是，如果业务代码因异常未执行 `unlock()`，watch dog 将持续续期，导致锁永远无法释放，其他节点无法获取锁，造成业务永久阻塞。

## 检查方法

- 静态分析：搜索所有 `lock.lock()` 调用，检查是否包含 leaseTime 参数
- 检查 `lock()` 调用是否仅传入了 `leaseTime` 和 `TimeUnit` 两个参数
- 检查 `tryLock()` 是否同时设置了 waitTime 和 leaseTime
- 脚本化检查：`python scripts/check_redisson_001.py <项目根目录>`

## 违规示例

```java
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import java.util.concurrent.TimeUnit;

@Service
public class OrderService {

    @Autowired
    private RedissonClient redissonClient;

    public void processOrder(String orderId) {
        RLock lock = redissonClient.getLock("order:lock:" + orderId);
        try {
            // 违规：未设置 leaseTime，依赖 watch dog 自动续期
            // 若业务异常未 unlock()，锁将永远无法释放
            lock.lock();
            doProcess(orderId);
        } finally {
            lock.unlock();
        }
    }

    private void doProcess(String orderId) {
        // 业务逻辑
    }
}
```

## 合规示例

```java
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import java.util.concurrent.TimeUnit;

@Service
public class OrderService {

    private static final long LOCK_LEASE_TIME = 30;
    private static final long LOCK_WAIT_TIME = 10;

    @Autowired
    private RedissonClient redissonClient;

    public void processOrder(String orderId) {
        RLock lock = redissonClient.getLock("order:lock:" + orderId);
        try {
            // 合规：使用 lock(leaseTime, TimeUnit) 显式设置持有时间
            lock.lock(LOCK_LEASE_TIME, TimeUnit.SECONDS);
            doProcess(orderId);
        } finally {
            if (lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }

    public void processOrderWithTryLock(String orderId) {
        RLock lock = redissonClient.getLock("order:lock:" + orderId);
        try {
            // 合规：使用 tryLock(waitTime, leaseTime, TimeUnit) 同时设置等待时间和持有时间
            boolean acquired = lock.tryLock(LOCK_WAIT_TIME, LOCK_LEASE_TIME, TimeUnit.SECONDS);
            if (!acquired) {
                throw new BusinessException("获取锁失败，订单正在处理中");
            }
            doProcess(orderId);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new BusinessException("获取锁被中断", e);
        } finally {
            if (lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }

    private void doProcess(String orderId) {
        // 业务逻辑
    }
}
```
