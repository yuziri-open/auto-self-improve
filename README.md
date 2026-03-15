# Auto Self-Improve Skill

`auto-self-improve-skill` is a Codex skill kit that turns another skill into a self-improving skill.

It adds a lightweight improvement loop to a target skill so that every invocation can:

- read recent lessons and constraints
- try at most one small, safe improvement
- record what worked, what failed, and what should happen next

The goal is simple: make a skill repair itself and improve over time without letting the improvement work overwhelm the main user task.

## Why This Exists

Many skills stay static after you write them once.

This kit is for the opposite workflow:

1. A skill runs on a real task.
2. It notices friction, missed context, regressions, or repeated cleanup.
3. It records those observations.
4. On the next run, it uses that evidence to make one bounded improvement.

It is inspired by iterative agent improvement ideas such as Karpathy's `autoresearch`, but packaged as a reusable Codex skill.

## What Gets Installed

When you install this kit into a target skill, it adds:

```text
_auto_self_improve/
  PROTOCOL.md
  CURRENT_FOCUS.md
  IMPROVEMENT_BACKLOG.md
  LESSONS.md
  INVARIANTS.md
  RUN_LOG.jsonl
scripts/
  skill_auto_self_improve.py
```

It also injects a small block into the target skill's `SKILL.md` so the skill remembers to read this state on every run.

## Quick Start

Install the kit into a target skill:

```bash
python3 scripts/install_auto_self_improve.py /absolute/path/to/target-skill
```

Then the target skill will:

1. Read `_auto_self_improve/PROTOCOL.md`
2. Read its current focus, invariants, backlog, lessons, and recent logs
3. Choose at most one safe improvement experiment
4. Complete the main task
5. Record the result for the next run

## Files

### Core Skill

- `SKILL.md`: the Codex skill definition
- `agents/openai.yaml`: UI-facing skill metadata
- `references/protocol.md`: the operating model behind the loop
- `references/skill_snippet.md`: the block injected into a target skill

### Installer

- `scripts/install_auto_self_improve.py`: installs the kit into another skill

The installer:

- copies the `_auto_self_improve` state templates
- copies the helper script into the target skill
- injects the embedded improvement-loop block into the target `SKILL.md`
- migrates older `_autoresearch` installs into `_auto_self_improve`

### Runtime Helper

- `templates/scripts/skill_auto_self_improve.py`: optional helper for reading and writing improvement state

Useful commands:

```bash
python3 scripts/skill_auto_self_improve.py summary
python3 scripts/skill_auto_self_improve.py record \
  --task "homepage refactor" \
  --hypothesis "shorter startup checklist reduces missed context" \
  --change "moved repeated instructions into CURRENT_FOCUS.md" \
  --outcome success \
  --learning "the skill missed less context when startup guidance was shorter" \
  --next-step "promote the shortcut if it keeps working"
```

## State Model

- `CURRENT_FOCUS.md`: what the next few runs should optimize for
- `IMPROVEMENT_BACKLOG.md`: queued repairs and upgrades
- `LESSONS.md`: stable learnings worth reusing
- `INVARIANTS.md`: rules the skill should not break
- `RUN_LOG.jsonl`: append-only evidence from each invocation

## Design Rules

- The user task always comes first.
- Repair beats optimization.
- One bounded experiment per run is enough.
- Strong lessons get promoted; weak hunches stay in the log.
- Improvement history should stay append-only unless you explicitly reset it.

## Optional vs Required

The Python scripts are helpful, but they are not the core idea.

- Required: the `SKILL.md` instructions and the `_auto_self_improve` state files
- Optional: the Python helpers that automate installation and structured logging

If you prefer a pure prompt-driven workflow, you can keep the state files and embedded snippet and ignore the helper scripts.
