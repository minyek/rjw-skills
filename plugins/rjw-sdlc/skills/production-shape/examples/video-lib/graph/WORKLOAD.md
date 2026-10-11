# Workload model: graph (planning and placement)

Relative to the root `WORKLOAD.md`. Numbers here are per parent; absolutes come from the
root. An entry belongs here only if getting its scale wrong would change a design choice.

## Entities

| Entity | Count per parent (mean / p50 / p99) | Size (mean / p99) | Distribution | Source | Retention |
|---|---|---|---|---|---|
| Intermediate frame buffer | per pipeline: pipeline depth x stages that change format, ~3 / 2 / 8 | `frame` size | | owned, pooled | reused across frames |
| Placement candidates | per `build`: backends per op, 2 to 4 | | | owned | one `build` |

Intermediate buffers are temporaries with their own entry: they are shared through a pool
and sized by absolute scales (`frame.pixels` x `streams`).

Derived checks (values as of 2026-08):
- Copy cost of one 4K RGBA frame each way = `frame.pixels` x 4 B x `fps` = ~2 GB/s per stream per crossing at supported; x `streams` 8 = 16 GB/s at supported, most of `host_device_link`. One CPU round trip mid-graph per frame doubles that, so the plan keeps a frame resident on one side for the whole graph wherever the ops allow.
- Buffer pool = `streams` x 3 buffers x `frame` size = 8 x 3 x 33 MB = ~800 MB at supported (4K RGBA), against `laptop_unified` 1 GB: pool by format, release on reconfigure, cap and report.
- Plan search = backends ^ `graph.ops`: 4 ^ 40 at ceiling, so placement is cost-based with pruning on residency, not exhaustive.

## Provided operations

**Plan** (called by: `build`)
- Choose a backend per op from what the platform supports, minimising transfers across
  `host_device_link` plus estimated op cost; fuse adjacent ops on the same backend.
- Fall back when `hw_codec` refuses a session: replan that op onto GPU or CPU.

**Run** (called by: `process`)
- Per frame: `graph.ops` kernel launches (fewer after fusion), crossings as planned.
