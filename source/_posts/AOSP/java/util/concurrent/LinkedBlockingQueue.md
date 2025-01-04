---
title: LinkedBlockingQueue
date: 2024-12-28 23:10:18
tags:
---
    

##  [offer](begin@@@1735398709)

```java
    final AtomicInteger count = this.count;

    private final ReentrantLock putLock = new ReentrantLock();

    public boolean offer(E e) {
        ...
        // 1. 已经满了，返回false
        if (count.get() == capacity)
            return false;
        // 2. 还没满
        final int c;
        // 3. 创建"队员"
        final Node<E> node = new Node<E>(e);
        // 4. 即将操作入队，先加个put锁(不用管take锁，巧妙设计从而添加和删除可以并发)
        putLock.lock();
        try {
        // 5. 加锁后再次检查，防止加锁期间被别的线程截胡
            if (count.get() == capacity)
                return false;
            // 6. 执行入队
            enqueue(node);
            c = count.getAndIncrement();
            if (c + 1 < capacity)
                notFull.signal();
            }
        } finally {
            // 8. 释放锁
            putLock.unlock();
        }
        if (c == 0)
            signalNotEmpty();
        return true;
    }
```
(end@@@1735398709)


## 参考

- [深入理解Java线程池，剖析LinkedBlockingQueue源码实现](https://juejin.cn/post/7329280514627665961?searchId=202412282306309B05CE6FC1DEE9F99437)