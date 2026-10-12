# Workload model: index

Relative to the root `WORKLOAD.md`. Numbers here are per parent; absolutes come from the
root. An entry belongs here only if getting its scale wrong would change a design choice.

## Entities

| Entity | Count per parent (mean / p50 / p99) | Size (mean / p99) | Distribution | Source | Retention |
|---|---|---|---|---|---|
| Trigram posting | per `file`: 3k / 2k / 50k | 4 B | zipf across trigrams | owned | while the file exists |
| File metadata | per `file`: 1 | 64 B (path id, mtime, size, hash) | | owned | while the file exists |
| Candidate set (query temporary) | per query: 50 / 20 / `repo.files` for a 1 to 2 character query | 4 B | | owned | one query |

The candidate set gets its own entry: it is a temporary, but its worst case is sized by an
absolute scale.

Derived checks (values as of 2026-09):
- Index size = `repo.files` x trigram postings x 4 B = ~24 GB uncompressed, ~5 GB compressed at ceiling, against `laptop.memory` = 500 MB: on disk and mapped, not resident.
- Metadata = `repo.files` x 64 B = 128 MB at ceiling: fits, but is a quarter of the budget.
- Cold build = `repo.files` x mean `file` size at ~1 GB/s, plus `repo.files` stats x 2 µs = ~2 s at target, ~20 s at ceiling: past the 10 s expectation at the ceiling, so results are served from a partial index while building.
- Worst-case verify for a short query = `repo.files` candidates (2M at ceiling): every file opened against `fd.limit` = 256 and 16 GB read, so candidates are capped and verified in a bounded, streaming pass.

## Provided operations

**Query** (called by: `queries`)
- Posting lookups: query length minus 2.
- Intersect postings into the candidate set.
- Verify candidates: per candidate 1 `open`, 1 read of the file (mean 8 KB), 1 `close`.

**Update** (called by: watcher's change batch)
- Per `change`: 1 `stat`; if mtime or size moved, 1 read and re-tokenise, then replace that file's postings.

**Build** (called by: `opens`, and rebuild on index format change)
- Walk the tree: `repo.files` stats, `repo.dirs` directory reads.
- Read every file once; write postings.

## Stores

**Index** (on disk, memory-mapped)

| Access pattern | Key or predicate | Order | Result size | Frequency |
|---|---|---|---|---|
| Posting lookup | trigram | file id | postings per trigram (zipf; common trigrams hit most files) | per query, length minus 2 |
| Change detection | path id | | 1 | per `change` |

Maintenance: replace a file's postings per `change`; full rebuild per repo per index format
version (about one tool upgrade in four), or on detected corruption.
