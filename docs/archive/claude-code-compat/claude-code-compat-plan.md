# claude-code-compat — plan

Slug: claude-code-compat (ticketless). Design: [design](claude-code-compat-design.md).
Requirements: [requirements](claude-code-compat-requirements.md).

Superseded in part: the requirements' "Changes during implementation" section withdraws the push and sign-off branches, the follow-up tracker branch, the triage write flow, the drift-repair sign-off and `jqwik.md`; where this document still describes them, that section wins.

Small full-path change by diff size (mostly prose): implemented inline, serially, TDD where code is involved.

| Task | Covers | Depends on | Touch-set |
|---|---|---|---|
| T1 test: skill metadata test (fails on current descriptions, version, invocation) | R4 R5 R9 R10 R12 | — | `plugins/rjw-sdlc/tests/test_skill_metadata.py` |
| T2 test: cache-directory tests (fail: no override, literal `/tmp`) | R6 | — | `pr-shepherd/tests/test_pr_shepherd.py` |
| T3 fix: deterministic `WaitPacingTest` (patch the helper's `time` global) | R7 | — | `pr-shepherd/tests/test_pr_shepherd.py` |
| T4 feat: `PR_SHEPHERD_CACHE_DIR` and `tempfile` default | R6 | T2 | `pr-shepherd/scripts/pr-shepherd.py` |
| T5 pr-shepherd SKILL.md: push, sign-off, follow-ups, invocation, description, cache env | R1–R5 | T1 | `pr-shepherd/SKILL.md` |
| T6 triage-issues SKILL.md | R5 R8 | T1 | `triage-issues/SKILL.md` |
| T7 consistency-review SKILL.md | R5 R9 | T1 | `consistency-review/SKILL.md` |
| T8 testing: neutral body, `flotilla.md`, `hypothesis.md`, `jqwik.md` | R5 R10 | T1 | `testing/*` |
| T9 production-shape timing line | R11 | — | `production-shape/SKILL.md` |
| T10 manifests to 1.7.0 | R12 | T1 | `.claude-plugin/marketplace.json`, `plugins/rjw-sdlc/.claude-plugin/plugin.json` |
| T11 behaviour scenarios: edited pr-shepherd vs the original as control | R1 R2 | T5 | none (scratch) |
| T12 justification report | R13 | T5–T10 | `docs/reports/claude-code-compatibility.md` |

T5–T9 have disjoint touch-sets but are short prose edits; they run serially in this session.

Gate: `python3 -m unittest discover` for `plugins/rjw-sdlc/tests` and `pr-shepherd/tests`, detached.
