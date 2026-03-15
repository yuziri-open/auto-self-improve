<!-- AUTO SELF IMPROVE LOOP START -->
## Embedded Improvement Loop

If `_auto_self_improve/PROTOCOL.md` exists in this skill folder, follow it on every invocation.

At the start of the run:

1. Read `_auto_self_improve/CURRENT_FOCUS.md`, `_auto_self_improve/INVARIANTS.md`, `_auto_self_improve/IMPROVEMENT_BACKLOG.md`, `_auto_self_improve/LESSONS.md`, and the last 5 entries of `_auto_self_improve/RUN_LOG.jsonl`.
2. Choose at most one small, reversible improvement experiment.
3. Repair obvious failures before attempting optimization.

At the end of the run:

1. Append a structured log entry to `_auto_self_improve/RUN_LOG.jsonl`.
2. Update `_auto_self_improve/CURRENT_FOCUS.md` and `_auto_self_improve/IMPROVEMENT_BACKLOG.md` if the priorities changed.
3. Promote stable learnings to `_auto_self_improve/LESSONS.md` and durable guardrails to `_auto_self_improve/INVARIANTS.md`.
<!-- AUTO SELF IMPROVE LOOP END -->
