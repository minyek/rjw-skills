# Operation lowering

**Operation lowering** is how intent becomes concrete operations: who decides how an operation executes, when, and with what knowledge. Choose the level on purpose, and let the best backend lower its own part: push operations down to whatever can execute them well, with adapters for less capable ones. This applies to storage, queues, kernel operations, renderers, workflows, anything with more than one way to execute.

The levels form a spectrum, not strict categories:

- **i. Fixed** (point solution): the concrete implementation is used directly. Right when the choices are known and few, and you can pick between them well.
- **ii. Uniform** (generic): one algorithm (a template method) treats every backend the same. Sometimes right, and always carrying an **expiry date**: the day a backend can do better than the template permits (an index, a native filter, a server-side selector). Name that date when you choose it.
- **iii. Interpreted** (adaptive): operations are expressed as data (a small algebra, the free-monad shape) and each backend interprets what it can natively. A simple compiler lowers the rest onto dumb, in-memory-like or less capable backends. Minimum contract: for each operation the backend answers **exact** (fully handled), **inexact** (narrowed, the engine re-checks) or **unsupported** (the engine does it), as DataFusion's filter pushdown does.
- **iv. Planned**: query planning and cost-based optimisation choose how to execute.
- **v. Replanned**: plan, execute 1..n steps or time units, measure error, replan or backtrack (MCTS, MPC).
- **vi. Agentic**: an agent decides. Easy to start, highest cost and error rate. Parts lower to more predictable levels as patterns settle, to improve the system rather than to eliminate the agent.

Prefer **generalization over abstraction**: a vocabulary wide enough to carry every backend's full capability, rather than a layer that passes only the common subset. Independent per-item fetches batch into one backend call (the DataLoader / Haxl shape).

Every level ends in level i: levels iv to vi often emit it on the fly. Levels iv and v are rarely needed and never "too complex to consider". The default question is whether level iii costs about the same as level ii here; it often does, and it keeps the best backends uncrippled.

Match the seam to the set. A closed enum is right for a genuinely closed set (states, protocol variants, a fixed list of formats). Where the set of backends or implementations can grow, the seam is open: a trait or an operation algebra that a new backend implements without editing the core.
