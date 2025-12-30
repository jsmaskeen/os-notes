# RAID (Redundant Array of Inexpensive Disks)


## 1. Introduction & Hardware

**RAID** uses multiple disks to work together to provide better performance, capacity, and reliability.

* **Hardware RAID:** A specialized controller with its own processor and RAM manages the disks. It presents the array to the OS as a single logical disk.

* **Benefits:**

    * **Performance:** Achieved via parallel I/O.

    * **Capacity:** Aggregates multiple disks.

    * **Reliability:** Redundancy improves data safety (at the cost of net capacity).

**Fault Model:**

* We assume a **Fail-Stop** model. A disk is either working or permanently failed. The RAID controller can easily detect a failure.

## 2. Evaluation Metrics
We evaluate RAID levels based on:

1.  **Capacity:** How much useful space is available?
2.  **Reliability:** How many disk failures can it withstand?
3.  **Performance:** Throughput and Latency.

**Workload Definitions:**

* **Sequential:** Accessing large contiguous ranges of data. Transfer Rate = $S$ MB/s.
* **Random:** Small accesses at random locations. Transfer Rate = $R$ MB/s.
* *Note:* $S \gg R$ (Sequential is much faster than Random).

---

## 3. RAID Level 0: Striping
RAID 0 is not technically a "Redundant" array as it offers no data protection. It splits data blocks across all disks.

**Structure:**

| Disk 0 | Disk 1 | Disk 2 | Disk 3 |
| :--- | :--- | :--- | :--- |
| 0 | 1 | 2 | 3 |
| 4 | 5 | 6 | 7 |
| 8 | 9 | 10 | 11 |

* **Stripe:** Blocks in the same row form a stripe (e.g., 0, 1, 2, 3).
* **Chunking:** Instead of striping every single block, we can stripe **chunks** of blocks (e.g., blocks 0,1 on Disk 0; 2,3 on Disk 1).

    * *Small Chunk:* High parallelism (files spread across many disks), but positioning time increases (determined by the slowest disk).
    * *Big Chunk:* Reduces positioning time but reduces intra-file parallelism.

**Formulas (Standard Striping):**

* $\text{Disk} = \text{Logical Block} \% \text{Num\_Disks}$
* $\text{Offset} = \text{Logical Block} / \text{Num\_Disks}$

**Analysis ($N$ disks, $B$ size per disk):**

* **Capacity:** $N \times B$.
* **Failures Allowed:** $0$.
* **Latency:** Read/Write = $T$ (single disk time).
* **Throughput:**

    * Sequential: $N \times S$ (Full parallelism).
    * Random: $N \times R$.

---

## 4. RAID Level 1: Mirroring
For each logical block, RAID keeps 2 copies (on separate disks).

**Structure (RAID 10 - Stripe then Mirror):**

| Disk 0 | Disk 1 | Disk 2 | Disk 3 |
| :--- | :--- | :--- | :--- |
| 0 | 0 | 1 | 1 |
| 2 | 2 | 3 | 3 |
| 4 | 4 | 5 | 5 |

* **RAID 10:** Mirrors pairs (0-1, 2-3) and stripes data across them.
* **RAID 01:** Stripes data first, then mirrors the huge stripes (less reliable than 10).

**Analysis:**

