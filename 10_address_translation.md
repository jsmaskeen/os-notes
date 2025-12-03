# Address Translation & Dynamic Relocation
*Revision Notes based on OSTEP*

## 1. The Basic Mechanism
**Hardware-based address translation** converts a Virtual Address (VA) into a Physical Address (PA).

### Base and Bounds (Dynamic Relocation)
To implement this efficiently, we use a technique called **Dynamic Relocation**, relying on two hardware registers within each CPU (part of the **Memory Management Unit (MMU)**).

1.  **Base Register:** Defines the start of the physical memory region.
2.  **Bounds (Limit) Register:** Defines the size (or end limit) of the region.

**The Translation Formula:**
$$PA = VA + \text{base}$$
* **Constraint:** The access is valid only if provided that $VA + \text{base} < \text{bounds}$ (or strictly within the size limit).
* **Note:** The bounds register may hold the physical end address *or* the size of the address space.

## 2. Hardware Requirements
To support this, the hardware must provide:
1.  **Privileged Instructions:** Special instructions to modify the base and bounds registers.
    * These allow the OS to change values when different processes run.
    * **Constraint:** These instructions are privileged and can **only** be run in **Kernel Mode**.
2.  **Exception Handling:** The CPU must be able to generate an exception if an address is out of bounds, invoking a specific handler.

## 3. OS Responsibilities
The OS manages memory using a structure called the **Free List**, which stores which ranges of physical memory are currently free.

### Lifecycle Management
1.  **Process Creation:** The OS must search the free list to find space to allot the memory range for the new process.
2.  **Context Switch:** Because the hardware only has *one* pair of base and bounds registers, the OS must save the current values into the **Process Control Block (PCB)** and restore them when the process runs again.
3.  **Process Exit:** The OS must clean/reclaim the memory once the process exits.
4.  **Relocation:** The OS can move an address space from one base-bounds range to another while the process is not scheduled.

## 4. Issues with Base and Bounds

### Internal Fragmentation
Since the address space is allocated as a contiguous unit, the space inside the region (specifically between the heap and stack) is often not used. This wasted space inside the allocated block is called **Internal Fragmentation**.

### External Fragmentation
As processes are allocated and freed, physical memory can develop "little holes" of free space that are too small to be useful. This is called **External Fragmentation**.