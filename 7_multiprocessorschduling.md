Difference between a single CPU and a multiprocessor CPU:

Each cpu has its own cache (hardware).
Caches have 2 kinds of locality, spatial and temporal. currently accesssed info might be accesed again. and Next access might be lclose to the crurrently accessed one.

There is a problem of Cache coherence.

Cache affinity:. when a prog runs on CPU, it builds up a fair bit of state in the caches (and
TLBs) of the CPU. So next time it is favorable to run the process on the same CPU.
otherwise on the new CPU it will be slightly slower than on the original one.

Approach:
SQMS (single queue multiprocessor schduling)
maintain a single queue, pop to the next available CPU.

There is an issue of cache affinity here., and we need locks to properly implement it.

Use affinity mechanisms to try to keep the processes on CPUs where they started.

MQMS (multi queue multiprocessor schduling)

Each processor has one queue, following some schdluling policy. When a job enters a system it is sent to a particular queue to run on it until completion.
SO essentially we need a load balancer for this.
say A,B,C,D are there and 2 processors.

processor 1 will run A,B in RR. and processor 2 will run C,D in rr.

More scalable but leads to load imbalance. so how to fix ?

Work migration. one way is that the source queue (more empty) will look at target queues (less empty), and try to steal their jobs (work stealing)
