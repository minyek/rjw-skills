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

## Starting with the state earlier runs left

Every start reads what earlier runs left behind: state files, journals, checkpoints, markers and logs. Sort each thing a start reads into one of two kinds, and write the kind into the design. Classify by what puts it right: when only an install or configuration step can, it is install-provided; otherwise it is runtime-written.

- **Install-provided**: configuration keys, files the installer ships, credentials. A start may refuse when one is missing or invalid, because putting it right is an install step.
- **Runtime-written**: anything the service, an earlier version of it, or an operator writes while it runs, including a file the installer seeds and the service then rewrites. A start never refuses over one, whether it is missing (a first start, the first start of the release that adds it, a lost disk), unreadable, corrupt, or of a version its evolution level cannot read. A refusal here can keep a production service down until someone ships a code fix.

A lock, pid file or session marker is runtime-written, but it can record a live owner. The start checks the owner: a pid that is running, a lease that has not expired, a peer that answers. A dead owner's marker is cleared and the start goes on, as in [FAILURE.md](FAILURE.md). A live owner's marker is not a leftover: the start waits for the owner or refuses, as the design's single-instance rule says ([FAILURE.md](FAILURE.md)), and its error names the owner. A marker that cannot be read is treated as a dead owner's: it is cleared and the start goes on. Where the marker is readable but its owner cannot be checked (a peer that does not answer), the design states which way the start errs; for money or safety it keeps the guarded function off rather than refusing the whole start.

When a runtime-written input cannot be used, even after any migration its evolution level provides, the start:

- sets the unusable copy aside under a new name, so it can be inspected or restored, when it holds data nothing else can rebuild. A derived or disposable input is discarded and rebuilt from its source of truth, as its level says. Set-aside copies have a retention rule. If setting a copy aside fails (a read-only directory, a full disk), the warning says so and the start goes on;
- runs in the degraded mode the design chose for that input: what the service does without it. For an input that guards money or safety, the design states whether the guarded function stays off until an operator acts or resumes from a fresh state, and why;
- logs a warning (an error when money or safety is degraded) that names the file, what needs it, what is degraded and how to restore it, and repeats it at a fixed interval while the degradation lasts.

Leaving the degraded mode never needs a code change: a documented command, request file or configuration value does it. A dependency the start calls (a database, a daemon, a remote service) is [FAILURE.md](FAILURE.md)'s concern, not this section's.

Verify it with two starts: one against an empty state directory, and one against a directory where every runtime-written file is junk (empty, truncated or random bytes). Both start and log the warnings; in the junk run, each file that holds data nothing else can rebuild is set aside, and each derived or disposable one is rebuilt. Where the service keeps a lock or marker, add a start against one whose owner is dead and one whose owner is alive. In review, a start that refuses or throws over a runtime-written input is a finding, unless the input is a lock or marker whose owner is alive.
