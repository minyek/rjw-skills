# Testing under flotilla

These apply on top of [SKILL.md](SKILL.md).

## Running as a flotilla crew (`FLOTILLA_CREW_ID` is set), in any repository

- **Decision ledger.** Record the test-design decisions with:

  ```
  flotilla artifact put --kind decision-ledger
  ```

- **Genuine blockers.** Stall the crew with:

  ```
  flotilla crew stall --reason "…"
  ```

- **Mutation check.** Record it in the PR body under a "Mutation check" heading.

## Working in the flotilla repository

- **Property library.** Use **Hegel** (the `hegeltest` crate, imported as `hegel`); [hegel.md](hegel.md) has the API.
- **Scenario engine.** For stateful and concurrent logic, extend the existing generated scenario engine (`crates/flotilla-daemon/tests/request_session_pair.rs`, `crates/flotilla-daemon/tests/convergence_property.rs`) rather than building a new harness.
- **Record and replay fixtures.** Re-record with `REPLAY=record`, and keep them exactly as recorded (see flotilla's `CLAUDE.md`).
- **Layout contracts.** The golden stored-record corpus (#2169) is the case where an exact serialized layout is the contract.

The evidence behind these rules is in flotilla-org/flotilla#2446.
