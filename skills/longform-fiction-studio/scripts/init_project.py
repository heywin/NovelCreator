#!/usr/bin/env python3
"""Create a compact long-form fiction project scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


FILES = {
    "PROJECT_ENTRY.md": "# Project Entry\n\n## Purpose\n\nThis is the first file a new AI should read before continuing this novel project. Do not draft from memory. Use the project files below as the source of truth.\n\nIf this project is not drafted yet, use this file to understand the design state and next required step. If the control pack is complete and the user says start, draft chapter by chapter until the planned stop point, updating state after each chapter or batch.\n\n## Required Read Order\n\n1. `PROJECT_ENTRY.md`\n2. `00-project-overview.md`\n3. `08-active-state.md`\n4. `06-continuity-ledger.md`\n5. `04-plot-lines.md`\n6. `05-chapter-roadmap.md`\n7. `01-cast-bible.md`\n8. `02-relationship-map.md`\n9. `03-timeline.md`\n10. `07-style-and-voice.md`\n11. Current or next `chapter-cards/NN-card.md`\n12. Recent completed chapters only, usually the last 1-3 chapter files.\n\n## Skill And Method\n\nFrom the repository root, read `AI_START_HERE.md`, `skills/longform-fiction-studio/SKILL.md`, and `skills/longform-fiction-studio/references/methodology.md` before major planning or drafting work.\n\nCore rule: project files are the memory. Do not rely on a previous AI's hidden context.\n\n## Current Progress\n\n- Completed chapters:\n- Current manuscript state:\n- Next intended task:\n- Next chapter card:\n- User approval state:\n\n## Handoff Brief\n\n- Current story position:\n- Facts confirmed:\n- Facts claimed but not confirmed:\n- Characters who know the key information:\n- Active plot lines that must return:\n- Forbidden drift:\n\n## Before Drafting Next Text\n\n- If the project design has not been shown to the user yet, summarize the design and wait for feedback.\n- If the user has requested changes, apply them to the control pack before drafting.\n- Confirm the next chapter's dominant purpose.\n- Check `08-active-state.md` line heat.\n- Check `06-continuity-ledger.md` for open loops and evidence status.\n- Read only the relevant recent chapters, not the whole manuscript unless auditing continuity.\n\n## After Drafting\n\n- Update `06-continuity-ledger.md`.\n- Update `08-active-state.md`.\n- Update `03-timeline.md` if time, location, knowledge, injury, travel, or public events changed.\n- Update `02-relationship-map.md` if a relationship's pressure or status changed.\n- Update `09-literary-revision.md` after every 3-6 chapters.\n- Run `python3 skills/longform-fiction-studio/scripts/validate_project.py <project-root>` from the repository root when available.\n\n## Completion And Delivery\n\n- Confirm all planned chapters exist.\n- Verify chapter lengths or total length.\n- Run continuity, timeline, character-knowledge, relationship, line-heat, payoff, and style checks.\n- Write or update `QUALITY_REPORT.md`.\n- Report final paths and validation results to the user.\n",
    "00-project-overview.md": "# Project Overview\n\n- Title:\n- Genre:\n- Scale:\n- Promise:\n- Audience:\n- Ending direction:\n- Boundaries:\n",
    "01-cast-bible.md": "# Cast Bible\n\n| Name | Role | Desire | Fear | Contradiction | Arc |\n| --- | --- | --- | --- | --- | --- |\n",
    "02-relationship-map.md": "# Relationship Map\n\n| From | To | Relation | Pressure | Debt or Leverage | Change |\n| --- | --- | --- | --- | --- | --- |\n",
    "03-timeline.md": "# Timeline\n\n| Order | Event | Who knows | Why it matters | Downstream effect |\n| --- | --- | --- | --- | --- |\n",
    "04-plot-lines.md": "# Plot Lines\n\n| Line | Function | Stage | Next turn | Collision point |\n| --- | --- | --- | --- | --- |\n",
    "05-chapter-roadmap.md": "# Chapter Roadmap\n\n| Ch | Purpose | Dominant line | Key beat | Exit condition |\n| --- | --- | --- | --- | --- |\n",
    "06-continuity-ledger.md": "# Continuity Ledger\n\nEvidence status: `observed`, `claimed`, `inferred`, `confirmed`, `contradicted`.\n\n| Fact | Source | Evidence status | Status | Risk | Follow-up |\n| --- | --- | --- | --- | --- | --- |\n",
    "07-style-and-voice.md": "# Style and Voice\n\n- Narration stance:\n- Paragraph behavior:\n- Dialogue behavior:\n- Banned habits:\n- Lexical limits:\n",
    "08-active-state.md": "# Active State\n\n- What changed last:\n- What is true now:\n- What must stay true:\n- What to check next:\n\n## Active Line Heat\n\n| Line | Last appeared | Current pressure | Next required return |\n| --- | --- | --- | --- |\n",
    "09-literary-revision.md": "# Literary Revision\n\n## Batch 01\n\n### Quality Verdict\n\n### Strong Scenes\n\n### Weak Scenes\n\n### Convenience Risks\n\n### Interior Arc Notes\n\n### Texture And World Notes\n\n### Rhythm And Length Notes\n\n### Required Revisions Before Next Batch\n\n### Deferred Revisions\n",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", help="Target project directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "chapters").mkdir(exist_ok=True)
    (root / "chapter-cards").mkdir(exist_ok=True)

    for name, content in FILES.items():
        path = root / name
        if path.exists() and not args.force:
            continue
        path.write_text(content, encoding="utf-8")

    print(str(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
