# Fork layout: main carries the fork's changes

Decided 2026-10-16 by the user.

**Decision.** `main` is the fork's version. Upstream is merged into it with a merge commit on a worktree branch,
which `main` fast-forwards to; ordinary changes land through `/sqmerge`. The plugin is installed from the fork's
GitHub `main`.

**Options.**
- *A long-lived branch (`andy-changes`) with upstream merged into it.* `main` would mirror upstream and GitHub's
  "Sync fork" would keep working. But `/worktree-new` and `/sqmerge` assume `main` is where work lands, so every
  change would need hand-run steps, and the installed plugin would depend on a worktree the delivery process deletes.
- *`main` as the fork's version (chosen).* The delivery commands work unchanged and the marketplace has a stable
  source. Merging from upstream is the same work either way: conflicts depend on how far the histories diverge, not
  on the branch name. The cost is that syncs need their own landing, because a squash would break upstream ancestry.

**Plugin source.** GitHub rather than the main checkout as a directory source: it installs only merged, pushed work.
