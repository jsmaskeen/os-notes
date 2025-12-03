Segmentation is generalized base and bounds.
have three pairs of base and bounds registers, one for each segment.
Code, stack, heap.

| Segment| Base |Size (Bound-Base)|
|---|---|---|
| Code |32K |2K|
| Heap |34K |3K|
| Stack| 28K |2K|

try to access an illeagal address that leads to segmentation fault.

Explicit appraoch of segmentation:

|Segment bits| Segment| Base |Size (Bound-Base)| Grows +ve |
|---|---|---|---|---|
|00| Code |32K |2K| 1|
|01| Heap |34K |3K| 1|
|11| Stack| 28K |2K| 0|

so say 14 bit virtual address then first 2 bits indicate segment. last 12 bits are offset.. add (subtract) offset to (from) the base to get the PA

Issue: one segment goes unused (10), and our max effective segment size is chopped, as its wil be divided by 4.
[each segment is limited to a maximum size]

We can implement code sharing here by adding protection bits. 

This is called coarse grained segmentation.
We can also have fine grained segmentation, where we had more segments (large number of smaller segments, early OS)
reqquired a segment table.

Here the main memeory will have small free holes. -> external fragmentation.

compacting the meory by moving segments is expensive.

there are algos such as best fit, worst fit, first fir, buddy algorithms (our xv6)


Holes in main mem-> external fragmentation

Allocators could of course also have the
problem of internal fragmentation; if an allocator hands out chunks of
memory bigger than that requested, any unasked for (and thus unused)
space in such a chunk is considered internal fragmentation (because the
waste occurs inside the allocated unit)