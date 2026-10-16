# skill-fixes-and-fork-setup — requirements

Slug: skill-fixes-and-fork-setup (ticketless). Design: [skill-fixes-and-fork-setup-design.md](skill-fixes-and-fork-setup-design.md).

Background: the conflict review in [2026-10-16-skill-conflict-review.md](../../reports/2026-10-16-skill-conflict-review.md).
On 2026-10-16 the user approved the review's recommendations ("I approve it all"). The approval covers:
- the test-timeout change;
- keeping the fork's changes on `main`, with the upstream-sync procedure as proposed: a real merge commit on a
  branch, `main` fast-forwarded to it, and the push needing the user's go-ahead or a command whose steps push.

| ID | Requirement | Verified by |
|---|---|---|
| R1 | production-shape: the record location comes from the root `WORKLOAD.md` or the agent instructions. When neither names one, the record goes with the project's existing design records rather than a new directory, and the location question is raised at the next point the instructions allow one. `docs/implementation-choices/` is the default only for a project with no design records. | Scenario I5 against the edited text: 3 of 3 runs write to the existing records directory and do not stop (baseline: 3 of 3 failed). The other two branches (the instructions name a location; no design records at all) are review-only, inferred. |
| R2 | testing: Java is named as the exception to the native property library, with the JUnit 5 seeded-generator recipe. The reason cites jqwik's user guide. | Scenario I7 against the edited text: 3 of 3 runs add no jqwik and use the recipe (baseline: 3 of 3 added jqwik) |
| R3 | pr-shepherd tests: `run_cli`'s subprocess timeout is a named deadlock guard of 300 seconds. | Review; the pr-shepherd suite passes |
| R4 | `CLAUDE.md` at the repository root states the items listed under "R4 contents" below. | Review |
| R5 | `.claude/delivery.env` sets an empty `JIRA_KEY`, gate commands that run both test suites, `GATE_ARM`, and `INSTALL_BY_USER` with the plugin update commands. | `/gate` in `/sqmerge` runs from it and writes a receipt |
| R6 | rjw-sdlc is 1.8.0 in both manifests. | `test_skill_metadata.py` (manifests agree) and review |
| R7 | The report records the review, its method (stated-intent runs), each item's baseline and green evidence, and why withdrawn items were withdrawn. The scenarios, preamble, tested text and tally are kept under `docs/reports/artefacts/2026-10-16-skill-conflict-review/`. | Review against the artefacts |
| R8 | `claude plugin validate` passes for the marketplace and the plugin. | Command output recorded in the final review |
| R9 | `docs/decisions/` holds an index with one entry each for the fork layout and for Java property testing without jqwik, linking their rationale. | Review |

## R4 contents

- **What `main` holds.** `main` carries this fork's changes on top of upstream (`rjwittams/rjw-skills`). It does not
  mirror upstream.
- **Upstream syncs.** A sync is this repository's exception to `/sqmerge` step 7, because a squash would make
  upstream's commits stop being ancestors of `main`:
  1. In a worktree branched from `main`, run `git merge --no-ff upstream/main`, resolve conflicts, and run the gate.
  2. With the user's go-ahead, fast-forward `main` to the branch (`git merge --ff-only`) and push `main` in the same
     step, so a sync never waits unpushed on `main` for the next `/sqmerge` push.
  3. Remove the worktree.
- **Ordinary changes.** They still go through `/worktree-new` and `/sqmerge`.
- **Upstream PRs.** A PR branches from `upstream/main` and applies only the landed commit's own plugin hunks
  (`git diff <commit>^ <commit> -- plugins/rjw-sdlc/ ':!plugins/rjw-sdlc/.claude-plugin/' | git apply -3`), never
  `docs/`, `.claude/`, `CLAUDE.md` or the fork's version bump. Whole-file checkouts were rejected because they carry
  earlier fork changes. Pushing the PR branch and opening the PR need the user's go-ahead.
- **The gate:** `/gate`, configured by `.claude/delivery.env`.
- **Installing the plugin from this fork.** Register the marketplace from GitHub, install the plugin, and update
  both after each merge to `main`, with the exact commands.

## Edge cases

- A project that keeps design records under a different name (an ADR set) follows R1 through "existing design
  records". A project with no design records keeps the original default.
- Java is the only language named in R2; other languages keep the general rule.

## Withdrawn before design

These were withdrawn on baseline evidence; see the report's "Baselines" section:
- pr-shepherd force-push guidance and posting guidance;
- follow-up issues for out-of-scope findings;
- production-shape mid-task questions about cardinalities;
- the consistency-review label for agent decisions;
- the comment self-check carve-out;
- the squash-message mutation record;
- the triage-issues label table location.

Each behaved as wanted with the current text. The report records two upstream issues filed under an explicit
pr-shepherd invocation without a separate ask; the invocation authorizes them under the user's reading.

## Changes during implementation

- **R1, implementation-choices bullet.** The final review found that "beside the project's other design records"
  could point away from a location `WORKLOAD.md` names. The bullet now says "at the location above". Scenario I5
  was rerun against the revised text and passed 3 of 3 (tally: "I5 v2").
- **R4, upstream PRs.** Whole-file checkouts would carry earlier fork changes, so the command applies the landed
  commit's own hunks: `git diff <commit>^ <commit> -- plugins/rjw-sdlc/ ':!plugins/rjw-sdlc/.claude-plugin/' | git apply -3`.
  It works only in this repository, where both histories are present. The sync procedure also covers a moved
  `main` and a push that fails after the fast-forward.
- **R5.** The gate runs in arm-run's latency class (`--class latency`), as `arm-run --help` asks of gates.
  `GATE_SCOPED` reuses `GATE_FULL`.
- **R8.** The marketplace gains the top-level `description` its validator warned about.
- **Not changed (review findings deferred):**
  - Whether "add the answer to the root `WORKLOAD.md`" means creating one. Green runs offered setup and created
    nothing.
  - "States the space it covers" in the Java recipe. All green runs stated the generator's space.
  - A seed override for the Java recipe. The fixed seed is deliberate, for reproducibility.
  - The helper's own subprocess timeouts. This is a production-behaviour decision, recorded in the report.
