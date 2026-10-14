# Project Entry Template

Use `PROJECT_ENTRY.md` as the first file a new actor reads when taking over a novel. Keep it short and current. Link to workflow task IDs and actual files rather than duplicating mutable status tables.

```markdown
# Project Entry

## Purpose

Project files are durable memory. Continue the authorized task or batch after inspecting actual manuscript versions. Drafted, reviewed and accepted are different milestones.

## Required Read Order

1. This entry and the repository's `AI_START_HERE.md`.
2. `workflow.json`: contract, actor assignment, current tasks, issues and review versions.
3. `00-project-overview.md`: creative intent and scope.
4. `08-active-state.md` and `06-continuity-ledger.md`: accepted state and open loops.
5. Relevant `04-plot-lines.md`, `05-chapter-roadmap.md` and `chapter-cards/NN-card.md`.
6. Relevant cast, relationship, timeline and style entries.
7. Actual recent chapters and review reports needed for the task.

Read the local skill and its collaboration protocol/schema before changing operational records. Do not load the full book for a small drafting task; whole-book review requires full-book coverage.

## Current Handoff

- Authorized scope and batch stop:
- User creative-review points and decisions already received:
- Accepted chapters:
- Drafted but not accepted chapters:
- Current task ID and actual assigned actor:
- Pending issue IDs and review reports:
- Next ready task and prerequisites:
- Last observed manuscript versions and check result:

## Story State

- Current story position:
- Facts confirmed:
- Facts claimed but not confirmed:
- Who knows the key information:
- Plotlines due to return:
- Forbidden drift:

## Before Work

- Compare actual files/hashes with workflow records; stale approvals require fresh review.
- For legacy projects, inspect first and initialize missing workflow records without overwriting prose or inferring approval.
- Honor user review points without re-asking settled questions.
- Confirm task prerequisites, allowed write paths, scene goals and count budget.
- Resolve outstanding repairs before drafting dependent chapters.

## Role Handoff

- Writer delivers assigned prose and proposed new facts/state changes.
- Continuity and literary editors submit independent version-bound review evidence.
- Writer repairs; editors verify the new version in context.
- Supervisor alone merges workflow, continuity, active state, timeline and relationship updates, then accepts.
- After editing earlier events, supervisor identifies affected later chapters for recheck.

## Batch Boundary

- Summarize literary findings in `09-literary-revision.md` using issue IDs.
- Update this handoff with exact unfinished work and next task.
- Run progress validation and report accepted versus pending work.
- Stop at the authorized boundary; do not declare full-book completion.

## Full Delivery

When in scope, follow the skill's revision protocol. Require all chapters to meet the fixed count contract, pass repetition checks, have fresh two-role reviews and supervisor acceptance, and receive fresh final whole-book reviews from both editors. Resolve critical/high findings with independent rechecks. Write `QUALITY_REPORT.md`, run release validation and report limitations honestly.

From the repository root:

    python3 -B skills/longform-fiction-studio/scripts/inspect_project.py <project-root> --json
    python3 -B skills/longform-fiction-studio/scripts/validate_project.py <project-root> --stage progress
    python3 -B skills/longform-fiction-studio/scripts/validate_project.py <project-root> --stage release
```
