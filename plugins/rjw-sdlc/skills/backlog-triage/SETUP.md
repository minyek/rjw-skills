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

**Older roles an assessment replaces.** `needs-triage` means "not yet assessed", which is now the absence of a `triage:*` label. `needs-info` is `triage:needs-answer` with the reporter as owner. Both stay canonical because the mattpocock-skills triage flow applies them, but setting a `triage:*` label removes them, so an issue never carries both.
| `wayfinder:map`, `wayfinder:build`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, `wayfinder:task` | Wayfinder missions and ticket types |

Topic labels (`bug`, `ui`, `cli`, …) stay per repo and are outside this skill.

## Per-repo config: `docs/agents/triage.toml`

```toml
[[component]]            # 10–20 coarse areas; used by `group` for sweep grouping
name = "recording"
description = "Recording and replay of sessions: asciicast output, transcripts, retention."
paths = ["crates/cleat/src/recording.rs", "crates/cleat/src/replay.rs"]

[needs]                  # dispatch-constraint vocabulary; each becomes a needs:<slug> label
windows = "Needs a Windows host or runner to build or verify"
quiet-window = "Touches so much that it must merge alone, in a quiet window"
```

`setup --config` proposes the `needs:*` labels; `plan --config` rejects `needs` values outside the vocabulary.

## Issue types

Org-level: `Task`, `Bug`, `Feature`, `Brainstorm`, `Mission`, `Lane`. Assessment proposes a type for any untyped issue it touches, so a sweep fills the gap as it goes.

## Each repo also needs

- **Native issue dependencies and sub-issues** enabled. They are on for GitHub organisations by default.
- **`docs/agents/triage.toml`**: components and needs vocabulary (above).
- **`docs/agents/triage-labels.md`** mapping the triage roles to label strings, as flotilla has, so skills that speak in roles find the labels.
- **A token** that can label, comment and add dependencies, for whoever applies plans. Investigators need read access only.

A repo's own gaps (missing labels, invalid priorities, untyped issues) are installation state: record the remediation in an issue in that repo or org, not here.
