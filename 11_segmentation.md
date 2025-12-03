# Segmentation


## 1. The General Concept
Segmentation is essentially **generalized base and bounds**. Instead of one pair of base and bounds registers for the entire process, we have multiple pairs—one for each logical segment of the address space:

* Code
* Stack
* Heap

## 2. Explicit Approach (Address Translation)
In the explicit approach, the hardware uses specific bits of the Virtual Address (VA) to determine which segment is being accessed.

**Example: 14-bit Virtual Address**

* **Top 2 bits:** Segment ID.
* **Bottom 12 bits:** Offset.

**Translation Logic:**

The hardware takes the offset and adds it to (or subtracts it from) the base register of the selected segment to obtain the Physical Address (PA).

### Segment Register Table

The hardware maintains a structure defining the bounds and growth direction for each segment.

| Segment Bits | Segment | Base | Size (Bound) | Grows Positive? |
| :--- | :--- | :--- | :--- | :--- |
| `00` | Code | 32K | 2K | 1 (Yes) |
| `01` | Heap | 34K | 3K | 1 (Yes) |
| `11` | Stack | 28K | 2K | 0 (No) |


> **Note:** Accessing an address outside these bounds leads to a **Segmentation Fault**.

## 3. Issues and Limitations

1.  **Wasted Segment Space:** With 2 bits for segments (4 combinations), if we only use 3 segments (Code, Heap, Stack), one segment (e.g., `10`) goes unused.
2.  **Limited Size:** The maximum effective segment size is reduced (chopped), as the total address space is divided by 4.

## 4. Advanced Features

* **Code Sharing:** We can implement code sharing by adding **protection bits** (e.g., Read-Only for code segments).
* **Granularity:**

    * **Coarse-Grained:** Small number of segments (Code, Heap, Stack) as described above.
    * **Fine-Grained:** Large number of smaller segments (used in early OSs). This requires a **Segment Table** stored in memory.

## 5. Fragmentation

Segmentation introduces specific memory management challenges.


### External Fragmentation
Because segments vary in size, physical memory becomes filled with small "holes" of free space between allocated segments.

* **Compaction:** Moving segments to compact memory is possible but **expensive**.
* **Allocation Algorithms:** To mitigate this, OSs use algorithms such as:

    * Best Fit
    * Worst Fit
    * First Fit
    * Buddy Algorithm (used in xv6).

### Internal Fragmentation
This occurs within the allocator itself. If an allocator hands out chunks of memory bigger than requested, the unused space inside that chunk is considered **Internal Fragmentation**.