# Setting up a workload reference

Run this when the project has no workload reference. Humans own the numbers: you propose, the user confirms.

1. **Look for one.** Check `docs/agents/workloads.md`, and for a link to a workload reference from `CODING_STANDARDS.md`, `AGENTS.md` or `CLAUDE.md`. Done when you have found one (stop here and use it) or confirmed there is none.
2. **When nobody can be asked, stop at the gap.** In an autonomous run, record the missing reference where the project records open questions, size for the largest plausible deployment, and continue the work. Setup needs a human.
3. **Draft the maturity and scales with the user.** Agree the project's maturity (prototype, personal tool, internal, production) first: it sets how high the ceiling goes. Take the entities from the project's domain glossary (`CONTEXT.md`) and the code's main collections. For each, propose a count and rate now (measured from real data where you can), a target and a ceiling, and say where each number came from. Then agree one or more reference deployments (an example host, a typical installation): the numbers each design is checked against, not a promise about every deployment. Done when the user has confirmed or corrected every row.
4. **Agree the conventions.** Ask where the project records design decisions, open questions, ADRs and implementation-choice records, unless its agent instructions already say.
5. **Write `docs/agents/workloads.md`** from the template below.
6. **Link it** with one bullet in `CODING_STANDARDS.md`; where there is none, in `AGENTS.md`, then `CLAUDE.md`. Ask before creating a new file for the link. The bullet: "Data-touching design and review: see [workload reference](docs/agents/workloads.md)."

Done when the file exists, the user has confirmed its numbers and conventions, and one standards or agents file links it.

## Template

```markdown
# Workload reference

Design and review data-touching work with the `production-shape` skill: production shape,
profiler test, naive shape, workload note, candidate walk, bounded consumer, snapshot then
deltas, query cover, operation lowering, single writer, steady state, match the defence to
the boundary.

## Maturity

<prototype / personal tool / internal / production; expected lifespan>

## Scales

The design holds at the target. The ceiling sets limits, seams and expiry conditions.

| Entity | Now | Target | Ceiling | Rate | Source |
|---|---|---|---|---|---|
| <entity> | <count> | <count> | <count> | <per second / per day> | <measured / estimated, date> |

## Reference deployments

<example installations designs are checked against: cores, memory, disk, network, co-tenants>

## Bounded consumers

<GUIs, TUIs, CLIs and agent-facing outputs, with their result limits>

## Conventions

- Design decisions: <decision log / PR description / ...>
- Open questions: <where gaps are recorded when nobody can be asked>
- ADRs: <path and format>
- Implementation choices: <docs/implementation-choices/ or elsewhere>

## Validation

<how and when these numbers were last checked against load tests or production>
```
