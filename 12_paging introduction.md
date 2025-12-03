# Paging: Introduction
*Revision Notes based on OSTEP*

## 1. The Concept
Paging divides memory into fixed-sized chunks.
* **Virtual Memory:** Divided into **Pages**.
* **Physical Memory:** Divided into **Page Frames**.

**Advantages:**
* Most flexible approach.
* **No External Fragmentation** (because all chunks are the same size).

## 2. Address Translation Mechanism

The Virtual Address (VA) is split into two parts:
1.  **VPN:** Virtual Page Number.
2.  **Offset:** The offset within the page.

### Example Calculation
Assume a system where the first 2 bits are VPN and the last 4 bits are the offset:
* **Page Size:** $2^{\text{offset bits}} = 2^4 = 16$ bytes.
* **Number of Pages:** $2^{\text{VPN bits}} = 2^2 = 4$ pages.
* **Total Address Space:** $4 \text{ pages} \times 16 \text{ bytes/page} = 64$ bytes.

### The Translation Logic
The OS uses a **Page Table** to map `VPN` $\to$ `PFN` (Physical Frame Number).
The Physical Address (PA) is calculated using bitwise operations:

1.  **Extract VPN:** Mask and shift the VA.
2.  **Lookup PFN:** `PFN = PageTable[VPN]`
3.  **Formulate PA:** Shift the PFN back and combine with the offset.
    $$PA = (\text{PFN} \ll \text{num\_bits\_offset}) \mid \text{offset}$$
   

## 3. The Page Table
The Page Table is a per-process data structure recorded by the OS to store where each virtual page is physically located.
* **Location:** The page table itself lives in **Kernel Space** (Main Memory).
* **Structure:** A simple **Linear Page Table** is an array indexed by the VPN.

### Page Table Entry (PTE)

A PTE is usually 4 bytes (32 bits) in size. It contains the PFN and several control bits:

| Bit/Flag | Description |
| :--- | :--- |
| **Valid Bit** | Indicates if the translation is valid. Unused space in the address space is marked invalid. |
| **Present Bit** | Indicates if the page is in physical memory (1) or swapped out to disk (0). |
| **Dirty Bit** | Indicates if the page has been modified since it was loaded into memory. |
| **Accessed Bit** | Used by the OS to track usage (e.g., for circular page replacement algorithms). |
| **Protection Bits** | Stores permissions (Read/Write/Execute). |

## 4. Context Switching
With paging, what must be saved/restored during a process context switch?
* A **pointer** to the page table (Page Table Base Register).
* The **size** of the page table.

## 5. Issues (Cons)
1.  **Performance (Too Slow):** Address translation requires an extra memory lookup (to read the page table) before accessing the actual data.
2.  **Memory Overhead (Too Much Memory):** Page tables can become very large, consuming significant physical memory.
3.  **Internal Fragmentation:** While paging solves external fragmentation, it can suffer from internal fragmentation (wasted space *inside* a page if the process doesn't use the full page size).