# rjw-sdlc under Claude Code: changes and why

Andy Wright, 2026-10-13, revised 2026-10-16. Applies to rjw-sdlc 1.6.3 → 1.7.0.

## Context

I run these skills in plain Claude Code, not in flotilla. My agent instructions forbid pushing, require sign-off
before anything visible outside the machine, track work in Jira, keep decision records under `docs/decisions/`,
and forbid hard-coded `/tmp`. I reviewed the five skills for how they behave in that setup and changed what
needed it. Each change is keyed to something the agent can observe: its instructions, `FLOTILLA_CREW_ID`, or the
repository it is in. Under flotilla the skills behave as before, with these exceptions: the mutation check runs the targeted tests
for each mutant rather than the whole suite; pr-shepherd's cache follows `TMPDIR` when it is set; consistency-review's
code search is `git grep` over every tracked path rather than `crates/` and `src/` Rust files: it drops paths containing
"test" where it used to drop lines containing "test", and it no longer sees untracked files; and testing's crew commands
(decision ledger, `crew stall`, the PR-body mutation record) and its scenario-engine guidance sit in `flotilla.md`,
reached from a pointer in the skill body that keys on `FLOTILLA_CREW_ID`. Every change below should be safe to take upstream.

## Changes

### pr-shepherd

| Change | Why |
|---|---|
| **Flaky pacing tests fixed.** `WaitPacingTest` now replaces the helper's own `time` global with a fake clock, instead of patching `sleep` and `time` on the shared `time` module. | CPython's `subprocess` waits for a child through `time.sleep` (a 1 ms backoff that doubles up to 50 ms). With the module patched, those waits landed in `self.sleeps` and advanced the fake clock whenever the fake `gh` outlived `communicate()`. The suite failed 1–3 pacing tests on every run on Python 3.12, 3.13 and 3.14. Under parallel load: 10 of 10 runs failed before the fix, 20 of 20 passed after. |
| **`PR_SHEPHERD_CACHE_DIR`.** The cache directory comes from this variable, else `pr_shepherd_cache` under `tempfile.gettempdir()`. Two tests pin both cases through the CLI. | The cache was fixed at `/tmp/pr_shepherd_cache`. Hosts that keep scratch off `/tmp`, or give each job its own `TMPDIR`, could not move it. The test harness now gives each test its own cache; before, every CLI test shared the machine's `/tmp` cache, including the learned CI-duration file. |
| **Helper runs through `uv run --script`** in every example. | It is what the shebang does anyway. The explicit form works when an installer drops the executable bit, and it matches `uv run` permission allow-lists, so the agent is not prompted for each call. |
| **Description states when to use the skill** ("Use when a GitHub pull request has review comments to answer, failing or pending CI checks, or merge conflicts…"). | Claude Code decides whether to load a skill from its description alone. A description that summarises the workflow invites the agent to follow the summary and skip the body. |

### consistency-review

| Change | Why |
|---|---|
| The search uses the decision-record, doc and tracker locations the agent's instructions name. `docs/adr/`, `CONTEXT.md`/`docs/` and GitHub Issues remain the defaults. | In my repositories decisions live in `docs/decisions/` and rulings in Jira, so the old search reported absence claims as standing after looking in places that do not exist. That is exactly the failure the skill exists to prevent. |
| Code search is `git grep -n "<TypeOrConst>" -- ':!*test*'`. | `grep … crates/ src/ --include="*.rs"` finds nothing outside Rust. |
| "Grill" becomes "a decision session"; the Notes paragraph describes a standing consistency reviewer without naming flotilla's role. | An agent without the flotilla vocabulary cannot act on "do not grill". |
| Description in trigger form. | As for pr-shepherd. |

§4 still repairs board drift in the same pass. In my baseline runs an agent about to write to a shared tracker
asked first when its instructions required that, so the skill needs no extra branch for it.

### triage-issues

| Change | Why |
|---|---|
| The description names GitHub Issues ("not Jira or other trackers"). | Without it the skill loads for any issue triage, and its `gh` commands do not apply to other trackers. |

### testing

| Change | Why |
|---|---|
| The body is project-neutral. `flotilla.md` holds the flotilla material in two parts: crew commands (decision ledger, `crew stall`), keyed on `FLOTILLA_CREW_ID` in any repository; and the flotilla repository's scenario engine, `REPLAY=record` fixtures and golden corpus. | Outside flotilla, the skill pointed agents at `crates/flotilla-daemon/...`, issue numbers and `flotilla` commands that do not exist. The two keys keep a crew in another repository recording decisions. |
| The skill opens with a reference list: `hegel.md` for any Rust project, `hypothesis.md` for Python, `flotilla.md` under flotilla, and the native property library elsewhere. | One entry point per language; `hegel.md` was already the de facto Rust reference. |
| Smaller wording: behaviour comments are "a comment above the test" (no `//`), and a genuine blocker is raised "the way your instructions say". | The `//` syntax and the stall command were Rust- and flotilla-specific. |
| New `hypothesis.md` for Python, in the same shape as `hegel.md`. Its examples were run: the stateful one shrank a planted bug to `delete(b)`, `put(b, 0)`. | Hypothesis is the native library for the Python half of my work. |
| Decisions are recorded "where the project records design decisions: the design doc, the ticket, or a decision ledger". | Same intent, without the flotilla CLI. |
| Mutation check: run the *targeted* tests per mutant; record the result in the PR body, or the commit message when there is no PR. | Running the whole suite per mutant is expensive. My changes land through a local squash-merge with no PR. |
| Description in trigger form; the checklist is titled "Before you hand off the change". | As above. |

### production-shape

| Change | Why |
|---|---|
| One sentence in Evidence: keep timing evidence in a benchmark or performance suite, never in functional tests. | Timing assertions in a functional suite fail on loaded machines and look like regressions. |
| The description drops its last sentence ("Chooses each design axis…"). | It summarised the workflow; the rest already states when to use the skill. |

The skill was otherwise already general-purpose. It defers record locations to `WORKLOAD.md` Conventions, which is
where I set my `docs/decisions/` paths.

### Plugin

- `plugins/rjw-sdlc/tests/test_skill_metadata.py` checks every skill has valid frontmatter, a `name` matching its
  directory, a "Use when" description of at most 500 characters, and relative links that resolve. It also checks
  the helper invocation, that the neutral skill bodies stay neutral, and that the two manifests agree on the
  version.
- Version 1.7.0 in both manifests.

## What I deliberately left alone

- **The push, posting and issue-filing flow in pr-shepherd, the write flow in triage-issues, and drift repair in
  consistency-review.** I expected to
  add "stop and ask" branches for users who forbid pushing or require sign-off. I first ran each original skill
  in fresh Claude Code agents carrying my instructions, three times each. Every run refused to push, drafted the
  replies, labels and follow-up issue, and asked once before writing anything. User instructions already outrank
  skills in Claude Code, so a branch for that case would add text without changing behaviour. Your autonomous
  flow stays as written.
- **`hegel.md`.** It is your Rust reference and is accurate for flotilla.
- **A Java (jqwik) reference.** I planned one, but jqwik's user guide (1.10.2) states that the project is not
  meant to be used by AI coding agents, so I did not write an agent reference for it.

## Noted, not changed

`CliHarness.run_cli` passes `timeout=10` to the helper subprocess. That is a wall-clock limit inside a functional
test and could trip on a heavily loaded machine. It did not trip in 20 loaded runs. A deadlock-guard value (for
example 300 s) would remove the risk; I left it for you to decide.
