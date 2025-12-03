Idea is to put a thread to sleep (wait for other thread to complete/signal) and wakeup when the other thread signals.

Using a shared variable + locks will waste CPU time.

```c
pthread_cond_wait(pthread_cond_t *c, pthread_mutex_t *m);
pthread_cond_signal(pthread_cond_t *c);
```

A CV is an explicit queue, that threads can put themselves on, when some condition is not as desired by some other thread (by waiting on the condition). When the condition evaluates to true, the other thread can signal (wakeup) one or more threads waiting for that condition.

wait call takes in mutex. it assumes that the mutex is locked before executing the call. It internally releases the lock and puts the process to sleep. After waking up it reacquires the lock and returns.

State variables are important while using Conditional variables.

It is recommended to hold the lock while singalling, however, there are some cases where it is okay not to hold the laock while signaling.

Eg: where it is must to hold lock while signalling.

```c
void thr_exit() {
    done = 1;
    Pthread_cond_signal(&c);
}

void thr_join() {
    if (done == 0)
        Pthread_cond_wait(&c);
}
```

Generalized semaphore, can be used as a lock or a cond variable.

Producer Consumer Problem, (Bounded Buffer Problem)

Setup: One or more producer threads produce and place items in a buffer
One or more consumer threads consume or take items out fo the buffer.
Producers cannot produce if the buffer is full .
consmers cannot comsume if the buffer is empty.

Wehn we pipe from one file to other a bounded buffer is used

say m produces, and n consumers. using a single conv dar isnt good because a producer might wakeup another producer. Or a consumer might wake up another consumer. [BUt for a single producer/consumer it will work.]

Hence we need 2 conditional variables, one to signal/wait for that the buffer is full, and one to signal/waitfor the buffer is empty

Signaling a thread only wakes them up; it is thus a hint that the state
of the world has changed (in this case, that a value has been placed in the
buffer), but there is no guarantee that when the woken thread runs, the
state will still be as desired

(Mesa Semantics) with condition variables is to always use while loops

Problem with a singe cond var. Say 2 consumers C1, C2 and one Producer P. C1,C2 run, goto sleep, wait for signal. Then P produces and sleeps, wakes C2 up. Now C2 consumes, and signals but that signal wakes C1 up instead of P. SO now (since we kept the cond wait in a whiel loop) it will run, see that buffer is empty and sleep. Now everyone is sleeping :3

2 reasons for using while, and not if:
1. If can be passed by just the semantics of singalling. The state may not have changed.
2. It will prevent spurious wakeups.

Covering Conditions: say free and malloc. malloc waits for param size ot be less than or eq bytesfree. free increments the bytesfree and signals. now say 2 programs, one does malloc(!00) and one does malloc(50), and 0 bytes are free, and we call free(60). Now we only have one CV. which malloc thread will wake up ? if 100 wakes up it will unnecessarily sleep, and wait for being woken up, and malooc(50) will also remian sleeping.. nothing will happen.

Hence we have a broadcast message. rather than signaling on the cond var, free can simple broadcast to wake up all sleeping threads on the condition. However it ads performance costs. that too many threads can be worken up.

Also we could have solved producer consumer by one cond var by simply using broadcast message.

Barrier(N).. ensures that all the N threads come to a common program point of execution, and then pass the barrier.
Can be built using cond variables.

```c
mutex m;
cond c;
int num;
int N;

void barrier_init(int* num, int* N, int n){
   *num = 0;
   *N = n;
   mutex_init(m);
   cond_init(c);
}

void barrier_check(int* num, int* N, mutex* m){
   lock(m);
   *num++;
   if (*num < *N){ // can be affected by spurious wakeup
        cond_wait(c,m);
   } else {
    *num = 0;
    broadcast(c);
   }
   unlock(m);
}
```
so better to use sleep on a specific channel. (sleep wakeup mechanism)