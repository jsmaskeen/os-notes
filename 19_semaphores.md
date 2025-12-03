Semaphore is an object with an integer value, can be manipulated with semup() and semdown()
Firstly we need to initialize the semaphore with a value ( a positive integer)

```c
sem_t s;
sem_init(&s, 0, 1);
```
Here we have initialised the semaphore with the value 1. the 0 indicates that the semaphore will be shared across al the threads in the current process.

-> Semaphores can be synchronixed across different processes by changing the 2nd value while initializing the semaphore.

```c
int sem_wait(sem_t *s) { // semdown ; these should be done atomically P()
    decrement the value of semaphore s by one
    wait if value of semaphore s is negative
}
int sem_post(sem_t *s) { // semup ; these should be done atomically V()
    increment the value of semaphore s by one
    if there are one or more threads waiting, wake one
}
```
The value of the semaphore, when negative, is equal to the number of waiting threads. The user cannot see the value of the semaphore.

Binary Semaphores (Equivalnt to Locks)
Semaphore with initial value as 1 acts as a lock.

Semaphores can act as condition vairables too.
eg:
```c
sem_t s;
child:
    semup(&s); // sempost
parent: 
    sem_init(&s,0,0);
    printf(waiting for child);
    child_thread_create();
    semdown(&s); // semwait
```
Semaphore's initial value should be `0`.

2 paths:
1. parent creates thread and runs.. the semdown decrements to -1 and waits.. Child runs and mkaes it 0.
2. parent creates thread, then thread runs, semup makes the value 1 and parent sees this and runs.
both result in the outcome of parent waiting for the child's signal.

Producer Consumer (Bounded Buffer Problem)

for one producer/consumer we can get away with mutex because the two semaphores will take care forit (one sempahore to indicate buffer is full, and one sempahore for buffer is empty)

Initially since all places int he buffer are empty, empty is initialised to len(buffer). and full is initialised to 0.

But in case of multiple producer and consumer, there can be a race condition if we dont use a mutex, cause, two producers can see that some buffer entries are empty and simply run their code to put(i), however there is a context switch before returning, then the other producer cna override at the same index. Hence we need a mutex for the buffer.

But there is an issue of deadlock. If we guard our producer and consumer with a mutex for the buffer then tehre can be a case that the buffer is full, and now a producer runs, it gets a lock and waits for buffer to have atlease one free entry. However no consumer can consume cause lock is held by the producer. Hence a deadlock.

The issue is while doing sem wait we hold the lock.. (This want the issue with cond var.)

How to solve this ? (Reduce the scope of mutex) First see if there is a free slot then only try to acquire the lock. Once produced or consumed, then release lock, then signal.

Reader-Writer Locks.

Eg. concurrent lists. Writes need to be lcoked. but if we can garuntee that no write is taking place, then we can perform many concurrent reads.

Read from book once. fig 31.9

Idea is that maintain a count of readers, the first reader will get the write lock, and the last reaer can release the write lock. this ensures, that no reader read when data is written and no writer writes whilst the data is being read.

Dining Philosopher's problem..

5 philosophers , 5 forks.. need both forks to eat. also 5 semaphores for each fork (mutex).


```c
void getforks() {
    sem_wait(forks[left(p)]);
    sem_wait(forks[right(p)]);
}
void putforks() {
    sem_post(forks[left(p)]);
    sem_post(forks[right(p)]);
}
```
Issue: Deadlock.. all pick the one on their left.

Fix: break the cycle: let the last philosopher pick in a differnt order.

```c
void getforks() {
    if (p == 4) {
        sem_wait(forks[right(p)]);
        sem_wait(forks[left(p)]);
    } else {
        sem_wait(forks[left(p)]);
        sem_wait(forks[right(p)]);
    }
}
```

See the cigarette smoker’s problem or the sleeping barber problem.

Making semphores using locks, cv.
```c
struct sem_t {
    int val;
    lock_t lck;
    cond_t cond;
}

void seminit(sem_t*s, int v){
    s->val = v;
    lock_init(s->lck);
    cond_init(s->cond);
}

void semup(sem_t*s){
    lock(s->lck);
    s->val++;
    cond_signal(&s->cond);
    unlock(s->lck);
}

void semdown(sem_t*s){
    lock(s->lck);
    while (s->val <=0){
        cond_wait(&s->cond, &s->lck);
    }
    s->val--;
    unlock(s->lck);
}

```
