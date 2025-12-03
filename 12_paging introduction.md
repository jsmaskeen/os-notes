Divide physical memory and virtual memory into fixed sized pages.

called pages in virtual memory, and page frames in physical memory

Most flexible, no external fragmentation

Per process page table is recorded by the OS to store where each virtual page is present in physical memory.

VA is split into virutal page number (VPN) and the offset.

say first 2 bits are VPN and last 4 are offset then page size is 2^4 bytes.
number of pages are 2^2 = 4.

total space is 4*16 = 64 bytes.

In page table VPN -> PFN (Physical Frame/Page number PFN or PPN) translations are stored.
Just do PA = ( PageTable(VA[VPN_mask]>>num_bits_offset) << num_bits_offset) | offset 
PageTable(VPN[mask]>>num_bits_offset) = PFN

Page table stores page table entries (PTE), usually 4 bytes in size, 32 bits.

stores VPN ,PFN, valid bit, protection, permission bits etc.

Pagetable lives in kernel spaces.

Simple Page Table:

Linear page table, indexed by VPN, sotres the PFN, valid bit (is the entry valid)
Unused space is invalid.

There is a present bit to tell if the page is in memory (1) or in disk (swap space) (0)

Dirty bit (if page is modified since loading into memory), accessed bit (for circular page replacement)

If page table size very large then we have internal fragmentation.

With paging, what is saved/restored on a process
context switch?
- Pointer to page table, size of page table
- Page table itself is in main memory

COns: too slow, too much memory.