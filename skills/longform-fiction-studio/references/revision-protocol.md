# Revision And Release Protocol

Use the chapter repair loop throughout a batch. Apply the full release gate only when the entire manuscript is intended for delivery. A completed first draft is not a release candidate.

## Lock And Measure The Contract

At creation, record planned chapters, chapter and total count ranges, and count mode in `workflow.json` according to [workflow-schema.md](workflow-schema.md). Summarize these alongside genre, intended reader effect, creative constraints and deliverables in the overview. Never change requirements merely to make validation pass; record user-authorized scope changes and re-plan affected tasks.

`han` counts Chinese characters in body text; `nonspace` counts non-whitespace body characters, including punctuation. Markdown headings are excluded. Use `inspect_project.py` for actual counts and hashes, not a prose estimate. Check individual chapters and the book total together. Repeated material remains a quality failure even when the raw length target is met.

## Two Accountable Reviews

The continuity editor checks causality, knowledge, time, location, objects, motives, relationships and setup/payoff. The literary editor covers both cold-reader response and line editing: attention, earned emotion, scene thickness, character voice, rhythm, imagery, repetition and narrative boundary.

Review the actual manuscript before the author's explanation. Reports must identify the current version and give located evidence. “Improve pacing” is insufficient; identify the scene, the effect on the reader, the proposed repair and what a successful recheck would show. Record all actionable findings in the structured ledger and link the detailed report. Do not replace review evidence with a generic pass checklist.

## Repair And Independent Recheck

Repair in this order when relevant:

1. Causality, timeline, knowledge and required story facts.
2. Character decisions and relationship pressure.
3. Scene pacing, information, emotional consequence and payoff.
4. Prose, imagery, dialogue, repetition and process-language leaks.

The writer provides a repair explanation; the responsible editor verifies the result. Any prose edit requires fresh chapter review records tied to the new hash before acceptance. After a consequential early-chapter edit, identify and recheck affected later chapters. Changed whole-book content invalidates the previous book review snapshot.

The supervisor alone merges canon and acceptance. Do not change established facts just to remove a contradiction unless that change has been reconciled with the user's requirements and downstream scenes. Critical/high findings must be resolved and independently rechecked; deferred status is not a release bypass. Follow the schema's exact statuses and evidence fields. Summarize the findings in `09-literary-revision.md` using issue IDs; do not invent a second status system.

## Batch Gate

At the user's chapter or batch stop point:

- Confirm what is drafted versus accepted, and what still needs repair or review.
- Update current state, plotline return plans and handoff.
- Run `python3 -B skills/longform-fiction-studio/scripts/validate_project.py <project-root> --stage progress` from the repository root.
- Report results as a batch milestone, not whole-book completion.

## Full Release Gate

After chapter-level acceptance, both editors read the complete current book. Their final reports must address opening/ending promise, cumulative pacing, long-range setup/payoff, knowledge progression, character arc, and cross-chapter repetition. Do not synthesize a whole-book pass by copying chapter reports.

Before delivery:

- Re-read opening and ending together, and every repair target in context.
- Confirm all planned chapters/cards, current review records, acceptance records and canon updates exist.
- Confirm actual chapter and total counts meet the fixed contract, and repetition checks pass.
- Resolve and verify every critical/high issue. Disclose any permitted lower-severity deferral with reason and effect.
- Write `QUALITY_REPORT.md` with current counts, review/report references, remaining limitations and validation results.
- Run `python3 -B skills/longform-fiction-studio/scripts/validate_project.py <project-root> --stage release` and require success before claiming release completion.

Validation verifies record consistency and deterministic constraints. It does not establish reviewer independence outside recorded actor IDs, prove that an actor read the text, or certify literary merit. The supervisor must assess the cited evidence and the prose itself.
