Process is a abstraction provided by OS for a running program

We need to provide illusion of many CPUs to the user, as a tone time only one program can run on one CPU.

How does OS virtualize CPU-> run one program after the other in fixed time slices and change between them very quickly,

more cpu sharing -> more time each program takes to complete. (assuming same priortity and runnign duration for each program)

Time sharing is one of the most basic techniques used by an OS to share
a resource. By allowing the resource to be used for a little while by one
entity, and then a little while by another, and so forth, the resource in
question (e.g., the CPU, or a network link) can be shared by many. The
natural counterpart of time sharing is space sharing, where a resource is
divided (in space) among those who wish to use it. For example, disk
space is naturally a space-shared resource, as once a block is assigned to
a file, it is not likely to be assigned to another file until the user deletes it.

Stopping one program and runnign another program is called a context switch. this is a time sharing mechanism

Policies are algorithms for making some
kind of decision within the OS
eg: scheduling policy, page replacement policy etc.


the memory that the process can address is called its address space. It is a part of process itself.
For the state (proc struct), we require Program Counter register/ instruction pointer register, top of stack, top of kstack, IO information etc.

HOw is a process created ? 

OS needs to load its code and static variables into the address space for that process. modern os loads programs lazily, as an when needed, code etc is loaded.
Then the program's runtime stack (Stack) is reserved in the address space for local variables, return addresses. We nned memory for heap (to assign and dellocate memory dynamically at runtime). OS loads the file IO descriptors and then starts running the program at the entry point, namely main().

States:
- New (initial): its a new process, being set up by OS right now
- Running: running right now
- Ready (Runnable): ready to run
- Sleeping (Waiting, Blocked): In sleeping state, or waiting for IO to complete. 
- Zombie (Terminated, Final): It will now be cleaned up by the OS

Scheduling is the process of Ready -> Running.

Whats Zombie  and WHy ?

This final state can be useful as it allows other processes
(usually the parent that created the process) to examine the return code
of the process and see if it the just-finished process executed successfully

1. A process finishes execution → it calls `exit()`.

   * At this point, its resources (memory, file descriptors, etc.) are freed.
   * But the kernel still keeps a small entry in the process table (its **exit status**, PID, and some accounting info).
   * This "dead but not yet fully removed" process is called a **zombie**.

2. The parent process is supposed to call `wait()` (or `waitpid()`) to collect that exit status.

   * Once the parent does this, the kernel removes the zombie entry from the process table completely.

3. If the parent **never calls wait()**, the zombie stays.

4. If the parent itself exits without waiting → the kernel reassigns the zombie to **`init` (PID 1)**.

   * `init` (or nowadays `systemd` in Linux) will automatically `wait()` on all orphaned zombies, cleaning them up.
   * So in practice, zombies don’t linger forever unless the parent is alive but not waiting.


OS needs a process list to keep track of all processes.
Every processer needs a register context to hold contents of its registers.

The proc struct in xv6 is often called a Process Control Block (PCB)

fork(): Makes a copy of the parent process and starts executing as if it had called fork() itself.
However the child process has a return value of 0 form fork, and the parent's fork gets a return value of the the PID of child.
If fork() < 0 then the fork failed.

Note it makes a deep copy!! Stack, heap, code everything.

It gets its own address space and everything.

But open file descriptors, and shared memory segemtns are common with the child process..

BUT!!! if child closes some file descriptor and exits then the parent's file descriptor will NOT be closed.

Child closes -> parent’s copy is still valid.
Parent closes -> child’s copy is still valid.

If parent calls wait(), then the parent will wait till the child completes its execution. (Wait is per process. So if you do fork 3 times then wait should be done three times.)

if the parent does happen to run
first, it will immediately call wait(); this system call won’t return until
the child has run and exited.


Wait here is blocking.. Once the child calls exit(), then the wait() unblocks and returns.

To make it nonblockign: waitpid(-1, &status, WNOHANG)... here it waits for any child, and immediately retuns 0 instead of blockgin..
if a child has exited then it returns the PID of the child.

Exec()

Given the name of an executable (e.g., wc), and some arguments (e.g.,
p3.c), it loads code (and static data) from that executable and overwrites its current code segment (and current static data) with it; the heap
and stack and other parts of the memory space of the program are reinitialized

Exec also has the same file descriptors as the calling process

a successful call to exec() never returns.

shell works with fork and exec

`prompt> wc p3.c > newfile.txt`

In the example above, the output of the program wc is redirected into
the output file newfile.txt (the greater-than sign is how said redirection is indicated). The way the shell accomplishes this task is quite simple: when the child is created, before calling exec(), the shell closes
standard output and opens the file newfile.txt. By doing so, any output from the soon-to-be-running program wc are sent to the file instead
of the screen.

kill() system call is used to send signals to a process, including directives to go to sleep, die, and other useful imperatives.

signals are a way of inter process communication.
