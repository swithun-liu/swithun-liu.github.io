---
title: test2
author: Swithun Liu
date: 2023-10-10
category: test
layout: post
mermaid: true
---

A ${\xrightarrow{test}} B

$$\xrightarrow{test2}$$


A $\xrightarrow{test}$ B

```mermaid
classDiagram
      class ClientTransactionItem {
      }
      class ActivityTransactionItem {
      }
      class ActivityRelaunchItem {
      }
      class BaseClientRequest {
         <<interface>>
         + execute(ClientTransactionHandler client, IBinder token,PendingTransactionActions pendingActions)
      }
      ClientTransactionItem <|-- ActivityTransactionItem
      ActivityTransactionItem <|-- ActivityRelaunchItem
      BaseClientRequest <|-- ClientTransactionItem: implements
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
