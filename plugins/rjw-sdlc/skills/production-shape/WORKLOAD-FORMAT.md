# WORKLOAD.md format

A **workload model** says what a system is asked to do and what budgets it has, at the scales it must hold. It never records how fast the implementation is: measured implementation costs live with the code and its benchmarks, and are checked against the budgets here.

Worked examples, each a root plus two components: a server ([examples/ci-service](examples/ci-service/WORKLOAD.md)), a desktop tool with file-system and OS limits ([examples/code-search](examples/code-search/WORKLOAD.md)), and a library with CPU, SIMD and GPU placement ([examples/video-lib](examples/video-lib/WORKLOAD.md)).

## Files and lookup

- A `WORKLOAD.md` can sit in any directory. For the code you are changing, walk up from its directory to the repository root and read every `WORKLOAD.md` on the way. The nearest file wins for anything it states; ancestors supply the rest.
- The **root** file holds every absolute number. **Component** files hold numbers relative to a parent entity and inherit everything else.
- An entity used by more than one component lives in the lowest `WORKLOAD.md` that is an ancestor of all of them, so lookup only ever walks up.

## What earns an entry

An operation, entity, store or dependency earns an entry when getting its scale wrong would change a design choice. Rare or bounded work is grouped or left out.

**Temporaries** (structures built within one operation) roll up into the operation that creates them. They get their own entry only when they outlive the operation, are shared across concurrent operations, or are sized by an absolute scale.

## Variables and formulas

- **Scale drivers** is the only table with now / target / ceiling. Every number that grows, counts and rates alike, is a named driver. For a library the columns read typical caller / supported / ceiling.
- Everywhere else, a cell holds a fixed value or refers to a driver or entity by its name in backticks, like named variables in a spreadsheet.
- **Derived checks** are formulas over those names. Each value states the column it uses and the date: `Job rows retained = pushes/day x pipeline x job x retention = ~12.5M at ceiling (2026-10)`. When a driver changes, grep its name and recompute.

## Root sections

- **Maturity**: prototype, personal tool, internal or production; expected lifespan.
- **Scale drivers**: name, now, target, ceiling, growth (trend and named steps), source.
- **Shared entities**: as in a component's Entities table.
- **Usage**: the dominant user-visible operations (requests, UI actions, public API calls), each named: arrival (open rate, or closed population and think time), rate, work per operation, latency, staleness tolerated.
- **Dependencies and budgets**: external services, OS facilities, hardware, and the project's own durable stores (the cost of a read crossing into them): what they are used for, their budget (rate limits, cost, limits, capacity) and availability (delivery guarantees, may be absent, refusable at runtime).
- **Evolution**: per surface that outlives a process (wire protocol, persisted store, schema, public API): its level from [EVOLUTION.md](EVOLUTION.md), its window, and refinements ("readable by stock tools").
- **Reference deployments**: example installations or platforms with this system's share of them.
- **Bounded consumers**: GUIs, TUIs, CLIs, agent-facing output: result limits and partiality signals.
- **Recording guidance**: what components under this file record beyond the standard format (for example syscalls per operation, or billed requests).
- **Conventions**: where design decisions, open questions, ADRs and implementation-choice records go.
- **Validation**: when and how the numbers were last checked, and what triggers a revision.

## Component sections

Open with the entry rule in one line, then:

- **Entities**: count per parent (mean / p50 / p99), size (mean / p99), distribution, source (owned, or the external system), retention.
- **Derived checks**: as above.
- **Provided operations**: each with the parent operation that calls it and, per invocation, the work it does below: calls, reads, writes, syscalls, transfers, temporaries and what sizes them. Lifecycle work (build, rebuild, rescan, archive) is operations too, with its trigger.
- **Stores**: access patterns (key or predicate, order, result size, frequency) and maintenance (inserts, updates, deletes, refreshes, retention).
- **Evolution**: only where a surface here differs from the level its ancestors give it.

## Layout rules

- Omit a column that is n/a for every row in a file.
- A parent's Recording guidance adds to these sections for every file below it.
- Humans own root numbers. Agents may draft component files in a change, with sources marked, for review.
