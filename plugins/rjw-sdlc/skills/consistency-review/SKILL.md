---
name: consistency-review
description: Use when about to file a ticket claiming something is missing or broken, post a resolution or ruling comment, or update a board, index or status summary, so the claim may contradict decisions already in the project's record.
argument-hint: "[issue-number | 'draft' | artifact-path]"
---

# Consistency Review

Verify a claim against the durable record **before** it becomes a ticket, a ruling comment, or a board entry. The failure this prevents: writing from session memory instead of the record, so that something already decided gets re-decided, or something never decided gets recorded as settled.

Run it on: a ticket you are about to file that asserts something is missing or broken; a resolution comment you are about to post; a derived artifact (board, index, summary) you are about to update.

## Directives

**Absence is a claim, and it is the one that needs evidence.** "X is missing", "nothing handles Y", "this needs a new mechanism" are the assertions that go wrong, because session memory reliably fails to recall a ruling made three weeks ago. Presence is self-evidencing; absence is not.

**An unimplemented decision is not an open question.** These fail in opposite directions and want opposite responses: a ruled-but-unbuilt mechanism wants *enactment* (cite the ruling, file the build ticket); an unruled mechanism wants a *decision*. Opening a decision session for the former wastes the session and pollutes the tracker with a settled question.

**Proposals and resolutions must be visually distinguishable in the record.** An inference written inside a ruling comment reads as ratified to every later reader, including you. Say "proposed", never "must", unless a human ruled it.

**Never present a correction as though the record were at fault.** If the record was right and the claim was wrong, say that plainly and withdraw the claim.

## 1. Extract the claims

State each checkable assertion in one line. For a draft ticket, these are usually its premises rather than its ask:

- "There is no path for X" → an absence claim.
- "The model does not express Y" → an absence claim.
- "Stage N must also do Z" → a decision claim; who ruled it?
- "Ticket #N is in flight" → a state claim.

Absence claims and decision claims get sections 2 and 3. State claims get section 4.

## 2. Check absence claims against the record

For each, search in this order and stop at the first hit. Use the locations your agent instructions name for decision records, design docs and the tracker; the defaults below apply when they name none.

```bash
# 1. Decision records (default docs/adr/) — the most commonly missed source
grep -ril "<mechanism>" <decision-records-dir>/

# 2. Domain/context docs and specs (default CONTEXT.md and docs/)
grep -ril "<mechanism>" CONTEXT.md docs/ 2>/dev/null

# 3. The code — is it declared but unimplemented, or implemented but unused?
git grep -n "<TypeOrConst>" -- ':!*test*'

# 4. Closed rulings on the tracker (bodies AND comments; rulings usually live in comments).
#    GitHub Issues shown; query the tracker your instructions name.
gh issue list --state closed --search "<keywords>" --json number,title
gh issue view <n> --json body,comments -q '.body, (.comments[].body)'
```

Classify each hit:

| Finding | Response |
|---|---|
| Ruled in an ADR, implemented | The claim is wrong. Withdraw it. |
| Ruled in an ADR, **not** implemented | Not an open question. File enactment citing the ADR; do not open a decision session. |
| Ruled in a closed issue comment | Cite the ruling; take only the genuinely-unruled residue to a decision. |
| Declared in code but unwired (enum variant missing, field unread) | Enactment gap. Say which symbol is missing. |
| Nothing found | The absence claim stands. Say where you looked. |

Report where you looked even when you find nothing — an unsupported absence claim and a searched-for-and-absent one deserve different confidence.

## 3. Check decision claims for authority

For each "we should / must / will" in the draft, identify who decided it:

- A human ruled it in this session or a recorded comment → cite the comment link.
- An ADR ruled it → cite the ADR.
- **You inferred it** → mark it "proposed" and, if it sits in a ruling comment on a decided ticket, move it out or label it explicitly as not ruled.

Pay attention to the case where a human explicitly *declined* to decide something. An observation they agreed with ("these two things are confusingly named") is not a ruling about what to do about it.

## 4. Reconcile derived artifacts wholesale

When updating a board, index, or status summary, never touch only the rows you came to edit. Sweep every entry whose state could have changed:

```bash
# every entry the artifact claims is open/in-flight/pending (GitHub shown; use your tracker)
for n in $CLAIMED_OPEN; do
  gh issue view "$n" --json number,state,title -q '"\(.number) \(.state) \(.title)"'
done
```

Anything the artifact asserts and the tracker contradicts is drift. Fix it in the same pass, and say how many entries were stale — silent repair hides a rotting artifact.

## 5. Report

```markdown
## Consistency review — <subject>

**Withdrawn:** <claims that were already ruled and implemented — with citations>
**Reclassified as enactment:** <ruled but unbuilt — ADR/comment link + missing symbol>
**Stands:** <absence claims that survived, with where you looked>
**Downgraded to proposal:** <inferences that were reading as decisions>
**Drift repaired:** <N entries corrected in derived artifacts>
```

If everything survives, say so in one line. The review is cheap and usually finds nothing; that is not a reason to skip it on the occasions it saves a wasted decision session.

## Notes

This skill is a stopgap for a role: a standing consistency reviewer whose corpus is the decision records and closed rulings rather than the test suite. When such a reviewer, or deterministic queries against a resource store, take over these checks, delete most of this file rather than maintaining it.
