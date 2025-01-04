---
title: Activity的启动流程
date: 2024-03-10 17:59:40
tags:
---

## startActivity

```mermaid
sequenceDiagram
autonumber

box green App进程
participant Activity
participant Instrumentation
participant IActivityTaskManager
participant ApplicationThread
participant ActivityThread
participant ActivityThread.H
participant TransactionExecutor
end

box rgba(33,66,99,0.5) AMS
participant ActivityTaskManagerService
participant ActivityStarter
participant ActivityRecord
participant RootWindowContainer
participant Task
participant TaskFragment
participant ActivityTaskSupervisor
participant ClientTransaction
participant ClientLifecycleManager
end

note over Instrumentation: 负责Application<br>和Activity的<br>创建和生命周期控制
note over IActivityTaskManager: AMS 在 App 进程的 <br> IBinder 接口 (IActivityManager)
note over ActivityTaskManagerService: System service <br>for managing activities<br> and their containers <br>(task, stacks, displays,... ).
note over ActivityStarter: 专门负责<br>一个 Activity 的启动操作。<br> 它的主要作用包括<br>解析 Intent、<br>创建 ActivityRecord、<br>如果有可能<br>还要创建 TaskRecord
note over ActivityRecord: 描述Activity相关信息, <br>一个Activity对应<br>一个ActivityRecord
note over ClientTransaction: 一种容器，<br>用于保存一系列<br>需要发送给 <br>App 进程的消息。<br>这些消息包括 <br>callbacks <br>和最终的<br>生命周期状态

Activity ->> Activity: startActivity
activate Activity
Activity ->> Activity: startActivityForResult
activate Activity
Activity ->> Instrumentation: execStartActivity
note over Activity, Instrumentation: Context who: 正在启动该Activity的上下文<br>Ibinder contextThread: 启动该Activity的上下文线程(ApplicationThread)<br>IBinder token: 启动该Activity的标识<br>Activity target: 启动该Activity的 Activity
activate Instrumentation
Instrumentation ->> IActivityTaskManager: startActivity
note over IActivityTaskManager,ActivityTaskManagerService: 跨进程调用
IActivityTaskManager ->> ActivityTaskManagerService: startActivity
activate ActivityTaskManagerService
ActivityTaskManagerService ->> ActivityTaskManagerService: startActivityAsUser
note right of ActivityTaskManagerService: 构造ActivityStarter
ActivityTaskManagerService ->> ActivityStarter: execute
activate ActivityStarter
ActivityStarter ->> ActivityStarter: executeRequest
ActivityStarter ->> ActivityRecord: new
ActivityStarter ->> ActivityStarter: startActivityUnchecked
ActivityStarter ->> ActivityStarter: startActivityInner
ActivityStarter ->> RootWindowContainer: resumeFocusedTasksTopActivities
activate RootWindowContainer
RootWindowContainer ->> Task: resumeTopActivityUncheckedLocked
activate Task
Task ->> Task: resumeTopActivityInnerLocked
Task ->> TaskFragment: resumeTopActivity
activate TaskFragment
TaskFragment ->> ActivityTaskSupervisor: startSpecificActivity
activate ActivityTaskSupervisor
ActivityTaskSupervisor ->> ClientTransaction: new
ActivityTaskSupervisor ->> ClientLifecycleManager: scheduleTransaction
activate ClientLifecycleManager
note over ClientLifecycleManager,ApplicationThread: 跨进程调用
ClientLifecycleManager ->> ApplicationThread: scheduleTransaction
activate ApplicationThread
ApplicationThread ->> ActivityThread: scheduleTransaction
ActivityThread->> ActivityThread.H: handleMessage
activate ActivityThread.H
ActivityThread.H ->> TransactionExecutor: execute
activate TransactionExecutor
TransactionExecutor ->> TransactionExecutor: executeCallbacks
TransactionExecutor ->> TransactionExecutor: cycleToPath
TransactionExecutor ->> TransactionExecutor: performLifecycleSequence
TransactionExecutor ->> TransactionExecutor: handleLaunchActivity
deactivate TransactionExecutor
deactivate ActivityThread.H
deactivate ApplicationThread
deactivate ClientLifecycleManager
deactivate ActivityTaskSupervisor
deactivate TaskFragment
deactivate Task
deactivate RootWindowContainer
deactivate ActivityStarter
deactivate ActivityTaskManagerService
deactivate Instrumentation
deactivate Activity
deactivate Activity
```


