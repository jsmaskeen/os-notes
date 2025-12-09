# Introduction to Operating Systems

## The Von Neumann Model

The processor fetches an instruction from memory, then decodes it, and executes it. This is the basis of the **Von Neumann model**. The hardware is responsible for executing these instructions, managing the flow between fetching, decoding, and execution.

## Operating System Basics

The **Operating System (OS)** is in charge of making sure the system operates correctly and efficiently in an easy-to-use manner. The

**Virtualization** is the process of taking a physical resource and transforming it into a more general, easy-to-use version of itself. The goal is for each program to think it has all the resources required for it exclusively (e.g., its own CPU or memory).

The OS provides **system calls** which are, well-defined interfaces that allow user programs to request services from the operating system. System calls act as the gateway between user programs and the hardware, enabling controlled access to resources such as files, memory, and devices. Because the OS manages and arbitrates access to these resources, it is often referred to as a **Resource Manager**.

### CPU Virtualization Concepts

* `spin()`: A function (often used in OSTEP examples) that repeatedly checks the time and returns once it has run for a second.
* **Policy:** When multiple programs are active, the question of "which should run next?" is answered by the **policy** of the OS (e.g., Scheduling).
* **Process Identifier (PID):** A unique identifier assigned to every running process.

### Memory Virtualization

Memory is effectively an array of bytes.

* **To read memory:** One must specify an address to access the data stored there.
* **To write (or update) memory:** One must specify the address and the data to be written.

**Address Spaces:** Each process accesses its own private **virtual address space** (often just called its address space). The OS maps this virtual space onto the physical memory of the machine.

## Concurrency

Programs can create threads using `pthread_create()`. This introduces concurrency issues, specifically regarding **atomicity**.

Example: The statement `x++;` is technically three instructions, not one:

1.  $$\text{Load } x \to \text{register/accumulator}$$
2.  $$\text{Increment register}$$
3.  $$\text{Store register} \to x$$

* **Atomic:** An operation is atomic if it completes entirely without any possibility of interruption or interference from other operations. Atomicity ensures that the operation appears indivisible, so no other thread or process can observe it in a partially completed state.
* **Individually:** Each of these three hardware instructions is atomic (the hardware executes them one by one).
* **As a group:** The statement `x++;` is **not atomic**. A context switch can occur *between* instructions 1 and 2, or 2 and 3, leading to concurrency bugs.

## OS Design Goals

* Provide high performance.
* Minimize overheads. Overheads arise in two forms:

    * **Extra time** (more instructions).
    * **Extra space** (in memory or on disk).

* Provide protection between applications, as well as between the OS and applications.
* Ensure **isolation** of processes.

## Limited Direct Execution & System Calls

The key difference between a **system call** and a standard procedure call is that a system call transfers control (jumps) into the OS while simultaneously raising the hardware privilege level.

### User Mode vs. Kernel Mode

* **User Mode:** User applications run here. The hardware restricts what applications can do. For example, an application in user mode cannot typically initiate an I/O request to the disk, access physical memory pages directly, or send a packet on the network.
* **Kernel Mode:** When the privilege level is raised, the OS has full access to the hardware (e.g., initiating I/O requests or allocating memory).

### The Trap Mechanism

1.  When a system call is initiated (usually through a special hardware instruction called a **trap**), the hardware detects this event and transfers control to a pre-specified **trap handler** (that the OS set up previously).
2.  Simultaneously, the hardware raises the privilege level to **Kernel Mode**, ensuring the OS has full access to system resources.
3.  When the OS is done servicing the request, the hardware helps pass control back to the user via a special **return-from-trap** instruction.
4.  This instruction, executed by the hardware, reverts the system to **User Mode** and passes control back to where the application left off.

> **Note:** It is not necessary to execute the same program after returning from a syscall (the OS may switch to a different process).