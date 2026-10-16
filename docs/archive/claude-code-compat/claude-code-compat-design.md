# claude-code-compat — design

Slug: claude-code-compat (ticketless). Requirements: [claude-code-compat-requirements.md](claude-code-compat-requirements.md).

Superseded in part: the requirements' "Changes during implementation" section withdraws the push and sign-off branches, the follow-up tracker branch, the triage write flow, the drift-repair sign-off and `jqwik.md`; where this document still describes them, that section wins.

## Problem

The rjw-sdlc skills were written for flotilla crews: autonomous agents that push, post to GitHub, file GitHub
issues and record decisions through the `flotilla` CLI. A Claude Code user whose rules forbid pushing, require
sign-off for outward-facing actions, track work in Jira and keep decision records under `docs/decisions/` hits
dead ends (a hook denies `git push` mid-loop), unwanted side effects (automatic issue filing) and searches of
directories that do not exist (`docs/adr/`, `crates/*.rs`).

## Approach: conditionals on observable predicates, not a fork of conventions

Each skill keeps its current behaviour where its predicate holds (flotilla crew, no restricting instructions)
and gains a branch keyed to what the agent can observe: its own instructions, a hook denial, the tracker the
project names. No user-specific path, tracker or project name enters a skill body. The user's conventions stay
in the user's own instructions, which the skills now defer to. This keeps every edit offerable upstream.

Rejected: rewriting the skills around the user's conventions (Jira, `docs/decisions/`). It would fork the skills
permanently and put one user's layout into reusable content. Rejected: leaving the skills alone and relying on
instruction precedence. Precedence cannot change the script's `/tmp` constant, and a skill whose loop says
"push" collides with the push hook on every cycle.

## Changes by skill

### pr-shepherd
- **Push.** After committing, when the agent's instructions forbid pushing or a push is denied, the cycle ends:
  report the commits ahead of the remote, ask the user to push, and stop. The next invocation starts the next
  cycle (the skill already says to re-run it per review cycle). Under flotilla and standalone-with-push nothing
  changes.
- **Outward-facing writes.** When the agent's instructions require sign-off for outward-facing actions and the
  user has not authorised posting on this PR, draft every reply, comment, `ack` and follow-up issue for the
  cycle, present them once, and post after approval.
- **Follow-up issues.** File in the tracker the project's instructions name (GitHub Issues by default). When the
  instructions treat deferred findings as won't-do unless the user asks, list them and ask once instead.
- **Invocation.** `uv run --script <skill-dir>/scripts/pr-shepherd.py`: works when an installer drops the
  executable bit, and matches `uv run` permission allow-lists.
- **Cache directory.** `PR_SHEPHERD_CACHE_DIR` overrides it; the default is `pr_shepherd_cache` under
  `tempfile.gettempdir()`, which honours `TMPDIR`. No literal `/tmp`.
- **Flaky pacing tests.** `WaitPacingTest` replaces the helper module's `time` global with a fake clock instead
  of patching attributes of the shared `time` module, so `subprocess` waits no longer reach the fake.
- **Description** in trigger form.

### triage-issues
- Description scoped to GitHub Issues, so it does not fire for Jira or other trackers.
- Writes (labels, edits, closures, blocked-by links) follow a triage table presented for one approval, unless the
  user asked to apply directly.
- §7 proposes the label table for the agent-instructions file instead of committing it unasked.

### consistency-review
- Search the decision records, domain docs and tracker that the project's agent instructions name; defaults
  remain `docs/adr/`, `CONTEXT.md`/`docs/` and GitHub Issues. Code search is language-agnostic.
- "Grill" becomes "a decision session"; the flotilla roadmap note becomes one neutral sentence.
- Drift repair on a shared tracker is an outward-facing edit: report the stale count and fix with sign-off where
  the instructions require it.
- Description in trigger form.

### testing
- Body becomes project-neutral. Flotilla specifics (scenario-engine paths, `REPLAY=record`, golden corpus,
  decision ledger, `flotilla crew stall`, evidence issue) move to `flotilla.md`, read when working in flotilla.
- Language references: `hegel.md` (Rust), new `hypothesis.md` (Python) and `jqwik.md` (Java).
- Decisions are recorded where the project records design decisions; a pause follows the agent's instructions.
- Mutation check runs targeted tests per mutant and is recorded in the PR body, or the commit message when the
  change lands without a PR.
- Description in trigger form.

### production-shape
- One line: timing or profile evidence lives in a benchmark or performance suite, never in functional tests.

### Plugin
- Version 1.7.0 in `marketplace.json` and `plugin.json`.
- New `plugins/rjw-sdlc/tests/test_skill_metadata.py`: every SKILL.md has valid frontmatter, a `name` matching its
  directory, a "Use when" description of at most 500 characters, and relative links that resolve.

### Shareable justification
`docs/reports/claude-code-compatibility.md`: each change, the problem it solves and why it is shaped to stay
upstream-compatible.

## Testing approach

- Script: unittest cases for the cache directory (override and `TMPDIR` default); pacing tests made
  deterministic and run repeatedly under parallel load.
- Skills: the metadata test; behaviour scenarios in fresh subagents for the pr-shepherd push and sign-off
  branches (original skill as control, edited skill as treatment).
- Gate: both unittest suites, run detached.
