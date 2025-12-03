# I/O Devices
*Revision Notes based on OSTEP*

## 1. System Architecture
A program without any input produces the same result every time (determinism). To interact with the world, we need Input/Output.

### Bus Hierarchy
The speed of a bus is generally **inversely proportional** to its length/size and **directly proportional** to its cost.
* **Memory Bus:** The fastest bus, connecting the CPU to Main Memory.
* **General I/O Bus:** Connects high-speed I/O devices (e.g., PCI = Peripheral Component Interconnect).
* **Peripheral I/O Bus:** The slowest bus, meant to support a large number of devices (e.g., SATA, SCSI, USB).


## 2. Canonical Device Structure
A device generally consists of two parts:
1.  **Hardware Interface:** The interface presented to the rest of the system, typically consisting of three registers:
    * **Status:** Shows the current state of the device.
    * **Command:** Tells the device to perform specific tasks.
    * **Data:** Used to pass data to/from the device.
2.  **Internal Structure:** Implementation-specific internals. Complex devices may have their own microcontroller and **Firmware** (software written within a hardware device).

## 3. Protocols: CPU-Device Communication

### Approach 1: Polling (Programmed I/O - PIO)
The protocol follows these steps:
1.  **Wait (Poll):** The OS reads the status register repeatedly until the device is not busy.
2.  **Write Data:** The OS writes data to the data register. (If the main CPU moves the data, it is called **Programmed I/O**).
3.  **Write Command:** The OS writes to the command register. This implicitly signals the device to execute.
4.  **Wait (Poll):** The OS polls the device again until it receives a success/failure code.

**Drawback:** Polling is inefficient. It wastes CPU cycles that could be used for other processes.

### Approach 2: Interrupts
To avoid wasting cycles:
1.  The OS issues the request, puts the calling process to **sleep**, and switches to another task.
2.  When the device finishes, it raises a hardware **Interrupt Request (IRQ)**.
3.  The CPU pauses execution, saves the state (e.g., PC), and jumps to a pre-determined **ISR (Interrupt Service Routine)** or interrupt handler.
4.  The ISR executes and wakes up the sleeping process.
* **Benefit:** Allows the overlap of computation and I/O.

**Issues with Interrupts:**
* **Performance:** If a device is extremely fast, the overhead of context switching for interrupts slows down the system. In these cases, polling is better.
* **Livelock:** If too many interrupts occur (e.g., a flood of network packets), the OS might spend 100% of its time processing interrupts and never make progress on the actual tasks.

**Optimizations:**
* **Hybrid Approach:** Poll for a short while; if not done, switch to interrupts.
* **Coalescing:** The device waits for multiple requests to complete (or a timer to expire) before raising a single interrupt. This improves efficiency but increases **latency**.

## 4. Data Movement: DMA
With Programmed I/O (PIO), the CPU spends too much time copying data word-by-word from memory to the device.

**Solution: Direct Memory Access (DMA)**
DMA is a specific device within the system that handles data transfers.
1.  **Setup:** The OS tells the DMA engine where the data is (source), how much to copy, and where to send it (destination).
2.  **Execution:** The OS continues with other work while the DMA engine copies the data directly from memory to the device.
3.  **Completion:** When done, the DMA raises an interrupt.


## 5. Addressing Devices
How does the OS communicate with specific device registers?

### Method 1: Explicit I/O Instructions
* The OS uses special hardware instructions to send data to specific device ports.
* **Protection:** These are **privileged** instructions.
    * Example: Linux uses protection rings (Ring 0 for Kernel/Privileged, Ring 3 for User). If a Ring 3 program tries to execute I/O instructions, the CPU raises a fault, allowing the OS to kill the process.

### Method 2: Memory Mapped I/O (MMIO)
* The hardware makes device registers available as if they were memory locations.
* To access a register, the OS simply issues a standard **Load** (read) or **Store** (write) to that address.
* **Benefit:** No new instructions are needed in the Instruction Set Architecture (ISA).

## 6. The Software Stack: Device Drivers
To support the varying interfaces of diverse devices, we use **Device Drivers**.
* **Definition:** Code that abstracts the specific details of a device, allowing the OS to interact with it via a standard interface.
* **Prevalence:** About 70% of the Linux kernel code consists of device drivers.

**The Abstraction Flow:**
1.  File System issues a generic request (e.g., Block Read).
2.  **Generic Block Layer** routes the request.
3.  **Device Driver** handles the specific communication with the device hardware.

**Downside:**
Rich device functionalities can go underutilized. For example, a "generic error" might be returned to the application because the generic block layer doesn't understand the specialized error code returned by the device.