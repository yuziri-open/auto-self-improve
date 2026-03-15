#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
AUTO_DIR = SKILL_ROOT / "_auto_self_improve"
FOCUS_PATH = AUTO_DIR / "CURRENT_FOCUS.md"
BACKLOG_PATH = AUTO_DIR / "IMPROVEMENT_BACKLOG.md"
LESSONS_PATH = AUTO_DIR / "LESSONS.md"
INVARIANTS_PATH = AUTO_DIR / "INVARIANTS.md"
LOG_PATH = AUTO_DIR / "RUN_LOG.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect or record the embedded self-improvement state for a skill."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    summary = subparsers.add_parser("summary", help="Print the current improvement state")
    summary.add_argument("--last", type=int, default=5, help="Number of recent log entries to show")

    record = subparsers.add_parser("record", help="Append a structured run log entry")
    record.add_argument("--task", required=True, help="The user task or task shape")
    record.add_argument("--hypothesis", required=True, help="The experiment hypothesis")
    record.add_argument("--change", required=True, help="What was changed or tried")
    record.add_argument(
        "--outcome",
        required=True,
        choices=["success", "mixed", "failed", "skipped"],
        help="Result of the experiment",
    )
    record.add_argument("--learning", required=True, help="What this run taught us")
    record.add_argument("--next-step", required=True, help="What to do next")
    record.add_argument("--tag", action="append", default=[], help="Optional tag")
    record.add_argument(
        "--promote-lesson",
        action="append",
        default=[],
        help="Stable lesson to append to LESSONS.md",
    )
    record.add_argument(
        "--promote-invariant",
        action="append",
        default=[],
        help="Guardrail to append to INVARIANTS.md",
    )

    return parser.parse_args()


def read_text(path: Path) -> str:
    if not path.exists():
        return "(missing)\n"
    return path.read_text(encoding="utf-8").strip() + "\n"


def read_recent_logs(limit: int) -> list[dict]:
    if not LOG_PATH.exists():
        return []

    entries: list[dict] = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("seed"):
            continue
        entries.append(entry)
    return entries[-limit:]


def append_unique_bullets(path: Path, items: list[str]) -> None:
    clean_items = [item.strip() for item in items if item.strip()]
    if not clean_items:
        return

    existing = read_text(path)
    lines = [
        line
        for line in existing.splitlines()
        if "None yet. Replace this line after the first repeated or clearly validated lesson." not in line
    ]
    seen = set(lines)
    additions = [f"- {item}" for item in clean_items if f"- {item}" not in seen]
    if not additions:
        return

    base = "\n".join(lines).rstrip()
    if base == "(missing)":
        base = f"# {path.stem.replace('_', ' ').title()}\n"
    updated = base + "\n\n" + "\n".join(additions) + "\n"
    path.write_text(updated, encoding="utf-8")


def cmd_summary(last: int) -> int:
    print("== Current Focus ==")
    print(read_text(FOCUS_PATH))
    print("== Backlog ==")
    print(read_text(BACKLOG_PATH))
    print("== Lessons ==")
    print(read_text(LESSONS_PATH))
    print("== Invariants ==")
    print(read_text(INVARIANTS_PATH))
    print("== Recent Runs ==")

    recent = read_recent_logs(last)
    if not recent:
        print("(no real runs logged yet)")
        return 0

    for entry in recent:
        timestamp = entry.get("timestamp", "unknown")
        task = entry.get("task", "")
        outcome = entry.get("outcome", "")
        learning = entry.get("learning", "")
        print(f"- {timestamp} | {outcome} | {task}")
        print(f"  learning: {learning}")
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    AUTO_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task": args.task.strip(),
        "hypothesis": args.hypothesis.strip(),
        "change": args.change.strip(),
        "outcome": args.outcome,
        "learning": args.learning.strip(),
        "next_step": args.next_step.strip(),
        "tags": [tag.strip() for tag in args.tag if tag.strip()],
    }
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=True) + "\n")

    append_unique_bullets(LESSONS_PATH, args.promote_lesson)
    append_unique_bullets(INVARIANTS_PATH, args.promote_invariant)

    print("Appended run log entry.")
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "summary":
        return cmd_summary(args.last)
    if args.command == "record":
        return cmd_record(args)
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
