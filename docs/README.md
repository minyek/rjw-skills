# docs

- `decisions/`: design decisions, one line each in its README, with the rationale in the linked file.
- `reports/`: write-ups, such as the Claude Code compatibility review of the rjw-sdlc skills. A report states its
  method, results and decisions in full and links no raw run output. What a later reader needs from a run goes in
  the report or the commit message; transcripts, per-run results and fixtures are not committed
  (`reports/artefacts/` is git-ignored).
- `archive/<slug>/`: the design, requirements and plan of a shipped change, bundled per change. Active planning
  docs live in `design/`, `requirements/` and `plans/` only while the change is in flight.
