Idea is to not optimise for turnaround or response, but try to garuntee that each job obtains a certain percentage of CPU time.

Lottery Scheduling:
assign tickets proportional to the percentage we want for each program.
At each tick hold a lottery, whichever program wins schedule that. 

Probabilistically achieves the goal! not deterministically.

use RNG to hold lottery (simple).

Over a long time the percentages for share of CPU for each program stabalizes.

Ticket manipulation ways:
1. Ticket Currency: Allows user with a set of tickets to allocate tickets to its own processes in any denomination. which will be converted to the global currecny.
    Eg. user has 100 tickets and has 3 processes. it can allocate 100, 300, 500 local tickets (100/8, 300/8 and 100/2) tickets in globa currency.
2. ticket transfer: A process can transfer its ticket to another process (like a process might require a helper process to do stuff, so to make it faster it gives its own tickets to the helper, which while returning, returns the tickets.)
3.  Ticket Inflation: A process can temporarily increase it s number of tickets to allow itsef to run more. This works ina  non competitive scenario where processes trst each other. No one is greedy.

Deterministic Lottery? => Stride scheduling
1. Divide a very large number (10k) by each of the ticket value. that gives us the stride value.
2. initially the pass value of each proc is 0. Run the one with lowest pass value.
3. Increment the pass value by stride once the process runs.
4. Repeat.

If a new process arrives set all the pass values ot 0.

Now why prefer lottery? => No global state like we have for stride scheduling (storing pass values)

Linux CFS:
Completely Fair Scheduler


SImple countic technique.. There is no fixed timeslice. Each process has a `vruntime` (Virtual runtime). which is accumulated as each rpocess runs.
During scheduling the CFS picks the process with lowest vruntime.

CFS uses the value `sched latency` (48ms) to determine how long should each process run before considering a switch. [Determines timeslice in a dynamic way]

CFS divides this value by the number (n) of processes running on the CPU to determine the time slice for a process.

Example: 4 processes, timeslice per process is 48/4 = 12ms. CPU runs them based on lowest vruntime.
Say A, B finish at 24 ms.. now remaining are 2 processes so timeslice now is 48/2 = 24.. this runs C and D in rr till completion.

If there are too many processes then this time slice will reduce, so to prevent that, CFS adds `min_granularity`, set to `6ms` so that CFS will never set timeslice for a process to go below 6ms.


CFS also enables user to assing priority using nice values. nice ranges from -20 to 19 for any process, default = 0. More nice value, lower priority, -ve value means higher priority.

Each nice value is ampped to a weight. we can compute the timeslice per process as:

timeslice_k = \frac{weight_k}{\sum_{i=0}^{n-1} weight_i} \times sched\_latency

vruntime_i = vruntime_i + \frac{weight_0}{weight_i}\times runtime_i

Runtime is scaled inversly by the weight.

CFS uses red black tree of current process to figure out next process.