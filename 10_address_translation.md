Hardware based address translation: converts VA to PA (pretty simple but useless.)

Base and Bounds (Dynamic reloacation)
we need two hardware registers in each CPU. [part of the MMU (memory management unit)]
One is the base register, and other is the bounds (limit) register.

PA = VA + base

provided VA + base < bounds

bounds register may hold the phyical address or the size.

The hardware will provide special instructions to modify base and bound registers, allowing OS to change them when different processes run.
These instructiosn are privilidges and can only be run in kernel mode. [only in kernel mode can the registers be modified]

Freelist: structure in the OS which stores what ranges of the memory is free.

CPU should be able to generate exception if address is out of bounds.
there should be a handler for this.

When process is created OS should do the follwoing
1. Find space in free list to allot the memory range.
2. Clean the memory once the process exits.
3. During context switch, it should store the value of the base and bounds in the PCB. as the hardware has only one base and bounds register.

OS can move address space form one base-bounds range to other.. while the process isnt schduled.

Since the space inside the region of heap and stack is wasted.. not often used.. this has what is called internal fragmentation.

There can be little holes as well so it also has external fraagmentation.