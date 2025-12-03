A lock is just a variable. It is either available (unlocked, free) or acquired (locked, held).

Exactly one thread can hold a lock at a given time.

We can include other data in the lock variable too such as which thread is holding it etc, but its usually hidden from the user.

Locks are used to provide mutual exclusion between the threads.

lock and unlock can take in the variable "lock", thus, we can have fine grained lock (which lock small number of instructions), and coarse grained locks. With fine grained locks, the concurrecny increases. 

Goals a lock should perform:

1. Provide Mutual Exclusion
2. Provide fairness to the threads waiting for that lock. THis means that once the lock is free, the threads waiting on it should fairly acquire the lock. [No thread should starve while competing for the lock]
3. Performance, overhead introduced by using locks. How will locks perfomr if we have multiple CPUs.

Making Locks work:

Method 1: Using interrupts (hardware support for turning on and off)

lock() -> Disable interrutps
unlock() -> enable interrupts.

Benefit: simplicity; Pitfals: requires threads to use a priviliged instruction, we need to trusst the program to not abuse this.

With this method, a greedy program (thread) can simply acqire lock at the begining, and simply use cpu. Or it may never unlock the lock hence OS never regains the control of the system.

This approach also doesnt work with multiple processors. (Imagine multiple threads, running on differnt cpu enter a crit section, even if we disable interrupts, threads can run on the other processor and enter crit section.)

When a CPU disables interrupts, it only affects that one CPU:
- It prevents that CPU from being interrupted (e.g., by a timer interrupt or I/O interrupt).
- It does not stop other CPUs from running.

Inefficient approach and interrrupts execute slowly on the CPU.

DIsabling interrupts on all CPUs: Technically prevents all concurrency but completely stalls the system 

also sometimes OS may require interrupts to run on its own so disabling interrupts might hinder the OS functionality.

Method 2: Peterson's turn based algo for 2 threads:

```c
int flag[2];
int turn;
void init() {
    flag[0] = flag[1] = 0; // 1->thread wants to grab lock
    turn = 0; // whose turn? (thread 0 or 1?)
}
void lock() {
    flag[self] = 1; // self: thread ID of caller
    turn = 1 - self; // make it other thread’s turn
    while ((flag[1-self] == 1) && (turn == 1 - self))
        ; // spin-wait
}
void unlock() {
    flag[self] = 0; // simply undo your intent
}
```
Initially no one has the lock and it's thread 0's turn to acquire the lock.

Idea is that when thread `i` says lock(); then flag[i] = 1 indicates that it is trying to get the lcok. and the next turn is of `j` (for 2 threads its `1-i`), now while the other thread (`j`) is trying to get the lock, and it is indeed their turn then we wait (spin).

Once thread `j` says unlock, we exit from the while and hence acquire the lock.

Thread i calls lock():
1. It sets flag[i] = 1 says “I want to enter critical section.”
2. Then it sets turn = 1 - i : gives priority to the other thread.
3. Then it spins while:
    - the other thread also wants to enter (flag[1 - i] == 1), and
    - it’s the other’s turn (turn == 1 - i).

When the other thread either
- no longer wants in (flag[1 - i] == 0), or
- gives up its turn (turn == i),
the condition fails : thread i enters the critical section.

On unlock():
- flag[i] = 0 : thread i no longer wants the lock.

Extension to N threads how ?? See filter and baker algo.

Method III: Test and Set (Atomic exchange)

```c

atomic thing: int test_and_set(int*ptr, int new){
    int old = *ptr;
    *ptr = new;
    return old;
}

typedef struct lockt {
    int flag;
} lockt;

void lock(lockt*mutex){
    while (test_and_set(&mutex->flag,1) == 1) // idea is to test the new value and return the old value.
    ; // spin   
}

void unlock(lockt*mutex){
    mutex->flag = 0;
}
```

THese are called spin locks. and on a single cpu system without premeption these done make any sense.

Spin locks are correct (mutual exclusion) but not fair (a thread may keep on spinning trying to acquire the lock) it may lead to starvation of some thread.

Performance is poor too. as say one thread is holding the lock and in a crit section. then the process is preempted, then cpu will check for all other n-1 threads waiting for this lock, and waste the cycles.

But on multiple CPUs, spinlocks work good (if num PCU = num threads)

The main oint is that, Spinning to wait for a lock held on another processor
doesn’t waste many cycles in this case, and thus can be quite effective.

Method IV: COmpare and Swap (compare and exchange)
same idea:

```c

int comp_and_swap(int*ptr, int old, int new){
    int cur = *ptr;
    if (cur == old){
        *ptr = new;
    }
    return cur;
}

void lock(lockt* mutex){
while (comp_and_swap(&mutex->flag, 0, 1) == 1); //spin while we dont have the lock
}
```

comp and swap is more powerful instruction than test and set (See this fact once)

To read : Load-Linked and Store-Conditional and Fetch-And-Add [More fair]

with N threads contending
for a lock; N − 1 time slices may be wasted in a similar manner, simply
spinning and waiting for a single thread to release the lock

for few threads, yeild will work
better than spinning but, say we have 100 threads, then 99 times we yeild. Can we optimise it further? And still there can be starvation, as a process might keep on yeilding.

Now to fix this we need to sleep rather than spin. Not leave it to chance, hence we introduce queues.

```c
typedef struct __lock_t {
    int flag;
    int guard;
    queue_t *q;
} lock_t;
```
We have a `park()` func to put a thread to sleep ,and `unpark(threadid)` to wake it up.

while acquiring the lock, do `while (test-and-set(&mutex->guard,1) == 1);` spin till we get a lock for the guard, then check if the lock is free by doing `mutex->flag == 0`, then do `mutex->flag = 1` and `mutex->guard = 0`.
But incase this check fails and the lock is held, simplt insert `getthread_id()` in `mutex->q`, `setpark()` and then do `mutex->guard = 0;`.

To unlock, acquire the guard by spinning and test-and-set. Then if queue is empty free the flag (lock), otherwise unpark the front thread in the queue.

set the guard to 0.

Here also we are spinwaiting but its for the guard which will be changed in every lock and unlock instruction. Hence not that bad. this also sort of does a FIFO on who wants the lock.

Notice that we do not set flag to 0 for the next thread which is waiting.. when it unparks, it is assumed that it has held the lock, as for that thread it would be asif it is returning from the park call.

