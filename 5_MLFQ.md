# Multi-Level Feedback Queue (MLFQ)
*Revision Notes based on OSTEP*

## 1. The Goals
The MLFQ scheduler tries to address two conflicting goals simultaneously:
1.  **Optimize Turnaround Time:** This is usually done by running short jobs first (like SJF).
2.  **Minimize Response Time:** This is critical for interactive users (like Round Robin).

## 2. Basic Structure
MLFQ has a fixed number of queues, each with its own priority level.
* A job that is ready to run will always be on a single queue.
* **Dynamic Priority:** Rather than giving a fixed priority, MLFQ varies the priority of a job based on its observed behavior (using the history of the job to predict its future).
    * **Interactive Jobs:** If a job repeatedly gives up the CPU (waiting for I/O), it remains at a high priority.
    * **CPU-bound Jobs:** If a job uses the CPU intensively, it moves down in priority.


## 3. The Basic Rules (Attempt 1)

### Priority Rules
* **Rule 1:** If $\text{Priority}(A) > \text{Priority}(B)$, A runs (B doesn't).
* **Rule 2:** If $\text{Priority}(A) = \text{Priority}(B)$, A and B run in Round Robin (RR).

### Placement Rule
* **Rule 3:** When a job enters the system, it is placed at the highest priority (the topmost queue).

### Behavior Rules (Naive Approach)
* **Rule 4a:** If a job uses up an entire time slice while running, its priority is reduced (moves down one queue).
    * *Note:* Queues at lower priorities may have longer time slices.
* **Rule 4b:** If a job gives up the CPU before the time slice is up, it stays at the same priority level.

### Logic: Approximating SJF
MLFQ approximates **Shortest Job First (SJF)** without knowing the length of the job in advance.
1.  It assumes a new job might be short, giving it high priority.
2.  If it is indeed short, it runs quickly and completes.
3.  If it is not short, it slowly moves down the queues, proving itself to be a long-running, batch-like process.

## 4. Problems with the Basic Approach
1.  **Starvation:** If too many interactive jobs enter the system, they will monopolize the top queue. Long-running jobs (at the bottom) will never get CPU time.
2.  **Gaming the Scheduler:** A malicious program can "trick" the scheduler.
    * *The Exploit:* The program runs for 99% of the time slice, then voluntarily gives up the CPU (yields) right before the slice ends.
    * *The Result:* Under **Rule 4b**, its priority is never reduced, allowing it to hog the CPU at the highest priority level.

## 5. Refinements (The Solutions)

### Solution to Starvation: Priority Boost
* **Rule 5:** After some time period $S$, move **all** the jobs in the system to the topmost queue.
    * This resets the system and guarantees that low-priority jobs eventually get a turn.
    * *Tuning $S$:* If $S$ is too high, long-running jobs starve. If $S$ is too low, short-running jobs might not get a proper share of the CPU.

### Solution to Gaming: Better Accounting
We must account for how much CPU a process uses *in total* at a given priority level, not just in a single burst.

* **Rule 4 [Updated]:** Once a job uses up its time allotment at a given level (regardless of how many times it has given up the CPU), its priority is reduced (i.e., it moves down one queue).