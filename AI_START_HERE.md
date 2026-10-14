# AI Start Here

This is the repository startup entry. Read the local [skill](skills/longform-fiction-studio/SKILL.md), then the target project's `PROJECT_ENTRY.md` when present. Project files are durable memory; do not resume from hidden recollection or a previous completion claim.

## Detect The Project

- If the user provides a path, inspect it first. An entry file or existing control files/chapters means an existing project.
- If continuing without a path, select a project under `novels/` only when unambiguous; otherwise ask which project.
- For a new novel, create `novels/<title-or-slug>/` using the [project template](skills/longform-fiction-studio/references/project-template.md).
- For an incomplete old project, preserve the manuscript, inspect it, and add missing control files within the requested scope. Missing workflow records are unverified, not implicitly approved.

## Set The Scope

Extract the requested genre, creative constraints, chapter count, chapter and total length ranges, counting mode, review preference, and batch stop point. Use prior authorization; do not ask again for an already approved design or scope. Resolve ordinary creative details yourself unless the user reserved those decisions.

Default to staged collaboration. If no batch size was specified, plan a small batch, normally three chapters, and state that assumption. Stop at the requested design review or batch boundary. Do not turn “continue” into an instruction to write the whole book. Resume an unfinished repair or review before starting new dependent prose.

## New Project

1. Read the [collaboration protocol](skills/longform-fiction-studio/references/collaboration-protocol.md) and [workflow schema](skills/longform-fiction-studio/references/workflow-schema.md).
2. Create the Markdown control pack. Lock user requirements and count convention in the overview and `workflow.json`; keep their descriptions aligned.
3. Initialize the task scaffold with `init_workflow.py`, supplying chapter count, chapter/total ranges and `han` or `nonspace`. The initializer does not assign actual actors, write fiction, or approve anything.
4. The supervisor assigns real actors and task ownership. Prepare the whole-book direction, then scene-level cards for the current batch; future cards may remain provisional.
5. Present the design if requested. Honor that review boundary; otherwise proceed within the authorized batch.

## Continue An Existing Project

1. Read `PROJECT_ENTRY.md`, `workflow.json` if present, current active state, unresolved issues and relevant chapter cards.
2. Run `inspect_project.py` to compare actual prose, counts, hashes and repetition against claims. A legacy `QUALITY_REPORT.md` is evidence to verify, not a substitute for current reviews.
3. If `workflow.json` is absent, initialize it non-destructively using the known contract. If the contract is materially ambiguous, resolve it before accepting prose. Do not infer completed task states or reviews from file existence.
4. Reconcile stale records and assign the next ready task. Preserve drafts and user changes; migration does not rewrite the novel.
5. Continue through the current batch's repair, review and acceptance work. Record a precise handoff at its boundary.

## Chapter Loop

Follow the role and ownership rules in the collaboration protocol:

1. Planner supplies a chapter card with scene goals, conflicts, choices, consequences, entry/exit state, constraints and length budgets.
2. Supervisor checks dependencies, scope and readiness, then assigns drafting.
3. Writer changes only the assigned prose and submits state-change proposals.
4. Run mechanical inspection and progress validation. Repair length or repetition failures before asking editors to accept the draft.
5. Continuity and literary editors read the actual version, independently of the author's self-assessment, and return located evidence and actionable findings.
6. Writer repairs; editors re-read the affected context and record fresh reviews. Recheck downstream chapters when earlier events change.
7. Supervisor verifies evidence and merges canonical state, then records acceptance. Accepted prose requires both fresh role reviews; authors cannot accept their own work.

Draft dependent chapters sequentially. Parallel review is useful only if the environment supports it and delegation is authorized. Role descriptions alone do not grant tool or communication permissions.

## Batch Handoff

After each batch, update `09-literary-revision.md` with scene thickness, interior motion, convenience risks, rhythm, repetition and required repairs. The supervisor updates the entry and active state with accepted chapters, unfinished tasks, blockers, next action and stop point. Distinguish “drafted,” “reviewed” and “accepted.” A successful progress check does not mean the book is complete.

## Release Acceptance Checklist

Use the [revision protocol](skills/longform-fiction-studio/references/revision-protocol.md) only when full delivery is in scope:

- All planned chapters and chapter cards exist and have substantive content.
- Every chapter and the book total satisfy the locked count convention and ranges.
- Mechanical checks pass, including repetition and narrative-boundary checks.
- All accepted chapters have two fresh role reviews and supervisor acceptance bound to current prose.
- Critical/high issues are resolved and independently rechecked, including affected later chapters.
- Canonical state reflects accepted prose; no unplanned cold plotline or outstanding required payoff remains.
- Both editors have reviewed the current complete book, including opening/ending promise, cumulative pacing and cross-chapter continuity.
- `QUALITY_REPORT.md` reports actual counts, validation output, review evidence and remaining limitations.
- Run `python3 -B skills/longform-fiction-studio/scripts/validate_project.py <project-root> --stage release` and require success before reporting release completion.

Tools check records and deterministic constraints. Editors must still assess the manuscript; literary quality is not certified by an exit code.
