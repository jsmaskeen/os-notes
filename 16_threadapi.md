# Pthread API
*Revision Notes based on OSTEP*

## 1. Function Pointers in C
To use pthreads, we often need to understand function pointers.
* **Why `void *`?** We use `void *` in signatures because it allows us to pass and return data of **any type**.

**Syntax Examples:**
* Function taking `int`, returning `void*`: `void * (*start_routine)(int)`.
* Function taking `void*`, returning `int`: `int (*start_routine)(void *)`.

## 2. Thread Creation
To create a thread, we use `pthread_create`.

```c
int pthread_create(
    pthread_t *thread,                  // pointer to thread identifier variable
    const pthread_attr_t *attr,         // specifies thread attributes (can be NULL)
    void *(*start_routine)(void *),     // func pointer: takes void*, returns void*
    void *arg                           // argument passed to start_routine
);
```

  * **Return Value:** Returns `0` for success and non-zero for failure.
  * **Arguments:** The `arg` passed must match the type expected by the `start_routine`.

## 3. Thread Completion

### `pthread_join()`

Waits for the specified thread to complete execution.

```c
int pthread_join(pthread_t thread, void **retval);
```

  * **`retval`:** Used to retrieve the return value from the thread’s start routine (which returns `void *`).

**Equivalence:**
Immediately creating a thread and then joining it is equivalent to a standard **function/procedure call**.

### `pthread_detach()`

If you call `pthread_detach(thread)`, you explicitly tell the OS that you will **not** join this thread.

  * **Effect:** You cannot call `pthread_join` on that thread anymore.
  * **Cleanup:** Detached threads clean up their own resources automatically when they exit.

> **Warning (Deadlock):** Calling `pthread_join` on **yourself** (the current thread) will cause the program to hang forever (deadlock).

## 4. Code Example

Here is a safe implementation of passing arguments and returning results:

```c
void *compute_sum(void *arg) {
    int n = *(int *)arg;
    
    // Allocate memory on heap for the result to persist after thread exits
    int *result = malloc(sizeof(int));
    *result = n * (n + 1) / 2; 
    return result;
}

int main() {
    pthread_t tid;
    int n = 10;
    void *res;

    pthread_create(&tid, NULL, compute_sum, &n);
    pthread_join(tid, &res); 
    
    printf("Sum = %d\n", *(int *)res);
    free(res); // Important: free the allocated memory
    return 0;
}
```

## 5. Memory Safety Guidelines

### Passing Arguments (Stack vs. Heap)

If you pass the address of a **local variable** (stack memory) to a thread:

  * You must ensure the main thread does not **modify** that variable or **go out of scope** (exit) before the new thread finishes using it.

### Returning Values

**Never** return a pointer to a local variable defined on the thread's stack.

  * **Reason:** When the thread exits, its stack memory is destroyed/reclaimed.
  * **Result:** The parent will receive a pointer to garbage values or unmapped memory, potentially causing a **Segmentation Fault**.

## 6. Synchronization: Condition Variables

Condition variables are used when one thread is waiting for another to do something before it continues.

### Locking Rules

1.  **Waiting (`cond_wait`):** Requires the **lock** (mutex) and the **condition variable**.
      * *Internally:* `cond_wait` releases the lock (so other threads can run) and puts the calling thread to sleep.
      * *Upon Return:* When returning from the wait, the thread automatically **re-acquires** the lock.
2.  **Signaling:** We should hold the lock while signaling to prevent race conditions.

### Spurious Wakeups

`cond_wait` should always be run inside a **`while` loop**, not an `if` statement.

  * **Reason:** To handle **spurious wakeups** (the thread might wake up even if the condition hasn't been met).

### Anti-Pattern: Spin Waiting

An alternative to condition variables is spinning:

```c
while (init == 0); // In thread A
init = 1;          // In thread B
```

  * **Verdict:** This is **not recommended**. It wastes CPU cycles (performs poorly) and is error-prone.