Two goals, optimise turnaround time and minimise the repsonse time.

MLFQ has a fixed number of queues, each with its own priority level.
A job that is ready to run will always be on a single queue.

Rather than giving a fixed priority, MLFQ varies the
priority of a job based on its observed behavior.
If a job repeatedly gives up CPU then it remains at a high priority.
hence it uses history of the job to predict its future.

Rules:
Rule 1: if Priority(A) > Priority(B), A runs and B doesnt run.
Rule 2: If Priority(A) = Priority(B), then A, B run in RR.

Rule 3: When a job enters the system, it is placed at the highest
priority (the topmost queue).

Rule 4a: If a job uses up an entire time slice while running, its priority is reduced (i.e., it moves down one queue) [each queue may have a differnet timeslice, increases as priority level decreases.].
Rule 4b: If a job gives up the CPU before the time slice is up, it stays
at the same priority level.

Approximating SJF:

because MLFQ doesn’t know whether a job will be a
short job or a long-running job, it first assumes it might be a short job, thus
giving the job high priority. If it actually is a short job, it will run quickly
and complete; if it is not a short job, it will slowly move down the queues,
and thus soon prove itself to be a long-running more batch-like process.
In this manner, MLFQ approximates SJF.

Problems:
Starvation (If too many interactive job comes (always stay on top queue))
If a malicious program comes and uses all but 1 ms of the timeslice of topmost queue.. it's prioirty will never decrease.


Rule 5: After some time period S, move all the jobs in the system
to the topmost queue.

If S is too high long running jobs will starve. If S is too low then short running jobs might not get proper share of the CPU.

How to prevent malicious program... ?

Rule 4 [Updated]: Once a job uses up its time allotment at a given level (regardless of how many times it has given up the CPU), its priority is
reduced (i.e., it moves down one queue).