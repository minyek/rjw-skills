# claude-code-compat — requirements

Slug: claude-code-compat (ticketless). Design: [claude-code-compat-design.md](claude-code-compat-design.md).

Background: a review of the rjw-sdlc skills found that they assume flotilla crews (autonomous push, posting,
GitHub Issues, the `flotilla` CLI). The user runs only Claude Code, under rules that forbid pushing, require
sign-off for outward-facing actions, use Jira, and forbid hard-coded `/tmp`. The user approved the triaged
review; these requirements restate it as testable clauses. Every edit must stay generic, so the author can
take it upstream.

| ID | Requirement | Verified by |
|---|---|---|
| R1 | pr-shepherd: when the agent's instructions forbid pushing or a push is denied, a cycle ends after committing with the commits-ahead count and a request to push; flotilla and push-permitted runs are unchanged. | Behaviour scenario (control vs edited skill) |
| R2 | pr-shepherd: when instructions require sign-off for outward-facing actions and posting is not authorised for the PR, all replies, comments, acks and issues of a cycle are drafted and presented once before posting. | Behaviour scenario |
| R3 | pr-shepherd: follow-ups go to the tracker the project's instructions name (default GitHub Issues); when deferred findings are won't-do unless asked, they are listed and the user asked once. | Review of SKILL.md §5 |
| R4 | pr-shepherd: every invocation in SKILL.md runs the helper through `uv run --script`. | Metadata test (grep) |
| R5 | Every SKILL.md description starts "Use when", states triggers only, and is at most 500 characters; every `name` matches its directory; relative links resolve. | `test_skill_metadata.py` |
| R6 | pr-shepherd helper: `PR_SHEPHERD_CACHE_DIR` sets the cache directory; otherwise it is `pr_shepherd_cache` under `tempfile.gettempdir()`; no literal `/tmp` in the script. | Unit tests |
| R7 | `WaitPacingTest` passes deterministically: no fake sleep or clock reaches `subprocess`. | 20 consecutive runs, under parallel load, all green (before: every run had 1–3 failures) |
| R8 | triage-issues: description names GitHub Issues; writes follow one approval of a triage table unless the user asked to apply directly; §7 proposes, does not commit, the label table. | Review of SKILL.md |
| R9 | consistency-review: sources come from the project's agent instructions with the current defaults; code search is language-agnostic; no "grill" or flotilla role names; tracker drift repair respects sign-off rules. | Review + metadata test (grep) |
| R10 | testing: the SKILL.md body names no project, issue number or flotilla command; flotilla specifics live in `flotilla.md`; `hypothesis.md` and `jqwik.md` exist with runnable-shaped examples matching their libraries' documented APIs; mutation checks run targeted tests and are recorded in the PR body or the commit message. | Review + metadata test (grep); Hypothesis example executed |
| R11 | production-shape: timing evidence belongs to a benchmark or performance suite, never functional tests. | Review |
| R12 | Plugin version is 1.7.0 in both manifests. | Metadata test |
| R13 | `docs/reports/claude-code-compatibility.md` justifies every change for the skills' author. | Review against this table |

Edge cases: a skill run under flotilla must behave as before (R1, R2 conditionals key on instructions, not on
the harness); a project with no named tracker or decision location falls back to the original defaults (R3, R9).

Options considered: see the design's "Approach" section.

## Changes during implementation

Each change below corrects a clause whose wording the evidence disproved while its intent stays met.

- **R1, R2, R3 withdrawn.** Baseline scenarios ran the original pr-shepherd skill in fresh agents carrying the
  user's instructions (3 runs). Every run refused to push, drafted replies, acks and the follow-up issue, and asked
  once before posting. The user's instructions already override the skill, and the process-guard hook denies
  `git push`. Guidance written for a failure that does not occur adds words without changing behaviour, so the
  skill text keeps the author's flow.
- **R8 narrowed to the description.** The same baseline for triage-issues (3 runs) wrote nothing before one
  approval and never edited CLAUDE.md unasked. Only the description change remains: it decides whether the skill
  loads, which instructions cannot fix.
- **R9: drift-repair sign-off withdrawn.** The triage-issues baseline is the same situation, an agent about to
  write to a shared tracker, and all 3 runs asked once before writing. The rest of R9 is met.
- **R5 extends to production-shape**, whose description ended with a workflow summary; that sentence is removed.
- **R10: jqwik reference withdrawn.** The jqwik user guide (1.10.2) states that the project is not meant to be
  used by AI coding agents. A reference steering agents to it would go against the maintainers' stated wishes, so
  Java falls back to the skill's general guidance. `flotilla.md` keys crew commands on `FLOTILLA_CREW_ID` (any
  repository) and repository specifics on working in flotilla, per the spec review. `hegel.md` stays as the
  author's Rust reference.
- **R12: the test checks that the manifests agree**, not a literal version, so upstream releases do not break it.
  Both manifests are at 1.7.0.
- **R6 note.** Outside a managed job `TMPDIR` may be unset, so the default is the system temp directory; a user
  who keeps scratch elsewhere sets `PR_SHEPHERD_CACHE_DIR` in their own environment.
- **Deferred.** `run_cli`'s 10-second subprocess timeout in the pr-shepherd tests is a wall-clock limit. It did
  not trip in 20 loaded runs. Widening it needs the user's test-change approval, so it is reported, not changed.
