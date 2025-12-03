Each thread is kind of like an independent agent running around
in a program.

A multi-threaded program has more than
one point of execution (i.e., multiple PCs, each of which is being fetched
and executed from).

They share the same address space and thus can access the same data.

withing same program, running Thread 2 after thread 1 requires a context switch. Each thread has its own PC, and set of registers for computation. But all threads share the same address space as the parent program. hence can access the same data. (Stack for each thread is different. THey are also called thread-local storage.)

For this context switching we have a Thread Control Block (TCB).    

pthread join() waits for a particular thread to complete.

Private registers: The registers are virtualized
by the context-switch code that saves and restores them

race condition: the results
depend on the timing execution of the code.

Due to race conditions we might get indeterministic output rather than a deterministic one.

A critical section is a piece of
code that accesses a shared variable (or more generally, a shared resource)
and must not be concurrently executed by more than one thread

atomic instructsion cannot be interrupted. Either they complete or they do not [garunteed by the hardware]. 

A race condition arises if multiple threads of execution enter the
critical section at roughly the same time; both attempt to update
the shared data structure, leading to a surprising (and perhaps undesirable) outcome

Using a few hardware instructions, we can build a good set of synchronization primitives.

An indeterminate program consists of one or more race conditions;
the output of the program varies from run to run, depending on
which threads ran when. The outcome is thus not deterministic,
something we usually expect from computer systems.


threads should use some kind of mutual
exclusion primitives so that only a single thread ever enters a critical section.

It is not necessary to join the threads, eg. indefinite web server. main program passes on requests to thread workers.

Condition variables are useful when some kind of signaling must take place
between threads, if one thread is waiting for another to do something before it can continue.

Useful for write()
Because an interrupt may occur at any time,
the code that updates to these shared structures (e.g., a bitmap for allocation, or the file’s inode) are critical sections

atomic means all or nothing.

the grouping of many actions into a single atomic action is called a transaction