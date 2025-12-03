Goals:
1. As time sharing increased, we needed more programs in memory.
2. SO we need to isoloate the programs form each otehr. 
3. Not let program alter code of other program/kernel itself.

SO makes a abstraction of physical memory called address space. address space is contigous and of the size what program needs.
The address space fo a proagram contains all its memory namely code, stack, heap etc.

Program code is at arr 0x0, heap grows positively, and stack's top is at end of the addres space and it grows -vely.
Stack and heap grow in opposite directions so that they can use the space efficiently

The virtual memory should be implemented in a way that is invisible to the running program.
The assignment should be as efficient as possible to minimise space wastage and time to lookup the value stored.
THe os should protect itself and otehr processes' memory from other processes.

Protection enables isolation.