## handleLaunchActivity

```mermaid
sequenceDiagram
autonumber
rect rgba(191, 223, 255, .1) 
    rect rgba(191, 223, 255, .1) 
        ActivityThread ->> ActivityThread: handleLaunchActivity
        rect rgba(191, 223, 255, .1) 
            ActivityThread ->> ActivityThread: performLaunchActivity
            ActivityThread ->> ActivityThread: [for Activity.attach()方法]<br>createBaseContextForActivity<br>(创建Activity的base Context)
            ActivityThread ->> Instrumentation: newActivity
            rect rgba(191, 223, 255, .1) 
                ActivityThread ->> Activity: attach()
                Activity ->> Activity: attachBaseContext(mBase = base)
                Activity ->> +Activity: 新建PhoneWindow赋值给Activity.mWindow
                rect rgba(191, 223, 255, .1) 
                    Activity ->> Activity: 给Activity.mWindow设置WindowManager
                    Activity ->> ContextImpl: getSystemService(Context.WINDOW_SERVICE)
                    ContextImpl ->> SystemServiceRegistry: getSystemService<br>(Activity是Context)
                    note over SystemServiceRegistry: SystemServiceRegistry是单例<br>SystemServiceRegistry的静态方法会执行registerService，<br>其中就包括Context.WINDOW_SERVICE对应的Fetcher<br>(Fetcher以Context为维度对实际的Service做了缓存<br>这里是工厂模式，可以将<br>Fetcher理解为Factory<br>通过Fetcher获取到真正的Service<br>而WINDOW_SERVICE对应的真正的Service<br>则是WindowManager)
                    SystemServiceRegistry ->> Activity: return WindowManager
                    Activity ->> Window: setWindowManger(return的WindowManger)<br>(这里的指Activity.mWindow)
                    Window ->> WindowManagerImpl: createLocalWindowManager
                    WindowManagerImpl ->> Window: return WindowManagerImpl
                    Window ->> Window: mWindowManager = 前面return的WindowManagerImpl
                    Activity ->> -Window: setWindowManager
                end
            end
        end
    end
end
rect rgba(191, 223, 255, .1) 
ActivityThread ->> Instrumentation: mInstrumentation.callActivityOnCreate
Instrumentation ->> Activity: performCreate
Activity ->> Activity: onCreate
end
```

## setContentView

```mermaid
sequenceDiagram
Activity ->> Window: setContentView
Window ->> PhoneWindow: (impl) setContentView
rect rgba(191, 223, 255, .1) 
    PhoneWindow ->> PhoneWindow: installDecor
    Note right of PhoneWindow: 初始化 mDecor <br> new DecorView()
    rect rgba(191, 223, 255, .1) 
        PhoneWindow ->> DecoreView: mDecor = generateDecor(-1)
    end
    rect rgba(191, 223, 255, .1) 
        PhoneWindow ->> PhoneWindow: mContentParent = generateLayout(mDecor)
        Note right of PhoneWindow: generateDecor(-1)只是new了DecorView<br>平时我们看到的系统-定义布局中<br>DecorView下面一般还有一些默认的layout<br>这一步就是根据你设置的window theme<br>选取不同的layout resource并且inflate并且add到DecorView中<br>不同的layout resource一定都有一个id为content的layout<br>用来添加用户(开发者)定义的具体内容布局<br>contentParent最终返回的也就是id为content的layout
        PhoneWindow ->> ViewGroup: mContentParent.addView(传入的view)
    end
end
```

## 参考

- [Android窗口机制（一）初识Android的窗口结构](https://www.jianshu.com/p/40a9c93b5a8d)
- [Android -- Activity启动过程中的上下文环境初始化分析](https://blog.csdn.net/csdn_of_coder/article/details/78147399)
- [Android 11源码分析： Activity的启动流程](https://juejin.cn/post/6994823348190445604#heading-1)
- [【Android 14源码分析】Activity启动流程-1](https://juejin.cn/post/7340301649766727721)
- [Activity 启动的整体流程](https://juejin.cn/post/6990297933790838798?searchId=20241027121056BD6132D4CC1C5176D170)
- [Android activity 启动流程](https://juejin.cn/post/7429188498850037795?searchId=20241201200856B3BFAC4094BECA3B7711)