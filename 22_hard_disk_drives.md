Interface of HDD:
1. Drive consists os sector. each sector is 512 B each. THey are numbered from 0 to n-1, with n sectors.
2. 0 to n-1 is the address space fo the drive.
3. multi sector writes are possible, but a 512B write is atomic (either it will hapen or it will not.) (manufacture garuntee). hence with a power loss during a 4KB write, there can be a torn write (incomplete write).
4. Accessing blocks in contigous chunk is faster than random.
5. accessing two blocks which are near each other is faster than two blocks which are far apart.

Geometry of Disk:
1. Platter: Circular hard surface with magnetic coating on which data is stored.
    - Each platter has 2 sides called surfaces. [each surface stores data]
2. Many platters are bound together around the spindle. Spindle is connected to a motor which spins the platters at constant RPM.
3. Data is encoded on each surface in concentric circles of sectors. each of these concentric circles is called a track.
4. Inner tracks have less sectors, outer tracks have more sectors because bruh.
5. Read-> sense a magnetic patter. Write -> induce a change in the magnetic pattern on disk.
6. disk head -> one per surface, does the read and write.
7. all disk heads are attached to a single disk arm, whic can move across a surface, to position head over desired track.

How to read, Delays:
1. Rotational Delay: Time taken to complete one full rotation = R [worse case]. On avg. it is R/2. [same for each track.]
2. Seek time: With multiple tracks, disk head has to move from one track to the other (if sector is on some other track), 
    - Acceleration phase: the disk arm starts moving
    - Coasting: arm is moving at full speed
    - Deceleration: arm slows down
    - Settling: arm settles on the right track. [significant time goes here]
3. Transfer the data.

Often tehre are these things too:
1. Track skew: blocks on subsequent tracks are shifted by skew offset so that when the arm moves to switch a track, there is less time taken to reposition the head, and the contigous block on the other track doesnt rotate away. (see image online)
2. Since outer tracks have more sectors, these are abstracted as multi zoned disk drives, each zone has equal number of sectors per track, but the outer tracks have more sectors in a zone.
3. Cache (or track buffer) 8-16 MB, (holds data read or written to the disk). eg. while reading a sector it might cache some previous / contigous sctors to quickly respond to subseqent reads in the same track.

Acknowledging writes:
1. Acknowledge write complete when data has been put in memory of the disk. - write back.
2. Acknowlege write complete when data has been actally written to the disk - write through.

Write back makes disk appear faster than it actually is but dangerous. (if application require data to be written in a certain order for correctness).

For random read and transfer:
$$
T_{IO} = T_{seek} + T_{rotation} + T_{transfer}
$$

Often we use $R_{IO}$ to compare disks: $R_{IO} = \frac{Size_{transfer}}{T_{IO}}$

avg seek time is 1/3rd of the full seek time [end to end]. because avg seek distance is 1/3 of full seek distance, see derivation in book.

Disks give higher $R_{IO}$ for sequential reads than random reads, as there is only one avg seek and one avg rotation in starting a sequential read.

Disk Scheduling: Two types, one OS does, and one disk does (includes caching etc.) We see the OS one.
- Given a set of IOs, disk scheduler examines them and decides the order of the requests. 
- It is easy to figure out time taken cause we know drive's seek time, rotation delay etc.

Methods:
1. SSTF (Shortest Seek time first, or SSF, shortest seek first (SJF like))
    - Sort the requests by their track position wrt to the current track over which head is there.
    - But OS cant possibly know disk geometry.
2. NBF (Nearest Block first)
    - schedule based on order of nearest blocks.
    - But it could lead to starvation. what if a sudden request comes for the near blcoks.
3. SCAN [elevator]
    - Moves across the disk, servicing requests in order, across the tracks.
    - Single pass across the disk is called a sweep.
    - If a request for a block comes during a sweep, which has already been serviced on this sweep, then it is queued for the enxt sweep.
    - FSCAN: freeze the queue to be serviced while performing the sweep; It places the requests during a sweep onto another queue, to be serviced later. This avoids starvation of far away requests, by delaying the service of nearby but late arriving requests.
    - CSCAN: Circular Scan: Instead of weeping in one direciton, sweep across the tracks, from inner to outer and from outer to inner.
4. Both SCAN, SSTF are not purely SJF, as they do no acount rotation, they only think of seek time.
5. Optimal: STPF (Shortest time to position first.)
    - If seek time > rotation time, then it makes sense to serve item on the closer track.
    - If rotation > seek time, then it makes sense to serve item on the farther track
    - But ofc it depends
    - But os cant often know all this but drive does. hence SPTF is usually performed inside of the drive.

Disk scheduler also perform IO merging, merging multiple consecutive block's requests into one read/write. after the merge happens, then they reorder requests based on the methods above.
    