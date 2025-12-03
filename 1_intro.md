the processor fetches an instruction from memory, then decodes it and executes it.
THis is the basics of VOn neumann model

operating system (OS) is in charge of making sure the
system operates correctly and efficiently in an easy-to-use manner

Virtualization is taking a physical resource and transforming it to a more general easy to use version of itself. such that each program thinks it has all the resources which are required for it.

OS provides system calls. SO is also called a resource manager.

Spin(), a function that repeatedly checks the time and
returns once it has run for a second.

amongst two programs which should run is answered by the policy of the OS.

Memory is just an array of
bytes; to read memory, one must specify an address to be able to access
the data stored there; to write (or update) memory, one must also specify
the data to be written to the given address.

the process identifier (the PID) of the running program.
This PID is unique per running process.

 Each process accesses its own private virtual address space
(sometimes just called its address space), which the OS somehow maps
onto the physical memory of the machine

programs can create threads using pthread_create()

x++; is three instructiosn, move to accumu, increment, and store
these three are not atomic..
atmoic -> execute in one go

overheads arise in a number of forms: extra time (more instructions) and extra space (in memory or on disk)

Goal of our OS design
- provide high performance
- minimize the overheads
- provide protection between applications, as well as between the OS and applications.
- isolation of processes.


The key difference between a system call and a procedure call is that
a system call transfers control (i.e., jumps) into the OS while simultaneously raising the hardware privilege level. User applications run in what
is referred to as user mode which means the hardware restricts what applications can do; for example, an application running in user mode can’t
typically initiate an I/O request to the disk, access any physical memory
page, or send a packet on the network. When a system call is initiated
(usually through a special hardware instruction called a trap), the hardware transfers control to a pre-specified trap handler (that the OS set up
previously) and simultaneously raises the privilege level to kernel mode.
In kernel mode, the OS has full access to the hardware of the system and
thus can do things like initiate an I/O request or make more memory
available to a program. When the OS is done servicing the request, it
passes control back to the user via a special return-from-trap instruction,
which reverts to user mode while simultaneously passing control back to
where the application left off.
IT is not necessary to execute the same program after returing form a syscall.


