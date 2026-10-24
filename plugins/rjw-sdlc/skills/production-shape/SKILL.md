---
name: production-shape
description: Use when designing a data path (a store, index, cache, sync, protocol, backend abstraction, or a listing a person or agent reads), when changing one on a scale-sensitive path, or when reviewing either.
---

# Production Shape

Build the **production shape** the first time. Decide each design axis on purpose, against the real operations and the project's reference scales, and stop only when you can say why your choice beats the obvious first answer.

The comparison is never build cost against build cost. It is build cost now against the full later bill: someone profiles it, cannot believe how naive it is, redoes it, and carries compatibility shims for a generation. That bill is larger, and it lands with embarrassment attached.

**Maturity sets the ceiling.** A prototype meant to be abandoned, or a personal tool, sizes its ceiling to its real use, and the shape that fits is its production shape. When such code is promoted, its shapes expire: that is a recorded condition, not a surprise.

## The profiler test

Picture an expert performance engineer profiling this at the project's ceiling a year from now. If they would be shocked at how naive it is, it is not the cheap option.

Make it concrete rather than imagined: for the hottest operation, write its cost at the ceiling (operations times cardinality, bytes moved, round trips) and the resident size. On a per-event path, the hottest operation is one event: write its cost per change. The test passes when those numbers fit the reference deployments' budgets and the expert would find nothing large left on the table.

## How much to do

- **New data path, new structure, new boundary crossing, or a change on a scale-sensitive path**: the full steps below. A path is **scale-sensitive** when it runs per item, per request or per event, or holds or streams a collection that grows with use.
- **A change inside a settled implementation choice**: cite its record and confirm its assumptions still hold.
- **Anything else**: one line saying why scale does not bear on it. A change to what a start reads from earlier runs also follows [EVOLUTION.md](EVOLUTION.md)'s start rules, whatever its tier.

## Steps

1. **Write the workload note** (below). Done when each field has a value or a named gap.
2. **Decide each axis that applies.** Read the axis file for every axis the work touches; change propagation is coupled to query model and to invalidation.
   - Data structures, layout, memory and steady state: [DATA-AND-MEMORY.md](DATA-AND-MEMORY.md)
   - Change propagation: [PROPAGATION.md](PROPAGATION.md)
   - Invalidation (how a fact ends: source liveness, leases, removal, derived state): [INVALIDATION.md](INVALIDATION.md)
   - Query model (cache, materialized view, replica, federation, at every tier boundary): [QUERY-MODEL.md](QUERY-MODEL.md)
   - Operation lowering (who decides how operations execute, pushdown to backends): [LOWERING.md](LOWERING.md)
   - Concurrency, ownership and backpressure: [CONCURRENCY.md](CONCURRENCY.md)
   - Protocol and wire format: [PROTOCOLS.md](PROTOCOLS.md)
   - Evolution of anything that outlives a process (wire, persisted formats, schemas, public APIs), and what a start does with the state files, journals, checkpoints and markers earlier runs left: [EVOLUTION.md](EVOLUTION.md)
   - Failure at boundaries, when the work calls across a process or network boundary: [FAILURE.md](FAILURE.md)
3. **Run the profiler test.** Done when every axis choice passes or is recorded as a smaller shape.
4. **Record** the choices following the project's conventions (below).

## Workload note

- **Operations**: each read, write, query and subscription, with its frequency (per call, per request, per second).
- **Cardinalities**: now, the target and the ceiling, from the workload model. The design holds at the target; the ceiling sets the limits, the seams and the expiry condition.
- **Locality**: same process, same host, or cross-host.
- **Resources**: a napkin sketch of network, disk, memory and CPU, each for bandwidth and latency, at the ceiling.
- **Invariants**: what you know and can exploit: ordering, closed sets, maximum sizes, platform facts.
- **Bounded consumers**: every result crossing into a GUI, TUI, one process's memory or an agent's context window has a result limit, signals partiality explicitly ("200 of ~40k"), and has a reveal story: paging, progressive disclosure, history windowing and retention. Spend the budget on what the reader can use, in their frame (paths they can reach, names they use) rather than implementation coordinates: for a person or an agent the cost is attention and focus, not just time.

The project's **workload model** is a `WORKLOAD.md` at the repository root plus any nearer the code: walk up from the code you are changing and read each one, nearest first. Together they state maturity, scale drivers, usage, dependencies and budgets, reference deployments and conventions. Read and write them as [WORKLOAD-FORMAT.md](WORKLOAD-FORMAT.md) describes. When the repository has no root file, follow [SETUP.md](SETUP.md); until it exists, size the ceiling at the largest plausible deployment and history. Humans own the root numbers and revise them as load tests and production teach them.

When you cannot fill a cardinality, ask. When nobody can be asked (an autonomous run), record the gap where the project records open questions and size for the largest plausible deployment.

