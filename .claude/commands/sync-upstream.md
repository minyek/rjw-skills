---
description: Merge upstream/main into this fork's main on a worktree branch, gate it, land it and push
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
5. **Land and push.** Invoking this command is the user's go-ahead. Run
   `git -C <main> merge --ff-only sync-upstream`, then `git -C <main> push origin main`, in that order and in one
   step, so a sync is never left unpushed on `main`.
   - If `--ff-only` refuses because `main` moved, merge `main` into the branch, run `/gate` again, and retry.
   - If the guard on the main checkout denies the merge, stop and report its message. Do not add
     `DELIVERY_OVERRIDE=1`; that prefix is the user's to type.
   - If the push fails after the fast-forward, report it and land nothing else on `main` until the user decides.
6. **Clean up.** Check that `main` and `origin/main` are at the same commit, `git worktree remove` the worktree and
   `git branch -d sync-upstream`. Tell the user to run
   `claude plugin marketplace update rjw-skills && claude plugin update rjw-sdlc@rjw-skills`, then restart Claude
   Code.
