# Condition Variables
*Revision Notes based on OSTEP*

## 1. The Concept
A **Condition Variable (CV)** is an explicit queue that threads can put themselves on when some condition is not as desired (waiting on the condition).
* **Goal:** To put a thread to sleep (waiting for another thread to complete/signal) and wake it up when the state changes, avoiding the CPU waste of busy-waiting (spinning).

### The API
```c
pthread_cond_wait(pthread_cond_t *c, pthread_mutex_t *m);
pthread_cond_signal(pthread_cond_t *c);
```

**How `wait` works:**

1.  It assumes the mutex `m` is **locked** when called.
2.  It internally **releases** the lock and puts the calling thread to sleep.
3.  When the thread wakes up (after a signal), it **re-acquires** the lock before returning to the caller.

## 2. Usage Guidelines

### State Variables

A CV is stateless; it must be used in conjunction with a **state variable** (e.g., an integer `done` or a buffer counter) to track the actual condition.

### Locking Rule

It is recommended to **hold the lock** while signaling.

  * While there are edge cases where it is okay not to, holding the lock prevents race conditions where a thread checks the state and tries to sleep just as another thread signals.

### Mesa Semantics (The `while` Loop Rule)

When using condition variables, **always use `while` loops**, not `if` statements.

```c
while (done == 0)
    pthread_cond_wait(&c, &m);
```

**Reasons:**

1.  **Signaling is a hint:** The signal wakes the thread, but there is no guarantee that the state is still desired when the thread actually runs.
2.  **Spurious Wakeups:** Threads might wake up without a signal due to OS implementation details.

> **Note (Refer to Book):** Look up **Hoare Semantics** vs. **Mesa Semantics** to understand the theoretical differences in how locks are transferred upon signaling.

## 3. The Producer-Consumer Problem (Bounded Buffer)

**Setup:**

  * **Producers:** Place items in a buffer. Cannot produce if the buffer is full.
  * **Consumers:** Take items out of the buffer. Cannot consume if the buffer is empty.
  * **Real-world Example:** Unix pipes use a bounded buffer.

### The Single CV Problem

Using a single condition variable is problematic with multiple producers/consumers.

  * *Scenario:* A consumer (`C1`) sleeps. A producer (`P`) fills a slot and signals, but accidentally wakes another consumer (`C2`) instead of `C1`. `C2` sees the buffer is empty (because `P` filled it but maybe `C1` ate it? Or `C2` runs and finds nothing).
  * *Result:* Everyone might end up sleeping.

### The Solution: Two CVs

Use two separate condition variables:

1.  `empty`: To signal/wait that the buffer is empty (used by producers).
2.  `full`: To signal/wait that the buffer is full (used by consumers).

## 4. Covering Conditions (Broadcast)

Sometimes, we do not know *which* thread to wake up.

**Example: Memory Allocation (`malloc` & `free`)**

  * Threads `A` (needs 100 bytes) and `B` (needs 50 bytes) are waiting.
  * Thread `C` calls `free(60)`.
  * If `C` signals and wakes `A`: `A` checks, sees 60 \< 100, and goes back to sleep. `B` remains asleep despite 60 bytes being enough for it.

**Solution:**
Use **Broadcast** (`pthread_cond_broadcast`).

  * This wakes **all** sleeping threads. They all check their conditions; the one that can proceed does, and the others go back to sleep.
  * *Trade-off:* Performance cost (thundering herd problem).

## 5. Barriers

A barrier ensures that $N$ threads reach a common point of execution before any of them proceed.

### Implementation

```c
typedef struct {
    int num;      // Counter for threads arrived
    int N;        // Total threads required
    mutex m;
    cond c;
} barrier_t;

void barrier_check(barrier_t *b) {
    lock(&b->m);
    b->num++;
    
    if (b->num < b->N) {
        // Not everyone is here yet, so wait
        cond_wait(&b->c, &b->m); // Spurious wakeups handled by re-check logic usually
    } else {
        // Everyone arrived! Reset and wake everyone
        b->num = 0;
        broadcast(&b->c);
    }
    unlock(&b->m);
}
```

> **Note (Refer to Book):** Generalized **Semaphores** can also be used as a lock or a condition variable. Check the book for the specific implementation details.
