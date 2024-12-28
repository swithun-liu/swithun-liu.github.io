---
title: ThreadPool
date: 2024-12-08 17:44:28
tags:
---

## 简易线程池实现

```kotlin
class SimpleThreadPool(threadSize: Int) {
    /** 1. 任务队列: 线程安全*/
    val taskQueue: BlockingQueue<Runnable> = LinkedBlockingQueue(10)

    /** 2. 所有线程: worker */
    val threads = ArrayList<SimpleThread>(threadSize)

    init {
        // 3 启动所有线程
        (1..threadSize).forEach { i: Int ->
            SimpleThread("swithun-task-thread-$i").also {
                it.start()
                threads.add(it)
            }
        }
    }

    fun execute(task: Runnable) {
        // 4 将任务放入“任务队列”
        taskQueue.put(task)
    }

    inner class SimpleThread(name: String) : Thread(name) {
        override fun run() {
            while (true) {
                // 5 每个线程都会不断的从“任务队列”中取任务 & 执行 & 哪个线程取到就在哪个线程执行
                val task: Runnable? = try {
                    taskQueue.take()
                } catch (e: Exception) {
                    println("swithun-xxxx taskQueue.take err : ${e.printStackTrace()}")
                    null
                }
                task?.run()
            }
        }
    }
}

fun main() {
    val pool = SimpleThreadPool(3)

    // 6 建立多个任务丢进线程池运行
    (1..5).forEach { i: Int ->
        try {
            pool.execute {
                println("swithun-xxxx pool.execute: [task: $i] in ${Thread.currentThread().name}")
            }
        } catch (e: Exception) {
            println("swithun-xxxx pool.execute err : ${e.printStackTrace()}")
        }
    }
}
```

```
swithun-xxxx pool.execute: [task: 2] in yes-task-thread-2
swithun-xxxx pool.execute: [task: 4] in yes-task-thread-2
swithun-xxxx pool.execute: [task: 5] in yes-task-thread-2
swithun-xxxx pool.execute: [task: 3] in yes-task-thread-3
swithun-xxxx pool.execute: [task: 1] in yes-task-thread-1
```

## ThreadPoolExecutor

### ctl: 状态&线程数

- 前3位用来表示状态
- 剩余位数用来表示线程数

```java
    private final AtomicInteger ctl = new AtomicInteger(ctlOf(RUNNING, 0));
    private static final int COUNT_BITS = Integer.SIZE - 3; // 32 - 3 = 29
    // (1 << 29) - 1 
    // = (1左移29位) - 1 
    // = 2^29 - 1 = 536870912 - 1 = 536870911 
    // = 0b11111111111111111111111111111
    // = 0b 0001 1111 1111 1111  1111 1111 1111 1111
    private static final int COUNT_MASK = (1 << COUNT_BITS) - 1; 

    // runState is stored in the high-order bits
    private static final int RUNNING    = -1 << COUNT_BITS;
    private static final int SHUTDOWN   =  0 << COUNT_BITS;
    private static final int STOP       =  1 << COUNT_BITS;
    private static final int TIDYING    =  2 << COUNT_BITS;
    private static final int TERMINATED =  3 << COUNT_BITS;
```

|31|30|29|28|...|0|
|-|-|-|-|-|-|
|state begin||state end|task count begin||task count end|


|state|||
|-|-|-|
|RUNNING    |1110 0000  0000 0000  0000 0000  0000 0000|-536870912|
|SHUTDOWN   |0000 0000  0000 0000  0000 0000  0000 0000|0|
|STOP       |0010 0000  0000 0000  0000 0000  0000 0000|536870912|
|TIDYING    |0100 0000  0000 0000  0000 0000  0000 0000|1073741824|
|TERMINATED |0110 0000  0000  0000 0000 0000  0000 0000|1610612736|

#### 状态转换

```java
     * RUNNING -> SHUTDOWN
     *    On invocation of shutdown()
     * (RUNNING or SHUTDOWN) -> STOP
     *    On invocation of shutdownNow()
     * SHUTDOWN -> TIDYING
     *    When both queue and pool are empty
     * STOP -> TIDYING
     *    When pool is empty
     * TIDYING -> TERMINATED
     *    When the terminated() hook method has completed
```

```mermaid
stateDiagram
classDef t1 fill:#FFB81C44
classDef t2 fill:#FF671F44
classDef t3 fill:#F04E9844
classDef t4 fill:#307FE244


[*] --> RUNNING
RUNNING --> SHUTDOWN: shutdown
SHUTDOWN --> STOP: shutdownNow
RUNNING --> STOP: shutdownNow
SHUTDOWN --> TIDING: 任务队列为空，线程数为0
STOP --> TIDING: 线程数为0
TIDING --> TERMINATED: terminated
TERMINATED --> [*]

class RUNNING t1
class SHUTDOWN t2
class STOP t3
class TIDING t4
```

### execute

核心线程：主力
非核心线程：临时工

```kotlin
if 线程数 < 核心线程池
    优先补充主力(addWorker)
else if 线程池运行中 && 提交任务到任务队列成功
    主力满了，优先放入队列等主力空闲
else if 新增非核心线程池失败
    等主力的队列满了，增加临时工处理任务(addWorker)
else 拒绝添加任务
```

### addWorker 添加工人(主力 or 临时工)

```kotlin
if 生命周期>SHUTDOWN
  拒绝
else if 生命周期=SHUTDOWN && 等待队列空了 (队列不空的时候还是允许增加工人去执行未执行的任务，只是不让继续增加任务了)
  拒绝
```

### workQueue

```java
    /**
     * The queue used for holding tasks and handing off to worker
     * threads.  We do not require that workQueue.poll() returning
     * null necessarily means that workQueue.isEmpty(), so rely
     * solely on isEmpty to see if the queue is empty (which we must
     * do for example when deciding whether to transition from
     * SHUTDOWN to TIDYING).  This accommodates special-purpose
     * queues such as DelayQueues for which poll() is allowed to
     * return null even if it may later return non-null when delays
     * expire.
     * 
     * 于存放任务并将其交给工作线程的队列。
     * 我们不要求 `workQueue.poll()` 返回 `null` 必然意味着 `workQueue.isEmpty()`，
     * 因此仅依赖 `isEmpty()` 来判断队列是否为空
     * （例如，在决定是否从 `SHUTDOWN` 状态过渡到 `TIDYING` 状态时，我们必须这样做）。
     * 这种做法适用于特殊用途的队列，例如 `DelayQueue`，在这些队列中，`poll()` 允许返回 `null`，
     * 即使稍后延迟过期时可能会返回非 `null` 的任务。
     */
    private final BlockingQueue<Runnable> workQueue;
```

### workQueue.offer

see [offer](slink@@@1735398709)

## 参考

- [如果你是 JDK 设计者，如何设计线程池？我跟面试官大战了三十个回合](https://juejin.cn/post/6968721240592744455)
- [ThreadPoolExecutor 源码解析(含流程图)](https://juejin.cn/post/6926471351452565512)