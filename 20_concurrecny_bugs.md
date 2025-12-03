# Concurrency Bugs
*Revision Notes based on OSTEP*

## 1. Non-Deadlock Bugs
Most concurrency bugs are not deadlocks. They typically fall into two categories:

### A. Atomicity-Violation Bugs
* **Definition:** Code that is intended to be atomic but is not enforced as atomic during execution.
* **The Fix:** Use **Locks** around the shared variable accesses to enforce atomicity.

### B. Order-Violation Bugs
* **Definition:** One thread assumes that a variable created or initialized in another thread is already present/active.
    * *Formal:* Thread A expects to run *before* Thread B, but this order is not enforced.
* **The Fix:** Use **Condition Variables** (or semaphores) to force the correct execution order.

## 2. Deadlocks
**Reasons for Deadlock:**
1.  **Circular Dependencies:** A cycle in the resource allocation graph.
2.  **Encapsulation:** With extensive encapsulation (e.g., in Java libraries), we may not know which locks are held by a function (like `A.add(B)`). If another thread calls `A.add(C)` in a different order, a deadlock may occur.

### The Four Necessary Conditions
For a deadlock to occur, **all four** of these conditions must hold:

1.  **Mutual Exclusion:** Threads claim exclusive control of resources that they require (e.g., a thread grabs a lock).
2.  **Hold and Wait:** Threads hold resources allocated to them (e.g., Lock L1) while waiting for additional resources (e.g., Lock L2).
3.  **No Preemption:** Resources (locks) cannot be forcibly removed from threads that are holding them.
4.  **Circular Wait:** There exists a circular chain of threads such that each thread holds a resource that is being requested by the next thread in the chain.


> **Key Takeaway:** If any *one* of these four conditions is not met, a deadlock cannot occur.

## 3. Deadlock Prevention
We can prevent deadlocks by writing code that breaks one of the four conditions.

### Strategy 1: Break "Circular Wait"
* **Solution:** Provide a **Total Ordering** on lock acquisition.
* **Mechanism:** If the system has locks L1 and L2, strictly enforce that L1 must always be acquired before L2. This prevents cyclic waits.

### Strategy 2: Break "Hold and Wait"
* **Solution:** Acquire **all** locks at once, atomically.
* **Mechanism:** Use a global "prevention" lock (meta-lock) to ensure atomicity when grabbing resources.
```c
lock(prevention); // Global lock
lock(L1);
lock(L2);
...
unlock(prevention);
```

  * **Pros:** Guarantees no context switch occurs while acquiring the batch of locks.

### Strategy 3: Break "No Preemption"

  * **Solution:** Use `pthread_mutex_trylock()` instead of blocking locks.
  * **Mechanism:** If a thread holds L1 and tries to get L2 but fails, it should **release** L1 and try again later.



```c
top:
lock(L1);
if (trylock(L2) == -1) {
    unlock(L1); // Preempt yourself
    goto top;
}
```

**New Problem: Livelock**

  * In the scenario above, two threads might repeatedly lock L1, fail to get L2, unlock L1, and repeat this cycle indefinitely. No progress is made (similar to thrashing in paging).
  * **Fix for Livelock:** Add a **random delay** before retrying.

### Strategy 4: Break "Mutual Exclusion"

  * **Solution:** Avoid the need for locks entirely by using **Wait-Free Data Structures**.
  * **Mechanism:** Use powerful atomic hardware instructions like **Compare-And-Swap (CAS)**.

**Compare-And-Swap Logic:**

```c
int CompareAndSwap(int *addr, int expected, int new) {
    if (*addr == expected) {
        *addr = new;
        return 1; // Success
    }
    return 0; // Failure
}
```

**Example: Lock-Free Atomic Increment**

```c
void incrementbyx(int *addr, int x) {
    do {
        int current = *addr; // Snapshot the value
    } while (CompareAndSwap(addr, current, current + x) == 0);
}
```

  * **Why the loop?** If `*addr` changes between the snapshot and the CAS, the CAS fails (returns 0). The loop forces a retry with the new value.
  * **Why not `CAS(addr, *addr, *addr + x)`?** This is flawed because the arguments are evaluated before the function call. By the time CAS runs, `*addr` might have changed, but the function would be using the stale value passed in the arguments.

**Example: Lock-Free List Insert**

```c
void insert(int value) {
    node_t *n = malloc(sizeof(node_t));
    assert(n != NULL);
    n->value = value;
    do {
        n->next = head; // Point to current head
    } while (CompareAndSwap(&head, n->next, n) == 0); // Try to swap head to n
}
```

> **Note (Refer to Book/Slides):** Review the specific algorithms and graphs for deadlock detection in the slides.
