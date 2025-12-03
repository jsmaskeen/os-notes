- Non deadlock bugs
    1. atomicity-violation bugs: Code that is intended to be atomic, but is not made atomic/ or enfored the atomicity during execution. SOlution is to use locks around shared variables.
    2. Order Violation Bugs: One thread assumes that a variabled created in the other thread is already present in scope.. Formally, `A` should always be executed before `B`, but the order is not enforced during execution. Fix: Use condition variables.

Deadlock Reasons:
1. Circular Dependencies.
2. Too much encapsulation. Eg. multithreaded A.add(B), we dont know how the locks are held. and if some other thread calls A.add(C) we might get into a deadlock.

Conditions for a deadlock:
These four should be there for a deadlock to occur:
1. Mutual Exclusion: Threads claim exclusive control of resources that they require.
2. Hold and Wait: Threads hold resources allocated to them while waiting for additional resources 
3. No preemption: Resources (e.g., locks) cannot be forcibly removed from threads that are holding them.
4. Circular Wait: There exists a circular chain of threads such that each thread holds one more resources (eg., locks) that are being requested by the next thread in the chain.

If any of these 4 isnt met then a deadlock cannot occur.

Prevention:
1. Circular Wait: Write code such that it naturally provides a total ordering on acquiring the locks. Basically prevent cyclic waits.

2. Hold and Wait: Acquire all the locks at once, eg:
```c
lock(prevention);
lock(L1);
lock(L2);
...
unlock(prevention);
```
The prevention lock garuntees that there is no context switch while acquiring all the needed locks.

3. No preemption: We can get into trouble, if we wait for a lock while holding the other. TO fix this we can use `trylock(lock)` which returns -1 if we cant acquire the lock otherwise it grabs the lcok.

```c
top:
lock(L1);
if (trylock(L2) == -1) {
    unlock(L1);
    goto top;
}
```

We can have another program try to get the locks in order L2 then L1, we wont have any deadlocks, but we can have a livelock (thrashing as example from paging.). No actual progress happens, but the threads keep competing for locks, and fail to acquire some. Solution for livelock: add a random delay to one of the threads.

4. Mutual Exclusion: Avoid the need of mutual exclusion. Idea is to have wait-free datastructures which use special hardware instrucitons to make operatiosn atomic.

Eg: increment with `compare-and-swap(int*addr, int expected, int new)` which checks `if *addr == expected`, then sets `*addr = new`, and returns `1`. otherwise return `0`.

Increment by one using compare-and-swap:

```c
void incrementbyx(int *addr,int x){
    do {int current = *addr;}
    while (compare_and_swap(addr, current, current+x) == 0);
}
```
If we dont do this do while thing, in that case, the current value might be differnt as some other thread might have changed it. If we did `CAS(addr, *addr, *addr + x)`, still it is flawyed, cause `*addr`, when evaluated might be different from `*addr` when evaluated in `*addr + x`.

Similarly,

```c
void insert(int value) {
    node_t *n = malloc(sizeof(node_t));
    assert(n != NULL);
    n->value = value;
    do {
        n->next = head;
    } while (CompareAndSwap(&head, n->next, n));
}
```

See slides for deadlock. algo and graphs.

