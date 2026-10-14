---
name: longform-fiction-studio
description: Plan, draft, review, and revise long-form fiction through supervisor, planner, writer, continuity-editor, and literary-editor roles with scene tasks, versioned reviews, and durable continuity. Use for creating or continuing novels, repairing a novel workflow, and managing chapter or batch handoffs.
---

# Longform Fiction Studio

Use project files as durable memory. Separate story invention, prose production, independent review and acceptance. Work to the user's chapter or batch boundary; whole-book completion is not the default.

Read workspace `AI_START_HERE.md` when available, then the selected project's `PROJECT_ENTRY.md`. Inspect existing files before deciding a project is new. Preserve existing prose and user changes when adding the collaboration workflow.

## Roles And Ownership

The five roles are `supervisor`, `planner`, `writer`, `continuity_editor` and `literary_editor`. The supervisor owns task assignment, canonical-state merges and acceptance. Planner and writer propose changes; editors provide evidence and rechecks. Authors must not review or accept their own deliverables. Use actual actor identities, not five labels that disguise one self-approval.

Read [collaboration-protocol.md](references/collaboration-protocol.md) when assigning or performing roles, and [workflow-schema.md](references/workflow-schema.md) before editing `workflow.json`. Separate sessions can fulfill roles; use parallel agents only when delegation is available and authorized. This skill does not create a background runner or imply permission to message external parties.

## Essential Workflow

1. Lock the creative requirements, chapter count, total/chapter length ranges and count mode. Honor user design review and batch stop points; do not re-request settled decisions.
2. Build compact Markdown controls from [project-template.md](references/project-template.md). Initialize `workflow.json` non-destructively with `scripts/init_workflow.py`; explicitly assign actors and complete the task scaffold.
3. Planner decomposes the next chapter into scenes with entry state, goal, resistance, choice, consequence, exit state and length budget. Supervisor checks readiness.
4. Writer drafts only the assigned chapter and proposes state changes. Dependent chapters are written sequentially.
5. Run `scripts/inspect_project.py` and `scripts/validate_project.py --stage progress` against the project root. Repair mechanical failures and verify counts under the fixed convention.
6. Both editors read the submitted version and record located evidence. Writer repairs; editors recheck the new version. Critical/high findings cannot be deferred past acceptance.
7. Supervisor checks reviews and repair evidence, merges continuity/active-state changes, and accepts the chapter. Do not draft dependent prose against stale state.
8. At the agreed batch boundary, summarize literary findings and hand off. Whole-book delivery additionally requires fresh two-role book reviews and `--stage release` validation under [revision-protocol.md](references/revision-protocol.md).

## Invariants

- A file's existence, an old quality report or a passing progress check is not acceptance.
- Reviews and acceptance must refer to the current manuscript hash. Any prose edit invalidates prior approval for that version; substantive changes also trigger downstream review.
- Count body text using the contract's `han` or `nonspace` mode. Do not switch modes or lower targets to conceal shortfall. Add missing conflict, response or consequence rather than repeated filler.
- Track disputed facts as `observed`, `claimed`, `inferred`, `confirmed` or `contradicted`; keep labels in controls, not fiction.
- Track plotline last appearance, present pressure and next return. Repair an unplanned cold line before advancing affected tasks.
- Translate plans into in-world action, dialogue, perception and consequence. Flag process commentary or control-language leaks, while judging naturally occurring words in context.
- Never alter established story truth merely to make a contradiction disappear. The supervisor must reconcile a proposed change and its downstream effects.
- Mechanical validation checks records and deterministic constraints; it cannot prove review authenticity or literary merit. Reviewers must read actual prose and cite real evidence.

## Focused References

- [methodology.md](references/methodology.md): story design, chapter-card structure, continuity and literary diagnostics.
- [collaboration-protocol.md](references/collaboration-protocol.md): role inputs, outputs, handoff and supervision.
- [workflow-schema.md](references/workflow-schema.md): authoritative machine-readable fields and state rules.
- [project-template.md](references/project-template.md): project file layout and control-pack content.
- [project-entry-template.md](references/project-entry-template.md): low-context project handoff.
- [workspace-entry-template.md](references/workspace-entry-template.md): workspace startup routing.
- [revision-protocol.md](references/revision-protocol.md): repairs, independent rechecks and full release.
