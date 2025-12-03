# File System Implementation (VSFS)
*Revision Notes based on OSTEP*

## 1. Overall Organization (VSFS Layout)
We introduce a simplified implementation known as **vsfs** (Very Simple File System), which mimics a typical UNIX file system.


The disk partition is divided into blocks (commonly **4 KB**) addressed from $0$ to $N-1$. The layout consists of:

1.  **Data Region:** The majority of the disk is reserved for user data.
2.  **Inode Table:** A reserved region to hold the array of on-disk inodes (metadata).
3.  **Bitmaps:** Used to track free/allocated space.
    * **Data Bitmap:** Tracks free data blocks.
    * **Inode Bitmap:** Tracks free inodes.
4.  **Superblock:** Located at the very beginning (Block 0).
    * Contains specific file system parameters: total number of inodes/data blocks, start location of the inode table, and a **magic number** to identify the file system type.
    * The OS reads this first when mounting the file system.

## 2. The Inode (Metadata)
**Inode** (Index Node) is the structure that holds the metadata for a given file.

* **Content:** File size, permissions, owner, access/modify times, and the location of data blocks.
* **Identification:** Each inode is referred to by a unique **i-number** (low-level name).
* **System Call:** `stat` or `fstat` retrieves this info from the filesystem.

### Calculating Inode Location
Given an i-number, the OS can calculate the exact physical address.
Since disks are sector-addressable (usually 512 bytes), not byte-addressable, the formula is:

$$\text{Sector} = \frac{(\text{i-number} \times \text{sizeof(inode)}) + \text{inodeStartAddr}}{\text{sectorSize}}$$



## 3. Indexing Strategies
How does the inode point to the data?

### A. Multi-Level Index (Pointer Based)

Used to support both small and large files efficiently.
* **Direct Pointers:** The inode contains a fixed number of direct pointers (e.g., 12) that point directly to user data blocks.
* **Indirect Pointer:** Points to a block that contains *more* pointers to data blocks.
* **Double/Triple Indirect Pointers:** Points to a block of indirect pointers (imbalanced tree structure).

**Capacity Calculation:**
Assuming 4KB blocks and 4-byte pointers (1024 pointers per block):
$$\text{Max Size} = (12 + 1024 + 1024^2) \times 4\text{KB} \approx 4\text{GB}$$


### B. Extents (Extent Based)

* **Definition:** An extent is a disk pointer plus a **length** (in blocks).
* **Pros:** More compact; requires less metadata than pointers.
* **Cons:** Less flexible; requires finding contiguous free space on disk. If the disk is fragmented, a file may require multiple extents.

## 4. Directory Organization
Directories are treated as a special type of file.
* **Content:** A list of `(entry name, inode number)` pairs.
* **Special Entries:**
    * `.` (dot): Current directory.
    * `..` (dot-dot): Parent directory.
* **Storage:** The directory has an inode (type marked as "directory"), and its data blocks contain the list of entries.
* **Deletion:** When a file is deleted, it may leave a gap. Directories track **Record Length** vs. **String Length** to manage this empty space or reuse it for new entries.

## 5. Free Space Management
The file system must track free inodes and data blocks.

* **Bitmaps:** vsfs uses one bitmap for inodes and one for data. A bit is `0` if free, `1` if used.
* **Pre-allocation Policy:** To improve performance (and allow extents/contiguous reads), the OS often looks for a sequence of free blocks (e.g., 8 blocks) rather than just one when writing a file.

## 6. Access Paths (Reading and Writing)
Understanding the flow of I/O operations is critical (The Crux).

### A. Reading a File
**Task:** `open("/foo/bar", O_RDONLY)` and read it.
1.  **Traverse Path:** The FS reads the root inode (usually i-number 2).
2.  **Lookup:** It reads root data to find `foo`, gets `foo`'s inode, reads `foo`'s data to find `bar`, then gets `bar`'s inode.
3.  **Read:** Access the data blocks pointed to by `bar`'s inode.
4.  **Update:** Update the **last accessed time** in the inode.

> **Note:** Reading does *not* access allocation structures (bitmaps).

### B. Writing to a File
**Task:** Create `/foo/bar` and write data.
Writing is much more expensive than reading. Each write logically generates roughly **5 I/Os**:
1.  **Read** Data Bitmap (find free block).
2.  **Write** Data Bitmap (mark allocated).
3.  **Read** Inode (to update pointers).
4.  **Write** Inode (commit new pointers).
5.  **Write** Data Block (actual data).

> **Note (Refer to Book/Slides):** *Plus additional I/O for directory updates during file creation!*

## 7. Caching and Buffering
To mitigate the high cost of I/O, the OS uses system memory (DRAM).

* **Read Caching:**
    * Modern systems use a **Unified Page Cache** (integrating virtual memory pages and file system pages).
    * Subsequent reads of the same file (or directory lookups) often hit the cache, requiring no disk I/O.

* **Write Buffering:**
    * Writes are delayed in memory (5–30 seconds).
    * **Benefits:**
        1.  **Batching:** Update a bitmap once for multiple writes.
        2.  **Scheduling:** Reorder I/Os for disk efficiency.
        3.  **Avoidance:** If a file is created and immediately deleted, the write never hits the disk.
    * **Durability Risk:** If the system crashes before the write propagates, data is lost. Applications needing guarantees use `fsync()`.