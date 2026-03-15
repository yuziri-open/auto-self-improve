#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


MARKER_START = "<!-- AUTO SELF IMPROVE LOOP START -->"
MARKER_END = "<!-- AUTO SELF IMPROVE LOOP END -->"
LEGACY_MARKER_START = "<!-- AUTORESEARCH LOOP START -->"
LEGACY_MARKER_END = "<!-- AUTORESEARCH LOOP END -->"
STATE_DIR = Path("_auto_self_improve")
LEGACY_STATE_DIR = Path("_autoresearch")

SNIPPET = """<!-- AUTO SELF IMPROVE LOOP START -->
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
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install an auto self-improve loop into a skill folder."
    )
    parser.add_argument("target", help="Path to the target skill folder")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Refresh installed tooling files without touching existing improvement state",
    )
    parser.add_argument(
        "--reset-state",
        action="store_true",
        help="Also overwrite existing files in _auto_self_improve/",
    )
    return parser.parse_args()


def ensure_skill_dir(target: Path) -> Path:
    skill_md = target / "SKILL.md"
    if not skill_md.is_file():
        raise SystemExit(f"Target skill is missing SKILL.md: {skill_md}")
    return skill_md


def migrate_legacy_state(target_root: Path) -> bool:
    legacy_dir = target_root / LEGACY_STATE_DIR
    state_dir = target_root / STATE_DIR
    if legacy_dir.exists() and not state_dir.exists():
        legacy_dir.rename(state_dir)
        return True
    return False


def copy_template_files(
    template_root: Path, target_root: Path, force: bool, reset_state: bool
) -> list[str]:
    state_files = {
        Path("_auto_self_improve/CURRENT_FOCUS.md"),
        Path("_auto_self_improve/IMPROVEMENT_BACKLOG.md"),
        Path("_auto_self_improve/LESSONS.md"),
        Path("_auto_self_improve/INVARIANTS.md"),
        Path("_auto_self_improve/RUN_LOG.jsonl"),
    }
    copied: list[str] = []
    for source in template_root.rglob("*"):
        if source.is_dir():
            continue
        if source.name == ".DS_Store" or "__pycache__" in source.parts:
            continue
        relative = source.relative_to(template_root)
        destination = target_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if relative in state_files and not reset_state:
                continue
            if relative not in state_files and not force:
                continue
        if destination.exists() and relative in state_files and not reset_state:
            continue
        shutil.copy2(source, destination)
        copied.append(str(relative))
    return copied


def inject_snippet(skill_md: Path) -> bool:
    original = skill_md.read_text(encoding="utf-8")
    if MARKER_START in original and MARKER_END in original:
        return False

    if LEGACY_MARKER_START in original and LEGACY_MARKER_END in original:
        start = original.index(LEGACY_MARKER_START)
        end = original.index(LEGACY_MARKER_END) + len(LEGACY_MARKER_END)
        updated = original[:start] + SNIPPET + original[end:]
        skill_md.write_text(updated, encoding="utf-8")
        return True

    snippet = SNIPPET.strip() + "\n\n"

    if original.startswith("---\n"):
        parts = original.split("---\n", 2)
        if len(parts) == 3:
            updated = f"---\n{parts[1]}---\n\n{snippet}{parts[2].lstrip()}"
            skill_md.write_text(updated, encoding="utf-8")
            return True

    updated = f"{snippet}{original.lstrip()}"
    skill_md.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    template_root = root / "templates"
    target = Path(args.target).expanduser().resolve()

    skill_md = ensure_skill_dir(target)
    migrated = migrate_legacy_state(target)
    copied = copy_template_files(template_root, target, args.force, args.reset_state)
    injected = inject_snippet(skill_md)

    print(f"Installed into: {target}")
    if migrated:
        print("Migrated legacy _autoresearch directory to _auto_self_improve")
    if copied:
        print("Copied files:")
        for item in copied:
            print(f"  - {item}")
    else:
        print("No template files copied; existing files were kept.")

    if injected:
        print("Injected embedded improvement loop into SKILL.md")
    else:
        print("SKILL.md already contained the embedded improvement loop.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
