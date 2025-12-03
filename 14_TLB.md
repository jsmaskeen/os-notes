# Translation Lookaside Buffer (TLB)


## 1. Introduction
To speed up address translation, we use the **Translation Lookaside Buffer (TLB)**.

* **Location:** It is part of the **Memory Management Unit (MMU)**.
* **Function:** It is a hardware cache that stores **VPN $\to$ PFN** translations.

## 2. Basic Operation
Upon each memory reference, the hardware first checks the TLB:

1.  **TLB Hit:** The TLB holds the PFN for the queried VPN. The translation is immediate.
2.  **TLB Miss:** The TLB does *not* hold the PFN for the queried VPN.

    * **Action:** The system must query the page table, update the TLB with the new `(VPN, PFN)` pair, and retry the instruction.


## 3. Handling TLB Misses
Who handles the miss?

* Once a miss occurs, the hardware raises an **exception**.
* Control is passed to the **Kernel Mode** trap handler.
* **OS Action:** The OS queries the page table, updates the TLB, and executes a **Return-from-Trap**.

### Distinction: Return-from-Trap
There is a key difference in where the execution resumes compared to a standard system call:

* **System Call:** Returns to the **next** instruction after the trap calling instruction.
* **TLB Miss:** Returns to the **same** instruction that caused the trap. This allows the hardware to **retry** the instruction (which should now result in a TLB Hit).

## 4. Performance & Locality
The performance of the TLB is measured by the Hit Rate:

$$\text{TLB Hit Rate} = \frac{\text{Num Hits}}{\text{Num Accesses}} \times 100\%$$


**Locality:**

* **Spatial Locality:** TLB improves performance because accessing one address often means accessing nearby addresses (which are on the same page).

    * *Page Size Effect:* Larger page sizes result in fewer TLB misses (as one entry covers more memory).

* **Temporal Locality:** If a program is re-run after its first execution, the TLB hit rate can approach **100%** because the translations are already cached.

## 5. Context Switching
When switching between processes, the TLB entries for the old process are no longer valid.

* **Approach 1 (Flush):** Flush (empty) the TLB on every context switch. This ensures correctness but hurts performance (cold cache).
* **Approach 2 (ASID):** Provide an **Address Space Identifier (ASID)** or PID to the TLB entries. This allows the TLB to differentiate entries between processes without flushing.

## 6. Replacement Policy
When the TLB is full, we must evict an entry to add a new one. The standard policy mentioned is **LRU** (Least Recently Used).