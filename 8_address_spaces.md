# Address Spaces: The Concept


## 1. Motivation
As time-sharing systems became more popular, the demand to keep multiple programs in memory simultaneously increased. This introduced critical requirements:

* **Isolation:** We need to isolate programs from each other.
* **Protection:** We must prevent a program from altering the code or data of another program or the operating system kernel itself.

## 2. The Abstraction
To achieve this, the OS creates an abstraction of physical memory called the **Address Space**.

* **Definition:** It is a contiguous block of memory sized to fit what the running program needs.
* **Contents:** The address space contains all the memory state of the running program: its code, stack, and heap.

## 3. Memory Layout

The typical layout of a process's address space is arranged as follows:

1.  **Code:** The program instructions are located at the bottom of the address space (starting at address `0x0`).
2.  **Heap:** Grows positively (upwards) from the code segment.
3.  **Stack:** The top of the stack is located at the very end of the address space and grows negatively (downwards).

> **Efficiency:** The stack and heap grow in opposite directions to allow them to share the free space in the middle efficiently.

## 4. Goals of Virtual Memory
The virtual memory system should be implemented with three key goals:

1.  **Transparency (Invisibility):** The implementation should be invisible to the running program. The program should behave as if it has its own private physical memory.
2.  **Efficiency:** The assignment of memory should be efficient to minimize:
    * **Space Wastage:** Reducing fragmentation.
    * **Time Overhead:** Minimizing the time required to look up values.
3.  **Protection:** The OS must ensure protection, enabling isolation between processes and protecting the OS itself from errant processes.