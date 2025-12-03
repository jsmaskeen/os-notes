# Proportional Share Scheduling
*Revision Notes based on OSTEP*

## 1. The Core Concept
The idea is **not** to optimize for turnaround or response time directly, but to guarantee that each job obtains a certain percentage of CPU time.

## 2. Lottery Scheduling
**Mechanism:**
* Assign **tickets** to processes proportional to the percentage of the resource they should receive.
* At each time tick (scheduling quantum), hold a lottery.
* Whichever program holds the winning ticket is scheduled.

**Key Characteristics:**
* **Probabilistic:** It achieves the goal probabilistically, not deterministically.
* **Implementation:** Uses a Random Number Generator (RNG) to hold the lottery (simple to implement).
* **Convergence:** Over a long period, the share of CPU for each program stabilizes to the desired percentage.

### Ticket Manipulation Mechanisms
1.  **Ticket Currency:** Allows a user with a set of tickets to allocate them among their own processes in any denomination. The OS converts this to the global currency.
    * *Example:* User has 100 global tickets. They run 3 processes and give them 100, 300, and 500 "local" tickets. The OS calculates the global share (e.g., $100/900 \times 100$ global tickets).
2.  **Ticket Transfer:** A process can transfer its tickets to another process temporarily.
    * *Use Case:* Client/Server. A client sends a request to a server and "hands over" its tickets so the server runs faster to complete that specific request.
3.  **Ticket Inflation:** A process can temporarily increase its own number of tickets to run more.
    * *Requirement:* This only works in a non-competitive scenario where processes trust each other (no one is greedy).

## 3. Stride Scheduling (Deterministic Lottery)
To avoid the randomness of Lottery scheduling, Stride scheduling is used.

**Algorithm:**
1.  **Calculate Stride:** Divide a very large number (e.g., 10,000) by each process's ticket value.
    $$\text{Stride} = \frac{\text{Large Constant}}{\text{Tickets}}$$
2.  **Pass Value:** Each process has a `pass` value, initially 0.
3.  **Schedule:** Run the process with the **lowest** pass value.
4.  **Update:** After running, increment the process's pass value by its stride.
    $$\text{pass} = \text{pass} + \text{stride}$$

**Comparison:**
* Why prefer Lottery over Stride? Lottery requires **no global state** (like storing pass values for every process). It is easier to add new processes without calculating appropriate pass values.

## 4. Linux CFS (Completely Fair Scheduler)
CFS implements proportional share principles efficiently.

**Basic Mechanism:**
* There is no fixed time slice.
* **vruntime (Virtual Runtime):** Each process accumulates `vruntime` as it runs.
* **Scheduling Decision:** CFS always picks the process with the **lowest** `vruntime`.

### Determination of Time Slice
CFS uses a target latency window called `sched_latency` (e.g., 48ms) to determine how long processes should run before considering a switch.

1.  **Calculation:** CFS divides `sched_latency` by the number of processes ($n$) to determine the per-process time slice.
    $$\text{time\_slice} = \frac{\text{sched\_latency}}{n}$$
    * *Example:* 4 processes, `sched_latency` = 48ms $\rightarrow$ Time slice = 12ms.
    * *Dynamic Adjustment:* If 2 processes finish, the remaining 2 get $48/2 = 24$ms each.

2.  **Minimum Granularity:** If there are too many processes, the calculated time slice becomes too small (causing context switch overhead).
    * CFS enforces `min_granularity` (e.g., 6ms). The time slice will never drop below this value.

### Weighting (Nice Values)
Users can assign priority using **nice** values.
* **Range:** -20 (Highest Priority) to +19 (Lowest Priority). Default is 0.
* **Mapping:** Each nice value is mapped to a geometric weight.

**Formulas:**
The time slice for process $k$ is proportional to its weight:
$$\text{timeslice}_k = \frac{\text{weight}_k}{\sum_{i=0}^{n-1} \text{weight}_i} \times \text{sched\_latency}$$

The `vruntime` accumulation is scaled inversely by weight (higher weight = slower vruntime growth = runs more often):
$$\text{vruntime}_i = \text{vruntime}_i + \frac{\text{weight}_0}{\text{weight}_i} \times \text{runtime}_i$$

### Data Structure
CFS uses a **Red-Black Tree** to store running processes, ordered by `vruntime`, allowing efficient retrieval of the next process to run.