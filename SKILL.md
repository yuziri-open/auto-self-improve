---
name: auto-self-improve-skill
description: Use when you want to turn a Codex skill into a self-improving skill that reviews recent runs, applies one safe improvement experiment per invocation, and stores lessons, invariants, backlog items, and run logs inside the skill folder.
metadata:
  short-description: Make skills self-improving
---

# Auto Self-Improve Skill

Use this skill to embed a self-improvement loop into another skill folder.

## Workflow

1. Read [references/protocol.md](references/protocol.md) for the operating model.
2. Run `python3 scripts/install_auto_self_improve.py /absolute/path/to/target-skill`.
3. Inspect the target [SKILL.md](SKILL.md) and confirm the injected block is present near the top.
4. If the target skill already has strict constraints, reflect them in `_auto_self_improve/INVARIANTS.md`.
5. Leave existing `_auto_self_improve` state files untouched unless the user explicitly wants them reset with `--reset-state`.

## What Gets Installed

- `_auto_self_improve/PROTOCOL.md`
- `_auto_self_improve/CURRENT_FOCUS.md`
- `_auto_self_improve/IMPROVEMENT_BACKLOG.md`
- `_auto_self_improve/LESSONS.md`
- `_auto_self_improve/INVARIANTS.md`
- `_auto_self_improve/RUN_LOG.jsonl`
- `scripts/skill_auto_self_improve.py`

## Operating Contract

- The parent skill still prioritizes the user task over self-improvement.
- Each invocation may try at most one safe process experiment.
- Repair comes before optimization.
- Stable lessons are promoted only when evidence is strong enough to avoid churn.
