# Virtualization: The Process

## 1. The Process Abstraction

A **process** is an abstraction provided by the OS for a running program.

### Time Sharing (CPU)

* **The Goal:** The OS must provide the illusion of many CPUs to the user, even though typically only one program can run on one CPU at a time.
* **The Mechanism:** The OS runs one program for a short while, then switches to another in fixed time slices. This technique is called **Time Sharing**.

    * **Consequence:** With more CPU sharing (more processes), the time each individual program takes to complete increases (assuming equal priority and duration).

> **Comparison:** The counterpart to time sharing is **Space Sharing**. Disk space is naturally space-shared; once a block is assigned to a file, it remains assigned until deleted. CPU is time-shared.

### Mechanisms

1.  **Context Switch:** The act of stopping one program and running another.
2.  **Scheduling Policy:** Algorithms (policies) used by the OS to decide which process to run next (e.g., SJF).

## 2. Process Memory & Creation

The memory that a process can address is called its **Address Space**. It is considered part of the process itself.

**Process State Requirements:**

To track a process, the OS (specifically the `proc` struct) requires the Program Counter (PC), the Stack Pointer (top of stack), the Kernel Stack (kstack), and I/O information.

### How is a process created?

1.  **Load Code:** The OS loads the code and static variables into the address space. Modern OSs perform this **lazily** (loading code only when needed).
2.  **Allocate Stack:** The runtime stack is reserved in the address space for local variables and return addresses.
3.  **Allocate Heap:** Memory is reserved for the heap (for dynamic memory allocation/deallocation).
4.  **I/O Setup:** The OS loads file descriptors (standard input/output/error).
5.  **Start:** The OS jumps to the entry point, usually `main()`.

## 3. Process States

* **New:** The process is being set up by the OS.
* **Running:** The process is currently executing instructions.
* **Ready (Runnable):** The process is ready to run but waiting for the OS to schedule it.
* **Sleeping (Blocked):** The process is waiting for an event, such as I/O completion.
* **Zombie (Terminated):** The process has finished but has not been cleaned up yet.

### The "Zombie" State

A process enters the **Zombie** state when it calls `exit()`.

* **Why?** It allows the parent process to examine the return code of the child to see if it executed successfully.

* **Cleanup:**

    1.  When a process exits, its resources (memory, FDs) are freed, but the entry (PID, exit status) remains in the process table.
    2.  The parent must call `wait()` to collect this status. Once done, the OS removes the zombie entry completely.
    3.  If the parent exits *without* waiting, the zombie is reassigned to `init` (PID 1), which automatically waits for and cleans up orphaned zombies.

## 4. Data Structures

* **Process List:** The OS maintains a list to keep track of all processes.
* **Process Control Block (PCB):** The structure holding process information (like the `proc` struct in xv6).
* **Register Context:** Holds the contents of the process's registers when it is not running.

## 5. The Process API (System Calls)

### `fork()`

Creates a new process by making a copy of the parent.

* **Return Values:**

    * Returns `0` to the **child** process.
    * Returns the `child PID` to the **parent** process.
    * Returns `< 0` if the fork failed.

* **Behavior:** It makes a **deep copy** of the stack, heap, and code. The child gets its own address space.

* **File Descriptors:** Open file descriptors are **shared**.

    * However, if the child closes a file descriptor, the parent's copy remains valid (and vice versa).

### `wait()`

Used by the parent to wait for the child to finish.

* **Blocking:** `wait()` blocks the parent until the child calls `exit()`.
* **Non-Blocking:** `waitpid(-1, &status, WNOHANG)` waits for any child but returns immediately (`0`) if no child has exited, rather than blocking.

### `exec()`

Given an executable name and arguments, `exec()` loads code and static data from that executable and **overwrites** the current process's code segment.

* The heap and stack are re-initialized.
* **Retains File Descriptors:** The new program inherits the open file descriptors of the calling process.
* **No Return:** A successful `exec()` **never returns** (because the code that called it has been overwritten).

### Shell Redirection Example

How does `prompt> wc p3.c > newfile.txt` work?
1.  The shell calls `fork()` to create a child.
2.  **Before** calling `exec()`, the child closes Standard Output (`STDOUT`) and opens `newfile.txt`.
3.  The child calls `exec()`.
4.  The program `wc` writes to `STDOUT`, but since that descriptor now points to the file, output goes to `newfile.txt`.

### `kill()`

The `kill()` system call is used to send **signals** to a process (e.g., sleep, die). Signals are a method of Inter-Process Communication (IPC).