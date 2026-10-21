---
description: Merge upstream/main into this fork's main on a worktree branch, gate it, and hand over the landing command
---

# Sync upstream

Run this repository's sync from `CLAUDE.md` ("Syncing from upstream"). A sync is a merge commit, never a squash, so
it does not go through `/sqmerge`.

## Steps

1. **Fetch and check.** `git -C <main> fetch upstream`, where `<main>` is the repository's main checkout. If
   `git -C <main> log --oneline main..upstream/main` is empty, report "already up to date" and stop. Otherwise list
   those commits and `git diff --stat main...upstream/main` in one short summary. Stop if `<main>` has uncommitted
   changes or a sync worktree already exists under `.worktrees/`.
2. **Worktree.** `git -C <main> worktree add .worktrees/sync-upstream -b sync-upstream main`, then work there.
3. **Merge.** `git merge --no-ff upstream/main` with the message "Merge upstream/main into main". Resolve conflicts
   by these rules, and report each in the summary:
   - **Version fields** in `.claude-plugin/marketplace.json` and `plugins/rjw-sdlc/.claude-plugin/plugin.json`: keep
     both manifests equal, and one minor above the larger of the fork's version and upstream's. The plugin cache is
     keyed by version, so a merge that changes plugin content must change the version.
   - **A skill upstream deleted or replaced** that the fork modified: take upstream's removal, and say which fork
     change is dropped with it.
   - **Anything else**: keep upstream's intent and the fork's own changes. If both cannot hold, stop and ask.
4. **Fit the fork's checks.** Run `/gate`. A new or changed upstream skill can fail the fork's own checks. Fix the
   fork side with the smallest change, for example a `description` that opens with "Use when" for
   `test_skill_metadata.py`. Add any new upstream test directory to `GATE_FULL` in `.claude/delivery.env`, so the gate
   covers it. Commit these in a separate commit after the merge commit, with explicit paths.
5. **Hand over the landing.** The hook on the main checkout refuses `git merge` there, even a fast-forward, and the
   landing must not be bypassed from here. Stop and print this for the user to run, with real paths and branch name:
   ```
   DELIVERY_OVERRIDE=1 git -C <main> merge --ff-only sync-upstream && git -C <main> push origin main
   ```
   Then wait. Never push yourself, and never leave the sync on `main` unpushed.
6. **After the user confirms.** Check that `main` and `origin/main` are at the same commit, remove the worktree
   (`git worktree remove`), and delete the branch (`git branch -d sync-upstream`). Tell the user to run
   `claude plugin marketplace update rjw-skills && claude plugin update rjw-sdlc@rjw-skills`, then restart Claude Code.
   If `--ff-only` refused because `main` moved, merge `main` into the branch, run `/gate` again, and print the
   command again.
