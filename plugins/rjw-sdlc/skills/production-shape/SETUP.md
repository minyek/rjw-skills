# Setting up a workload reference

Run this when the project has no workload reference. Humans own the numbers: you propose, the user confirms.

1. **Look for one.** Check `docs/agents/workloads.md`, and for a link to a workload reference from `CODING_STANDARDS.md`, `AGENTS.md` or `CLAUDE.md`. Done when you have found one (stop here and use it) or confirmed there is none.
2. **In an autonomous crew, stop at the gap.** Record the missing reference in the decision ledger under "If asking were free", size for the system limit, and continue the work. Setup needs a human.
3. **Draft the scales with the user.** Take the entities from the project's domain glossary (`CONTEXT.md`) and the code's main collections. For each, propose a count and rate now (measured from real data where you can), a target and a ceiling, and say where each number came from. Done when the user has confirmed or corrected every row.
4. **Write `docs/agents/workloads.md`** from the template below.
5. **Link it** with one bullet in `CODING_STANDARDS.md`; where there is none, in `AGENTS.md`, then `CLAUDE.md`. Ask before creating a new file for the link. The bullet: "Data-touching design and review: see [workload reference](docs/agents/workloads.md)."

Done when the file exists, the user has confirmed its numbers, and one standards or agents file links it.

## Template

```markdown
# Workload reference

Design and review data-touching work with the `production-shape` skill: production shape,
profiler test, workload note, bounded consumer, snapshot then deltas, query cover,
operation lowering, single writer, steady state, match the defence to the boundary.

## Scales

The design holds at the target. The ceiling sets limits, seams and expiry conditions.

| Entity | Now | Target | Ceiling | Rate | Source |
|---|---|---|---|---|---|
| <entity> | <count> | <count> | <count> | <per second / per day> | <measured / estimated, date> |

## Machines

<the hosts this runs on: cores, memory, disk, network; what else shares them>

## Bounded consumers

<GUIs, TUIs, CLIs and agent-facing outputs, with their result limits>

## Validation

<how and when these numbers were last checked against load tests or production>
```
