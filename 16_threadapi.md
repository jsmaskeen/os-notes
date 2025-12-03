Function pointers in C:

needs int, return void*: `void * (*start_routine)(int)`
needs void*, return int: `int (*start_routine)(void *)`

why void* ? we can make use of it as any type!

Create:

```c
int pthread_create(
    pthread_t *thread, // pointer to thread identifier var
    const pthread_attr_t *attr, // specifies thread attributes (can be NULL)
    void *(*start_routine)(void *), // func pointer, needs void* and retunrs void*
    void *arg // argument passed. the type must match the above signature.
);
```

this returns 0 for success and non zero for fail.

Join:
```c
int pthread_join(pthread_t thread, void **retval);
```
waits for the specified thread to complete

retval: Used to retrieve the return value from the thread’s start routine (void *return_value).

```c

void *compute_sum(void *arg) {
    int n = *(int *)arg;
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
    free(res); // free the allocated memory
    return 0;
}
```

If you call pthread_detach(thread), you can’t join that thread anymore.

Detached threads clean up their own resources automatically when they exit.

Calling pthread join on urself will make it hang forever, deadlock

As an argument:
If you pass the address of a local variable, ensure that the main thread doesn’t modify or go out of scope before the new thread finishes.

If we return a value of a local variable from thread's stack, then When the thread exits, its stack memory is destroyed / reclaimed. hence we might get garbage value or that memory might be unmapped so we can get a segfault.

immediately creating and joining a thread is equivalent to a function call/procedure call.


we should hold the lock while signalling, to prevent race conditions

cond_Wait takes in the lock and the initializser
while signal only requres the initializer, this is because, while waiting we should release the lock. SO that the other thread can acquire it, run and then signal us.

and when returning from wait we should reaquire it.

Cond wait runs in a while loop, to prevent spurious wakeups.

rather than using conv var and locks we can do: 

while (init == 0);

and in the other thread, init=1

this isnt recommeneded cause it performs poorly on the CPU, wastes cpu cycles, and error prone.

