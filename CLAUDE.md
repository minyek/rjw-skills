# rjw-skills (fork)

This is a fork of [rjwittams/rjw-skills](https://github.com/rjwittams/rjw-skills), a Claude Code plugin marketplace
holding the `rjw-sdlc` plugin. Remotes: `origin` is the fork (`minyek/rjw-skills`), `upstream` is the original.

## What main holds

`main` is this fork's version: upstream plus the fork's own changes. It does not mirror upstream. Ordinary changes
go through `/worktree-new` and `/sqmerge` as anywhere else. Why: [docs/decisions/fork-layout.md](docs/decisions/fork-layout.md).

## Syncing from upstream

`/sync-upstream` ([.claude/commands/sync-upstream.md](.claude/commands/sync-upstream.md)) runs these steps.

A sync is this repository's one exception to `/sqmerge`'s squash: squashing would make upstream's commits stop being
ancestors of `main`, and every later sync would merge all of upstream's history again.

1. `git -C <main> fetch upstream`, then create a worktree branched from `main` under `.worktrees/`.
2. In it, `git merge --no-ff upstream/main`, resolve conflicts, and run `/gate`.
3. With the user's go-ahead, land and push in one step: `git -C <main> merge --ff-only <branch>`, then
   `git -C <main> push origin main`. Never leave a sync unpushed on `main`, where the next `/sqmerge` push would
   carry it without that go-ahead.
   - If `--ff-only` refuses because `main` moved, merge `main` into the branch, run `/gate` again, and retry.
   - If the push fails after the fast-forward, report it and land nothing else on `main` until the user decides.
4. Remove the worktree and delete the branch.

## Contributing upstream

A PR to upstream branches from `upstream/main` and applies only that change's own plugin hunks, in this repository,
where both histories are present:
`git diff <commit>^ <commit> -- plugins/rjw-sdlc/ ':!plugins/rjw-sdlc/.claude-plugin/' | git apply -3`.
Checking out whole files from `main` would also carry every earlier fork change to them. Where a hunk's context
came from an earlier fork change, or has no counterpart upstream, resolve it against upstream's text. A PR never
takes `docs/`, `.claude/`, this file or the fork's version bump. Pushing the PR branch and opening the PR need the
user's go-ahead.

## Gate

`/gate`, configured by [.claude/delivery.env](.claude/delivery.env): the plugin and helper test suites.

## Installing the plugin from this fork

Register the marketplace from GitHub and install the plugin. When switching from another source, uninstall and
remove it first; afterwards `extraKnownMarketplaces.rjw-skills` in `~/.claude/settings.json` should show the GitHub
source:

```bash
claude plugin uninstall rjw-sdlc@rjw-skills
claude plugin marketplace remove rjw-skills
claude plugin marketplace add minyek/rjw-skills
claude plugin install rjw-sdlc@rjw-skills
```

After each merge to `main`, update both and restart Claude Code:

```bash
claude plugin marketplace update rjw-skills && claude plugin update rjw-sdlc@rjw-skills
```

The plugin cache is keyed by version (`~/.claude/plugins/cache/rjw-skills/rjw-sdlc/<version>/`), so a release bumps
both manifests.

## Records

Design records: [docs/decisions/](docs/decisions/README.md). Reports: `docs/reports/`. A report carries its method, results and decisions; never commit the raw evidence behind it (transcripts, per-run output, fixtures), and put what a later reader needs in the report or the commit message.
