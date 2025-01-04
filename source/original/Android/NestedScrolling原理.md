---
title: NestedScrolling原理
date: 2024-05-12 16:44:23
tags:
---

[android MD进阶[四] NestedScrollView 从源码到实战..
](https://juejin.cn/post/7084926146675998756)

[基础精读：NestedScrolling机制详解](https://juejin.cn/post/7141723017914089508)

```
parent I  PARENT-2: onStartNestedScroll true
parent I  PARENT-2: onNestedScrollAccepted kotlin.Unit
child  D  CHILD-1: stopNestedScroll
parent I  PARENT-2: onStartNestedScroll true
parent I  PARENT-2: onNestedScrollAccepted kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-1: dispatchNestedPreFling false
parent I  PARENT-1: onNestedPreFling false
child  D  CHILD-1: dispatchNestedPreFling false
parent I  PARENT-1: onNestedFling false
child  D  CHILD-1: dispatchNestedFling false
parent I  PARENT-2: onStartNestedScroll true
parent I  PARENT-2: onNestedScrollAccepted kotlin.Unit
child  D  CHILD-1: stopNestedScroll
child  D  CHILD-2: dispatchNestedPreScroll false
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
parent D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-2: onNestedPreScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
parent I  PARENT-3: onNestedScroll kotlin.Unit
child  D  CHILD-3: dispatchNestedScroll kotlin.Unit
child  D  CHILD-2: dispatchNestedPreScroll false
child  D  CHILD-2: dispatchNestedPreScroll false
```

```mermaid
sequenceDiagram
participant child
participant childHelper
participant parent
participant parentHelper

child -> child: onTouchEvent （DOWN）
activate child
  child -> childHelper: startNestedScroll
  activate childHelper
   childHelper -> parent: onStartNestedScroll
  deactivate childHelper
  activate childHelper
   activate parent
    childHelper -> parent: onNestedScrollAccepted
    activate parent
     parent -> parentHelper: onNestedScrollAccepted
    deactivate parent
    activate parent
     parent -> parent: startNestedScroll
    deactivate parent
   deactivate parent
  deactivate childHelper
deactivate child
```

```mermaid
sequenceDiagram
participant child
participant childHelper
participant parent
participant parentChildHelper
participant parentHelper

child -> child: onTouchEvent （MOVE）
activate child
 activate child
  child -> childHelper: dispatchNestedPreScroll
  activate childHelper
   childHelper -> parent: onNestedPreScroll
   activate parent
    parent -> parentChildHelper: dispatchNestedPreScroll
   deactivate parent
  deactivate childHelper
 deactivate child

 activate child
  child -> childHelper: dispatchNestedScroll
  activate childHelper
   childHelper -> parent: onNestedScroll
   activate parent
    parent -> parentChildHelper: dispatchNestedScroll
   deactivate parent
  deactivate childHelper
 deactivate child
deactivate child
```

```mermaid
sequenceDiagram
participant child
participant childHelper
participant parent
participant parentChildHelper
participant parentHelper

child -> child: onTouchEvent （UP）
activate child
 child -> childHelper: stopNestedScroll
 activate childHelper
  childHelper -> parent: onStopNestedScroll
  activate parent
   activate parent
    parent -> parentHelper: onStopNestedScroll
   deactivate parent
   activate parent
    parent -> parent: stopNestedScroll
    parent -> parentChildHelper: stopNestedScroll
    activate parentChildHelper
    deactivate parentChildHelper
   deactivate parent
  deactivate parent
 deactivate childHelper
deactivate child
```