# Evolution

Every surface that outlives one process has a contract with time: a wire protocol with peers on other versions, a persisted format with your past and future selves, a public API with callers you do not control. Choose how each surface evolves from a ladder of levels; the project's `WORKLOAD.md` names the level for each surface, with refinements.

## Levels

- **Disposable**: break freely; nothing kept depends on it. Prototypes, caches.
- **Rebuildable**: version-tagged; on a mismatch, discard and rebuild from the source of truth. Derived indexes, materialised views. Requires that the source of truth exists and the rebuild fits the workload.
- **Forward-migrated**: each upgrade migrates the data one way; there is no rollback. Single-user applications and local tools' own state.
- **Rollback-safe**: the previous generation reads and writes what the current one writes. Changes go expand, then contract, across releases. Nothing persisted depends on runtime code (triggers calling custom functions, stored procedures, serialized type names), and derived structures rebuild from the source of truth. Services with rolling deploys or rollback.
- **Mixed-version**: versions coexist indefinitely. Readers skip what they do not know, tags and names are never reused, peers handshake on version. Federated peers, clients in the wild.
- **Public contract**: consumers you do not control. A written deprecation policy and window, versioned releases. Libraries, public APIs, file formats users keep.

## Choosing and changing a level

- Read the level for the surface you are changing from the nearest `WORKLOAD.md`. When none is named, ask; when nobody can be asked, assume the strictest level the surface plausibly needs and record the gap.
- Refinements in `WORKLOAD.md` add to a level: "readable by stock tools", the deprecation window, the migration tooling in use.
- Levels move as a project matures. Record each move in `WORKLOAD.md`, and treat moving up as work done before the declaration: add version tags before claiming rebuildable, ship the first expand-then-contract change before claiming rollback-safe.
- Write the evolution rules for a new surface before its first release: how a field or column is added, deprecated and removed at its level.
