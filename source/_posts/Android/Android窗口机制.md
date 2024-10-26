---
title: Android窗口机制
date: 2024-03-10 17:59:40
tags:
---


![alt text](./Android窗口机制/image.png)


## startActivity

```mermaid
sequenceDiagram
Activity -> Activity: startActivity
activate Activity
Activity -> Activity: startActivityForResult
activate Activity
Activity -> Instrumentation: execStartActivity
note right of Instrumentation: 负责Application<br>和Activity的<br>创建和生命周期控制
activate Instrumentation
note right of Instrumentation: 夸进程调用
Instrumentation -> ActivityTaskManagerService: startActivity
activate ActivityTaskManagerService
ActivityTaskManagerService -> ActivityTaskManagerService: startActivityAsUser
note right of ActivityTaskManagerService: 构造ActivityStarter
ActivityTaskManagerService -> ActivityStarter: execute
note right of ActivityStarter: 专门负责<br>一个 Activity 的启动操作。<br> 它的主要作用包括<br>解析 Intent、<br>创建 ActivityRecord、<br>如果有可能<br>还要创建 TaskRecord
activate ActivityStarter
ActivityStarter -> ActivityStarter: executeRequest
ActivityStarter -> ActivityRecord: new
ActivityStarter -> ActivityStarter: startActivityUnchecked
ActivityStarter -> ActivityStarter: startActivityInner
ActivityStarter -> RootWindowContainer: resumeFocusedTasksTopActivities
activate RootWindowContainer
RootWindowContainer -> Task: resumeTopActivityUncheckedLocked
activate Task
Task -> Task: resumeTopActivityInnerLocked
Task -> TaskFragment: resumeTopActivity
activate TaskFragment
TaskFragment -> ActivityTaskSupervisor: startSpecificActivity
activate ActivityTaskSupervisor
ActivityTaskSupervisor -> ClientTransaction: new
ActivityTaskSupervisor -> ClientLifecycleManager: scheduleTransaction
activate ClientLifecycleManager
ClientLifecycleManager -> ApplicationThread: scheduleTransaction
activate ApplicationThread
ApplicationThread -> ActivityThread: scheduleTransaction
ActivityThread-> ActivityThread.H: handleMessage
activate ActivityThread.H
ActivityThread.H -> TransactionExecutor: execute
activate TransactionExecutor
TransactionExecutor -> TransactionExecutor: executeCallbacks
TransactionExecutor -> TransactionExecutor: cycleToPath
TransactionExecutor -> TransactionExecutor: performLifecycleSequence
TransactionExecutor -> TransactionExecutor: handleLaunchActivity
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

```mermaid
classDiagram
class Context
class ContextWrapper {
    mBase Context
}
class ContextThemeWrapper
class Activity

ContextWrapper --|> Context
Context --o ContextWrapper
ContextThemeWrapper --|> ContextWrapper
Activity --|> ContextThemeWrapper
```


```mermaid
classDiagram
class ViewManager {
    <<interface>>
}
class WindowManager {
    <<interface>>
}
class Window {
    <<abstract>>
    WindowManager mWindowManager
}
class Activity {
    Window mWindow
    WindowManager mWindowManager
}
class ViewGroup
class WindowManagerImpl

WindowManager --|> ViewManager: extend
ViewGroup --|> ViewManager: impl
WindowManagerImpl --|> WindowManager: impl
Window --> WindowManager
Activity --> Window
Activity --> WindowManager
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

```mermaid
classDiagram
class Activity {
    setContentView()
}
class Window
class PhoneWindow {
    mDecor: DecoreView
    mContentParent ViewGroup
    setContentView()
}
PhoneWindow --|> Window
```


## 参考

- [Android窗口机制（一）初识Android的窗口结构](https://www.jianshu.com/p/40a9c93b5a8d)
- [Android -- Activity启动过程中的上下文环境初始化分析](https://blog.csdn.net/csdn_of_coder/article/details/78147399)
- [Android 11源码分析： Activity的启动流程](https://juejin.cn/post/6994823348190445604#heading-1)