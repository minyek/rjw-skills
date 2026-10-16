# skill-fixes-and-fork-setup — design

Slug: skill-fixes-and-fork-setup (ticketless). Requirements: [skill-fixes-and-fork-setup-requirements.md](skill-fixes-and-fork-setup-requirements.md).

## Problem

A review of the rjw-sdlc skills against the user's own instructions and skills found thirteen candidates (report:
[2026-10-16-skill-conflict-review.md](../../reports/2026-10-16-skill-conflict-review.md)). Baseline runs of the current
text, three fresh agents per item, reproduced two:

- **production-shape record location.** With no `WORKLOAD.md` and no convention in the agent instructions, agents
  stopped mid-implementation to ask where records go, or created `docs/implementation-choices/` beside an existing
  `docs/decisions/`. 3 of 3 runs failed.
- **testing in Java.** "Use the native property library" sent every run to jqwik. jqwik's user guide (1.10.2,
  "Anti-AI Usage Clause") says the project is not meant to be used by AI coding agents. 3 of 3 runs failed.

The user also approved two things:
- widening `run_cli`'s 10-second subprocess timeout in the pr-shepherd tests to a deadlock guard;
- keeping this fork's own changes on `main`.

Keeping changes on `main` needs a repository `CLAUDE.md` saying how upstream is merged and how the plugin is
installed, and a `.claude/delivery.env` for the gate.

## Approach

1. **production-shape, Project conventions.** The location comes from the root `WORKLOAD.md` or the agent
   instructions. When neither names one, the record goes with the project's existing design records instead of a
   new directory, and the location question waits for the next point the instructions allow one. The
   implementation-choices bullet names `docs/implementation-choices/` only for a project with no design records.
2. **testing, reference list.** Java is named as the exception to "use the native property library". The recipe is
   JUnit 5 `@ParameterizedTest` fed by a `@MethodSource` drawing from a fixed-seed `java.util.Random`, with the seed
   in the failure message.
3. **pr-shepherd tests.** `run_cli`'s timeout becomes a named deadlock-guard constant of 300 seconds.
4. **Fork setup.** `CLAUDE.md` covers:
   - what `main` holds;
   - the upstream sync procedure, the repository's one exception to `/sqmerge`'s squash;
   - how upstream PRs are cut so that fork-only files stay out;
   - the gate;
   - how the plugin is installed and updated.

   `.claude/delivery.env` configures `/gate`. `docs/decisions/` records the fork layout and the Java decision.
5. **Release.** rjw-sdlc 1.8.0 in both manifests. The marketplace gains the top-level description its validator
   asks for (R8). The report and its artefacts record the evidence.

**Green runs.** Both skill edits were checked with the same scenarios after the change: 3 of 3 runs passed for each.

**What the implementation copies.** It applies exactly the two tested `SKILL.md` hunks; the tested files are kept
as artefacts.
- **Don't copy the rest.** The tested copies were taken from the installed 1.7.0 cache. That cache was built from
  an uncommitted tree, so its `testing/hypothesis.md` has a sentence that `main` deliberately removed.
- **Don't copy anything else.** No other file from the tested copies is part of this change.

The wording of both edits is project-neutral, so it can go upstream unchanged; the patch context may need resolving
against upstream's text (`CLAUDE.md`, "Contributing upstream").

## Earlier decisions

- **Record locations.** [claude-code-compatibility.md](../../reports/claude-code-compatibility.md) deferred them to
  `WORKLOAD.md` Conventions. R1 supersedes that: no repository the user works in has a `WORKLOAD.md`, so agents fell
  through to asking or to the default directory.
- **jqwik.** The earlier change withdrew a jqwik reference
  ([requirements R10](../claude-code-compat/claude-code-compat-requirements.md)) and left Java to the general
  rule. R2 follows that change's reason (the maintainers' clause) and reverses its consequence: the general rule is
  what leads agents to jqwik.
- **Neutral wording.** The earlier design's rule ("no user layout in reusable text") holds. R1 names no directory
  of the user's.

## Options considered

- **Where the fixes live.**
  - The options: the user's own instructions (an override table, as for superpowers), or the fork.
  - The choice: both failures would hit any user of the skills, and a fix in the skill text sits where the agent
    acts, so both fixes go in the fork.
  - The items about the user's own policies would have gone in `~/.claude`. Their baselines showed no failure, so
    none is needed.
- **Java approach.**
  - jqwik anyway: rejected, against the maintainers' stated wish.
  - An unmaintained QuickCheck port: rejected (inferred: no maintained alternative is known).
  - Plain JUnit 5 with a seeded generator: chosen. It adds no dependency and is reproducible, at the cost of
    automatic shrinking.
- **Fork layout.**
  - The options: a long-lived `andy-changes` branch, or `main` as the fork's version.
  - The choice: `main`. It keeps `/worktree-new` and `/sqmerge` working unchanged and gives the marketplace a stable
    source. Merge difficulty is the same either way.
  - The one cost: an upstream sync must not be squashed, so syncs get their own documented landing.
- **Plugin source.**
  - The options: the GitHub fork, or the main checkout as a directory source.
  - The choice: GitHub. It installs only merged, pushed work and never another session's uncommitted edits.
  - The cost: an update needs the push first, and `/sqmerge` pushes anyway.
