# Setup

The skill uses one vocabulary in every repo. Check a repo against it:

```bash
scripts/backlog-triage.py setup OWNER/REPO...
```

It reports, per repo: canonical labels that are missing, `priority:*` labels whose value isn't a dispatch tier (with how many open issues carry each), open issues with no issue type, and issue types missing from the org. Its `actions` list holds one `create_label` action per missing label. Save the output as a plan, `show` it, and `apply` it after approval, like any other plan.

## Canonical labels

| Label | Purpose |
|---|---|
| `triage:clear`, `triage:blocked`, `triage:needs-answer`, `triage:needs-rewrite`, `triage:waiting` | Triage state; exactly one per assessed issue ([SKILL.md](SKILL.md#states)) |
| `needs-triage`, `needs-info`, `ready`, `ready-for-human`, `wontfix`, `duplicate` | Triage roles shared with the mattpocock-skills triage flow. `ready` is earned: the body is a dispatchable contract |
| `wayfinder:map`, `wayfinder:build`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, `wayfinder:task` | Wayfinder missions and ticket types |

Topic labels (`bug`, `ui`, `cli`, …) stay per repo and are outside this skill.

## Issue types

Org-level: `Task`, `Bug`, `Feature`, `Brainstorm`, `Mission`, `Lane`. Assessment proposes a type for any untyped issue it touches, so a sweep fills the gap as it goes.

## Each repo also needs

- **Native issue dependencies and sub-issues** enabled. They are on for GitHub organisations by default.
- **`docs/agents/triage-labels.md`** mapping the triage roles to label strings, as flotilla has, so skills that speak in roles find the labels.
- **A token** that can label, comment and add dependencies, for whoever applies plans. Investigators need read access only.

## Remediation (flotilla-org, 2026-10-16)

The first `setup` run across flotilla, cleat, wheelhouse and andamento found:

1. **`triage:*` labels missing everywhere.** Create them in all four repos.
2. **Triage roles missing outside flotilla.** cleat, wheelhouse and andamento lack `needs-triage`, `needs-info` and `ready-for-human`.
3. **Wayfinder labels incomplete.** cleat lacks `wayfinder:map`; wheelhouse lacks `wayfinder:build`; andamento lacks the wayfinder ticket labels.
4. **Invalid priorities in cleat:** `priority:later` (17 open issues) and `priority:soon` (8). `priority:next` is unused. Dispatch accepts only `urgent`, `high`, `medium` and `low`, and an invalid explicit priority can fail the project closed once readiness is live. Map each issue to a valid tier or remove the label, then delete the three labels. This needs the maintainer's call on the mapping.
5. **Untyped open issues:** flotilla 65, cleat 81, wheelhouse 78, andamento 24. Sweeps propose types; a separate pass can type the rest.
6. **`docs/agents/triage-labels.md`:** flotilla has one; add it to the others, with the `triage:*` rows.

Steps 1–3 and 6 are mechanical. Steps 4 and 5 need decisions per issue.
