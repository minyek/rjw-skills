# Decisions

One line per decision; the linked file holds the rationale.

- [Fork layout](fork-layout.md): `main` carries the fork's changes; upstream syncs land as merge commits, never squashed.
- [Java property tests](java-property-tests.md): JUnit 5 with a seeded generator, not jqwik, whose maintainers ask AI agents not to use it.
