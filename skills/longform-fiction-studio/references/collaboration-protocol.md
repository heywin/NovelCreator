# Collaboration Protocol

Use one supervisor to coordinate a bounded batch. This is a file-based operating protocol for AI sessions or authorized agents, not an automatic scheduler. Roles should have separate review context and actual actor identities. Do not invent independent reviewers or record a review that was never performed.

The exact JSON fields, status vocabulary and hashes are defined in [workflow-schema.md](workflow-schema.md). This document describes how to produce trustworthy records rather than redefining that schema.

## Roles

| Role | Required input | Deliverable | Write boundary |
| --- | --- | --- | --- |
| `supervisor` | User scope, workflow, control pack, actual drafts, findings | Ready tasks, assignments, acceptance decision, merged state, next handoff | Sole merge owner for `workflow.json`, accepted controls and acceptance records |
| `planner` | Contract, cast, lines, accepted state, prior payoff commitments | Chapter/scene plans, budgets, proposed setting or roadmap changes | Assigned planning files; proposes canonical changes |
| `writer` | Ready task, chapter card, relevant accepted state, style guide | Assigned prose, deviations, state-change proposals and repair explanation | Assigned chapter files; never self-accepts |
| `continuity_editor` | Contract, actual manuscript, relevant timeline/knowledge/ledger | Located contradictions, impact, proposed acceptance criteria and repair recheck | Assigned review report; never silently changes canon |
| `literary_editor` | Contract, actual manuscript, style guide, chapter purpose | Reader response, scene/pacing/voice findings, repetition analysis and recheck | Assigned review report; never repairs by lowering the contract |

A reviewer must be a different actor from the author of the reviewed prose. Preserve that separation during repairs; if an editor writes replacement prose, arrange another qualified reviewer for that revision. The supervisor must also be separate from the author whose work is being accepted. Role names alone do not establish independence.

If independent sessions are unavailable, save a draft and a pending independent-review task rather than claiming release acceptance. The user may perform a role where appropriate; do not record their approval without an actual decision.

## Contract And Task Decomposition

At creation, record chapter count, chapter and total count ranges, count mode, genre, intended reader effect, required beats, prohibited drift, user review points and the current batch stop. Requirements belong in `workflow.json` and a readable overview; follow the schema for which fields are executable. Keep creative constraints in Markdown where they need explanation.

The workflow stores one task per chapter, progressing through planning, drafting, reviewing, repairing and acceptance. The supervisor assigns each role its step within that task; do not add separate phase tasks outside the schema. Each assignment must answer:

- What specific artifact or version is its input?
- What may this actor change, and what must remain a proposal?
- Which earlier task or accepted state must exist first?
- What will be delivered, and who checks it?
- What concrete result will count as done?

Use the schema's task and scene fields as the source of truth. Chapter cards reference scene IDs and add prose guidance only where useful; do not duplicate mutable budgets or states. Keep repair work attached to the original issue and chapter so it cannot disappear into a new task list.

A scene record contains the schema's stable ID, goal, entry state, conflict, exit state and minimum/maximum budget. The card may explain viewpoint/time/place, the pivotal decision and its consequence by referencing that scene ID. The sum of scene budgets should fit the chapter range with room for revision. For a 6,000–8,000-character chapter, an initial target near 7,000 is a useful starting point, not a mandatory formula. A short draft requires diagnosis of missing dramatic material before extension.

## Dispatch And Review Packet

Give each actor a compact packet:

```text
Role and actual actor ID:
Assigned task and authorized chapter/scene:
Read these exact files and versions:
Dependencies and accepted entry state:
Required outcome and constraints:
Allowed write paths:
Deliverable and acceptance criteria:
Return findings/proposed state changes to the supervisor:
Stop after this task; do not claim project completion:
```

A drafting packet should include relevant canon and style, not the entire repository. An editor must read the real prose, contract and necessary canon before reading the writer's explanation or prior quality verdict. This reduces pressure to rubber-stamp the author. Later repair rechecks should include the original finding and the affected neighboring scenes.

## Chapter Cycle

1. **Plan:** Planner supplies scene tasks and budgets; supervisor resolves missing prerequisites and assigns the work.
2. **Draft:** Writer writes the assigned chapter and lists deviations or newly introduced facts. Proposed facts are not automatically accepted canon.
3. **Measure:** Use the scripts to inspect actual body counts, hashes, long exact-paragraph repetition and process-language flags; editors also check near-duplicates and repeated narrative structure. Repair objective failures; explain any intentional repetition with precise locations rather than blanket exemptions.
4. **Review:** Both editors independently assess the same submitted version. Each report names the reviewed version, inspected scope, evidence locations, issue severity, desired correction and passing conditions. A pass still needs substantive evidence of what was checked.
5. **Repair:** Writer changes assigned targets. Refresh hashes and mechanical results. Reopen relevant review work; old passes do not apply to edited prose.
6. **Recheck:** Editors verify the correction in context and check newly affected facts or scenes. A writer's “fixed” message is not a resolution decision.
7. **Accept:** Supervisor checks both fresh reviews, issue dispositions, actual measurements and state proposals; merges accepted canon and records acceptance for that exact version.

Dependent prose waits until the preceding chapter is accepted and state is current. Planning future chapters may continue provisionally. Parallel editor reviews are safe when both are read-only against a fixed manuscript; use them only within authorized delegation. Do not have several actors concurrently edit shared canon or the same chapter.

## Supervision And Recovery

`workflow.json` is the canonical operational ledger. `PROJECT_ENTRY.md`, `08-active-state.md` and `09-literary-revision.md` are readable handoff/story views; reference task and issue IDs rather than maintaining contradictory status lists. The supervisor merges role reports into the ledger after checking the actual artifacts. Keep review reports as evidence.

On every resumption, compare stored hashes with actual files, inspect open issues and select a task with satisfied dependencies. Do not infer acceptance from a filename, a prior conversation summary, or the fact that a chapter is long enough. After a major rewrite, explicitly identify downstream chapters whose knowledge, timeline, motivation or payoff depends on the change and re-review them.

If the same correction fails repeatedly, the supervisor should re-plan the scene or narrow the task. Record the unresolved condition and next action when progress cannot continue; do not invent a pass, weaken the contract, or keep repeating an ineffective rewrite. Creative decisions reserved by the user remain review points. Ordinary implementation choices and already-authorized work need no renewed permission.

## Batch And Book Boundaries

At the chosen batch boundary, run progress validation, summarize literary findings, and provide accepted/drafted/pending chapter counts with the next task. A staged project may pass progress checks while still having future work. Preserve the remaining scope and stop where requested.

Before full delivery, follow [revision-protocol.md](revision-protocol.md): every chapter needs current two-role reviews and supervisor acceptance, and the whole current book needs final reviews by both editors. Critical/high issues cannot be deferred. Low/medium deferrals need reasons, effects and a follow-up decision as defined by the schema. Report limitations honestly; neither a reviewer record nor a script exit code proves literary quality.
