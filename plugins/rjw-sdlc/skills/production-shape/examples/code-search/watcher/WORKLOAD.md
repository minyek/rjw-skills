# Workload model: watcher

Relative to the root `WORKLOAD.md`. Numbers here are per parent; absolutes come from the
root. An entry belongs here only if getting its scale wrong would change a design choice.

## Entities

| Entity | Count per parent (mean / p50 / p99) | Size (mean / p99) | Distribution | Source | Retention |
|---|---|---|---|---|---|
| Watch (Linux) | per directory: 1 | ~1 KB kernel memory | | external: `fs.watch` | while the repo is open |
| Raw event | per `change`: 3 / 2 / 6 | | editors write a temp file then rename | external: `fs.watch` | coalescing window |

Derived checks (values as of 2026-09):
- Watches = `repos.open` x `repo.dirs` = 10 x 200k = 2M at ceiling, against `inotify.max_user_watches` (often 8,192, shared): per-directory watches do not scale; use a recursive mechanism (fanotify, FSEvents) or fall back to scanning.
- Raw events on `branch_switch` = `branch_switch.files` x 3 = 600k at ceiling, within seconds: expect overflow, so overflow handling is the main path at the ceiling, not an edge case.

## Provided operations

**Watch** (called by: `opens`)
- Linux: 1 watch per directory (`repo.dirs`). macOS: 1 stream per repo root.

**Coalesce and emit** (called by: OS events)
- Collect raw events for 100 ms, dedupe by path, emit one change batch to the index.

**Rescan** (called by: overflow, or on resume after sleep)
- Walk the affected subtree: 1 `stat` per file; emit files whose mtime or size differ from
  the index's metadata. This is the resync path: compare against metadata, then resume
  events.
