# Change propagation

Consumers receive changes, not repeated copies of the whole state. Choose this axis together with [QUERY-MODEL.md](QUERY-MODEL.md): what is replicated decides what is propagated.

Production shapes, pick by what the data and consumers need:

- **Snapshot, then deltas.** A consumer connects, receives current state once, then each change as it happens (Kubernetes: list, then watch from the resource version; on Gone, re-list). Event sourcing (the change log is the record, state is derived) is the stronger form; reach for it when history, replay or audit matter.
- **Poke, then pull since cursor.** The source sends a tiny "something changed" signal; the consumer pulls changes since its cursor. Good when payloads are large or consumers fetch at their own pace.
- **Constant work.** The source pushes its full state on a fixed cadence. Right only when that state is small and bounded at the ceiling: it buys simplicity and predictable load.
- **Content-addressed sync.** Merkle-tree-like hashing lets two sides compare roots and fetch only differing subtrees. Strong for large, mostly-stable state, peers that reconnect after long gaps, and anti-entropy between replicas.

**Resync is for when deltas cannot bridge the gap**: the log was compacted, the consumer's position expired, or it never had a baseline. The consumer detects this (sequence numbers, generations, resource versions) and takes a fresh snapshot, or diffs content hashes, then resumes. Resync will happen: make it correct, tested and routine, since it is the correctness backstop.

**Polling is a transport choice, not a design.** Reading a log from an offset (Kafka, long-poll from a cursor, a spin on a ring) is event delivery done by polling, and fine. Polling is also correct when the consumer is time-slice bounded: a frame-oriented GUI samples latest state once per frame. What stays at the edge is polling a source for its *whole state* because it cannot push: one adapter does that, turns what it sees into deltas, and owns the interval, conditional requests and rate budget. Every protocol and consumer downstream sees changes.

**Backpressure is explicit**: decide what happens when a consumer is slow (see bounds in [CONCURRENCY.md](CONCURRENCY.md)).
