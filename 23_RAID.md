RAID: Redundant Array of Inexpensive Disks 

Hardware raid (Raid controller has its own RAM, processor etc. just to manage disks.)
Raid offers performance (parallel IO), capacity, and can improve reliablility at cost of net capacity.

When a file system issues a logical IO, the raid controller decides, which disk and how many disks to write to and how to.

Fault Model: Fail stop. In this model, the disk can be in exactly one of the state, working or not working. A failed disk is assumed to be permanently lost. Once a disk fails we asusme raid controler can easily detect it.

Raid Evaluation: On basis of useful capacity, reliability, and performance.

Workload types:
- Sequential : Access a large sequenial range of data.
- Random: A series of random accesses at random block numbers of random, small sizes.
- Disk Transfer Rate = S MB/s under sequential load.
- Disk Transfer Rate = R MB/s under random load.
- S >> R


1. Raid 0: Striping
    - Not a raid level per se cause no redundancy.
    - Simply stripe the blocks across disks.

        | Disk  0|  Disk  1| Disk 2| Disk 3|
        |--|--|--|--|
        | 0|  1|  2|  3|
        | 4|  5|  6|  7|
        | 8|  9|  10|  11|
        | 12|  13|  14|  15|

    - Blokcs in same row are called a stripe.
    - Extracts the maximum parallelism from using multiple disks. 4 IO ops can be done parallely.
    - Large sequential reads are also easy.
    - rather than striping every block we can strip chunks of block. like 0,1 on dsk 0 then 2,3 on disk1 and so on.
    - Lets say chunk size of 2, then each stripe stores 8 blocks.
    - disk_number = logical_block/no_of_disks
    - offset_in_disk = logical_block % no_of_disks
    - small chunk size means many files will be striped across many disks, more parallelism. But positioning time increases, cause its determined by the slowest disk.
    - big chunk reduces intra file parallelism, but reduces the positining time also
    - Capacity: N*B, N = num of disks, B = size of each disk
    - No.of disks that can fail = 0
    - Throughput:
        - Sequential: N*S 
        - Random: N*R
    - Latency:
        - Read: T
        - Write T

2. Raid 1: Mirroring
    - For each logical block, RAID keeps 2 copies

        |Disk 0 |Disk 1 |Disk 2 |Disk 3|
        |--|--|--|--|
        |0| 0| 1| 1|
        |2| 2| 3| 3|
        |4| 4| 5| 5|
        |6| 6| 7| 7|

    - THe above one is RAID 10, mirror first then stripe the data.
    - We can also have RAID 01, first stripe the data, then mirror it (interchange disk1 with disk 2).
    - while reading it can read from the copy too.
    - while writing it has to update both disks, but that can be done in parallel.
    - Capacity: N*B/2
    - No.of disks that can fail = 1 to N/2
    - Throughput:
        - Sequential Read, Write: N*S/2
        - Random Write: N*R/2
        - Random Read: N*R [we can read 2 different blocks in same disk, parallely, one from the disk and other from its copy]
    - Latency:
        - Read: T
        - Write T [slighly more, cause logical write has to wait for both writes, and avg rot delay/seek time might affect]

3. Handling Crashes: Suppose we wrote to Disk 0 and before mirroring to Disk 1, power loss happened, now we have an inconsistent state how to recover? For this, RAID controller ahs a write ahead log. which logs the stuff raid is about to do. And they store this in a non volatile RAM, separately as stoing it to disk isexpensive, performance wise. 

4. RAID 4: Parity Based
    - 5 disk system example:

        |Disk 0| Disk 1| Disk 2| Disk 3| Disk 4|
        |--|--|--|--|--|
        |0 |1 |2 |3 |`P0`|
        |4 |5 |6 |7 |`P1`|
        |8 |9 |10 |11 |`P2`|
        |12 |13 |14 |15 |`P3`|

    - parity func allows us to withstand loss of any one blokc from the stripe.
    - P = XOR(0,1,2,3)
    - with this parity, RAID 4 maintains the invariant that number of ones in any stripe are even.
    - TO recover any block just take XOR of all other blocks within the stripe.
    - perform bitwise XOR to all the bits in the blocks.
    - Capacity: (N-1)*B
    - No.of disks that can fail = 1
    - Throughput:
        - Sequential Read: (N-1)*S
        - Sequential Write: (N-1)*S [Compute the parity block and then write all 5 bloks of the stripe. this is called a full stripe write]
        - Random Read: (N-1)*R
        - Random Write: ok but how to compute parity?
            - Additive parity: write data first then xor the stripe.
            - Subtractive parity: first XOR the bits we wnat to overwrite with parity bits then write the new dta, xoring it with respective bits. better: (old xor new) xor parity
            - For  1 or 2 data disks, use addtitive parity
            - For more than equal to 3 data disks, use subtractive 
            - Assuming subtrctive parity, If multiple small writes are there even in different disks, the parity disk will be the bottle neck. which will make it essentialy sequential. this is called small write problem in raid.
            - Since we have 2 IOs on parity disk (one to read and other to write), our throughput decreases, to **R/2**.
    - Latency:
        - Read: T
        - Write 2T [need to do 2 (read-write). These reads and writes can happen in parallel. so 2T]
5. RAID 5: Rotating Parity
    - have one parity block in each disk.

        |Disk 0| Disk 1| Disk 2| Disk 3| Disk 4|
        |--|--|--|--|--|
        |0 |1 |2 |3 |`P0`|
        |5 |6 |7 |`P1` |4|
        |10 |11 | `P2`|8 |9|
        |15 |`P3` |12 |13 |14|
        |`P4` |16 |17 |18 |19|

    - Capacity: (N-1)*B
    - No.of disks that can fail = 1
    - Throughput:
        - Sequential Read: (N-1)*S
        - Sequential Write: (N-1)*S [Compute the parity block and then write all 5 bloks of the stripe. this is called a full stripe write]
        - Random Read: N*R [we can utilize all the disks to read]
        - Random Write: Parity disk bottleneck is now gone. and disks are used evenly so N*R/4 [4 because we need to o 4 IO for writing.] 

    - Latency:
        - Read: T
        - Write 2T [need to do 2 (read-write). These reads and writes can happen in parallel. so 2T]

Caveats:
- seek time in a mirrored system is higher cause it is max of all the seek times.
- if need performance not reliability, striping only is the best.
- if need all random io read, write reliablility raid 5 is best.
