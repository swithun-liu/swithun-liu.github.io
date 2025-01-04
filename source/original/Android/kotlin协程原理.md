---
title: kotlin协程原理
date: 2024-08-18 19:41:40
tags:
---

```kotlin
import kotlinx.coroutines.delay
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlin.coroutines.resume

suspend fun testDelay(time: Long): Int {
    val a = testDelay1(time)
    val b = testDelay2(time)
    val c = testDelay3(time, "haha")
    return a + b + c
}
suspend fun testDelay1(time: Long): Int {
    delay(time)
    return 1
}

suspend fun testDelay2(time: Long): Int {
    delay(time)
    return 2
}
suspend fun testDelay3(time: Long, msg: String): Int {
    delay(time)
    println(msg)
    delay(time)
    return 3
}
````

```java
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.Boxing;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlinx.coroutines.DelayKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 2,
   d1 = {"\u0000\u0010\n\u0000\n\u0002\u0010\b\n\u0000\n\u0002\u0010\t\n\u0002\b\u0005\u001a\u0016\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u0003H\u0086@¢\u0006\u0002\u0010\u0004\u001a\u0016\u0010\u0005\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u0003H\u0086@¢\u0006\u0002\u0010\u0004\u001a\u0016\u0010\u0006\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u0003H\u0086@¢\u0006\u0002\u0010\u0004\u001a\u0016\u0010\u0007\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u0003H\u0086@¢\u0006\u0002\u0010\u0004¨\u0006\b"},
   d2 = {"testDelay", "", "time", "", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "testDelay1", "testDelay2", "testDelay3", "app_debug"}
)
public final class Test1Kt {
   @Nullable
   public static final Object testDelay(long time, @NotNull Continuation var2) {
      Object $continuation;
      label37: {
         // 检查传入的 var2类型，第一次调用testDelay时，var2是父函数调用的，var2不符合要求
         if (var2 instanceof <undefinedtype>) {
            $continuation = (<undefinedtype>)var2;
            // Integer.MIN_VALUE -> 10000000  00000000 00000000  00000000
            // Integer.MIN_VALUE 用来表示"挂起状态"
            // labal & Integer.MIN_VALUE 不为0 表示
            
            /**
             * ## &操作 如何理解?
             * 
             * > 从第二次开始才会走到这里
             * 
             * 1. 假设 lable之前没有 |= 过Integer.MIN_VALUE，那么lable就是1
             * 00000000 00000000 00000000 00000001 (this.label) 1
             * &
             * 10000000 00000000 00000000 00000000 (Integer.MIN_VALUE) (-2^31 即 -0)
             * -------------------------------------
             * 00000000 00000000 00000000 00000000 (result) (0)
             *
             * 2. 假设 lable之前有 |= 过Integer.MIN_VALUE，那么lable就是-1
             * 10000000 00000000 00000000 00000001 (this.label) 1
             * &
             * 10000000 00000000 00000000 00000000 (Integer.MIN_VALUE) (-2^31 即 -0)
             * -------------------------------------
             * 10000000 00000000 00000000 00000000 (result) -1 Integer.MIN_VALUE
             * > 以上可以得出结论，如果lable曾经 |= 过Integer.MIN_VALUE，然后再&Integer.MIN_VALUE，那么值就是Integer.MIN_VALUE，否则就是0
             * > 即，如果continuation曾经标记为挂起，那么&结果 != 0
             * 
             * ## &操作示例
             * 
             * ### 2ed
             * 10000000 00000000 00000000 00000001 (this.label) -1  
             * &  
             * 10000000 00000000 00000000 00000000 (Integer.MIN_VALUE) (-2^31 即 -0)  
             * -------------------------------------  
             * 10000000 00000000 00000000 00000000 (result) -1 Integer.MIN_VALUE  
             * 
             * ### 3rd  
             * 10000000 00000000 00000000 00000010 (this.label) -2  
             * &  
             * 10000000 00000000 00000000 00000000 (Integer.MIN_VALUE) (-2^31 即 -0)  
             * -------------------------------------  
             * 10000000 00000000 00000000 00000000 (result) -1 Integer.MIN_VALUE  
             * 
             * ## 结论
             * 如果“被挂起”则
             */

            if ((((<undefinedtype>)$continuation).label & Integer.MIN_VALUE) != 0) {
               /**
                * ## -=操作如何理解
                * - Integer.MIN_VALUE(10000000 00000000 00000000 00000000)即加它的补码(取反+1)
                *  10000000 00000000 00000000 00000000
                *  11111111 11111111 11111111 11111111 // 取反（符号位外，各位取反）
                *  10000000 00000000 00000000 00000000 // +1
                *  即原码补码一样
                * 10000000 00000000 00000000 00000001 (this.label) -1  
                * +  
                * 10000000 00000000 00000000 00000000 (Integer.MIN_VALUE) (-2^31 即 -0)  
                * -------------------------------------  
                *100000000 00000000 00000000 00000001 (result) 1 Integer.MIN_VALUE  
                * -1 变成1，即去掉符号位的1，变成 |= 之前的数值
                * 
                * ## -=操作示例

                * ### 2ed
                * 10000000 00000000 00000000 00000001 (this.label) -1  
                * +  
                * 10000000 00000000 00000000 00000000 (Integer.MIN_VALUE) (-2^31 即 -0)  
                * -------------------------------------  
                *100000000 00000000 00000000 00000001 (result) 1 Integer.MIN_VALUE  
                * 
                * ## 结论
                * 结束挂起
                */
               ((<undefinedtype>)$continuation).label -= Integer.MIN_VALUE;
               break label37;
            }
         }

         // 初始化$continuation，在var2上包了一层ContinuationImpl
         $continuation = new ContinuationImpl(var2) {
            // $FF: synthetic field
            Object result;
            int label;
            long J$0;
            int I$0;
            int I$1;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               /**
                * ## |=操作示例
                * ### 1st
                * 00000000 00000000 00000000 00000000 (this.label)
                * OR
                * 10000000 00000000 00000000 00000000 (Integer.MIN_VALUE) (-2^31 即 -0)
                * -------------------------------------
                * 10000000 00000000 00000000 00000000 (result)

                * ### 2ed
                * 00000000 00000000 00000000 00000001 (this.label) 1
                * OR
                * 10000000 00000000 00000000 00000000 (Integer.MIN_VALUE) (-2^31 即 -0)
                * -------------------------------------
                * 10000000 00000000 00000000 00000001 (result) -1

                * ### 3rd
                * 00000000 00000000 00000000 00000010 (this.label) 2
                * OR
                * 10000000 00000000 00000000 00000000 (Integer.MIN_VALUE) (-2^31 即 -0)
                * -------------------------------------
                * 10000000 00000000 00000000 00000010 (result) -2
                * 
                * ## 结论
                * 标志被挂起
                */
               this.label |= Integer.MIN_VALUE;
               return Test1Kt.testDelay(0L, this);
            }
         };
      }

