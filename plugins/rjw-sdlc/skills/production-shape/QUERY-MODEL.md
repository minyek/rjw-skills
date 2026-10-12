# Query model

Any system that answers questions about data it does not hold in full decides where each query is answered. Decide it per dataset and query, from the data and its consumers; a model used elsewhere in the same system is one candidate among these. Choose this axis together with [PROPAGATION.md](PROPAGATION.md).

Decide it at **every tier boundary**: between hosts, and also between a process's memory and its own durable store. The durable store holds the truth for durability; it is not automatically the read path. Crossing into it costs decoding, serialization, locks and sometimes a worker hop, so count those crossings like network calls.

## Shapes

Named by what the nearer copy is for and what it guarantees:

- **Cache** (`k -> v`, for keys fetched): serves key fetches, and is exactly right when access is by key. It cannot answer a query, because it cannot know which keys it is missing.
- **Cached transform** (`k -> f(v)`, same key space): a cache of derived values.
- **Materialized view**: a derived result maintained from the source's changes and rebuildable from it. It answers the query it was built for, or serves as a common subpart that many queries build on. A useful heuristic: when the key differs from the source's (`k' -> f(many v)`, often a singleton or an aggregate), it is a view rather than a cached transform.
- **Partial replica**: serves a subset of arbitrary source queries. Which queries it covers is knowable (**query cover**), and covered queries always come back within stated correctness bounds. It may omit columns or be lightly transformed. Answer covered queries locally; route the rest. A conservative cover check is fine. Every result says whether it is **complete** or **partial**.
- **Full replica**: covers every source query, within the same correctness bounds. Cost is memory or storage and the change stream.
- **Federation**: the query goes to the owner(s) and results are combined. Cost is latency and the owners' availability.

Mixed shapes are normal (a resident partial replica of the hot subset, the cold tail queried in the store) when each query's route is stated. Name the shape you build, and give it the guarantees of that shape.

## Decide from

- **Size** of the dataset and of the subset the queries touch, against the workload.
- **Access pattern**: by key (cache), one fixed question (materialized view), or varied queries (replica).
- **Update frequency** at the source, and so the cost of keeping the copy current.
- **Staleness tolerance** of each consumer.
- **Why a nearer copy exists**: a slow, rate-limited or paid source; offline use; or hot-path reads that should not cross into the durable store. Each reason sets different freshness and eviction rules.

## Resident copies in a process

A copy held in a process's memory (replica, view or cache) is the production shape when:

- it fits the memory budget at the ceiling ([DATA-AND-MEMORY.md](DATA-AND-MEMORY.md));
- the process is the single writer of that data, or the store gives it a change stream ([CONCURRENCY.md](CONCURRENCY.md), [PROPAGATION.md](PROPAGATION.md));
- its startup load fits the startup budget, or it loads progressively and reports partiality until loaded;
- on restart it rebuilds from the durable store (the rebuildable level in [EVOLUTION.md](EVOLUTION.md)).

Where those conditions fail, the store is the read path, with indexes or views it maintains itself.
