# skill-fixes-and-fork-setup — plan

Slug: skill-fixes-and-fork-setup (ticketless). Design: [design](skill-fixes-and-fork-setup-design.md).
Requirements: [requirements](skill-fixes-and-fork-setup-requirements.md).

Small change by the inline threshold: three tasks, well under 300 changed lines. Implemented inline, serially.

## T1 — skill text (R1, R2)
- Depends on: none. Touches: `plugins/rjw-sdlc/skills/production-shape/SKILL.md`, `plugins/rjw-sdlc/skills/testing/SKILL.md`.
- Test first: the failing test is the baseline scenarios I5 and I7 (3 of 3 failed on the current text); the passing
  test is the same scenarios against the candidate text (3 of 3 passed). Evidence in the report. Apply only the two
  tested `SKILL.md` hunks (artefacts `green-production-shape-SKILL.md`, `green-testing-SKILL.md`), then confirm with
  `diff` against the artefacts that nothing else differs. Copy no other file from the tested tree.
- Then: `test_skill_metadata.py` still passes (descriptions, links, neutrality).

## T2 — pr-shepherd test timeout (R3)
- Depends on: none. Touches: `plugins/rjw-sdlc/skills/pr-shepherd/tests/test_pr_shepherd.py`.
- A named module constant for the deadlock guard (300 s) replaces the literal in `run_cli`. No behaviour test: the
  constant only bounds a hang. The pr-shepherd suite passes.

## T3 — fork setup and release (R4, R5, R6, R8, R9)
- Depends on: T1, T2 (the version bump releases them). Touches: `CLAUDE.md`, `.claude/delivery.env`,
  `.claude-plugin/marketplace.json`, `plugins/rjw-sdlc/.claude-plugin/plugin.json`, `docs/decisions/README.md`,
  `docs/decisions/fork-layout.md`, `docs/decisions/java-property-tests.md`, `docs/README.md`.
- `CLAUDE.md`: the items in the requirements' "R4 contents" section.
- `docs/decisions/`: an index and one entry each for the fork layout and Java property tests; `docs/README.md`
  names the folder.
- `.claude/delivery.env`: `JIRA_KEY=`, `GATE_FULL`/`GATE_SCOPED` running both suites, `GATE_ARM`, `INSTALL_BY_USER`.
- Both manifests at 1.8.0; `test_skill_metadata.py::ManifestTest` pins that they agree.
- `claude plugin validate` on the repository root and on `plugins/rjw-sdlc`; the marketplace gets the top-level
  `description` the validator warns about.

## Independence
T1 and T2 have disjoint touch-sets and no dependency; T3 follows both.

## Documentation
The report and its artefacts (R7) are committed with the design. `docs/README.md` gains a line for `decisions/`.