      Object var10000;
      int a;
      int b;
      label31: {
         Object var8;
         label30: {
            Object $result = ((<undefinedtype>)$continuation).result;
            // 标志程序被挂起
            var8 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
            switch (((<undefinedtype>)$continuation).label) {
               // 初次调用 label为0
               case 0:
                  ResultKt.throwOnFailure($result);
                  ((<undefinedtype>)$continuation).J$0 = time;
                  // 推进状态机，将label设置为1
                  ((<undefinedtype>)$continuation).label = 1;
                  var10000 = testDelay1(time, (Continuation)$continuation);
                  // 如果testDelay1返回了var8
                  // 说明程序在testDelay1的执行中被挂起
                  if (var10000 == var8) {
                     return var8;
                  }
                  break;
               case 1:
                  time = ((<undefinedtype>)$continuation).J$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break;
               case 2:
                  a = ((<undefinedtype>)$continuation).I$0;
                  time = ((<undefinedtype>)$continuation).J$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break label30;
               case 3:
                  b = ((<undefinedtype>)$continuation).I$1;
                  a = ((<undefinedtype>)$continuation).I$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break label31;
               default:
                  throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
            }

            a = ((Number)var10000).intValue();
            ((<undefinedtype>)$continuation).J$0 = time;
            ((<undefinedtype>)$continuation).I$0 = a;
            ((<undefinedtype>)$continuation).label = 2;
            var10000 = testDelay2(time, (Continuation)$continuation);
            if (var10000 == var8) {
               return var8;
            }
         }

         b = ((Number)var10000).intValue();
         ((<undefinedtype>)$continuation).I$0 = a;
         ((<undefinedtype>)$continuation).I$1 = b;
         ((<undefinedtype>)$continuation).label = 3;
         var10000 = testDelay3(time, (Continuation)$continuation);
         if (var10000 == var8) {
            return var8;
         }
      }

