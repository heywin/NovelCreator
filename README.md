# Novel Creator

Novel Creator is a portable long-form fiction workflow for AI-assisted novel writing.

The goal is to let an AI plan, draft, continue, revise, and QA a multi-chapter novel without relying on one model's hidden memory. The durable memory lives in project files.

## Start Here

Tell the AI:

```text
Read AI_START_HERE.md first. If this is a new project, create the full novel control pack for my requested topic, length, and chapter count. Show me the story design before drafting. When I say start, draft chapter by chapter and deliver the final QA report.
```

For an existing project:

```text
Read AI_START_HERE.md first. Use this project path. Detect whether PROJECT_ENTRY.md exists, then continue from the current state until the manuscript is complete and QA'd.
```

## Repository Layout

```text
AI_START_HERE.md
skills/
  longform-fiction-studio/
    SKILL.md
    references/
    scripts/
```

Generated novel projects should be created under `novels/`, but `novels/` is ignored by git by default so manuscripts are not accidentally committed.

## Basic Commands

Create a new project:

```bash
python3 skills/longform-fiction-studio/scripts/init_project.py novels/my-novel
```

Validate a project:

```bash
python3 skills/longform-fiction-studio/scripts/validate_project.py novels/my-novel
```

## What The Workflow Enforces

- one startup entry for new and existing projects
- one project entry per novel project
- character bible, relationship map, timeline, plot lines, chapter roadmap
- continuity ledger with evidence status
- active state with line heat
- chapter cards for low-context drafting
- batch literary revision after every 3-6 chapters
- final validation and quality report

## Important Rule

Do not draft from hidden memory. Read `AI_START_HERE.md`, then either create a new project or follow the existing project's `PROJECT_ENTRY.md`.
