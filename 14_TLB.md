TO speed up address translation, we have somehtign called TLB, the translation lookaside buffer.
A TLB is a part of MMU

hardware cache, stores VPN -> PFN translations.

Upon each reference we check first in TLB then if miss then query pagetable.

TLB hit: TLB holds the PFN for queired VPN
TLB miss: TLB doesnt hold the PFN for queired VPN

If miss then we access the page table and update the TLB with the (VPN,PFN) pair
and return it.

TLB hit rate = \frac{Num hits}{Num access} \times 100 \%
TLB improves performance due to spatial locality.

large page size, less TLB misses. Small pagesize, more TLB misses.

If program is rerun after its first execution, TLB hit rate can be 100%, improving performance due to temporal locality.

Who handles TLB miss ?

once miss, the hardware raises an exception, and control is passed to kernel mode's trap handler. Now os will do what it needs to (query page table), update TLB and return execution at the point of exception.
then the hardware retries.

FOR RETRUN FROM TRAP IN SYSCALL, next instructoin is after the trap calling instruction

but for TLB, next instruction is the instruction that caused trap (we want to requery after updating TLB)

On context switch we can flush the TLB as it will not store the VPN-FPN entries for the new process.
We can also provide ASID (or PID) address space identifier to the TLB. so it can differentiate the entires between processes.

Cache Replacement: LRU

