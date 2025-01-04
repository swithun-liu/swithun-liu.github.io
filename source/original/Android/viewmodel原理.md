---
title: ViewModel配置变更后仍然存在原理
author: Swithun Liu
date: 2023-10-10
category: Android
tag: A
layout: post
mermaid: true
---

## 目录

*   [Activity创建ViewModel](##Activity创建ViewModel)
*   [Activity重建ViewModel保持存在的实现](##Activity重建ViewModel保持存在的实现)
    *   [relaunch之后新的Activity获取之前的viewModel](###relaunch之后新的Activity获取之前的viewModel)
    *   [relaunch过程中保存旧Activity的viewModel](###relaunch过程中保存旧Activity的viewModel)
*   [reference](##reference)

> 2022/08/21

## Activity创建ViewModel

*   创建ViewModel
    ```kotlin
    // MyActivity#onCreate()

    val mainViewModel = 
                [V1]   ViewModelProvider(this)
                  [V2]       .get(MainViewModel::class.java)
    ```
*   `[V1]`

    ViewModelProvider构造函数

    ```kotlin
    // androidx.lifecycle.ViewModelProvider#get(java.lang.Class<T>)
        public constructor(
            owner: ViewModelStoreOwner
        ) : this(owner.viewModelStore, defaultFactory(owner), defaultCreationExtras(owner))
    ```

    this指MyActivity，即MyActivity应该是`[I]ViewModelStoreOwner`类型

    MyActivity继承`[C]ComponentActivity]`，ComponentActivity实现了`[I]ViewModelStoreOwner`接口

    ```java
    // CompnentActivity
    public class ComponentActivity extends androidx.core.app.ComponentActivity implements
            // ...
            ViewModelStoreOwner,
            // ... {
    ```

    `this(owner.viewModelStore, defaultFactory(owner), defaultCreationExtras(owner))` ，这里使用 `owner.viewModelStore`从ViewModelStoreOwner中取出`[OC]ViewModelStore]`

    ```kotlin
    // ViewModelStoreOwner
    interface ViewModelStoreOwner {

        /**
         * The owned [ViewModelStore]
         */
        val viewModelStore: ViewModelStore
    }
    ```

    然后调用下面的构造函数

    ```kotlin
    // ViewModelStoreOwner

    /**
     * Creates a ViewModelProvider
     *
     * @param store `ViewModelStore` where ViewModels will be stored.
     * @param factory factory a `Factory` which will be used to instantiate new `ViewModels`
     * @param defaultCreationExtras extras to pass to a factory
     */
    @JvmOverloads
    constructor(
        private val store: ViewModelStore,
        private val factory: Factory,
        private val defaultCreationExtras: CreationExtras = CreationExtras.Empty,
    ) {
    ```
*   `[V2]`

    调用了get方法⬇️

    ```kotlin
    // androidx.lifecycle.ViewModelProvider#get(java.lang.Class<T>)
        @MainThread
        public open operator fun <T : ViewModel> get(modelClass: Class<T>): T {
            val canonicalName = modelClass.canonicalName
                ?: throw IllegalArgumentException("Local and anonymous classes can not be ViewModels")
       [W1]  return get("$DEFAULT_KEY:$canonicalName", modelClass)
        }

    ```
*   `[W1]`
    ```kotlin
    // androidx.lifecycle.ViewModelProvider#get(java.lang.String, java.lang.Class<T>)
        @MainThread
        public open operator fun <T : ViewModel> get(key: String, modelClass: Class<T>): T {
        [X1]val viewModel = store[key]
        [X1]if (modelClass.isInstance(viewModel)) {
                ....
        [X1]    return viewModel as T
            ....
        [X2]return try {
        [X2]     factory.create(modelClass, extras)
        [X2] catch (e: AbstractMethodError) {
        [X2]    factory.create(modelClass)
        [X2]}.also { store.put(key, it) }
        }

    ```
*   `[X1]`⬅️`[W1]`

    从store(`[OC]ViewModelStore`)中能找到viewmodel则直接返回
*   `[X2]`⬅️`[W1]`

    store中找不到则需要新创建一个viewmodel并放入store，这里说明只要使用同一个ViewModelStore获取ViewModel则不同地方获取到的都是同一个ViewModel

    `[OC]ViewModelStore`看起来是个Map，事实上他的实现就是维护一个map，放出get和put方法

    ```kotlin
    open class ViewModelStore {

        private val map = mutableMapOf<String, ViewModel>()
        ...

        fun put(key: String, viewModel: ViewModel) {
        }

        operator fun get(key: String): ViewModel? {
            return map[key]
        }
        ...
    }
    ```

总结上面，Activity在onCreate时创建viewModel，Activity是一个ViewModelStoreOwner其中有一个ViewModelStore其中维护一个map，ViewModelProvier作为一个工具类在使用默认的/我们提供的Factory（为了适配构造函数有参的ViewModel）创建ViewModel的同时会将其存入这个map。

所以，在relaunch过程中，销毁旧的Activity时如果能保存它的mViewModelStore，然后将其赋值新的Activity的mViewModelStore就能实现配置变更viewModel不变更的效果。

## Activity重建ViewModel保持存在的实现

### relaunch之后新的Activity获取之前的viewModel

viewModel存在ViewModelStore中，说明ViewModelStore在Activity重建的过程中能保持存在，看下`[C]ComponentActivity`如何如何获取`[OC]ViewModelStore`的

```kotlin
    public ViewModelStore getViewModelStore() {
        if (getApplication() == null) {
            throw new IllegalStateException("Your activity is not yet attached to the "
                    + "Application instance. You can't request ViewModel before onCreate call.");
        }
   [T1] ensureViewModelStore();
        return mViewModelStore;
    }



```

*   `[T1]`

    在getViewModelStore()方法中调用了ensureViewModelStore()确保mViewModelStore不为空

    ```kotlin
        @SuppressWarnings("WeakerAccess") /* synthetic access */
        void ensureViewModelStore() {
            if (mViewModelStore == null) {
            [U1] NonConfigurationInstances nc =
                        (NonConfigurationInstances) getLastNonConfigurationInstance();
                if (nc != null) {
                    // Restore the ViewModelStore from NonConfigurationInstances
            [U2]    mViewModelStore = nc.viewModelStore;
                }
                if (mViewModelStore == null) {
                    mViewModelStore = new ViewModelStore();
                }
            }
        }
    ```
*   `[U1]`⬅️`[T1]`
    ```kotlin
    // Activity

        @Nullable
        public Object getLastNonConfigurationInstance() {
            return mLastNonConfigurationInstances != null
                    ? mLastNonConfigurationInstances.activity : null;
        }
    ```
    Activirty.mLastNonConfigurationInstances类型为`[C]Activity.NonConfigurationInstances`
    ```java
    // android.app.Activity.NonConfigurationInstances
        static final class NonConfigurationInstances {
            Object activity;
            ....
        }
    ```
    mLastNonConfigurationInstances.activity在`[U1]`处被强转为`[C]ComponentActivity.NonConfigurationInstances`
    ```kotlin
    // androidx.activity.ComponentActivity.NonConfigurationInstances
        static final class NonConfigurationInstances {
            Object custom;
            ViewModelStore viewModelStore;
        }
    ```
*   `[U2]`⬅️`[T1]`

    如果`[U1]`获取的nc不为空，则将mViewModelStore赋值为nc.viewModelStore 即Activity.mLastNonConfigurationInstances.activity.viewModelStore

    所以想要保存给新Activity使用原来的viewModel，重点就是要在relaunch过程中保存旧的Activity.mLastNonConfigurationInstances然后再赋值给新Activity.mLastNonConfigurationInstances

### relaunch过程中保存旧Activity的viewModel

设备变更，系统调用AMS的updateConfiguration 方法

[ActivityManagerService.java - Android Code Search](https://cs.android.com/android/platform/superproject/+/master:frameworks/base/services/core/java/com/android/server/am/ActivityManagerService.java;l=462?q=ActivityManagerService\&sq=\&ss=android/platform/superproject "ActivityManagerService.java - Android Code Search")

```java
// ActivityManagerService
    @Override
    public boolean updateConfiguration(Configuration values) {
        return mActivityTaskManager.updateConfiguration(values);
    }
```

```java
// ActivityTaskManagerService
    @Override
    public boolean updateConfiguration(Configuration values) {
           ....
                updateConfigurationLocked(values, null, false, false /* persistent */,
           ....
    }
```

```java
// ActivityTaskManagerService
    boolean updateConfigurationLocked(Configuration values, ActivityRecord starting,
            boolean initLocale, boolean persistent, int userId, boolean deferResume,
            ActivityTaskManagerService.UpdateConfigurationResult result) {
            ....
            「I1」  changes = updateGlobalConfigurationLocked(values, initLocale, persistent, userId);
            ....
            「I2」 kept = ensureConfigAndVisibilityAfterUpdate(starting, changes);
            ....
    }
```

*   `「I1」`

    updateGlobalConfigurationLocked 更新当前配置信息
*   `「I2」`

    ensureConfigAndVisibilityAfterUpdate 确保给定的activity更新使用的配置

    这里starting传入的是null，需要ensureConfigAndVisibilityAfterUpdate中自己获取

    ```kotlin
    // ActivityTaskManagerService
        boolean ensureConfigAndVisibilityAfterUpdate(ActivityRecord starting, int changes) {
            boolean kept = true;
         「J1」   final Task mainRootTask = mRootWindowContainer.getTopDisplayFocusedRootTask();
            ....
                 「J2」 starting = mainRootTask.topRunningActivity();
            ....
                 「J3」 kept = starting.ensureActivityConfiguration(changes,
            ....
        }
    ```
*   `「J1」`⬅️`「I2」`

    获取根窗口容器中当前具有焦点的顶级任务（root task）
*   `「J2」`⬅️`「I2」`

    获取顶级任务（root task）中当前正在运行的顶级Activity（top running Activity）的ActivityRecord赋值给starting
*   `「J3」`⬅️`「I2」`

    ActivityRecord对应的Activity更新Configuration

    ```kotlin
    // com.android.server.wm.ActivityRecord#ensureActivityConfiguration(int, boolean)
        boolean ensureActivityConfiguration(int globalChanges, boolean preserveWindow) {
            return ensureActivityConfiguration(globalChanges, preserveWindow,
                    false /* ignoreVisibility */);
        }

    ```

    ```java
    // com.android.server.wm.ActivityRecord#ensureActivityConfiguration(int, boolean, boolean)
        boolean ensureActivityConfiguration(int globalChanges, boolean preserveWindow,
                boolean ignoreVisibility) {
                ....
                    relaunchActivityLocked(preserveWindow);
                ....
        }
    ```

    ```java
     // com.android.server.wm.ActivityRecord#relaunchActivityLocked
        void relaunchActivityLocked(boolean preserveWindow) {
                ....
           「K2」  final ClientTransactionItem callbackItem = ActivityRelaunchItem.obtain(pendingResults,
                ....
           「K1」  final ClientTransaction transaction = ClientTransaction.obtain(app.getThread(), token);
           「K2」  transaction.addCallback(callbackItem);
                ....
           「K3」  mAtmService.getLifecycleManager().scheduleTransaction(transaction);
                ....
        }
    ```
*   `「K1」`⬅️`「J3」`

    token来自`[C]ActivityRecord`继承的`[C]WindowToken`中的token

    ```kotlin
    class WindowToken extends WindowContainer<WindowState> {
        private static final String TAG = TAG_WITH_CLASS_NAME ? "WindowToken" : TAG_WM;

        /** The actual token */
        final IBinder token;

        /** The type of window this token is for, as per {@link WindowManager.LayoutParams} */
        final int windowType;
    ```

    ```kotlin
     // ClientTransaction
        /** Obtain an instance initialized with provided params. */
        public static ClientTransaction obtain(IApplicationThread client, IBinder activityToken) {
            ClientTransaction instance = ObjectPool.obtain(ClientTransaction.class);
            if (instance == null) {
                instance = new ClientTransaction();
            }
            instance.mClient = client;
            instance.mActivityToken = activityToken;

            return instance;
        }
    ```

    将transaction.mActivityToken设置为ActivityRecord.token
*   `「K2」`⬅️`「J3」`

    给transaction放入callback：`[C]ActivityRelaunchItem`
*   `「K3」`⬅️`「J3」`

    执行transaction

    ```java
    // com.android.server.wm.ClientLifecycleManager#scheduleTransaction(ClientTransaction)
        void scheduleTransaction(ClientTransaction transaction) throws RemoteException {
            ....
            transaction.schedule();
            ....
        }
    ```

    ```kotlin
    // ClientTransaction
        public void schedule() throws RemoteException {
       「L1」  mClient.scheduleTransaction(this);
        }
    ```
*   `「L1」`⬅️`「K3」`

    `[C]ClientTransaction`使用mClient执行自己

    *   mClient是什么?&#x20;
        ```kotlin
        // ClientTransaction
            /** Target client. */
            private IApplicationThread mClient;
        ```
        这里是使用AIDL(基于Binder)进行进程间通信，对应文件`IApplicationThread.aidl`⬇️
        ```kotlin
        oneway interface IApplicationThread {
            ....
            void scheduleTransaction(in ClientTransaction transaction);
        ```
        这里mClient是客户端，对应的客户端为`[c]ApplicationThread`
        ```kotlin
            private class ApplicationThread extends IApplicationThread.Stub {
        ```
*   `「M1」`⬅️`「L1」`

    所以下面从 android.app.ActivityThread.ApplicationThread#scheduleTransaction方法继续

    ```kotlin
    // android.app.ActivityThread.ApplicationThread#scheduleTransaction
            @Override
            public void scheduleTransaction(ClientTransaction transaction) throws RemoteException {
                ActivityThread.this.scheduleTransaction(transaction);
            }

    ```

    这里scheduleTransaction是调用的ActivityThread的基类ClientTransactonHandler中的scheduleTransaction方法

    ```kotlin
    // android.app.ClientTransactionHandler#scheduleTransaction
        void scheduleTransaction(ClientTransaction transaction) {
     「N1」  transaction.preExecute(this);
     「N2」  sendMessage(ActivityThread.H.EXECUTE_TRANSACTION, transaction);
        }

    ```
*   `「N1」`⬅️`「M1」`

    为后面transaction的执行做些准备，这里this传入的是`[C]ActivityThread`

    ```java
        public void preExecute(android.app.ClientTransactionHandler clientTransactionHandler) {
            if (mActivityCallbacks != null) {
                ....
                for (int i = 0; i < size; ++i) {
                「O1」  mActivityCallbacks.get(i).preExecute(clientTransactionHandler, mActivityToken);
                ....
        }

    ```
*   `「O1」`⬅️`「N1」`

    执行每个callback的preExecute方法，callback只有一个之前在`「K2」`处放入的ActivityRelaunchItem

    ```java
     // android.app.servertransaction.ActivityRelaunchItem#preExecute
        public void preExecute(ClientTransactionHandler client, IBinder token) {
        「P1」 mActivityClientRecord = client.prepareRelaunchActivity(token, mPendingResults,
                    mPendingNewIntents, mConfigChanges, mConfig, mPreserveWindow);
        }

    ```
*   `「P1」`⬅️ `「O1」`

    从ActivityThread(即client)获取要relaunch的ActivityRecord存入ActivityRelaunchItem.mActivityClientRecord

    ```java
        @Override
        public ActivityClientRecord prepareRelaunchActivity(IBinder token,
                List<ResultInfo> pendingResults, List<ReferrerIntent> pendingNewIntents,
                int configChanges, MergedConfiguration config, boolean preserveWindow) {
        「Q1」     ....

        「Q2」     target = new ActivityClientRecord();
        「Q2」     target.token = token;
                    ....
        「Q3」     mRelaunchingActivities.add(target);
                    ....

            return ....target....;
        }
    ```
*   `「Q1」`⬅️`「P1」`

    检查是否目标activity是否已经正在relaunch了，如果是则返回
*   `「Q2」`⬅️`「P1」`

    目标activity没有已经正在relaunch（这里认为是没有，这个判断只是为了防止relaunch正在relaunch的activity），则构造一个`[sC]ActivityClientRecord`记录要relaunch的Activity的token等信息
*   `「Q3」`⬅️`「P1」`使用ActivityThread.mRelaunchingActivities记录所有要准备重启的ActivityClientRecord
    ```text
    +-----------------------------------------------------+
    |                                                     |
    |                 ActivityThread                      |
    |                                                     |
    |       +-----------------------------------+         |
    |       |    mRelaunchingActivities         |         |
    |       |                                   |         |
    |       |   +------------------------+      |         |
    |       |   | ActivityClientRecord   |      |         |
    |       |   +------------------------+      |         |
    |       |                                   |         |
    |       |   +------------------------+      |         |
    |       |   | ActivityClientRecord   |      |         |
    |       |   +------------------------+      |         |
    |       |                                   |         |
    |       |           ....                    |         |
    |       |                                   |         |
    |       |                                   |         |
    |       +-----------------------------------+         |
    |                                                     |
    +-----------------------------------------------------+

    ```
*   `「N2」`⬅️`「M1」`

    这里使用Handler去真正执行transaction，obj传入的就是transaction

    ```java
    // android.app.ClientTransactionHandler#sendMessage
        abstract void sendMessage(int what, Object obj);
    ```

    ```java
    // android.app.ActivityThread#sendMessage(int, java.lang.Object)
        void sendMessage(int what, Object obj) {
            sendMessage(what, obj, 0, 0, false);
        }
    ```

    ⬇️构造Message

    ```java
    // android.app.ActivityThread#sendMessage(int, java.lang.Object, int, int, boolean)
        private void sendMessage(int what, Object obj, int arg1, int arg2, boolean async) {
            ....
            msg.what = what;
            msg.obj = obj;
            ....
            mH.sendMessage(msg);
        }
    ```

    ⬇️handler：ActivityThread.H 收到消息并处理

    ```java
    // android.app.ActivityThread.H#handleMessage
            public void handleMessage(Message msg) {
                ...
                 switch (msg.what) {
                    ...
                    case EXECUTE_TRANSACTION:
                  「R1」  final ClientTransaction transaction = (ClientTransaction) msg.obj;
                  「R2」  mTransactionExecutor.execute(transaction);
                        ....


    ```
*   `「R1」`⬅️`「N2」`从message中取出transaction
*   `「R2」`⬅️`「N2」`交给mTransactionExecutor执行

    mTransactionHandler 是谁？是`[C]ActivityThread`，从TransactionExecutor的构造函数⬇️中可以看出

    ```kotlin
    // ActivityThread
        private final TransactionExecutor mTransactionExecutor = new TransactionExecutor(this);

    ```

    ```kotlin
        /** Initialize an instance with transaction handler, that will execute all requested actions. */
        public TransactionExecutor(ClientTransactionHandler clientTransactionHandler) {
            mTransactionHandler = clientTransactionHandler;
        }

    ```

    TransactionExecutor.mTransactionHandler是对持有该TransactionExecutor的ActivityThread的引用

    ```text
    +-------------------------------------------------------------------------------------+
    |                                    ActivityThread <-------+                         |
    |                                                           |                         |
    |                                                           |                         |
    |      +-----------------------------------------------------------------+            |
    |      |  mTransactionExecutor: TransactionExecutor         |            |            |
    |      |                                                    |            |            |
    |      |                                                    |            |            |
    |      |  +-------------------------------------------------+---------+  |            |
    |      |  |   mTransactionHandler: ClientTransactionHandler           |  |            |
    |      |  |                                                           |  |            |
    |      |  |                                                           |  |            |
    |      |  +-----------------------------------------------------------+  |            |
    |      |                                                                 |            |
    |      |                                                                 |            |
    |      +-----------------------------------------------------------------+            |
    |                                                                                     |
    +-------------------------------------------------------------------------------------+

    ```

    ```java
    // android.app.servertransaction.TransactionExecutor#execute
        public void execute(ClientTransaction transaction) {
            ....
            executeCallbacks(transaction);
            ....
        }
    ```

    ```kotlin
    // android.app.servertransaction.TransactionExecutor#executeCallbacks
        public void executeCallbacks(ClientTransaction transaction) {
            final List<ClientTransactionItem> callbacks = transaction.getCallbacks();
            ....
      「S1」 final IBinder token = transaction.getActivityToken();
            ....
            for (int i = 0; i < size; ++i) {
                final ClientTransactionItem item = callbacks.get(i);
                ....
        「S2」  item.execute(mTransactionHandler, token, mPendingActions);
                ....
        }
    ```
*   `「S1」`⬅️`「R2」`

    从transaction中获取activityToken`「K1」`⬅️`「J3」`
*   `「S2」`⬅️`「R2」`

    callback（为ActivityRelaunchItem）执行，execute方法来自ActivityRelaunchItem 实现的接口BaseClientRequest的execute方法

    至于mTransactionHandler是谁，在`「R2」`已经解释

    execute方法来自ActivityRelaunchItem实现的接口BaseClientRequest中的execute方法⬇️

    ```kotlin
    public interface BaseClientRequest extends ObjectPoolItem {

        ....
        void execute(ClientTransactionHandler client, IBinder token,
                PendingTransactionActions pendingActions);
        ....

    }
    ```

    ActivityRelaunchItem和BaseClientRequest的关系⬇️

    ```kotlin
    public abstract class ClientTransactionItem implements BaseClientRequest
    ```

    ```kotlin
    public abstract class ActivityTransactionItem extends ClientTransactionItem
    ```

    ```kotlin
    public class ActivityRelaunchItem extends ActivityTransactionItem
    ```

    ```mermaid
    classDiagram
          class ClientTransactionItem 
          class ActivityTransactionItem 
          class ActivityRelaunchItem 
          class BaseClientRequest {
             <<interface>>
             + execute(ClientTransactionHandler client, IBinder token,PendingTransactionActions pendingActions)
          }
          ClientTransactionItem <|-- ActivityTransactionItem
          ActivityTransactionItem <|-- ActivityRelaunchItem
          BaseClientRequest <|-- ClientTransactionItem: implements
    ```

    该execute方法由`[C]ActivityRelaunchItem`的基类ActivityTransactionItem实现

    ```kotlin
    // ActivityTransactionItem
        public final void execute(ClientTransactionHandler client, IBinder token,
                PendingTransactionActions pendingActions) {
       「A1」  final ActivityClientRecord r = getActivityClientRecord(client, token);

       「A2」  execute(client, r, pendingActions);
        }
    ```
*   `「A1」`根据token获取ActivityClientRecord
    ```kotlin
    // ActivityTransactionItem
        @NonNull ActivityClientRecord getActivityClientRecord(
                @NonNull ClientTransactionHandler client, IBinder token) {
            final ActivityClientRecord r = client.getActivityClient(token);
            ....
            return r;
        }

    ```
    client是 TransactionExecutor.mTransactionHandler，也就是持有TransactionExecutor的ActivityThread
    ```java
    // ActivityThread 
        @Override
        public ActivityClientRecord getActivityClient(IBinder token) {
            return mActivities.get(token);
        }
    ```
*   `「A2」`继续执行 ⬇️
    ```java
    // ActivityRelaunchItem
        @Override
        public void execute(ClientTransactionHandler client, ActivityClientRecord r,
                PendingTransactionActions pendingActions) {
            ....
      「B1」  client.handleRelaunchActivity(mActivityClientRecord, pendingActions);
        }
    ```
*   `「B1」`mActivityClientRecord从哪里来？之前🔗`「P1」`⬅️ `「O1」`
    ```kotlin
    // ActivityThread
        @Override
        public void handleRelaunchActivity(ActivityClientRecord tmp,
                PendingTransactionActions pendingActions) {
            ...
        「C1」 ActivityClientRecord r = mActivities.get(tmp.token);
            ...
        「C2」handleRelaunchActivityInner(r, configChanges, tmp.pendingResults, tmp.pendingIntents,
                    pendingActions, tmp.startsNotResumed, tmp.overrideConfig, "handleRelaunchActivity");
            ...
        }
    ```
*   `「C1」`⬅️`「B1」`

    这里从`mActivities`中根据token获取`[sC]ActivityClientRecord`

    ```text
    +----------------------------------------------------------------+
    |   ActivityThread                                               |
    |                                                                |
    |                                                                |
    |    +------------------------------------------------------+    |
    |    |  mActivities                                         |    |
    |    |             +--------------------------------------+ |    |
    |    |             |      +---------------+               | |    |
    |    |             |      |    Activity   |               | |    |
    |    |             |      +---------------+               | |    |
    |    |             |                                      | |    |
    |    |             |   +-------------------------------+  | |    |
    |    |             |   | lastNonConfigurationInstances |  | |    |
    |    |             |   +-------------------------------+  | |    |
    |    |             |                                      | |    |
    |    |             +--------------------------------------+ |    |
    |    |             +--------------------------------------+ |    |
    |    |             |                                      | |    |
    |    |             |                                      | |    |
    |    |             +--------------------------------------+ |    |
    |    |             +--------------------------------------+ |    |
    |    |             |                                      | |    |
    |    |             |                                      | |    |
    |    |             +--------------------------------------+ |    |
    |    |                                                      |    |
    |    |                           ...                        |    |
    |    |                                                      |    |
    |    +------------------------------------------------------+    |
    +----------------------------------------------------------------+

    ```
*   `「C2」`⬅️`「B1」`

    传递r给

    ```java
    // ActivityThread
        private void handleRelaunchActivityInner(ActivityClientRecord r, int configChanges,
                List<ResultInfo> pendingResults, List<ReferrerIntent> pendingIntents,
                PendingTransactionActions pendingActions, boolean startsNotResumed,
                Configuration overrideConfig, String reason) {
            ...
    「D1」        handleDestroyActivity(r, false, configChanges, true, reason);
            ...
    「D2」        handleLaunchActivity(r, pendingActions, customIntent);
        }
    ```
*   `「D1」`⬅️`「C2」`

    ⬇️Destroy原来的Activity，其中getNonConfigInstance传入了true

    ```java
    // ActivityThread
        @Override
        public void handleDestroyActivity(ActivityClientRecord r, boolean finishing, int configChanges,
                boolean getNonConfigInstance, String reason) {
            performDestroyActivity(r, finishing, configChanges, getNonConfigInstance, reason);
            ...
        }
    ```

    ⬇️将原来的activity的nonConfigurationInstances存入ActivityRecord.lastNonConfigurationInstances

    ```java
    // ActivityThread
        /** Core implementation of activity destroy call. */
        void performDestroyActivity(ActivityClientRecord r, boolean finishing,
                int configChanges, boolean getNonConfigInstance, String reason) {
            ...
        「E1」 if (getNonConfigInstance) {
                ....
                「E2」  r.lastNonConfigurationInstances = r.activity.retainNonConfigurationInstances();
                ....
    ```
*   `「E1」`这里如果是getNonConfigInstance为true（前面传的是true），
*   `「E2」`

    则️将retainNonConfigurationInstances的结果放入`[sC]ActivityClientRecord`.lastNonConfigurationInstances，其中就包含viewModelStore

    ```java
     // Activity
        NonConfigurationInstances retainNonConfigurationInstances() {
    「F1」 Object activity = onRetainNonConfigurationInstance();
            ...
            NonConfigurationInstances nci = new NonConfigurationInstances();
            nci.activity = activity;
            ....
            return nci;
        }
    ```
*   `「F1」`Activity默认实现中只返回了null，但是`[C]ComponentActivity`重写了这个方法⬇️
    ```java
     // ComponentActivity
        public final Object onRetainNonConfigurationInstance() {
            // Maintain backward compatibility.
    「G1」  Object custom = onRetainCustomNonConfigurationInstance();

            ViewModelStore viewModelStore = mViewModelStore;
    「G2」  if (viewModelStore == null) {
                ....
            }
            ....

    「G3」   NonConfigurationInstances nci = new NonConfigurationInstances();
            nci.custom = custom;
            nci.viewModelStore = viewModelStore;
            return nci;
        }


    ```
*   `「G1」`我们可以通过重写onRetainCustomNonConfigurationInstance()创建custom即自定义的在configuration改变后仍然想要保存的数据。
*   `「G2」`这里当viewModelStore为空的时候会查看`[C]ComponentActivity.NonConfigurationInstances`中是否有viewModelStore，这里对应从来没有地方调用过getViewModelStore，也就不会初始化ComponentActivity.mVieModelStore，但是我们这里情况是之前有创建viewmodel，`this(owner.viewModelStore, defaultFactory(owner), defaultCreationExtras(owner))` ，这里使用 `owner.viewModelStore`从ViewModelStoreOwner中取出`[OC]ViewModelStore`调用过，所有不会走到viewModelStore == null的分支
*   `「G3」`这里创建了`[C]ComponentActivity.NonConfigurationInstances`存入 custom和viewModelStore并返回。
*   `「D2」`⬅️`「C2」`执行LaunchActivity
    ```java
    // android.app.ActivityThread#handleLaunchActivity
        public Activity handleLaunchActivity(ActivityClientRecord r,
                PendingTransactionActions pendingActions, Intent customIntent) {
            ....
            final Activity a = performLaunchActivity(r, customIntent);
            ....
            return a;
        }
    ```
    ```kotlin
    // android.app.ActivityThread#performLaunchActivity
        private Activity performLaunchActivity(ActivityClientRecord r, Intent customIntent) {
            ....
            Activity activity = null;
            try {
                java.lang.ClassLoader cl = appContext.getClassLoader();
          「H1」 activity = mInstrumentation.newActivity(
                        cl, component.getClassName(), r.intent);
                ....

            try {
                ....
                if (activity != null) {
                    ....
            「H2」   activity.attach(appContext, this, getInstrumentation(), r.token,
                            r.ident, app, r.intent, r.activityInfo, title, r.parent,
                            r.embeddedID, r.lastNonConfigurationInstances, config,
                            r.referrer, r.voiceInteractor, window, r.activityConfigCallback,
                            r.assistToken, r.shareableActivityToken);
            ....
            return activity;
        }
    ```
*   `「H1」`

    实例化一个Activity
*   `「H2」`

    使用原来的ActivityRecord给Activity设置参数，其中第12个参数就是在`「E2」`处保存的lastNonConfigurationInstances，其中就有viewModel

    这里就回答了上面`[U2]`处的问题，串起来了

# reference

code

*   [Android 面试总结 - ViewModel 是怎么保存和恢复？ - 掘金 (juejin.cn)](https://juejin.cn/post/6976025197333708837 "Android 面试总结 - ViewModel 是怎么保存和恢复？ - 掘金 (juejin.cn)")
*   [Android Framework之Activity启动流程(一) | 柚子 | pomeloJiang](https://pomelojiang.github.io/android_framework_start_activity_1 "Android Framework之Activity启动流程(一) | 柚子 | pomeloJiang")
*   [Zygote的启动流程 - 掘金 (juejin.cn)](https://juejin.cn/post/6844904179299778567 "Zygote的启动流程 - 掘金 (juejin.cn)")
*   [Android屏幕旋转源码探索及应用实践 | 奔哲明的博客 (benzblog.site)](https://benzblog.site/2017-06-19-all-about-rotations/ "Android屏幕旋转源码探索及应用实践 | 奔哲明的博客 (benzblog.site)")
*   [Configuration 变更时Activity的生命周期探究 - 掘金 (juejin.cn)](https://juejin.cn/post/6844903869814669319 "Configuration 变更时Activity的生命周期探究 - 掘金 (juejin.cn)")

