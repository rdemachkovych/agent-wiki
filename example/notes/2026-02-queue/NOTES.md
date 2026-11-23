# Queue for invoice e-mails

- **Goal:** checkout never waits on the mail provider.
- **Built:** checkout puts a job on a queue; a worker sends the mail, 3 retries with backoff.
- **Result:** checkout p95 dropped from 1.9 s to 310 ms; 0 lost mails over a week (queue depth and dead-letter count checked daily).
- **Learned:** took a baseline of checkout p95 before the change, same as the cache work.
