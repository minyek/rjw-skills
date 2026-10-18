# Single source for test rules: evidence

Date: 2026-10-17. Change: `test-rules-single-source`. Its planning documents (design and requirements) are in
the user's configuration repository.
Evidence: the fixture, prompts, rubric, per-run outputs and scoring are not kept in this repository. The
run transcripts quote the user's private instructions and are kept in the user's private configuration
repository under `docs/reports/artefacts/test-rules-single-source/transcripts/`.

## Question

The change makes `rjw-sdlc:testing` the one home for generic test-design rules (new §10 "Earn each test", a
narrower §2 constant-map example, a §6 mutation sentence) and moves the matching rules out of the user's
instructions, which now point at the skill. Does an agent still get the rules, through routing alone, and do
they change what it writes and catches?

## Method

Headless `claude -p` runs (model `opus`) against three isolated configurations:

| Arm | Instructions | Plugins |
|---|---|---|
| `control` | Today's instructions with every test rule removed | None |
| `today` | Today's instructions | rjw-sdlc 1.8.0, clean-code 1.1.0 |
| `new` | The change's candidate instructions (rules replaced by a pointer and a routing row) | rjw-sdlc 1.9.0 candidate, clean-code 1.2.0 candidate |

- **Isolation.** The design asked for `claude -p --bare`, which accepts only an API key; the machine has none.
  Each run instead gets an empty `CLAUDE_CONFIG_DIR` holding only a link to the OAuth credentials, the arm's
  instructions through `--add-dir` (with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`) and its plugins
  through `--plugin-dir`. Probes confirmed that each arm sees its own instructions and plugins and nothing of
  the user's (`probe.md`). clean-code defines its plugins
  only in `marketplace.json`, so each arm builds a one-plugin directory from the arm's `skills/python`.
- **No hints.** The prompt names the task only, never a skill or rule, so routing is observed, not assumed.
- **Scenarios, three runs per arm.**
  - `review`: review a test diff with six planted problems (an assertion that never runs, config read from
    outside the test directory, a duplicate test, an all-zeros fixture column, a change-detector, a reviewer
    blocking on a missing conceivable test) and one decoy (a test of wire codes a cited spec fixes).
  - `map`: add a country-code-to-region map with case folding and a fallback, and test it.
  - `threshold`: add a configured free-shipping threshold and test it.
  - `mutation`: run a mutation check on configuration-heavy code whose fixture already holds value-restating tests.
- **Scoring** by `rubric.md`, one scorer per batch, each
  following the earlier batch's conventions.

## Results

Counts are runs out of 3.

| Scenario | control | today | new |
|---|---|---|---|
| Review: all six planted problems caught | 2 | 3 | 3 |
| Review: decoy wrongly flagged | 0 | 0 | 0 |
| Map: value-restating test written | 3 | 3 | 3 |
| Threshold: value-restating test written | 2 | 0 | 0 |
| Mutation: edited literal counted as caught (rubric reading) | 0 | 0 | 0 |
| Mutation: same, counting the report's headline total | 2 | 2 | 1 |
| Loaded `rjw-sdlc:testing` | 0 of 12 | 1 of 12 | 11 of 12 |

- **Routing works.** Without the rules in the always-loaded instructions, the `new` arm loaded the testing
  skill in 11 of 12 runs; the one exception stopped at a spec-approval gate before writing anything. Under
  today's layout the skill loaded once in 12 runs: the rules reached agents through the user's instructions,
  not the skill.
- **Review.** `new` meets the design's bar: all six planted problems in 3 of 3 runs. `control` missed the
  duplicate test once (2 of 3 against 3 of 3), a difference of one run, so review does not separate the arms
  beyond noise: a strong model catches these problems unprompted. The threshold scenario, not review, is the
  evidence that the rules change behaviour. No arm flagged the decoy, so §10 did not make reviewers over-apply
  it.
- **Threshold.** The rules matter. `control` wrote a test that loads the shipped config and asserts `== 50.00`
  in 2 of 3 runs. `today` wrote the same test twice and deleted it, citing the instructions' "tests must not
  depend on config outside the test directory". `new` never wrote it: both implementing runs checked that the
  threshold comes from settings by moving it and watching the price flip, which is §10's "assert what the code
  does with a value".
- **Map.** No effect. Every run in every arm restated the full seven-code table, alongside real tests of the
  case folding and the fallback. The `new` runs called the table "the requested contract", which §5 allows:
  the prompt itself lists every mapping, so this scenario cannot tell a restated value from a stated
  requirement. The scenario did not discriminate, so §2's narrower example rests on review of its text, not
  on these runs.
- **Mutation.** Small. Every arm reverted the code and noted which mutants only a restating test caught. Under
  the stricter reading, `new` counted such a mutant in its headline once, against twice for the other arms.

## Decisions taken from the evidence

- **§6 sentence kept.** The design drops it if the baseline already passes. Under the rubric's reading it does
  (0 of 3); under the headline reading it does not (2 of 3). The evidence does not settle which reading
  answers the design's question, the sentence costs one line, and it removes a contradiction in §6's own text.
- **The threshold scenario was rerun.** In its first batch 5 of 6 baseline runs stopped at the instructions'
  spec-approval gate, because a new config key is a contract change there. The rerun prompt says the design
  is approved. The first batch, in which 8 of 9 runs stopped at that gate, is kept in
  `results/superseded/threshold-first-batch/`.

## Limits

- Three runs per arm and one model; differences of one run are noise.
- Each batch had one scorer; `tally.md` records every
  ambiguous call and its alternative.
- The account's claude.ai connectors and its `anthropic-skills:*` skills load in every arm; none concerns tests.
- Hypothesis is not installed, so no run could write property-based tests.
- Two amendments, both user decisions, came after the runs, so no run saw them: two lines of
  `testing/SKILL.md` §10 gained the caller-level and wall-clock-forms clauses, and the test-removal bullet in
  the candidate user instructions now says "existing test".
