We cannot increase the page size, as it will cause internal fragmentation
We can use paging with segments, this is a hybrid approach.

So have three page tables
One for code, one for heap and one for stack. This will reduce the unused space in the big page table. we will not need to store invalid entries.

here base bound pair for each segment indicate the start and end of each page table.

we will have first 2 bits as the segment (to identify the code, heap, stakc) Next 18 bits for VPN and last bits for Offset

But this segmentation may casue sparse tables, and it can cause issue of external fragmentation.
(page size is fixed but page tables can be of arbitrary sizes)

MLTP (Multi level page tables)
converting  alinear page table into a tree.

We have a page directory (which is itself a page)
each entry (PDE) tells where a page of page table is. Or it can tell if the entire page is invalid.
PDE has a valid bit and a PFN
IF PDE is valid then atleast one page of the frame at PFN is valid.

Allocates space in proportion of addresses used.

so the VPN has say 14 bits
first 4 bits give the page directory index (figure out Page number), next 4 give the page table index (find out PTE) and last 6 give the offset

We can have three level page table too first 4 bits pd0 next 4 pd1 next 4 pt index last remaining offset

Demand paging.. disk space to move pages back and forth between ram and disk
we have swap space.. we need to remember the disk address of a page for this.

The act of accessing a page that is not in physical memory is commonly
referred to as a page fault.

Upon page fault, page-fault handler code runs

present bit tells if page is in physical memory or disk (present bit is present in PTE)
Swap in (Disk → Memory)
Swap out (Memory → Disk)

To keep a small amount of memory free, most operating systems thus
have some kind of high watermark (HW) and low watermark (LW) to
help decide when to start evicting pages from memory. How this works is
as follows: when the OS notices that there are fewer than LW pages available, a background thread that is responsible for freeing memory runs.
The thread evicts pages until there are HW pages available

