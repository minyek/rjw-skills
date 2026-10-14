# Invalidation

A fact ends because its source says so, because its source is gone, or because time says so. Decide which for each kind of fact, and make that path reliable. Choose this axis together with [PROPAGATION.md](PROPAGATION.md): propagation carries changes; invalidation decides how a fact stops being true.

- **Liveness belongs to the source.** A connection, session or subscription is alive or not. While it is down, its facts are kept and marked **stale**: unknown, not removed. Removing the source retracts all of its facts in one operation. Consumers rarely mean per-item liveness.
- **A per-item lease is constant work.** A fact that expires unless it is reasserted makes its producer resend everything on a cadence. That is the constant-work shape in [PROPAGATION.md](PROPAGATION.md), with a write and a deadline per item. It also conflates a slow source with a removed item: a refresh slower than the lease makes items vanish and return. Choose a lease only where the leased state is small and bounded at the ceiling, or where the producer cannot say when a fact ends. Record it as constant work with its expiry.
- **Removal is a message.** Once nothing expires, a lost removal leaks forever. Either deliver removals at least once (retried until acknowledged, idempotent by key), or reconcile: the producer sends its whole set and the consumer drops what is absent (resync in [PROPAGATION.md](PROPAGATION.md)). State which, and test the lost-removal case.
- **Only the writer removes.** A removal names its source, and it does not remove a value another source wrote since. Where values are last writer wins, a removal by an earlier writer is a no-op.
- **Uncertainty is not removal.** A producer that cannot read an item this time (a failed probe, a timeout, a denied permission) keeps its last facts instead of withdrawing them. Withdrawing on a failed read makes the item flap.
- **Derived state is invalidated by its inputs, not by time.** A memo, resolution or view inside a process records the generations of the inputs it read, and is recomputed when one of them changes. Work per change then follows the change, not the size of the state. A timer that guesses when derived state is out of date is either stale or wasteful.

Keeping a nearer copy fresh (pull, push or rebuild) is in [PROPAGATION.md](PROPAGATION.md); the rules above apply to what that copy holds.
