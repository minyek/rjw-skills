---
name: production-shape
description: Use when designing, brainstorming or implementing anything that holds, moves, queries or exposes data: a store, index, cache, protocol, sync path, backend abstraction, planner, CLI or UI listing. Choose data structures, change propagation, query model, operation lowering, concurrency and wire format on purpose against the project's reference scales, and record any smaller shape with its expiry condition.
---

# Production Shape

Build the **production shape** the first time. Decide each design axis on purpose, against the real operations and the project's reference scales, and stop only when you can say why your choice beats the obvious first answer.

The comparison is never build cost against build cost. It is build cost now against the full later bill: someone profiles it, cannot believe how naive it is, redoes it, and carries compatibility shims for a generation. That bill is larger, and it lands with embarrassment attached.

## The profiler test

A thought experiment, not a profiling run. Picture a competent engineer profiling this at the project's ceiling scale a year from now. If they would be shocked at how naive it is, it is not the cheap option. Build the shape that passes.

## Steps

1. **Write the workload note** (below) before choosing a shape. Done when every field has a number or an explicit gap.
2. **Decide each axis that applies.** Read the axis file for every axis the work touches; most data work touches several, and change propagation and query model are coupled.
   - Data structures, layout and memory: [DATA-AND-MEMORY.md](DATA-AND-MEMORY.md)
   - Change propagation (how changes reach consumers): [PROPAGATION.md](PROPAGATION.md)
   - Query model (replication, cache, federation): [QUERY-MODEL.md](QUERY-MODEL.md)
   - Operation lowering (who decides how operations execute, pushdown to backends): [LOWERING.md](LOWERING.md)
   - Concurrency, ownership and backpressure: [CONCURRENCY.md](CONCURRENCY.md)
   - Protocol and wire format: [PROTOCOLS.md](PROTOCOLS.md)
   - Failure at boundaries, when the work calls across a process or network boundary to something that can be slow, down or wrong: [FAILURE.md](FAILURE.md)
3. **Run the profiler test** on the result. Done when every axis choice passes it or is recorded as a smaller shape.
4. **Record** the choices in the PR description, non-obvious ones as implementation choices (below), and any smaller shape in the decision ledger.

## Workload note

- **Operations**: each read, write, query and subscription, with its frequency (per call, per turn, per second).
- **Cardinalities**: realistic now, the design target, and the ceiling, read from the project's workload reference (below). The design holds at the target; the ceiling sets the limits, the seams and the expiry condition. Everything must still fit on the machines it runs on.
- **Locality**: same process, same host, or cross-host.
- **Resources**: a napkin sketch of network, disk, memory and CPU, each for bandwidth and latency, at the ceiling.
- **Invariants**: what you know and can exploit: ordering, closed sets, maximum sizes, platform facts.
- **Bounded consumers**: every result crossing into a GUI, TUI, one process's memory or an agent's context window has a result limit, signals partiality explicitly ("200 of ~40k"), and has a reveal story: paging, progressive disclosure, history windowing and retention.
- **Evidence**: reasoning about the operations rejects the first answer. A **candidate walk** justifies a choice, including a custom structure: list the properties the operations need, and reject each standard candidate by the property it fails. Claims about numbers ("the simple shape holds on this hot path", "fits the memory budget at the ceiling") take basic timing or a profile; inspect generated code only for hot loops where timing cannot explain the result.
- **Assumptions**: mark each assumption a shape relies on (closed set, ordering, maximum size, platform) where the code depends on it, with an assert or a named marker, so a broken assumption points at every dependent site. Assume what you know; keep what you expect to change behind a seam.

The project's **workload reference** (for example `docs/agents/workloads.md`) states the reference scales: the entities, their counts and rates now, the target and the ceiling, and the machines. It should have been provided; if not, ask the user to write one, and meanwhile size the ceiling at the system limit (all repos, all hosts, months of history). Humans own it and revise it as load tests and production teach them.

When you cannot fill a cardinality, ask; in an autonomous crew record it under "If asking were free" and size for the system limit.

## Implementation choices

Settled choices accumulate where the code is, so later agents build on them instead of re-deriving them.

- **Write a record** when a choice is non-obvious: it rejected a candidate a reasonable agent would reach for. Ordinary choices get none.
- **At the code**: one doc comment on the type or module naming the choice and its assumption markers, ending `Choice: docs/implementation-choices/<name>.md`.
- **In the record**: the workload numbers it was sized against, the candidate walk with each rejection, the assumptions, and the expiry condition.
- **Read** a record only for code you are changing. **Revisit** it only when an assumption marker fires, the workload reference's ceiling moves, or the code's operations change; otherwise it is settled.
- **Escalate to an ADR** when the choice fixes something others depend on: a wire or disk format, or a seam other modules use.

## Choosing a smaller shape

Effort is the tiebreak, not the test. When the production shape costs about the same, build it. When it is genuinely bigger, you may build the smaller shape and record it in the decision ledger:

- **Choice**: the shape built, named by axis (for example "lowering level ii: uniform filter over decoded kind").
- **Alternative**: the production shape.
- **Expiry**: the concrete condition under which it fails the profiler test ("past ~10k messages per convoy", "when a second backend can index").
- **Seam**: what keeps the later move cheap (the wire format, the trait, the query interface that already admits the better shape).

A smaller shape that bakes its limit into a protocol, an on-disk format or a public interface is not smaller; its expiry costs a migration.

## Scope

YAGNI decides whether a feature exists. This skill decides its shape once it does, in application code as much as in substrate.
