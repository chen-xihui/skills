# REDISSON-005：禁止 watch dog 场景下无限等待

| 属性 | 说明 |
|------|------|
| 规则ID | REDISSON-005 |
| 风险等级 | 风险 |
| 规则描述 | tryLock 必须设置 leaseTime 或等待时间 |

## 问题说明

调用 `lock.tryLock()` 不带任何参数时，该调用会立即返回（waitTime=0, leaseTime=-1），但实际上不会等待获取锁。更常见的问题场景是调用 `lock.lock()` 或 `lock.tryLock(0, -1, TimeUnit.SECONDS)`，其中 leaseTime 为 -1 会触发 watch dog 机制无限续期。如果业务代码因死锁、死循环或未捕获异常而未能调用 `unlock()`，watch dog 将持续为锁续期，导致锁永远无法释放。

此外，在 `tryLock` 中只设置 waitTime 而不设置 leaseTime（如 `tryLock(10, -1, TimeUnit.SECONDS)`），同样会触发 watch dog，存在相同风险。必须同时设置 waitTime 和 leaseTime，确保锁在合理时间内自动释放。

## 检查方法

- 静态分析：搜索所有 `tryLock()` 调用，检查参数个数和值
- 检查 `tryLock()` 无参调用是否被替换为带参版本
- 检查 `tryLock(waitTime, -1, TimeUnit)` 模式（leaseTime 为 -1）
- 脚本化检查：`python scripts/check_redisson_005.py <项目根目录>`

## 违规示例

```java
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import java.util.concurrent.TimeUnit;

@Service
public class PaymentService {

    @Autowired
    private RedissonClient redissonClient;

    // 违规：无参 tryLock()，不会等待但可能被误解为等待获取锁
    public void processPaymentV1(String paymentId) {
        RLock lock = redissonClient.getLock("payment:lock:" + paymentId);
        try {
            boolean acquired = lock.tryLock(); // 违规：无参调用，语义不清
            if (acquired) {
                doProcess(paymentId);
            }
        } finally {
            if (lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }

    // 违规：leaseTime 为 -1，触发 watch dog 无限续期
    public void processPaymentV2(String paymentId) {
        RLock lock = redissonClient.getLock("payment:lock:" + paymentId);
        try {
            // waitTime=10 但 leaseTime=-1，watch dog 永久续期
            boolean acquired = lock.tryLock(10, -1, TimeUnit.SECONDS);
            if (acquired) {
                doProcess(paymentId);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            if (lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }

    private void doProcess(String paymentId) {
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
public class PaymentService {

    private static final long LOCK_WAIT_TIME = 10;
    private static final long LOCK_LEASE_TIME = 30;

    @Autowired
    private RedissonClient redissonClient;

    public void processPayment(String paymentId) {
        RLock lock = redissonClient.getLock("payment:lock:" + paymentId);
        try {
            // 合规：同时设置 waitTime 和 leaseTime
            // waitTime=10 秒内等待获取锁，leaseTime=30 秒后锁自动释放
            boolean acquired = lock.tryLock(LOCK_WAIT_TIME, LOCK_LEASE_TIME, TimeUnit.SECONDS);
            if (!acquired) {
                throw new BusinessException("获取支付锁失败，请稍后重试");
            }
            doProcess(paymentId);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new BusinessException("获取锁被中断", e);
        } finally {
            if (lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }

    private void doProcess(String paymentId) {
        // 业务逻辑
    }
}
```
