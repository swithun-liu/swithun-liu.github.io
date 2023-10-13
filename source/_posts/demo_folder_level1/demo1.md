---
title: demo_title_1
author: Swithun Liu
date: 2023-10-10
category: demo
layout: post
mermaid: true
---

## math

- inline : A $\xrightarrow{test}$ B
- block: 
$$\xrightarrow{test2}$$

## mermaid
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

## code

this is `inline code`

java

```java
class A {
  System -> {

  }
}
```

kotlin
```kotlin
class B {
    fun test() {

    }
}
```

# 普通文本

你好，hello, A -> B