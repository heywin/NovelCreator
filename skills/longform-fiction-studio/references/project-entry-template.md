# Project Entry Template

Use `PROJECT_ENTRY.md` as the first file a new AI reads when taking over a novel project.

It should be short, current, and operational. It must not become a second manuscript or a duplicate of every control file.

```markdown
# Project Entry

## Purpose

This is the first file a new AI should read before continuing this novel project. Project files are the memory.

If this project is not drafted yet, use this file to understand the design state and next required step. If the control pack is complete and the user says start, draft chapter by chapter until the planned stop point, updating state after each chapter or batch.

## Required Read Order

1. `PROJECT_ENTRY.md`
2. `00-project-overview.md`
3. `08-active-state.md`
4. `06-continuity-ledger.md`
5. `04-plot-lines.md`
6. `05-chapter-roadmap.md`
7. `01-cast-bible.md`
8. `02-relationship-map.md`
9. `03-timeline.md`
10. `07-style-and-voice.md`
11. Current or next `chapter-cards/NN-card.md`
12. Recent completed chapters only, usually the last 1-3 chapter files.

## Skill And Method

From the repository root, read the local longform-fiction method if available:

- `AI_START_HERE.md`
- `skills/longform-fiction-studio/SKILL.md`
- `skills/longform-fiction-studio/references/methodology.md`

Core rule: do not draft from hidden memory.

## Current Progress

- Completed chapters:
- Current manuscript state:
- Next intended task:
- Next chapter card:
- User approval state:

## Handoff Brief

- Current story position:
- Facts confirmed:
- Facts claimed but not confirmed:
- Characters who know the key information:
- Active plot lines that must return:
- Forbidden drift:

## Before Drafting Next Text

- If the project design has not been shown to the user yet, summarize the design and wait for feedback.
- If the user has requested changes, apply them to the control pack before drafting.
- Confirm the next chapter's dominant purpose.
- Confirm the current chapter card has a `Narrative Boundary` section.
- Check `08-active-state.md` line heat.
- Check `06-continuity-ledger.md` for open loops and evidence status.
- Read only the relevant recent chapters unless auditing continuity.

## After Drafting

- Update `06-continuity-ledger.md`.
- Update `08-active-state.md`.
- Update `03-timeline.md` if time, location, knowledge, injury, travel, or public events changed.
- Update `02-relationship-map.md` if relationship pressure or status changed.
- Update `09-literary-revision.md` after every 3-6 chapters.
- Run the manual acceptance checklist in `AI_START_HERE.md`.

## Completion And Delivery

- Confirm all planned chapters exist.
- Verify chapter lengths or total length.
- Run continuity, timeline, character-knowledge, relationship, line-heat, payoff, and style checks.
- Run narrative-boundary checks on `chapters/`: no author notes, reader address, writing-process language, control-card labels, evidence-status labels, line-heat labels, or project-file references inside manuscript text.
- Write or update `QUALITY_REPORT.md`.
- Report final paths and validation results to the user.
```
