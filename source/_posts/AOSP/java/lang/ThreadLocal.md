---
title: ThreadLocal
date: 2024-10-07 19:28:29
tags:
---

## set

```mermaid
sequenceDiagram
participant Other
participant T as ThreadLocal<T>
participant ThreadS as Thread(类)
participant Thread
participant TT as ThreadLocal.ThreadLocalMap

Other ->> T: new
T -->> Other: threadLocal
Other ->> T: set(T value)
T ->> ThreadS: currentThead()
ThreadS ->> T: Thread(当前线程)
T ->> Thread: get threadLocals
note over Thread: ThreadLocal.ThreadLocalMap threadLocals = null <br> Key: ThreadLocal <br> Value: <T>
Thread -->> T: ThreadLocal.ThreadLocalMap threadLocals
T ->> TT: set(Key, value)
note over T,TT: set(前面新建的ThreadLocal, T)
```

```plaintText
                                            ▼                                
                                                                             
                                                                             
                                                                             
set： find currentThread, and call Thread.threadLocals.set(ThreadLocal, value)
                                                                             
┌────────────────────────┐                                                   
│                        │                                                   
│                        │                                                   
│       ┌────────────────▼────────────────────────────────────┐              
│       │                                                     │              
│       │                        Thread                       │              
│       │                                                     │              
│       │    ┌───────────────────────────────────────┐        │              
│       │    │       threadLocals: ThreadLocalMap    │        │              
│       │    │                                       │        │              
│       │    │                                       │        │              
│       │    │  ┌─────────────────┐────────────────┐ │        │              
└───────┼────┼──┼ ThreadLocal     │   Value        │ │        │              
        │    │  │                 │                │ │        │              
        │    │  └─────────────────┘────────────────┘ │        │              
        │    │  ┌─────────────────┐────────────────┐ │        │              
        │    │  │ ThreadLocal     │   Value        │ │        │              
        │    │  │                 │                │ │        │              
        │    │  └─────────────────┘────────────────┘ │        │              
        │    │  ┌─────────────────┐────────────────┐ │        │              
        │    │  │ ThreadLocal     │   Value        │ │        │              
        │    │  │                 │                │ │        │              
        │    │  └─────────────────┘────────────────┘ │        │              
        │    │  ┌─────────────────┐────────────────┐ │        │              
        │    │  │ ...             │   ...          │ │        │              
        │    │  │                 │                │ │        │              
        │    │  └─────────────────┘────────────────┘ │        │              
        │    │                                       │        │              
        │    └───────────────────────────────────────┘        │              
        │                                                     │              
        └─────────────────────────────────────────────────────┘              
```

## get

```mermaid
sequenceDiagram
participant Other
participant T as ThreadLocal<T>
participant ThreadS as Thread(类)
participant Thread
participant TT as ThreadLocal.ThreadLocalMap

rect rgba(191, 223, 255, .1) 
    Other ->> T: new
    T -->> Other: threadLocal
    Other ->> T: set(T value)
end
rect rgba(191, 223, 255, .1) 
    Other ->> T: get()
    T ->> ThreadS: currentThead()
    ThreadS ->> T: Thread(当前线程)
    T ->> Thread: get threadLocals
    Thread -->> T: ThreadLocal.ThreadLocalMap threadLocals
    T ->> TT: getEntry(key)
    note over T,TT: getEntry(ThreadLocal)
    TT -->> T: value
    note over TT,T: value: <T>
end 
```

```plaintText
            2. find currentThread call Thread.threadLocals.get(ThreadLocal)
            ┌────────────────────────┐                                     
            │                        │                                     
            │                        │                                     
            │       ┌────────────────▼─┬──────────────────────────────────┐
            │       │                  │                                  │
            │       │                  │     Thread                       │
            │       │                  │                                  │
            │       │    ┌─────────────▼─────────────────────────┐        │
            │       │    │       threadLocals: ThreadLocalMap    │        │
            │       │    │             ─────────────┐            │        │
            │       │    │                          │            │        │
            │       │    │  ┌─────────────────┐─────▼──────────┐ │        │
            └───────┼────┼──┼ ThreadLocal     │   Value        │ │        │
────────────────────┼────┼─►│                 │                │ │        │
   1. get           │    │  └─────────────────┘────────────────┘ │        │
                    │    │  ┌─────────────────┐────────────────┐ │        │
                    │    │  │ ThreadLocal     │   Value        │ │        │
                    │    │  │                 │                │ │        │
                    │    │  └─────────────────┘────────────────┘ │        │
                    │    │  ┌─────────────────┐────────────────┐ │        │
                    │    │  │ ThreadLocal     │   Value        │ │        │
                    │    │  │                 │                │ │        │
                    │    │  └─────────────────┘────────────────┘ │        │
                    │    │  ┌─────────────────┐────────────────┐ │        │
                    │    │  │ ...             │   ...          │ │        │
                    │    │  │                 │                │ │        │
                    │    │  └─────────────────┘────────────────┘ │        │
                    │    │                                       │        │
                    │    └───────────────────────────────────────┘        │
                    │                                                     │
                    └─────────────────────────────────────────────────────┘
```