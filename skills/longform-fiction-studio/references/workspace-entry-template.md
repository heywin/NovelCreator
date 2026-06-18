# Workspace Entry Template

Use this file as the model for a workspace-level entry such as `AI_START_HERE.md`.

The workspace entry is different from `PROJECT_ENTRY.md`, but it should be the single startup file the user can point any AI to:

- `AI_START_HERE.md` teaches a new AI how to use the whole workspace and skill package.
- `PROJECT_ENTRY.md` teaches a new AI how to continue one specific novel project.

Startup rule:

1. Read `AI_START_HERE.md`.
2. If a target path contains `PROJECT_ENTRY.md`, it is an existing project.
3. If a target path lacks `PROJECT_ENTRY.md` but has novel control files, repair the project by adding `PROJECT_ENTRY.md`.
4. If there is no target project, create a new project under `novels/`.

Minimum sections:

- Core Principle
- First Decision: New Project Or Existing Project
- Path A: Start A New Novel Project
- Path B: Continue An Existing Novel Project
- Required Project Files
- Acceptance Standard
- User-Facing Shortcut

The workspace entry should explain the whole lifecycle:

1. User gives genre, topic, target length, and chapter count.
2. AI builds the project control pack.
3. AI presents the story design for user feedback.
4. User says start.
5. AI drafts chapter by chapter.
6. AI updates continuity and active state after every chapter or batch.
7. AI runs batch literary revision.
8. AI validates continuity and narrative boundary, then writes final quality report.
9. AI delivers the manuscript paths and quality verdict.
