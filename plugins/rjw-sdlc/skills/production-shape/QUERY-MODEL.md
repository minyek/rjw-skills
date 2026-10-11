# Query model

Any system that answers questions about data it does not hold in full decides where each query is answered. Decide it per dataset and query, from the data and its consumers; a model used elsewhere in the same system is one candidate among these. Choose this axis together with [PROPAGATION.md](PROPAGATION.md).

The options, by what the local site knows:

- **Full replication**: the whole dataset is local. Any query is answerable locally; cost is storage and the change stream.
- **Partial replication**: a defined subset is local, and the site can compute **query cover**: whether a given query is fully answerable from what it holds. Answer covered queries locally; route the rest. A conservative cover check is fine. Every result says whether it is **complete** or **partial**, so consumers never mistake a partial answer for the whole.
- **Cache**: the site knows only which keys it holds. It serves key fetches; it cannot answer a query, because it cannot know what it is missing.
- **Federation**: the query goes to the owner(s) and results are combined. Cost is latency and the owners' availability.

Decide from:

- **Size** of the dataset and of the subset the queries touch, against the workload.
- **Update frequency** at the source, and so the cost of keeping a replica current.
- **Staleness tolerance** of each consumer.
- **Why a nearer copy exists**: offline use, a slow source, a rate-limited or budgeted source, a source that costs money per call. Each reason sets different freshness and eviction rules.

Mixed models are normal (replicate the hot subset, federate the tail) when each query's route is stated. Name the model you are building: a TTL cache in front of a query is a cache, and answers as one.
