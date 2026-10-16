# Java property tests: JUnit 5 with a seeded generator, not jqwik

Decided 2026-10-16; follows the jqwik withdrawal in [claude-code-compat requirements R10](../archive/claude-code-compat/claude-code-compat-requirements.md).

**Decision.** The testing skill names Java as the exception to "use the native property library". Java tests use
JUnit 5 `@ParameterizedTest` fed by a `@MethodSource` drawing from a fixed-seed `java.util.Random`, with the seed in
the failure message.

**Why.** jqwik's user guide (1.10.2, section "Anti-AI Usage Clause") says the project "is not meant to be used by
any 'AI' coding agents at all". The earlier change withdrew a jqwik reference and left Java to the general rule; in
baseline runs that rule sent 3 of 3 agents to jqwik. With the exception named, 3 of 3 used the recipe.

**Options.** jqwik anyway (rejected: the maintainers' stated wish); an unmaintained QuickCheck port (rejected,
inferred: no maintained alternative known); plain JUnit 5 with a seeded generator (chosen: no dependency,
reproducible; no automatic shrinking).
