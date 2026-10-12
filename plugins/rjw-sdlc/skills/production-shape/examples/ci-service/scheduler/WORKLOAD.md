# Workload model: scheduler

Relative to the root `WORKLOAD.md`. Numbers here are per parent; absolutes come from the
root's scale drivers and usage. An entry belongs here only if getting its scale wrong would
change a design choice.

## Entities

| Entity | Count per parent (mean / p50 / p99) | Size (mean / p99) | Distribution | Source | Retention |
|---|---|---|---|---|---|
| Pipeline config | per repo: 1 | 8 KB | changes ~1/week per repo | external: forge | cached; refetch on push to config path |

Derived checks (formulas over root quantities; values as of 2026-10):
- Job rows retained = `pushes`/day x `pipeline` x `job` x `job` retention = ~12.5M at ceiling.
- Jobs ready at once = `bot_burst` x `job` = ~27k at ceiling, against `runners` = 300 at ceiling.
- Forge config reads if uncached = `pushes` peak/s x 3,600 = 7,200/hour at ceiling, against `forge.budget` = 5,000/hour.

## Provided operations

**Create pipeline** (called by: `push`, `bot_day`)
- 1 read of the repo's pipeline config (cached; forge only when the config path changed).
- Builds the job graph in memory: a temporary sized by jobs per pipeline, rolled up here.
- Inserts jobs-per-pipeline job rows in one transaction.

**Claim job** (called by: `claim`)
- 1 read: oldest ready job whose labels the runner satisfies.
- 1 update: ready to running.

**Complete job** (called by: runner, at job end)
- 1 update: running to done.
- Per dependent job (p50 1, p99 20): 1 update, blocked to ready when its last dependency completes.

## Stores

**Jobs**

| Access pattern | Key or predicate | Order | Result size | Frequency |
|---|---|---|---|---|
| Claim | state = ready, labels match runner | enqueue time | 1 | per claim |
| Repo build list | repo id | newest first | 50 per page | per list call |

Maintenance: 1 insert and ~3 state updates per job; deletes at retention (90 days). Writes
outnumber reads roughly 4:1 outside page views.
