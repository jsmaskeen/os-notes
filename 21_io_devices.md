Program without any input produces the same result everytime
SPeed of bus is inversely proportional to the size, and directly to the cost.

Systems usually have a hiereacical bus structure, CPU is attached to main mem with memory bus (fastest)
then, we have general IO bus, (PCI= Peripheral Component Interconnect)
and lastly we have SATA, SCSI, USB etc. this is the peripheral IO bus, the slowest.

slwoer buses can support a lot of devices.

Firmware = software written within a hardware device.

General structure of a device:

1. It has a hardware interface, which it presents to the rest of the system. Interface consists of 3 registers: data, command and status.
2. Then it has an internal structure, which could be propiertary and implementation specific. it might have its own microcontroller, firmware etc.

Command register tells device to perform specific commands, status shows the current status, and data register is sued to pass the data to the device.

General protocol to communicate with a device:

1. OS waits until device status is not busy [polls the device repeatedly]
2. OS then writes data on the data register. If main CPU is involved in data movement then it is refered to as Programmed IO (PIO).
3. OS then puts command on the command register. this implictly signals the device that both data and command aret here and it should now execute the command.
3. OS polls the device again until it gets a status code.


In this protocol, polling is inefficient. we waste cpu cycles and it might slow down the host device.. as it could use the CPU cycles for some process.

To get away with polling, we can use interrrupts:
1. isntead of polling, OS issues an interrupt, and puts the calling process to sleep [hence switches to another task].
2. when device is finsished doing the operation, it will raise an hardware interrupt (irq, interrupt request), then CPU will jump into OS at a predetermined ISR (interrupt service routine, or the interrupt handler). (CPU finished current instruciton, save state of registers like PC), jumps to ISR, and executes the instruction there. and it will wake up the sleeping proces (which is waiting for IO).

Interrupts allow the overlap of computation and IO.

But using interrupts is not always the best solution, for example, if a deice performs tasks very quickly, interrupts can slow down the system. hence polling is better there.

Often systems have a hybrid method, poll for a while then if not done yet, switch to interrupts.

SOmetimes interrupts can lead to a livelock. for example when a lot of packets come and generate interrupts, OS might keep serving interrupts and not actually service the request.

Another wau is coalescing the interrupts. Here device, before raising an interrupt will wait for other requests to come. hence multiple requests can go under one interrupt. but this increases the latency, if waiting time is too large.

ANother issue, COpying of the data (With programmed IO)
if a file is large, and process executes IO, then first CPU will copy the data to the device one word at a time, then the device will execute IO, after the copy is compelte. Hence with PIO, CPU spends too much time copying the data (When it has to send to the device)

Hence we have a separate controller, DMA (direct memory access) [this is also a device within the system]. 
1. THe OS tells the DMA, how much data to copy and from where to copy. the DMA engine has access to the main memory, hence process' memory and the IO device's registers. 
2. Os is then done, and then DMA handles the copying separately. 
3. When DMA is done, it raises an hardware interrupt signallign the oS that it is done.

How should OS communicate with the device ? (the commands ?)

1. ONe way is to have explicit IO instructions, which gives a way to OS to send the data to specific device registers. 
    - But these instructiosn are usually priviledged. and a malicious program can simply run them.
    - To prevent that hardware has protection.. for example linux has 2 rings, ring 0 for privilged instructison, and ring 3 for user. So there if CPU detects a priviliged instruction from ring 3, then it raises a fault and transfers control to OS to kill the process or do whatever.
2. A better way is to use mmap, memory mapped IO. 
    - Harware makes device register available as if they are memory locations.
    - To access a particular register, the OS issues a load (to read) or store (to write) the address; the hardware then routes the load/store to the device instead of main memory.
    - MMAP is nice cause we dont need to provide any new isntructiosn to the Instrution set which we have.

Now to support varying interfacees of multiple devices, how to program the OS ?

Use device drivers, these are pieces of codes which extend the OS to support the interface of a device. (70% of linux kernel is device drivers.) This is an abstraction.

block read, block writes are issued, then the generic block layer routes it to specific device driver which handles the request and communication with the device.

This has a downside too that rich device functionalities can go underutilised if the above layer doesnt support it. (like rich error codes might come to the application as a generic error, because the generic block layer might not know what is this specialied error code.)





