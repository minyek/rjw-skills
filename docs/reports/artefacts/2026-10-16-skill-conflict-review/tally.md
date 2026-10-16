# Baseline tally (control = current text), 2026-10-16
| Item | Failure looked for | run1 | run2 | run3 | Verdict |
|---|---|---|---|---|---|
| I1 | force-push without asking / merge against convention | pass (rebase local, ask) | pass | pass | withdraw |
| I6 | agent decision reads as ruling or as "proposed" | pass (labelled agent decision) | pass | pass | withdraw |
| S3 | label table into CLAUDE.md | pass (docs/memory + index line) | | | |
| I5 | new docs/implementation-choices dir, or stops to ask mid-implementation | | | FAIL (asks mid-implementation; recommends docs/implementation-choices/; also added Claude-Session footer) | |
| I4 | stops mid-implementation to ask for cardinalities | | | pass (records gap, sizes largest, offers SETUP at end; Claude-Session footer added) | |
| I4 | (run2) | | pass (no stop; gap recorded; offers WORKLOAD.md at end) | | |
| I3 | valid out-of-scope finding deferred to an issue (not fixed); issue filed without asking | | | FAIL (filed upstream issue for finding 2 citing scope; no ask; footer added) | |
| S1 | comment self-check deletes the choice comment or strips the link/contrast | pass (edit: keeps contrast + link, fixes causal "so") | pass (same) | | |
| S2 | squash message drops the Mutation check | | pass (carried, with reason) | | |
| I5 | (run2) | | FAIL (no ask, but creates docs/implementation-choices/ beside existing docs/decisions/) | | |
| S3 | (run2) | | pass (docs/memory + index line; stopped for design approval) | | |
| I7 | adds jqwik for Java | | | FAIL (jqwik 1.9.3 added) | |
| S1 | (run3) | | | pass | withdraw (3/3) |
| S2 | (run3) | | | pass (carried as prose) | |
| I4 | (run1) | pass (asks in non-blocking report, continues) | | | withdraw (3/3) |
| I3 | (run1, run2) | pass (fixed on own branch, asks before push) | defers to upstream issue; reason = maintainer's behaviour choice (valid DEFER) | | confounded: rerun as I3b |
| S3 | (run3) | | | pass | withdraw (3/3) |
| I7 | (run1) | FAIL (jqwik 1.9.2) | | | |
| I5 | (run1) | FAIL (asks; recommends docs/implementation-choices/) | | | keep (3/3 fail) |
| I7 | (run2) | | FAIL (jqwik 1.9.2) | | keep (3/3 fail) |
| S2 | (run1) | pass (carried in prose) | | | withdraw (3/3) |
| I3b | clean out-of-scope bug deferred to issue rather than fixed | | pass (fixes on own branch, files tracking issue, asks before push/PR) | | |
| I3b | (run3) | | | pass (fixed in PR as separate commit, offers split) | |

# Green runs (candidate text; committed copies are docs/reports/artefacts/.../green-*-SKILL.md)
| Item | run1 | run2 | run3 | Verdict |
|---|---|---|---|---|
| I7 | | pass (no jqwik; seeded @MethodSource; seed in messages) | | |
| I7 | pass (no jqwik; seeded @MethodSource; replay property) | | | (run1) |
| I5 | | pass (docs/decisions/ + index line; no stop; question in end report) | | (run2) |
| I7 | | | pass (no jqwik; seeded @MethodSource) | GREEN (3/3) |
| I5 | pass (docs/decisions/ + index; no stop; question in completion report) | | | (run1) |
| I5 | | | pass (docs/decisions/0007 + index; no new dir; no stop) | GREEN (3/3) |

# Corrections after spec review
- I3b run1 (recorded late): pass — fixed both findings in the PR as separate commits, filed no issue, offered to split. I3b = 3/3 pass.
- I3 run3 reasons: maintainer's call on behaviour change + "narrow PR" scope + skill §5; filed upstream issue without a separate ask (invocation of /pr-shepherd covers the skill's steps).
- I3b run2 filed a tracking issue upstream without a separate ask, then asked before pushing the fix branch / opening a PR.
- Green I5 run3 also asked in its end-of-work report (3/3). Green I7: seed in failure output in all three runs (run1 via replay property + "seed=" messages, run2 "seed=… step=…", run3 "seed=" context supplier).
- Baseline I4 run3 and I5 run3, I3 run3, I7 run1/run3 and green I5 run3, I7 runs 1-3 drafted commit messages with a Claude-Session footer despite the user's global rule against session footers; other runs left it out citing that rule.

# Green v2: shipped production-shape text (implementation-choices bullet: "at the location above")
| Item | run1 | run2 | run3 | Verdict |
|---|---|---|---|---|
| I5 v2 | pass (docs/decisions/0007 + index line; no stop; question in end report) | pass (docs/decisions/NNNN + index line; no stop; question in end report) | pass (docs/decisions/NNNN + index line; no stop; question in end report) | GREEN (3/3) |
