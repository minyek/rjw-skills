# Workload model: kernels

Relative to the root `WORKLOAD.md`. Numbers here are per parent; absolutes come from the
root. An entry belongs here only if getting its scale wrong would change a design choice.

## Entities

| Entity | Count per parent (mean / p50 / p99) | Size (mean / p99) | Distribution | Source | Retention |
|---|---|---|---|---|---|
| Kernel variant | per op: one per ISA and backend, 3 / 3 / 6 | | | owned | build time |

Derived checks (values as of 2026-08):
- Per-op CPU budget = 1 / `fps` / `graph.ops` = 16.7 ms / 12 = ~1.4 ms per op per frame at supported.
- Per-pixel budget for a single-pass op = 1.4 ms / `frame.pixels` 8.3M = ~0.17 ns per pixel at supported. Kernel benchmarks are checked against this; a scalar loop does not meet it, so each op ships SIMD or GPU variants.

## Provided operations

**Execute** (called by: graph `Run`)
- Per op per frame: one pass over `frame.pixels` (memory-bound ops) or a tile walk (filters
  with neighbourhoods); output written to a pooled buffer.

**Select variant** (called by: library load)
- Pick the best kernel per op for the detected `cpu.simd` and `gpu`; hand the planner a cost
  estimate per variant.
