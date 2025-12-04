# Limited Direct Execution (Mechanism)

## 1. The Basic Approach

The strategy is **Limited Direct Execution**.

* **Direct Execution:** Just load the program and run it directly on the CPU.
* **The Problem:** What if the program needs to perform a restricted action (like I/O)? We cannot give an unprotected program full access to hardware resources.

## 2. Solution: User Mode vs. Kernel Mode

To solve this, the system distinguishes between two execution modes:

1.  **User Mode:** Applications run here. They do *not* have full access to hardware resources.
    * *Constraint:* If a process attempts a privileged operation (like I/O) in user mode, the OS will kill the process.
2.  **Kernel Mode:** The OS runs here. It has access to the full resources of the machine.

## 3. System Calls & Traps

To perform a privileged operation, a user program must perform a **System Call** (syscall).


### The Mechanism

1.  **Trap Instruction:** The program executes a special `trap` instruction.

    * It simultaneously **jumps into the kernel** and **raises the privilege level** to kernel mode.
2.  **Hardware Actions:** The processor pushes the **Program Counter (PC)**, **Flags**, and other registers onto the per-process **Kernel Stack**.
3.  **Execution:** The OS performs the required privileged operations.
4.  **Return-from-Trap:** When finished, the OS calls this special instruction.

    * It pops the values (PC, flags) off the stack.
    * It simultaneously returns to the user program and **reduces the privilege level** back to user mode.

> **Note:** The OS may not necessarily return to the *calling* process; it might switch to another.

### The Trap Table

How does the hardware know where to jump during a trap?

* **Boot Time:** The OS sets up a **Trap Table** and informs the hardware of the locations of these **Trap Handlers**.

## 4. Regaining Control (The Switch)

If a process is running on the CPU, the OS is *not* running. How does the OS regain control to switch processes?

### Approach 1: Cooperative (Wait for System Call)

The OS trusts programs to behave reasonably.

* The process voluntarily gives up the CPU via a `yield` system call.
* Or, the process does something illegal (misbehaves), triggering a trap, which hands control to the OS to terminate it.

### Approach 2: Preemptive (Timer Interrupt)

The OS does not trust the process.

* **Timer Device:** Raises an interrupt every few milliseconds.
* **Action:** The current process is halted, and a pre-configured interrupt handler in the OS runs.

## 5. Context Switching

When switching from Process A to Process B, the OS performs a **Context Switch**.

1.  **Save State:** The OS saves a few register values for the currently running process and pushes them to its kernel stack (kstack).
2.  **Restore State:** The OS restores the saved registers for the next process.

### Distinction: Interrupt vs. Context Switch

There is a subtle difference in *what* gets saved and *who* saves it:

| Scenario | Who Saves? | What is Saved? | Where? |
| :--- | :--- | :--- | :--- |
| **Timer Interrupt** | **Hardware** | User Registers (Current) | Running Process's **Kernel Stack** |
| **OS Switch Decision** | **OS Software** | Kernel Registers (OS Context) | Process A's **PCB / Proc Structure** |

* **Interrupt:** The hardware automatically saves user registers to the kernel stack so the OS code can run.
* **Switch:** When the OS decides to switch processes (scheduler), it explicitly saves its own kernel-mode registers into the PCB of Process A, then loads the saved state of Process B.

## 6. Concurrency Control

**Problem:** What if an interrupt occurs while the OS is already handling an interrupt?

**Solution:** The OS often **disables interrupts** during interrupt processing. This ensures that when one interrupt is being handled, no other one will be delivered to the CPU, preventing race conditions.