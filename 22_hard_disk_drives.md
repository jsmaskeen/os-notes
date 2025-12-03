# Hard Disk Drives (HDD)


## 1. The Interface
From the perspective of the OS, the drive presents a simple interface:
* **Sectors:** The drive consists of sectors, typically **512 bytes** each.
* **Address Space:** Sectors are numbered from $0$ to $n-1$. This is the address space of the drive.
* **Performance:**
    * Accessing blocks in a **contiguous** chunk is faster than random access.
    * Accessing blocks near each other is faster than accessing blocks far apart.

### Atomicity & Torn Writes
* **The Guarantee:** A 512-byte write is atomic (it either completes or doesn't happen).
* **The Risk:** Multi-sector writes are possible, but if a power loss occurs during a larger write (e.g., 4KB), it results in a **Torn Write** (an incomplete write where only some sectors were updated).

## 2. Disk Geometry

1.  **Platter:** A circular hard surface with a magnetic coating to store data. Each platter has 2 sides (surfaces).
2.  **Spindle:** Connected to a motor that spins the platters at a constant **RPM** (Rotations Per Minute).
3.  **Tracks:** Data is encoded in concentric circles called tracks.
4.  **Disk Head & Arm:** There is one disk head per surface to read/write. All heads are attached to a single **disk arm** which moves across the surface to position the head over the desired track.
5.  **Operation:**
    * **Read:** Sense a magnetic pattern.
    * **Write:** Induce a change in the magnetic pattern.

### Advanced Features
* **Track Skew:** Blocks on subsequent tracks are offset (skewed). This ensures that when the head switches tracks (seek), the next logical block hasn't rotated past the head during the repositioning time.
    * **Multi-Zoned Disk Drives:** Outer tracks are physically longer than inner tracks. To maximize capacity, outer tracks have **more sectors** per track than inner tracks (organized into zones).
* **Cache (Track Buffer):** Small memory (8-16 MB) on the drive. It holds data for write buffering or read-ahead (caching contiguous sectors during a read).

## 3. I/O Performance: The Math
The total time for an I/O request ($T_{IO}$) consists of three components:

$$T_{IO} = T_{seek} + T_{rotation} + T_{transfer}$$


### 1. Rotational Delay
The time waiting for the desired sector to rotate under the disk head.
* **Max:** $R$ (one full rotation).
* **Average:** $R/2$.

### 2. Seek Time
The time to move the disk arm to the correct track. It involves four phases:
1.  **Acceleration:** Arm starts moving.
2.  **Coasting:** Arm moves at full speed.
3.  **Deceleration:** Arm slows down.
4.  **Settling:** Arm positions itself precisely on the track (significant time goes here).

> **Rule of Thumb:** Average seek time is roughly **1/3** of full seek time (end-to-end).

### 3. Transfer Time
The time to actually read/write the data.

### I/O Rate ($R_{IO}$)
To compare disks or workloads:
$$R_{IO} = \frac{Size_{transfer}}{T_{IO}}$$


* **Sequential vs. Random:** Disks give much higher $R_{IO}$ for sequential reads because there is only one seek and one rotational delay at the start, amortized over many sectors.

## 4. Write Acknowledgement Policies
When does the disk tell the OS the write is done?
1.  **Write Back:** Acknowledge when data is put in the **disk cache** (memory).
    * *Pros:* Makes disk appear faster.
    * *Cons:* Dangerous; data can be lost on power failure before hitting the platter.
2.  **Write Through:** Acknowledge when data is actually written to the **disk surface**.
    * *Pros:* Safe.
    * *Cons:* Slower.

## 5. Disk Scheduling
Given a set of I/O requests, the scheduler decides the order of execution.

### Basic Algorithms
1.  **SSTF (Shortest Seek Time First):**
    * Pick the request on the track closest to the current head position.
    * *Issue:* The OS doesn't perfectly know the disk geometry (tracks/cylinders).
2.  **NBF (Nearest Block First):**
    * Schedule based on the nearest logical block address.
    * *Issue:* **Starvation**. A stream of requests for nearby blocks can prevent far-away blocks from ever being serviced.

### SCAN Algorithms (The Elevator)
1.  **SCAN:** The arm sweeps across the disk (e.g., inner to outer), servicing requests in order.
2.  **FSCAN (Freeze SCAN):** To avoid starvation of far-away requests, it freezes the queue during a sweep. New requests arriving during the sweep are placed in a separate queue for the *next* sweep.
3.  **C-SCAN (Circular SCAN):** Sweeps in only one direction (e.g., outer to inner), then resets to the start without servicing. This provides more uniform wait times.

> **Note:** SCAN and SSTF are not "purely" optimal because they ignore rotational delay.

### Optimal: SPTF (Shortest Positioning Time First)
Also called **SPTF** or **SATF** (Shortest Access Time First).
* **Logic:** It considers both **Seek Time** and **Rotational Delay**.
* *Example:* If Seek Time > Rotation Time, it picks the item on the closer track. If Rotation > Seek, it might pick a slightly farther track if the sector is rotationally aligned better.
* **Implementation:** Usually performed inside the **disk drive controller** (since the drive knows the exact geometry and head position).

### I/O Merging
The scheduler often merges multiple consecutive block requests into a single, larger request before reordering. This reduces overhead.