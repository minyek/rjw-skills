# Failure at boundaries

Decide what happens when the other side of a boundary is slow, down, absent or wrong, and translate its types and errors into your own at the boundary so nothing inside depends on its vocabulary. **Match the defence to the boundary**: each rung adds to the one above it.

**Degraded paths are visible.** Every fallback, cached or partial answer says which path served it, in the log and in the result, so consumers and operators can tell a degraded answer from a normal one.

**Domain rules belong to the domain.** A rule a domain expert would state (a lawyer cannot act for both sides of a transaction; an issuer cannot sell protection on itself) is checked in domain code, where the context it needs is in view and it can change with the business. Data-representation layers enforce well-formedness only: types, nullability, referential integrity, key uniqueness. A refined type such as `ValidTransaction` is fine when only the domain check can construct it.

- **Problems can be values.** When someone will act on them (fix, review, waive), keep the entity and every problem found together as data, rather than forcing them into control flow: an exception or an either-or result stops at the first problem and drops the value.
- **Each problem names the rule and the parties**, in the domain's terms, never a constraint name or an error code from the store.
- **Run the check atomically with the write it guards**: a single writer for the aggregate, or a transaction over everything the check reads. Taking a rule out of the store gives up the atomicity the store was providing.

1. **In-process**: ordinary error handling. No boundary defences.
2. **Same host, a daemon you cannot start** (a system service, another user's process): a timeout on every call, fail fast, and an error that names the missing service and how to start it.
3. **Same host, a daemon whose lifecycle you can trigger** (a per-user daemon spawned on demand): the client brings it up on demand, so design the start path as carefully as the call path:
   - **Single instance**: a lock decides who starts it; concurrent clients wait on the winner rather than racing.
   - **Readiness, not sleep**: wait for the daemon to report ready (a handshake on the socket), with a deadline.
   - **Stale state**: detect and clear a dead socket or pid file left by a crash.
   - **Version skew**: handshake on version; say what a newer client does with an older running daemon (use it, restart it, refuse).
   - **Who stops it**: idle exit, explicit stop, or session-scoped; and where its logs go when the client that started it has exited.
4. **Cross-host, or a third-party service** (forge APIs, rate-limited or paid services): the full stability set:
   - **Timeouts** on every call, connect and read separately.
   - **Retry budgets** with backoff and jitter; retries only for idempotent operations, or with an **idempotency key**.
   - **Bulkheads**: one slow dependency gets its own bounded pool and cannot stall unrelated work.
   - **Circuit breakers** where repeated failure is expected and calls are costly.
   - **Rate budgets** owned by one adapter per source (see the polling edge in [PROPAGATION.md](PROPAGATION.md)).
