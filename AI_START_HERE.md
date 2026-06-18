# AI Start Here

This is the single startup entry file for this Novel Creator repository.

If you are a new AI taking over this workspace or a novel project inside it, read this file first. Do not ask the user whether this is a new or old project until you have checked the target path.

## Core Principle

Novel creation in this workspace must not depend on one AI's hidden memory. The durable memory is stored in project files.

Use the local skill package:

- `skills/longform-fiction-studio/SKILL.md`
- `skills/longform-fiction-studio/references/methodology.md`
- `skills/longform-fiction-studio/references/project-template.md`
- `skills/longform-fiction-studio/references/project-entry-template.md`

## First Decision: New Project Or Existing Project

Always start with this decision.

### If The User Gives A Project Path

Check whether the target path contains:

`PROJECT_ENTRY.md`

If it exists, this is an existing novel project. Follow **Path B: Continue An Existing Novel Project**.

If it does not exist but the path contains novel-like control files such as `00-project-overview.md`, `chapters/`, or `chapter-cards/`, treat it as an incomplete project and repair it by creating `PROJECT_ENTRY.md` before continuing.

If the path does not exist or has no novel project files, follow **Path A: Start A New Novel Project**.

### If The User Does Not Give A Project Path

If the user asks for a new novel, create a new project under:

`novels/<title-or-slug>/`

If the user asks to continue "this project" or "the current novel", inspect likely project directories under `novels/` and choose the one with `PROJECT_ENTRY.md` only when unambiguous. If ambiguous, ask a short clarification.

All relative paths in this file are relative to the repository root.

## Path A: Start A New Novel Project

Use this path only after the first decision confirms there is no existing project to continue.

### 1. Understand The User Request

Extract and confirm:

- target form: medium-length novel, long novel, serial, novella, etc.
- total target length or per-chapter length
- chapter count
- genre and subject matter
- required tone, audience, taboo boundaries, and any must-have elements
- whether the user wants to approve the story design before drafting

If the user has already provided enough information, do not over-ask. Make reasonable creative choices and proceed.

### 2. Create The Project

Create a project under this workspace, usually:

`novels/<title-or-slug>/`

Run:

```bash
python3 skills/longform-fiction-studio/scripts/init_project.py novels/<title-or-slug>
```

Do not create novel projects in the user's home directory.

### 3. Build The Control Pack Before Drafting

Fill these files before writing chapters:

- `PROJECT_ENTRY.md`
- `00-project-overview.md`
- `01-cast-bible.md`
- `02-relationship-map.md`
- `03-timeline.md`
- `04-plot-lines.md`
- `05-chapter-roadmap.md`
- `06-continuity-ledger.md`
- `07-style-and-voice.md`
- `08-active-state.md`
- `09-literary-revision.md`
- `chapter-cards/NN-card.md` for every planned chapter

The control pack must make the story creatable with low context. Do not rely on hidden planning that is not written into files.

### 4. Present The Story Design To The User

Before drafting the manuscript, summarize:

- title and premise
- genre and target effect
- main characters
- relationship web
- main line and side lines
- chapter roadmap
- ending direction
- risks or open design choices

Wait for user feedback if the user wants to review the design before drafting.

### 5. When The User Says Start

Draft chapter by chapter. For each chapter:

1. Read `PROJECT_ENTRY.md`.
2. Read the project pack needed for the current chapter.
3. Read the current `chapter-cards/NN-card.md`.
4. Draft only the current chapter into `chapters/NN.md`.
5. Update `06-continuity-ledger.md`.
6. Update `08-active-state.md`.
7. Update `03-timeline.md` and `02-relationship-map.md` if facts, time, knowledge, or relationships changed.
8. After every 3-6 chapters, update `09-literary-revision.md`.
9. Continue until the planned manuscript is complete, unless the user asks to pause.

### 6. Final QA And Delivery

After all planned chapters are complete:

- run the project validator
- verify chapter count
- verify chapter lengths or total length against the user's requirement
- check continuity, timeline, character knowledge, relationship changes, line heat, payoff fairness, and style consistency
- write or update `QUALITY_REPORT.md`
- clean temporary files and caches
- report final paths, validation result, length statistics, and quality verdict

Run:

```bash
python3 skills/longform-fiction-studio/scripts/validate_project.py novels/<title-or-slug>
```

## Path B: Continue An Existing Novel Project

Use this path when the target project contains `PROJECT_ENTRY.md`, or when an incomplete project is repaired by adding `PROJECT_ENTRY.md`.

### 1. Read The Project Entry First

Open the target project's entry file:

`<project-root>/PROJECT_ENTRY.md`

Do not draft before reading it.

### 2. Follow Its Read Order

Then read the files listed in that project's `PROJECT_ENTRY.md`, usually:

1. `00-project-overview.md`
2. `08-active-state.md`
3. `06-continuity-ledger.md`
4. `04-plot-lines.md`
5. `05-chapter-roadmap.md`
6. `01-cast-bible.md`
7. `02-relationship-map.md`
8. `03-timeline.md`
9. `07-style-and-voice.md`
10. current or next `chapter-cards/NN-card.md`
11. only the recent completed chapters needed for continuity

### 3. Determine The Next Action

Use `PROJECT_ENTRY.md` and `08-active-state.md` to determine whether the next action is:

- draft the next chapter
- revise an existing chapter
- rebuild a missing chapter card
- repair continuity
- run final QA
- deliver the finished manuscript

### 4. Continue Automatically When Asked

If the user says to continue or start, keep working chapter by chapter until the planned stop point or full manuscript completion. After each chapter or batch, update the control files. Do not make the user restate the whole story.

### 5. Final Delivery

When the remaining work is complete, run validation and produce a final quality report the same way as a new project.

## Required Project Files

Every novel project should contain:

- `PROJECT_ENTRY.md`
- `00-project-overview.md`
- `01-cast-bible.md`
- `02-relationship-map.md`
- `03-timeline.md`
- `04-plot-lines.md`
- `05-chapter-roadmap.md`
- `06-continuity-ledger.md`
- `07-style-and-voice.md`
- `08-active-state.md`
- `09-literary-revision.md`
- `chapters/`
- `chapter-cards/`

## Acceptance Standard

A project is not complete just because chapters exist. It is complete only when:

- all planned chapters exist
- chapter lengths match the user's requested range or scale
- continuity files are updated
- line heat has no unplanned cold lines
- evidence status is clear where facts are disputed
- batch literary revision has been run
- final quality report exists
- validator passes

## User-Facing Shortcut

For a new project, the user can say:

> Read `AI_START_HERE.md`, then create or continue the appropriate novel project. If it is new, use this topic, length, and chapter count. Show me the story design first. When I say start, draft the whole manuscript chapter by chapter and deliver it after QA.

For an existing project, the user can say:

> Read `AI_START_HERE.md`, use the project path I provide, detect whether `PROJECT_ENTRY.md` exists, then continue from the current state until the manuscript is complete and QA'd.
