# Embedded Auto Self-Improve Protocol

Run this loop on every invocation of the parent skill.

## Startup Checklist

1. Read `CURRENT_FOCUS.md`.
2. Read `INVARIANTS.md`.
3. Read `IMPROVEMENT_BACKLOG.md`.
4. Read `LESSONS.md`.
5. Read the last 5 entries from `RUN_LOG.jsonl`.

## Improvement Rule

- Choose at most one bounded experiment.
- Keep the user task primary.
- Prefer repair before optimization.
- Prefer reversible edits over broad rewrites.
- If no safe experiment exists, log the friction and move on.

## Shutdown Checklist

1. Append a run record to `RUN_LOG.jsonl`.
2. Update `CURRENT_FOCUS.md` if the next priority changed.
3. Update `IMPROVEMENT_BACKLOG.md` with new friction or newly unlocked work.
4. Promote durable learnings to `LESSONS.md`.
5. Promote hard constraints to `INVARIANTS.md`.
