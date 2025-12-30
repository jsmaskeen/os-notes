# Concurrency: Introduction & Threads


## 1. The Thread Abstraction
Each thread acts as an independent agent running within a program.

* **Multiple Execution Points:** A multi-threaded program has more than one point of execution, meaning it has multiple Program Counters (PCs) being fetched and executed simultaneously.


### Shared vs. Private Data
Threads share the same **Address Space**, meaning they can access the same data. However, there are key differences in storage:

| Resource | Scope | Description |
| :--- | :--- | :--- |
| **Address Space** | **Shared** | All threads in the program share the heap and code. |
| **Registers** | **Private** | Each thread has its own set of registers for computation, such as the **Program Counter (PC)**, **Stack Pointer (SP)**, and **General-Purpose Registers**. These are virtualized by saving/restoring them during context switches. |
| **Stack** | **Private** | Each thread has its own stack (often called **Thread-Local Storage**). |

### Context Switching

* **Mechanism:** Switching from Thread 1 to Thread 2 requires a context switch.
* **Data Structure:** The OS uses a **Thread Control Block (TCB)** to manage this state, similar to a PCB for processes.

## 2. The Problem: Race Conditions

**Race Condition:** A situation where the results of a program depend on the timing execution of the code, specifically when multiple threads access shared data and attempt to modify it concurrently without proper synchronization.

* **Indeterminacy:** Due to race conditions, we might get **indeterministic** output (varying from run to run) rather than the deterministic output usually expected from computer systems.

### Critical Sections

A **Critical Section** is a piece of code that accesses a shared variable (or shared resource) and must **not** be concurrently executed by more than one thread.

* **The Danger:** A race condition arises if multiple threads enter the critical section at roughly the same time and attempt to update the shared data structure, leading to surprising or undesirable outcomes.
* **Example:** Code that updates shared structures like a file allocation bitmap or an inode during a `write()` operation acts as a critical section.

## 3. The Solution: Atomicity & Synchronization
To solve these issues, we rely on **Atomicity** and **Synchronization Primitives**.

### Atomicity

* **Definition:** Atomic means "all or nothing".
* **Hardware Guarantee:** Atomic instructions cannot be interrupted. Either they complete entirely, or they do not execute at all.
* **Transactions:** The grouping of many actions into a single atomic action is called a transaction.

### Synchronization Primitives
Using a few hardware instructions, we can build a set of synchronization primitives to ensure correctness.

* **Mutual Exclusion:** Threads should use primitives (locks) so that only a **single thread** ever enters a critical section.
* **Condition Variables:** Useful when signaling must take place between threads (e.g., if one thread is waiting for another to do something before it can continue).

## 4. Thread Usage Patterns

* **`pthread_join()`:** A function used to wait for a particular thread to complete.
* **Independent Threads:** It is not always necessary to join threads.
    * *Example:* An indefinite web server where the main program passes requests to thread workers and they run independently.