* **Capacity:** $(N \times B) / 2$.
* **Failures Allowed:** 1 disk guaranteed; up to $N/2$ if lucky (matching pairs don't fail).
* **Latency:**

    * Read: $T$
    * Write: Slightly $> T$ (must update both copies; wait for slower of the two).

* **Throughput:**

    * Sequential Read/Write: $(N \times S) / 2$.
    * Random Write: $(N \times R) / 2$.
    * Random Read: $N \times R$ (Can read distinct blocks from the primary and the mirror in parallel).

### Crash Consistency

**Problem:** If power fails after writing to Disk 0 but before Disk 1, the mirror is inconsistent.

**Solution:** The controller uses a **Write-Ahead Log (WAL)** in non-volatile RAM to record intentions before writing. On reboot, it replays the log to fix inconsistencies.

---

## 5. RAID Level 4: Parity-Based
Uses a dedicated parity disk to achieve redundancy without the 50% capacity cost of mirroring.

**Structure (5 Disks):**

| Disk 0 | Disk 1 | Disk 2 | Disk 3 | Disk 4 (Parity) |
| :--- | :--- | :--- | :--- | :--- |
| 0 | 1 | 2 | 3 | **P0** |
| 4 | 5 | 6 | 7 | **P1** |

**Parity Logic:**

* $P = \text{XOR}(\text{Block}_0, \text{Block}_1, \text{Block}_2, \text{Block}_3)$.
* **Invariant:** The number of 1s in any stripe (including parity) is even.
* **Recovery:** $\text{Lost Block} = \text{XOR}(\text{Remaining Blocks} + \text{Parity})$.

**Analysis:**

* **Capacity:** $(N-1) \times B$.
* **Failures Allowed:** 1.
* **Throughput:**

    * Sequential Read: $(N-1) \times S$.
    * Sequential Write: $(N-1) \times S$ (Efficient: known as a **Full Stripe Write**).
    * Random Read: $(N-1) \times R$.
    * Random Write: **Poor**. Limited to $R/2$.

**The Small Write Problem:**

To update a single block randomly, we must update the parity.

* **Subtractive Parity Formula:** $P_{new} = (C_{old} \oplus C_{new}) \oplus P_{old}$.
* **Cost:** 2 Reads ($C_{old}, P_{old}$) + 2 Writes ($C_{new}, P_{new}$) = 4 operations.
* **Bottleneck:** The parity disk is accessed for *every* write. It serializes all writes, halving the throughput.

---

## 6. RAID Level 5: Rotating Parity
Solves the "Small Write Problem" (parity disk bottleneck) by rotating the parity block across all disks.

**Structure:**

| Disk 0 | Disk 1 | Disk 2 | Disk 3 | Disk 4 |
| :--- | :--- | :--- | :--- | :--- |
| 0 | 1 | 2 | 3 | **P0** |
| 5 | 6 | 7 | **P1** | 4 |
| 10 | 11 | **P2** | 8 | 9 |
| 15 | **P3** | 12 | 13 | 14 |
| **P4** | 16 | 17 | 18 | 19 |

**Analysis:**

* **Capacity:** $(N-1) \times B$.
* **Failures Allowed:** 1.
* **Throughput:**

    * Sequential Read/Write: $(N-1) \times S$.
    * Random Read: $N \times R$ (All disks utilized).
    * Random Write: $\frac{N \times R}{4}$.

        * Why divide by 4? Each logical write still generates 4 physical I/Os (Read Data, Read Parity, Write Data, Write Parity). However, since parity is distributed, these ops are spread across all disks rather than hitting one bottleneck.

## 7. Summary

* **RAID 0:** Best for performance, zero reliability.
* **RAID 1:** Best for random I/O performance and reliability, but expensive (50% capacity loss).
* **RAID 5:** Best balance of capacity and reliability. Good for sequential I/O and random reads.


| Metric           | RAID 0  | RAID 1                               | RAID 4        | RAID 5        |
| ---------------- | ------- | ------------------------------------ | ------------- | ------------- |
| **Capacity**     | `N · B` | `(N · B) / 2`                        | `(N − 1) · B` | `(N − 1) · B` |
| **Reliability**  | `0`     | `1 (for sure)` \| `N / 2 (if lucky)` | `1`           | `1`           |
| **Throughput**   |         |                                      |               |               |
| Sequential Read  | `N · S` | `(N / 2) · S`                       | `(N − 1) · S` | `(N − 1) · S` |
| Sequential Write | `N · S` | `(N / 2) · S`                       | `(N − 1) · S` | `(N − 1) · S` |
| Random Read      | `N · R` | `N · R`                              | `(N − 1) · R` | `N · R`       |
| Random Write     | `N · R` | `(N / 2) · R`                        | `(1 / 2) · R` | `(N / 4) · R` |
| **Latency**      |         |                                      |               |               |
| Read             | `T`     | `T`                                  | `T`           | `T`           |
| Write            | `T`     | `T`                                  | `2T`          | `2T`          |