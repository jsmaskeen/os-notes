# Multiprocessor Scheduling


## 1. Background: Multiprocessor Hardware

To understand scheduling on multiple CPUs, we must understand the hardware differences compared to a single CPU.

* **Caches:** In a multiprocessor system, each CPU has its own cache.
* **Locality:** Caches rely on two types of locality:
    * **Temporal Locality:** Currently accessed info might be accessed again soon.
    * **Spatial Locality:** The next access might be close in memory to the currently accessed one.

### The Cache Coherence Problem
Because each CPU has its own cache, updates to memory on one CPU might not be immediately visible to others, leading to the problem of **Cache Coherence**.

### Cache Affinity

When a program runs on a specific CPU, it builds up a significant amount of state in that CPU's caches and TLBs.

* **Benefit:** Next time the process runs, it is favorable to run it on the *same* CPU to leverage this cached state.
* **Cost:** If moved to a new CPU, execution will be slower because the cache is "cold" (data must be reloaded).

## 2. Approach 1: SQMS (Single Queue Multiprocessor Scheduling)

**Mechanism:**

* Maintain a single global queue of ready jobs.
* When a CPU is available, it pops the next job from this queue.

**Issues:**

1.  **Synchronization:** We need locks to ensure the global queue is accessed safely, which limits scalability.
2.  **Cache Affinity:** Jobs effectively bounce randomly between CPUs, losing the benefits of cache affinity.

    * *Fix:* SQMS implementations often use **affinity mechanisms** to try to keep processes on the CPUs where they started.

## 3. Approach 2: MQMS (Multi-Queue Multiprocessor Scheduling)

**Mechanism:**

* Each processor has its own private queue.
* When a job enters the system, it is assigned to a particular queue (using a load balancer) and remains there until completion.
* **Example:** With 2 processors ($P_1, P_2$) and jobs A, B, C, D:

    * $P_1$ runs A and B in Round Robin.
    * $P_2$ runs C and D in Round Robin.

**Pros & Cons:**

* **Pro:** It is more scalable (less lock contention) and naturally respects cache affinity.
* **Con:** It suffers from **Load Imbalance**.

    * *Scenario:* If A and B finish, $P_1$ sits idle while $P_2$ is still busy with C and D.

## 4. Solving Load Imbalance

To fix the imbalance in MQMS, we use **Work Migration**.

### Work Stealing

This is a common technique to implement migration.

* **Mechanism:** A "source" queue (which is empty or low on work) looks at "target" queues (which are full).
* **Action:** The source attempts to "steal" jobs from the target to balance the load.