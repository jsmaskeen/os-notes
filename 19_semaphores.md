# Semaphores


## 1. Definition and Initialization
A **Semaphore** is an object with an integer value that can be manipulated using two specific routines: `sem_wait()` and `sem_post()`.

**Initialization:**

We must initialize the semaphore with a positive integer value before using it.
```c
#include <semaphore.h>
sem_t s;

// args: pointer to sem, pshared (0=threads, 1=processes), initial value
sem_init(&s, 0, 1); 
```

  * **Initial Value:** Here, initialized to 1.
  * **Sharing:** The second argument `0` indicates that the semaphore is shared among threads in the current process. To synchronize across different **processes**, change this value to 1.

## 2. The Operations

These operations must be performed **atomically**.

### `sem_wait()` (semdown / P)

```c
int sem_wait(sem_t *s) {
    decrement the value of semaphore s by one;
    wait if value of semaphore s is negative;
}
```

### `sem_post()` (semup / V)

```c
int sem_post(sem_t *s) {
    increment the value of semaphore s by one;
    if there are one or more threads waiting, wake one;
}
```

> **Note:** Internally, if the value of the semaphore is negative, the absolute value typically represents the number of waiting threads. However, the user cannot see this internal value directly.

## 3. Usage Patterns

### A. Binary Semaphores (Locks)

A semaphore initialized with the value **1** acts as a lock (Mutex).

  * `sem_wait()` $\approx$ `lock()`
  * `sem_post()` $\approx$ `unlock()`

### B. Ordering (Condition Variables)

Semaphores can be used to order events (e.g., making a parent wait for a child).

  * **Initial Value:** Must be **0**.

```c
sem_t s;

void child() {
    // Do work
    sem_post(&s); // Signal parent
}

void parent() {
    sem_init(&s, 0, 0); // Init to 0
    printf("waiting for child");
    child_thread_create();
    sem_wait(&s); // Wait for child
}
```

**Why this works (Two Paths):**

1.  **Parent runs first:** Calls `sem_wait`, decrements to -1, and goes to sleep. Child runs later, calls `sem_post`, increments to 0, and wakes parent.
2.  **Child runs first:** Calls `sem_post`, increments to 1. Parent runs later, calls `sem_wait`, decrements to 0, and proceeds immediately without waiting.

## 4. The Producer-Consumer Problem

(Also known as the Bounded Buffer Problem).

**Setup:**

  * `empty`: Semaphore initialized to `buffer_size` (tracks empty slots).
  * `full`: Semaphore initialized to `0` (tracks filled slots).

### The Role of Mutex

In a multi-producer/multi-consumer scenario, semaphores alone are insufficient because race conditions can occur when inserting/removing from the buffer index. We need a **Mutex** to protect the buffer modification.

### The Deadlock Issue

If we implement the lock naively, we get a deadlock:

```c
// BAD CODE (Deadlock Risk)
lock(&mutex);       // Acquire Lock
sem_wait(&empty);   // Wait for empty slot
    put(i);
sem_post(&full);
unlock(&mutex);
```

**Scenario:** If the buffer is full, the producer acquires the lock and *then* waits on `empty`. The consumer cannot run (to make space) because the producer holds the lock. **Deadlock.**

### The Solution: Scope of Lock

Move the `sem_wait` **outside** the mutex lock.

1.  Wait for a free slot (`sem_wait`).
2.  **Then** acquire the lock to manipulate the buffer.
3.  Release the lock.
4.  Signal (`sem_post`).

## 5. Reader-Writer Locks

Useful for concurrent lists where we want many concurrent reads but exclusive writes.

**The Logic:**

1.  **First Reader:** Acquires the write lock (blocks any writers).
2.  **Middle Readers:** Just read (since the write lock is already held by the group).
3.  **Last Reader:** Releases the write lock (allows writers to proceed).

> **Note (Refer to Book):** See **Figure 31.9** for the implementation details. Note that this approach can lead to writer starvation.

## 6. The Dining Philosophers Problem

**Setup:** 5 philosophers, 5 forks. A philosopher needs **two** forks (left and right) to eat.

**Naive Solution:**

```c
void getforks() {
    sem_wait(forks[left(p)]);
    sem_wait(forks[right(p)]);
}
```

**Issue:** **Deadlock**. If all 5 philosophers grab their left fork simultaneously, they all wait forever for their right fork.

**Solution (Breaking the Cycle):**
Change the order for the last philosopher (Philosopher 4).

  * Philosophers 0-3: Grab **Left**, then **Right**.
  * Philosopher 4: Grab **Right**, then **Left**.

> **Note (Refer to Book):** Also look up the **Cigarette Smoker’s Problem** and the **Sleeping Barber Problem**.

## 7. Implementation: Zemaphores

Building a Semaphore using Locks and Condition Variables.

```c
typedef struct {
    int val;
    lock_t lck;
    cond_t cond;
} sem_t;

void sem_init(sem_t *s, int v) {
    s->val = v;
    lock_init(&s->lck);
    cond_init(&s->cond);
}

void sem_post(sem_t *s) {
    lock(&s->lck);
    s->val++;
    cond_signal(&s->cond); // Wake up a sleeper
    unlock(&s->lck);
}

void sem_wait(sem_t *s) {
    lock(&s->lck);
    while (s->val <= 0) {
        cond_wait(&s->cond, &s->lck); // Sleep if value is <= 0
    }
    s->val--;
    unlock(&s->lck);
}
```