## Evidence

- **Reasoning rejects** the first answer: the operations at the ceiling are enough.
- **A candidate walk justifies** a choice, including a custom structure: list the properties the operations need, and reject each standard candidate by the property it fails.
- **Claims about a dependency** (what it can or cannot do, what it guarantees) cite its source or documentation, not memory.
- **Claims about numbers** ("the simple shape holds on this hot path", "fits the memory budget") take basic timing or a profile. Inspect generated code only for hot loops where timing cannot explain the result. Keep that timing in a benchmark or performance suite, never in functional tests, which must not fail on a slow or loaded machine.
- **Find resident waste by census**, not by guess. Count what a structure holds by kind: values against distinct values (the **duplication ratio**), and string-keyed maps against distinct keysets (the **shape count**), counting each shared allocation once. A counting allocator gives the total and a heap profiler the allocation sites. Where resident size is a recurring budget, keep the census as code run against a recorded real workload, so the next change reruns it.
- **Mark assumptions** a shape relies on (closed set, ordering, maximum size, platform) where the code depends on them, with an assert or a named marker, so a broken assumption points at every dependent site. Assume what you know; keep what you expect to change behind a seam.

## Project conventions

Record decisions the way the project already does: its decision log, ADR set, PR descriptions, and where implementation-choice records live. The root `WORKLOAD.md` names them, or your agent instructions do. When neither does, put the record with the project's existing design records rather than starting a new directory, and raise the location as a question at the next point your instructions allow one. Add the answer to the root `WORKLOAD.md`, so the next run follows it without asking.

## Implementation choices

Settled choices accumulate where the code is, so later work builds on them instead of re-deriving them.

- **Write a record** when a choice is non-obvious: it rejected a candidate a reasonable engineer would reach for. Ordinary choices get none.
- **At the code**: one doc comment on the type or module naming the choice and its assumption markers, ending with a link to the record: at the location above, or `docs/implementation-choices/<name>.md` when the project has no design records.
- **In the record**: the workload numbers it was sized against, the candidate walk with each rejection, the assumptions, and the expiry condition.
- **Read** a record only for code you are changing. **Revisit** it only when an assumption marker fires, a ceiling it was sized against moves, or the code's operations change; otherwise it is settled.
- **Escalate to an ADR** (in the project's ADR set and format) when the choice fixes something others depend on: a wire or disk format, or a seam other modules use.

## Choosing a smaller shape

Effort is the tiebreak, not the test. When the production shape costs about the same, build it. When it is genuinely bigger, you may build the smaller shape and record it in the project's decision log, in that log's own format, carrying:

- the shape built, named by axis (for example "lowering level ii: uniform filter over decoded kind");
- the production shape it stands in for;
- the **expiry**: the concrete condition under which it fails the profiler test ("past ~10k messages per thread", "when a second backend can index");
- the **seam** that keeps the later move cheap (the wire format, the trait, the query interface that already admits the better shape).

A smaller shape that bakes its limit into a protocol, an on-disk format or a public interface is not smaller; its expiry costs a migration.

## Reviewing

Review is static: arithmetic is the evidence.

- For each data path in the change, compute the hottest operation's cost at the ceiling from the workload model. A **naive shape** is a finding when that arithmetic shows it; it needs no profile.
- Report naive shapes separately from size findings. The production shape is often less code, so never trade one against the other in a single finding.
- On a scale-sensitive path, a missing workload note, or a smaller shape without an expiry and a seam, is a finding. Elsewhere it is not.
- A change that adds a store, a dominant operation or a dependency without updating the nearest `WORKLOAD.md` is a finding.
- A durable-store read on a per-event, per-request or per-pass path is a finding unless the workload note records why that data is not held resident.
- On a per-event path, work proportional to the whole state for each change is a naive shape, unless that state is small and bounded at the ceiling: the production shape recomputes only what the change's inputs reach ([INVALIDATION.md](INVALIDATION.md)).
- A per-item lease on facts that share one source and grow with use, without a recorded constant-work choice, is a finding. So is a design without time-based expiry that does not say how a lost removal is recovered.
- A per-entry field with no named reader is a finding: it costs its size times the count.
- A change to a wire protocol, persisted format, schema or public API that breaks the rules of its evolution level is a finding, as is a fallback that does not say it served the answer.
- A start that refuses or throws over a runtime-written input (a state file, journal, checkpoint or marker an earlier run left) is a finding, unless it is a lock or marker whose owner is alive ([EVOLUTION.md](EVOLUTION.md)).
- A domain rule enforced only as a schema constraint or a basic-type restriction is a finding, as is one checked apart from the write it guards.
- Check that assumption markers exist where records say they do.

## Scope

YAGNI decides whether a feature exists. This skill decides its shape once it does, in application code as much as in infrastructure.
