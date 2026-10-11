# Data and memory

Choose structures from the operations in the workload note. Where there's one, there's many: design for the collection, not the single item.

- **Cost every operation.** For each read, write, update and query: time complexity at the ceiling, update cost, and memory per entry. A structure is right when its worst common operation is cheap, not its first one.
- **Shape follows the query.** If the hot query is "by convoy" or "by label", the structure is indexed by convoy or label. Scanning a whole kind and filtering is a choice that needs a cardinality bound to justify it.
- **Pack and place.** Decide where each piece of information lives for locality: next to the data it is read with, in the process that reads it most. Pack hot fields densely; keep cold or large fields out of the hot path (interning, IDs instead of copies, columnar layouts, arenas).
- **Walk the candidates** (see the evidence rule in [SKILL.md](SKILL.md)). What survives is the choice.
- **Custom structures are in bounds.** A purpose-built index, ring, trie or packed table is justified by the candidate walk. Reaching past the standard library is ordinary engineering, not gold-plating.
- **Allocate by lifetime.** Group data that dies together (arenas, nested lifetimes) and release a lifetime in one operation; stable addresses let other structures refer into it.
- **Share instead of copy.** One owned copy, shared by reference (`Arc`, borrowed views, `Bytes`, slices) to every consumer. A clone is a decision with a size.
- **Stream instead of materialise.** Process results as they arrive (iterators, streams, incremental parsing) and collect only what the consumer must hold at once.
- **Keep the representation the hot path needs.** Decode to the fields that are read, not a generic tree or the whole resource; keep wire bytes and decode on access when that is cheaper (see [PROTOCOLS.md](PROTOCOLS.md)).
- **Memory is a budget.** State the resident size at the ceiling and check it fits the machine and its other tenants. Everything resident has a lifetime: an eviction or retention rule, so memory holds at steady state.
