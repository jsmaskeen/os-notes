# CPU Scheduling

## 1. Scheduling Metrics
To evaluate scheduling policies, we use two primary metrics:

### Turnaround Time (Performance)
Defined as the time at which the job completes minus the time at which the job arrived in the system.
$$T_{turnaround} = T_{completion} - T_{arrival}$$

### Response Time (Fairness)
Defined as the time from when the job arrives in a system to the first time it is scheduled.
$$T_{response} = T_{first\_run} - T_{arrival}$$

## 2. Non-Preemptive Algorithms

### FIFO (First In, First Out) / FCFS
* **Mechanism:** Simple and easy to implement.
* **Preemption:** None.
* **Issue (Convoy Effect):** A number of relatively short potential consumers of a resource get queued behind a heavyweight resource consumer. This hurts average turnaround time significantly.


### SJF (Shortest Job First)
* **Mechanism:** Given that all jobs arrive at the same time, the shortest job is run first.
* **Preemption:** None.

#### Proof of Optimality (for simultaneous arrival)
**Goal:** Minimize Average Waiting Time ($WT$).
$$\text{Average } WT = \frac{1}{n}\sum_{i=1}^{n} WT_i$$

1.  Suppose we have $n$ processes with burst times $B_1, B_2, ... B_n$ arriving at $t=0$.
2.  Take any scheduling order that is **not** sorted by burst time.
3.  Find two adjacent processes $P_i, P_{i+1}$ where the longer process precedes the shorter one ($B_i > B_{i+1}$).
4.  **Swap them.**
    * The waiting time of $P_i$ increases by $B_{i+1}$.
    * The waiting time of $P_{i+1}$ decreases by $B_i$.
    * Since $B_i > B_{i+1}$, the net waiting time **decreases**.
5.  Repeating this swap sorts the processes in ascending order of burst time (SJF), proving it is optimal for minimizing waiting time.

## 3. Preemptive Algorithms

### STCF (Shortest Time to Completion First) / PSJF
* **Also known as:** Preemptive Shortest Job First (PSJF).
* **Mechanism:** Any time a new job enters the system, the scheduler determines which of the remaining jobs (including the new one) has the least time left, and schedules that one.

### Round Robin (RR)
* **Mechanism:** Run each job for a fixed time slice (scheduling quantum).
* **Goal:** Optimize **Response Time** (Fairness).

**The Time Slice Trade-off:**
* **Shorter Slice:** Better response time.
* **Longer Slice:** Better overall system efficiency (amortizes switching costs).
* **The Cost:** Reducing slice time induces the cost of context switching. We need to make the slice long enough to amortize this cost without making the system unresponsive.

**Context Switch Overheads:**
Switching is not free. It involves:
1.  Saving register states.
2.  Performance penalties from losing the **Cache**, **TLB**, and **Branch Predictors**.

## 4. Handling I/O
How do schedulers incorporate I/O?
* The scheduler treats each CPU burst as a **separate job**.
* When a process initiates I/O, it blocks, and the scheduler picks another job. When I/O completes, the process becomes ready again with a new (usually short) CPU burst.