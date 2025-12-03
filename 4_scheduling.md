The turnaround time of a job is defined
as the time at which the job completes minus the time at which the job
arrived in the system. 

Turnaround time is a performance metric.

FIFO/FCFS:
simple and easy to implement.
has convoy effect where
a number of relatively-short potential consumers of a resource get queued
behind a heavyweight resource consumer
No preemeption

SJF:
Given that all jobs arrive at the same time, the shortest job is run first.
Still no preemeption

Optimal if all jobs arrive at same time:
Proof:
Suppose we have n processes, P1, P2 .. Pn, with burst times B1, B2, ... Bn
All processes arrive at time 0.
Let waiting time (WT) of a process = time spent in the ready queue before starting execution.

we need to minimise
Average WT=\frac{1}{n}\sum_{i=1}^{n}WT_i​

waiting time of a process depends on the sum of burst times of all processes scheduled before it


Take any scheduling order that is not sorted by burst time.

Find two adjacent processes where a longer process precedes a shorter process, say Pi, Pi+1, with Bi >  Bi+1


Swap them:

Waiting time of Pi increases by Bi+1 - Bi < 0

Waiting time of Pi+1 decreases by same amount.
	​

Net effect: total waiting time decreases.

Repeat swapping all such pairs -> processes are sorted in ascending order of burst time.

SCTF: Shortest time to completion first.
PSJF: premetive SJF

Any time a new
job enters the system, it determines of the remaining jobs and new job,
which has the least time left, and then schedules that one.


Response time is a fairness metric.
Response time is defined as the time from when the job arrives in a
system to the first time it is scheduled.

Round Robin (RR):
run each job for a fixed time slice (scheduling quantum)
(also called time slicing).

Shorter slice -> shorter response time.. but reducing slice time will induce the cost of context switching time.
We need to make time slice long enough to amortize the cost of switching without
making it so long that the system is no longer responsive.

Cost of context switching involves: saving register states, (losing the cache, TLB, beanch predictors etc.)

How schedulers incorporate IO ?
Treat each burst as a separate job.
