# Advanced Paging & Demand Paging


## 1. The Problem with Linear Page Tables
We cannot simply increase the page size to reduce page table size, as this causes **internal fragmentation**. To solve the memory overhead of large linear page tables, we look at alternative structures.

## 2. Approach 1: Hybrid Approach (Paging + Segmentation)
This approach combines paging with segmentation.
* **Mechanism:** Instead of one large page table, we have three separate page tables: one for **Code**, one for **Heap**, and one for **Stack**.
* **Hardware:** The Base/Bounds register pair for each segment now indicates the **start and end of each page table** (rather than the data segment itself).
* **Benefit:** This reduces unused space (invalid entries) in the page table, as we only allocate page table space for valid segments.

**Address Translation:**
The Virtual Address (VA) is split as follows:
* **Top 2 bits:** Segment ID (identifies Code, Heap, or Stack).
* **Next 18 bits:** VPN (Virtual Page Number).
* **Last bits:** Offset.

**The Issue:**
While page sizes are fixed, the *Page Tables* themselves can now be of arbitrary sizes. This re-introduces the problem of **External Fragmentation** when allocating memory for the page tables.

## 3. Approach 2: Multi-Level Page Tables (MLPT)

This approach converts a linear page table into a **tree** structure.

### Structure
1.  **Page Directory (PD):** The root of the tree. It contains Page Directory Entries (PDE).
2.  **Page Directory Entry (PDE):**
    * Contains a **Valid Bit** and a **PFN** (Physical Frame Number).
    * **Logic:** If a PDE is valid, it means at least one page in that specific page table chunk is valid. If the PDE is invalid, the entire corresponding page of the page table is invalid/unallocated.

**Benefit:** It allocates space in proportion to the addresses actually used, drastically saving memory for sparse address spaces.

### Address Translation Example
Assuming a 14-bit VPN:
1.  **First 4 bits:** Page Directory Index (to locate the PDE).
2.  **Next 4 bits:** Page Table Index (to locate the PTE).
3.  **Last 6 bits:** Offset.

> **Note:** We can go deeper, for example, a three-level page table (PD0 bits $\to$ PD1 bits $\to$ PT bits $\to$ Offset).

## 4. Demand Paging
To support address spaces larger than physical memory, we use **Demand Paging**.
* **Swap Space:** Disk space used to move pages back and forth between RAM and disk.
* **Requirement:** The OS must remember the disk address of every page.

### Mechanisms
* **Page Fault:** The act of accessing a page that is not currently in physical memory.
* **Page-Fault Handler:** The OS code that runs upon a page fault.
* **Present Bit:** A bit in the PTE that indicates if the page is in physical memory (1) or on disk (0).

**Operations:**
* **Swap In:** Moving data from Disk $\to$ Memory.
* **Swap Out:** Moving data from Memory $\to$ Disk.

## 5. Page Replacement Policy (Swap Daemon)
Most operating systems try to keep a small amount of memory free using a background thread (often called the swap daemon).

**Watermarks:**
The OS uses a **High Watermark (HW)** and **Low Watermark (LW)** to decide when to evict pages.

1.  **Trigger:** When the OS notices that `Available Pages < LW`, the background thread runs.
2.  **Action:** The thread evicts pages (frees memory) until `Available Pages > HW`.