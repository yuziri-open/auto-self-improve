# Protocol

This kit uses an iterative self-improvement loop for Codex skills: inspect the current state, run a small bounded experiment, keep evidence, and use that evidence to choose the next improvement.

## Start Of Every Invocation

1. Read `_auto_self_improve/CURRENT_FOCUS.md`.
2. Read `_auto_self_improve/INVARIANTS.md`.
3. Read `_auto_self_improve/IMPROVEMENT_BACKLOG.md`.
4. Read `_auto_self_improve/LESSONS.md`.
5. Read the last 5 entries from `_auto_self_improve/RUN_LOG.jsonl`.

## Decision Rule

- Pick at most one improvement experiment.
- Only choose an experiment that is small, reversible, and lower priority than completing the current user task.
- If there is clear breakage or repeated friction, repair that before attempting a broader improvement.
- If there is no safe experiment, do no extra change and only record the friction.

## End Of Every Invocation

1. Append a structured record to `_auto_self_improve/RUN_LOG.jsonl`.
2. Update `_auto_self_improve/CURRENT_FOCUS.md` if priorities changed.
3. Update `_auto_self_improve/IMPROVEMENT_BACKLOG.md` by removing completed items and adding newly observed friction.
4. Promote durable learnings into `_auto_self_improve/LESSONS.md`.
5. Promote hard constraints and regression guardrails into `_auto_self_improve/INVARIANTS.md`.

## State Model

- `CURRENT_FOCUS.md`: what the next few runs should optimize for.
- `IMPROVEMENT_BACKLOG.md`: candidate repairs and improvements sorted by priority.
- `LESSONS.md`: stable, compact, repeated learnings.
- `INVARIANTS.md`: promises that should not be broken.
- `RUN_LOG.jsonl`: append-only evidence from each run.

## Safety

- Do not let the loop overwhelm the main task.
- Avoid large speculative rewrites.
- Prefer recording evidence over forcing a change with weak justification.
- Keep logs append-only so the next run can reason from history.
