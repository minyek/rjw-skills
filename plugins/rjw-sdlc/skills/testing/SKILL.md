---
name: testing
description: Use when writing or changing tests, or implementing a feature or bug fix that needs them, especially for pure logic, data structures, state machines, concurrency or lifecycles where property-based or scenario tests fit.
---

# Testing

Tests specify what the code **should** do, so that they fail when it doesn't. You decide the test design yourself and record it.

Read the reference that matches the work:

- Rust: [hegel.md](hegel.md) (Hegel, the `hegeltest` crate).
- Python: [hypothesis.md](hypothesis.md).
- Running as a flotilla crew (`FLOTILLA_CREW_ID` is set), or working in the flotilla repository: [flotilla.md](flotilla.md), for the decision ledger and stall command, and the repository's scenario engine, fixtures and golden corpus.

In other languages, use the native property library.

## 1. State the behaviour first

Before each assertion, write one or two sentences naming the behaviour or invariant under test. Take them from the **issue, spec, `CONTEXT.md`, an ADR, or a doc comment**. Put them in a comment above the test or in the property's name.

The assertion then checks that stated behaviour. When the code's output differs from the stated behaviour, the test stands and the code is what needs fixing.

## 2. Choose the scale

Pick the smallest shape that fully expresses the behaviour:

- **Function or type property** (the default for pure logic and data structures). Generate inputs for one piece of logic and assert an invariant: round-trip (`decode(encode(x)) == x`), idempotence, ordering or monotonicity, conservation, or "invalid input is rejected". Write an **explicit generator** that spans the interesting space (ranges that cross boundaries, values that collide, every variant of an enum), and say in a comment what space it covers.
- **Scenario or stateful property** (for routing, replication, concurrency and lifecycles). Generate a *sequence of operations* against an in-memory harness and check the invariants after **every** step. When the project already has a generated scenario harness, extend it. This is deterministic simulation testing.
- **Metamorphic or differential relation**, when there's no single right answer to state. Assert how two runs relate: "adding a duplicate changes nothing", "these two routes agree", "re-running is stable".
- **One example test** for simple glue: a thin delegation, a format string, a constant map. Note why one example suffices (`glue: single call-through`).

## 3. Collaborators

Use **real collaborators or in-memory fakes**. Introduce a test double only at a true process or network boundary (a subprocess, a socket, an HTTP endpoint, the git CLI), with a one-line comment saying which boundary it stands in for. Re-record record-and-replay fixtures with the project's record mode, and keep them exactly as recorded.

## 4. Edge cases

Cover, as named cases or through generator coverage: **empty, boundary (min, max, off-by-one), duplicate, error or invalid, and concurrent interleaving** inputs. A stateful property covers interleavings by drawing operation sequences, and a function property covers boundaries by generating across them. Note any case you leave out and why.

## 5. Assert on behaviour

Assert on observable behaviour through the public interface: return values, emitted events, stored state read back through its API, refusals and errors. Assert on an exact serialized layout when the layout **is** the contract, as with a golden corpus of stored records.

## 6. Mutation check (before handing off the change)

Introduce at least **2 targeted mutants** into the code under test: flip a comparison (`<` to `<=`), drop a branch, change a `+` to `-`, remove a `!`. For each one, run the targeted tests for that code, confirm a test **fails**, then revert. When a mutant survives, strengthen the test until it catches it. Record the mutants and results under a **"Mutation check"** heading in the PR body, or in the commit message when the change lands without a PR.

## 7. Bug fixes: fails before, passes after

For a bug fix, also confirm the new test **fails against the unpatched code** and passes with the fix.

## 8. Decide and record

**Decide** the seams, the test scale, the generators and the collaborators yourself, and **record** the decisions where the project records design decisions: the design doc, the ticket, or a decision ledger. Record which seams you chose and why, the invariant each property asserts, and any edge case you left out.

Keep working through design choices. Stop only for a genuine blocker, such as a contradiction in the spec or a dependency you can't provision, and raise it the way your instructions say.

## 9. Every property can fail

Confirm each property **can** fail: the mutation check in §6 shows it directly. Keep generators broad enough that the invariant is genuinely exercised, crossing boundaries and including the interesting inputs.

## Before you hand off the change

- [ ] Each test states its intended behaviour, taken from the spec, issue or docs.
- [ ] The scale was chosen deliberately; stateful and concurrent logic goes through a scenario harness.
- [ ] Generators are explicit and span the interesting space, with their coverage stated.
- [ ] Edge cases (empty, boundary, duplicate, error, interleaving) are named or generated.
- [ ] Real collaborators or fakes are used; any boundary double carries a one-line note.
- [ ] Mutation check done: at least 2 mutants, each caught, reverted, and written up in the PR body or commit message.
- [ ] Bug fix: the test failed before the fix.
- [ ] Decisions are recorded where the project records design decisions.
