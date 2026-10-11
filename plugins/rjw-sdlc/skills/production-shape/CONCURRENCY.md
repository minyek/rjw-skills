# Concurrency

Decide who owns each piece of mutable state, how others read it, and what bounds the work in flight.

- **Single writer by default.** One task, actor or thread owns each piece of mutable state; others send it messages. The owner is the natural source of the deltas in [PROPAGATION.md](PROPAGATION.md).
- **Readers take snapshots.** Immutable snapshots or generations (arc-swap, MVCC, epochs) let readers proceed without holding the writer up.
- **Threads are a valid answer.** Pick async tasks, OS threads or a mix from the work: blocking syscalls, CPU-bound work and latency-critical loops often want real threads.
- **Bound everything in flight.** Every channel, queue and fan-out has a stated limit sized from the workload, and a stated behaviour at the limit: block the producer, coalesce to latest state, shed, or drop the consumer to resync.
- **Shared-memory synchronisation is engineered.** When state is genuinely shared, choose lock granularity from measured contention, state the memory ordering each atomic needs and why, and reach for lock-free or wait-free structures when the latency or progress guarantee is the requirement.
