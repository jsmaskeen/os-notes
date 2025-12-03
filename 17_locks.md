# Locks & Synchronization


## 1. The Lock Abstraction
A lock is simply a variable that exists in one of two states:
1.  **Available** (unlocked, free).
2.  **Acquired** (locked, held).

**Constraint:** Exactly one thread can hold a lock at a given time. This property allows locks to provide **Mutual Exclusion** between threads.

### Granularity
* **Fine-grained:** Locks protect a small number of instructions (increases concurrency).
* **Coarse-grained:** Locks protect large segments of code.

## 2. Goals of a Lock
Any lock implementation should satisfy three goals:
1.  **Mutual Exclusion:** Ensure only one thread enters the critical section.
2.  **Fairness:** When the lock becomes free, threads waiting for it should have a fair chance to acquire it. No thread should starve.
3.  **Performance:** Minimize the overhead introduced by using locks (especially regarding how they perform on multiple CPUs).

---

## 3. Method I: Controlling Interrupts
The earliest strategy (for single-processor systems) was to disable interrupts.

**Mechanism:**
* `lock()` $\rightarrow$ Disable interrupts.
* `unlock()` $\rightarrow$ Enable interrupts.

**Analysis:**
* **Benefit:** Simplicity.
* **Pitfalls:**
    1.  **Trust:** Requires the thread to perform a privileged instruction. A greedy program could acquire the lock and never release it (OS never regains control).
    2.  **Multiprocessor Failure:** This does **not** work on multiple processors. Disabling interrupts only affects one CPU; threads on other CPUs can still enter the critical section.
    3.  **Inefficiency:** Interrupt masking is slow on modern CPUs.

---

## 4. Method II: Software-Only (Peterson's Algorithm)

A 2-thread algorithm that works without special hardware instructions.

### The Code
```c
int flag[2]; // flag[i]=1 means thread i wants the lock
int turn;    // whose turn is it?

void lock() {
    flag[self] = 1;      // I want the lock
    turn = 1 - self;     // I give priority to the other thread
    
    // Spin wait while:
    // 1. The other thread wants the lock
    // 2. AND it is the other thread's turn
    while ((flag[1-self] == 1) && (turn == 1 - self)); 
}

void unlock() {
    flag[self] = 0; // I no longer want the lock
}
````

### How it works

1.  **Intent:** Thread $i$ sets `flag[i] = 1` to indicate it wants to enter.
2.  **Priority:** Thread $i$ sets `turn = 1 - i` to yield priority to the other thread.
3.  **Spin:** It waits only if the other thread wants in **AND** it is the other thread's turn.

> **Note (Refer to Book):** For extending this logic to $N$ threads, look up the **Filter Algorithm** and **Bakery Algorithm**.

-----

## 5. Method III: Hardware Primitives (Spin Locks)

Modern systems use atomic hardware instructions to build locks.

### A. Test-and-Set (Atomic Exchange)

This instruction updates a value and returns the *old* value atomically.

```c
int test_and_set(int *ptr, int new) {
    int old = *ptr;
    *ptr = new;
    return old;
}

void lock(lockt *mutex) {
    // Spin while the old value was 1 (meaning it was already locked)
    while (test_and_set(&mutex->flag, 1) == 1); 
}
```

### B. Compare-and-Swap (Compare-and-Exchange)

This instruction checks if the current value equals `old`; if so, it updates it to `new`. It is generally more powerful than Test-and-Set.

```c
int comp_and_swap(int *ptr, int old, int new) {
    int cur = *ptr;
    if (cur == old) {
        *ptr = new;
    }
    return cur;
}

void lock(lockt *mutex) {
    while (comp_and_swap(&mutex->flag, 0, 1) == 1);
}
```

> **Note (Refer to Book):** Read about **Load-Linked / Store-Conditional** and **Fetch-And-Add** (which provides better fairness).

### Analysis of Spin Locks

  * **Correctness:** They provide mutual exclusion.
  * **Fairness:** They are **not fair**. A thread may spin forever (starvation).
  * **Performance:**
      * **Single CPU:** Poor performance. If a thread holding the lock is preempted, the scheduler might run $N-1$ other threads that just spin and waste time slices.
      * **Multiple CPUs:** Works well. Spinning to wait for a lock held on another processor is often effective (doesn't waste many cycles if the critical section is short).

-----

## 6. Method IV: Sleeping (Queue-Based Locks)

To solve the problem of wasting CPU cycles while spinning, we use queues to put waiting threads to sleep.

### Mechanisms

  * `yield()`: A thread voluntarily gives up the CPU. Better than spinning, but still inefficient with many threads (context switch overhead) and allows starvation.
  * `park()`: Puts the calling thread to sleep.
  * `unpark(threadID)`: Wakes a specific thread.

### The Solaris-Style Lock (Flag + Guard + Queue)

```c
typedef struct __lock_t {
    int flag;     // The actual lock
    int guard;    // Protects the lock structure (spinlock)
    queue_t *q;   // Queue of waiting threads
} lock_t;
```

**The Algorithm:**

1.  **Acquire Guard:** Use `test-and-set` on `guard` to safely manipulate the struct.
2.  **Check Lock (`flag`):**
      * If `flag == 0` (free): Set `flag = 1`, set `guard = 0` (release guard), and enter critical section.
      * If `flag == 1` (busy):
        1.  Insert `getthread_id()` into queue `q`.
        2.  Call `setpark()` (prepare to sleep).
        3.  Release `guard = 0`.
        4.  `park()` (sleep).

**The Handover (Unlock):**

1.  Acquire `guard`.
2.  If the queue is empty, release `flag` (`flag = 0`).
3.  If the queue is **not** empty:
      * `unpark()` the front thread.
      * **Note:** Do *not* set `flag = 0`. The waking thread assumes it holds the lock immediately upon returning from `park()`.
4.  Release `guard`.