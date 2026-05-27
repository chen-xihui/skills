package com.example.redis.service;

import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

/**
 * 分布式锁服务
 */
@Service
public class DistributedLockService {

    private final RedissonClient redissonClient;

    @Autowired
    public DistributedLockService(RedissonClient redissonClient) {
        this.redissonClient = redissonClient;
    }

    /**
     * 获取分布式锁
     * @param lockKey 锁 key
     * @param waitTime 最大等待时间
     * @param leaseTime 锁持有时间
     * @return 是否获取成功
     */
    public boolean tryLock(String lockKey, long waitTime, long leaseTime) {
        RLock lock = redissonClient.getLock(lockKey);
        try {
            return lock.tryLock(waitTime, leaseTime, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        }
    }

    /**
     * 释放锁
     * @param lockKey 锁 key
     */
    public void unlock(String lockKey) {
        RLock lock = redissonClient.getLock(lockKey);
        if (lock.isHeldByCurrentThread()) {
            lock.unlock();
        }
    }

    /**
     * 执行业务逻辑（自动加锁/释放）
     * @param lockKey 锁 key
     * @param waitTime 最大等待时间
     * @param leaseTime 锁持有时间
     * @param action 业务逻辑
     * @return 是否执行成功
     */
    public boolean executeWithLock(String lockKey, long waitTime, long leaseTime, Runnable action) {
        if (tryLock(lockKey, waitTime, leaseTime)) {
            try {
                action.run();
                return true;
            } finally {
                unlock(lockKey);
            }
        }
        return false;
    }
}