      int c = ((Number)var10000).intValue();
      return Boxing.boxInt(a + b + c);
   }

   @Nullable
   public static final Object testDelay1(long time, @NotNull Continuation var2) {
      Object $continuation;
      label20: {
         if (var2 instanceof <undefinedtype>) {
            $continuation = (<undefinedtype>)var2;
            if ((((<undefinedtype>)$continuation).label & Integer.MIN_VALUE) != 0) {
               ((<undefinedtype>)$continuation).label -= Integer.MIN_VALUE;
               break label20;
            }
         }

         $continuation = new ContinuationImpl(var2) {
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return Test1Kt.testDelay1(0L, this);
            }
         };
      }

      Object $result = ((<undefinedtype>)$continuation).result;
      Object var5 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      switch (((<undefinedtype>)$continuation).label) {
         case 0:
            ResultKt.throwOnFailure($result);
            ((<undefinedtype>)$continuation).label = 1;
            if (DelayKt.delay(time, (Continuation)$continuation) == var5) {
               return var5;
            }
            break;
         case 1:
            ResultKt.throwOnFailure($result);
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      return Boxing.boxInt(1);
   }

   @Nullable
   public static final Object testDelay2(long time, @NotNull Continuation var2) {
      Object $continuation;
      label20: {
         if (var2 instanceof <undefinedtype>) {
            $continuation = (<undefinedtype>)var2;
            if ((((<undefinedtype>)$continuation).label & Integer.MIN_VALUE) != 0) {
               ((<undefinedtype>)$continuation).label -= Integer.MIN_VALUE;
               break label20;
            }
         }

         $continuation = new ContinuationImpl(var2) {
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return Test1Kt.testDelay2(0L, this);
            }
         };
      }

      Object $result = ((<undefinedtype>)$continuation).result;
      Object var5 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      switch (((<undefinedtype>)$continuation).label) {
         case 0:
            ResultKt.throwOnFailure($result);
            ((<undefinedtype>)$continuation).label = 1;
            if (DelayKt.delay(time, (Continuation)$continuation) == var5) {
               return var5;
            }
            break;
         case 1:
            ResultKt.throwOnFailure($result);
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      return Boxing.boxInt(2);
   }

   @Nullable
   public static final Object testDelay3(long time, @NotNull Continuation var2) {
      Object $continuation;
      label20: {
         if (var2 instanceof <undefinedtype>) {
            $continuation = (<undefinedtype>)var2;
            if ((((<undefinedtype>)$continuation).label & Integer.MIN_VALUE) != 0) {
               ((<undefinedtype>)$continuation).label -= Integer.MIN_VALUE;
               break label20;
            }
         }

         $continuation = new ContinuationImpl(var2) {
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return Test1Kt.testDelay3(0L, this);
            }
         };
      }

      Object $result = ((<undefinedtype>)$continuation).result;
      Object var5 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      switch (((<undefinedtype>)$continuation).label) {
         case 0:
            ResultKt.throwOnFailure($result);
            ((<undefinedtype>)$continuation).label = 1;
            if (DelayKt.delay(time, (Continuation)$continuation) == var5) {
               return var5;
            }
            break;
         case 1:
            ResultKt.throwOnFailure($result);
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      return Boxing.boxInt(3);
   }
}

```