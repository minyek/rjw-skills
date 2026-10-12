# Workload model: logs

Relative to the root `WORKLOAD.md`. Numbers here are per parent; absolutes come from the
root's scale drivers and usage. An entry belongs here only if getting its scale wrong would
change a design choice.

## Entities

| Entity | Count per parent (mean / p50 / p99) | Size (mean / p99) | Distribution | Source | Retention |
|---|---|---|---|---|---|
| Log line | per job: 15k / 2k / 500k; truncated at 5M | 120 B | heavy tail | owned | hot: 24 h after job end; cold: 90 days |
| Ingest buffer | per running job: 1 | 256 KB | | owned | job duration |

The ingest buffer is a temporary with its own entry: it outlives each append and its count
is sized by an absolute scale (one per running job, so up to the runner count).

Derived checks (formulas over root quantities; values as of 2026-10):
- Jobs per day = `pushes`/day x `pipeline` x `job` = ~139k at ceiling.
- Cold store = jobs per day x cold retention x lines per job x line size = ~22 TB raw, ~2.2 TB compressed at ceiling.
- Hot store = jobs per day x hot retention x lines per job x line size = ~250 GB at ceiling, against `standard.memory` = 64 GB: on disk, not in memory.
- Ingest buffers = `runners` x buffer size = 75 MB at ceiling.
- `object_store` writes = jobs per day = ~139k/day at ceiling; reads = old-build scrolls.

## Provided operations

**Append** (called by: runner, while a job runs)
- One chunk of up to 64 KB, about 1 per second per running job, into that job's ingest buffer.
- Buffer flushes to the hot store at 256 KB or every 2 s.

**Tail** (called by: `watch_log`)
- From a line offset: snapshot of the requested window, then each new chunk.

**Fetch range** (called by: log viewer scroll and jump)
- Lines by (job, offset range), at most the viewer's 10k-line window.
- Old builds: 1 ranged GET per scroll against object storage.

**Archive** (called by: scheduler's complete job)
- Compresses the job's log and writes it to object storage: 1 PUT per job.
- Removes it from the hot store 24 h after job end.

## Stores

**Hot store** (running and recently finished jobs)

| Access pattern | Key or predicate | Order | Result size | Frequency |
|---|---|---|---|---|
| Tail | job id, from offset | line order | new chunks | per viewer, ~1/s |
| Fetch range | job id, offset range | line order | <= 10k lines | per scroll |

Maintenance: appends at ~1 chunk/s per running job; entries leave 24 h after job end.

**Object storage** (finished jobs)

| Access pattern | Key or predicate | Order | Result size | Frequency |
|---|---|---|---|---|
| Fetch range | job id, offset range | line order | <= 10k lines | per scroll of an old build |

Maintenance: one write per job at archive; deletes at retention (90 days).
