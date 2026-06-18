#!/usr/bin/env python3
"""Validate a long-form fiction project scaffold and batch-control files."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REQUIRED_FILES = [
    "PROJECT_ENTRY.md",
    "00-project-overview.md",
    "01-cast-bible.md",
    "02-relationship-map.md",
    "03-timeline.md",
    "04-plot-lines.md",
    "05-chapter-roadmap.md",
    "06-continuity-ledger.md",
    "07-style-and-voice.md",
    "08-active-state.md",
    "09-literary-revision.md",
]

REQUIRED_DIRS = ["chapters", "chapter-cards"]

REVISION_SECTIONS = [
    "### Quality Verdict",
    "### Strong Scenes",
    "### Weak Scenes",
    "### Convenience Risks",
    "### Interior Arc Notes",
    "### Texture And World Notes",
    "### Rhythm And Length Notes",
    "### Required Revisions Before Next Batch",
]


def has_content_after(content: str, heading: str) -> bool:
    start = content.find(heading)
    if start == -1:
        return False
    rest = content[start + len(heading) :]
    next_heading = rest.find("\n### ")
    section = rest if next_heading == -1 else rest[:next_heading]
    return any(line.strip() and not line.strip().startswith("#") for line in section.splitlines())


def validate(root: Path, min_chapters_for_revision: int) -> list[str]:
    errors: list[str] = []

    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append(f"missing required file: {name}")

    for name in REQUIRED_DIRS:
        if not (root / name).is_dir():
            errors.append(f"missing required directory: {name}")

    ledger = root / "06-continuity-ledger.md"
    if ledger.is_file():
        text = ledger.read_text(encoding="utf-8")
        if "Evidence status:" not in text or "| Fact | Source | Evidence status |" not in text:
            errors.append("continuity ledger does not use evidence-status format")

    active = root / "08-active-state.md"
    if active.is_file():
        text = active.read_text(encoding="utf-8")
        if "## Active Line Heat" not in text:
            errors.append("active state is missing line heat table")

    entry = root / "PROJECT_ENTRY.md"
    if entry.is_file():
        text = entry.read_text(encoding="utf-8")
        required_entry_sections = [
            "## Required Read Order",
            "## Skill And Method",
            "## Current Progress",
            "## Handoff Brief",
            "## Before Drafting Next Text",
            "## After Drafting",
            "## Completion And Delivery",
        ]
        for section in required_entry_sections:
            if section not in text:
                errors.append(f"project entry missing section: {section}")

    chapters_dir = root / "chapters"
    chapter_count = len(sorted(chapters_dir.glob("*.md"))) if chapters_dir.is_dir() else 0
    revision = root / "09-literary-revision.md"
    if chapter_count >= min_chapters_for_revision and revision.is_file():
        text = revision.read_text(encoding="utf-8")
        for section in REVISION_SECTIONS:
            if section not in text:
                errors.append(f"literary revision missing section: {section}")
            elif not has_content_after(text, section):
                errors.append(f"literary revision section is empty: {section}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", help="Novel project directory")
    parser.add_argument("--min-chapters-for-revision", type=int, default=3)
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    errors = validate(root, args.min_chapters_for_revision)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Project is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
