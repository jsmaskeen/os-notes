basic approach.. laod the program and run on CPU.

But what if IO task is needed.. we cant give unprotected access to a program to IO.. 

THats why a separation of user and kernel mode.


In user mode, applications do not have full access to hardware resources.
In kernel mode, the OS has access to the full resources of the machine.
Special instructions to trap into the kernel and return-from-trap back to
user-mode programs are also provided, as well instructions that allow the
OS to tell the hardware where the trap table resides in memory.

If proc does IO in usermode, OS will kill the process.

to enable something in priviledged mode the program has to perform a system call or a syscall.

To execute a system call, a program must execute a special trap instruction. This instruction simultaneously jumps into the kernel and raises the
privilege level to kernel mode; once in the kernel, the system can now perform whatever privileged operations are needed (if allowed), and thus do
the required work for the calling process. When finished, the OS calls a
special return-from-trap instruction, which, as you might expect, returns
into the calling user program while simultaneously reducing the privilege level back to user mode.

[It may not necessarily return to the calling process.]

 the processor will push the program
counter, flags, and a few other registers onto a per-process kernel stack;
the return-from-trap will pop these values off the stack and resume execution of the user-mode program

How to handle traps? 
the OS sets upa trap table at boot time. OS informs hardware about trap handlers. trap handlers simply tell hardware what to do when this trap is triggered.

If a process is running  on CPU then how can OS regain control to switch between processe ?

two approaches: 
- Cooperative approach: OS trusts programs to behave reasonably, give up CPU (yeild syscall) or give up CPU once it runs. Or if it misheaves, trap is triggered and OS terminates the process.
- Preemptive approach (Non cooperative approach): Timer interrupt. raise timer interrupt every few milliseconds (from a timer device), the current running process is halted and pre configured interrupt handler in the OS runs.

Context switch: OS has to save a few register's values, for the current runnign proc, and push it to its kstack. and restore these for the next running process.

Difference between timerinterrupt and when OS decides to switch:

When a timer interrupt happens (e.g., for preemptive multitasking), the CPU automatically saves the current registers onto the kernel stack of the running process.
This is done by the hardware, not by the OS code.
After this, the OS can run its scheduler to decide which process runs next.


Sometimes the OS itself decides to switch processes (not because of an interrupt).
Here, the kernel’s own registers (the ones used while in kernel mode) are not automatically saved.
So the OS code explicitly saves these registers into the process control block (PCB) or process structure of process A.
Then the OS loads process B’s saved state from its PCB and resumes it.

What if during an interrupt another interrupt occurs?

One simple thing an OS might do is disable interrupts during interrupt processing; doing so ensures that when
one interrupt is being handled, no other one will be delivered to the CPU

