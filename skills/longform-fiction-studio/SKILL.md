---
name: longform-fiction-studio
description: Design, plan, draft, and revise long-form fiction projects with many characters, multiple plotlines, continuity tracking, chapter sequencing, and low-context continuation. Use when creating or repairing a novel workflow, character bible, relationship map, timeline, chapter roadmap, or chapter draft that must stay coherent across a large manuscript.
---

# Longform Fiction Studio

## Overview

Use this skill to run a long novel like a production system: separate story invention, continuity control, chapter planning, and drafting. Keep the AI creative, but force every chapter to obey project truth, cast truth, timeline truth, and line-tracking truth.

The model should not rely on a giant prompt. Instead, load only the current project pack and the current chapter card, then update shared state after each step.

If available in a workspace, read the unified startup entry first, usually `AI_START_HERE.md`. It explains how to detect whether the target is a new project or an existing project. If the target contains `PROJECT_ENTRY.md`, treat it as an existing project and follow that file's handoff rules. If no project entry exists, create or repair the project before drafting.

## Core Model

Treat the work as four roles:

1. Story lead: decides the main direction, ending pressure, and thematic cost.
2. Continuity supervisor: checks names, dates, relationships, geography, props, and previous commitments.
3. Line producer: keeps main line, side lines, and chapter load balanced.
4. Drafting writer: turns the current plan into prose without expanding beyond the active brief.

Do not merge these roles into one undifferentiated outline. Separate them in the project files.

## Required Project Files

Create and maintain these files for every novel project:

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

Use these files as the canonical source of truth.

`PROJECT_ENTRY.md` is the handoff and startup file. A new AI should read it first to learn the read order, current progress, next intended task, and which project files must be updated after drafting. It should not contain the whole novel; it should point to the right control files and summarize the active handoff state.

## Hard Operating Rules

- After every chapter or chapter batch, update `06-continuity-ledger.md` and `08-active-state.md` before drafting more text.
- Treat state writeback as part of acceptance, not cleanup.
- Do not advance to the next chapter if the active state still describes the pre-chapter state.
- Track evidence status explicitly when a fact matters: `observed`, `claimed`, `inferred`, `confirmed`, or `contradicted`.
- Track line heat in `08-active-state.md` for active plot lines: last appeared, current pressure, and next required return.
- If a side line has gone cold without a return plan, stop and restore it in the roadmap before continuing.
- After every 3-6 chapters, run a literary revision gate before drafting the next batch.
- Do not treat logical coherence as finished literary quality. Check scene thickness, inner arc, anti-convenience, rhythm, and lived texture.
- Keep narrative levels separate. Control files may use planning language, but chapter manuscripts must not mention the author, reader, chapter purpose, plot line, theme, evidence label, continuity ledger, line heat, chapter card, or future payoff.

## Workflow

### 1. Align the project

Before drafting, lock:

- genre and target effect
- main promise
- ending direction
- protagonist pressure
- cast size and relation density
- main line and side lines

If these are not clear, ask for them first.

### 2. Build the control pack

Fill the project files with compact, reusable truth:

- `00-project-overview.md`: premise, scope, rules, target length
- `01-cast-bible.md`: stable character facts, speech traits, motives, secrets, arcs
- `02-relationship-map.md`: ties, tensions, debts, alliances, contradictions
- `03-timeline.md`: chronological events, ages, travel, public events, causality
- `04-plot-lines.md`: main line, side lines, turning points, convergence points
- `05-chapter-roadmap.md`: chapter purpose, load, POV, payoff, cliff or hinge
- `06-continuity-ledger.md`: constraints, open loops, callbacks, unresolved promises
- `07-style-and-voice.md`: diction, sentence rhythm, POV distance, banned habits
- `08-active-state.md`: what is currently true, what was just changed, what must be remembered next
- `09-literary-revision.md`: batch-level quality findings, revision tasks, and prose-level risks
- `PROJECT_ENTRY.md`: first-read handoff file, read order, current progress, next task, forbidden drift, and post-draft update checklist

Keep entries short and factual. Prefer tables or bullet lists over essays.

### 3. Draft by chapter

For each chapter:

- read only the current project pack and the current chapter card
- choose one dominant purpose for the chapter
- keep all subplots subordinate to that purpose
- draft only what the current state supports
- translate control intent into scene, action, dialogue, object, silence, and perception
- reject manuscript text that leaks control language or addresses the reader
- update continuity and active state immediately after the chapter

Do not draft a chapter from memory alone.

### 4. Validate before release

Check the draft against:

- character consistency
- timeline consistency
- relationship consistency
- payoff fairness
- line balance
- style consistency
- chapter purpose
- narrative boundary: no fourth-wall break, author note, reader address, control-file label, or writing-intent explanation inside the manuscript

If any check fails, repair the project files first, then rewrite.

### 5. Run batch literary revision

After every 3-6 chapters, update `09-literary-revision.md` with:

- whether the batch feels like scenes, not task completion
- where evidence appears too conveniently
- where characters need more interior motion
- where life texture is too thin
- where chapter length or rhythm feels compressed
- which scenes need expansion, delay, misdirection, or quieter aftermath

Do not continue the next batch until the high-priority revision tasks are either applied or consciously deferred.

## Low-Context Operating Rule

To save tokens, keep two layers of memory:

- persistent project files for stable truth
- one short active brief for the current chapter

The active brief should usually contain:

- chapter number
- chapter goal
- current POV
- required callbacks
- forbidden drift
- expected end condition
- evidence status for disputed facts
- active line heat for dominant and secondary lines

Do not carry the whole novel into each prompt.

## Typical Uses

- start a new multi-character novel
- build a character bible and relationship graph
- convert a vague idea into a chapter-by-chapter plan
- continue a serialized novel with limited context
- repair continuity drift or dropped plotlines
- split a large novel into controllable chapters and arcs

## Helpful References

- `references/methodology.md`: fiction production method and validation rules
- `references/project-template.md`: compact file layout for a new novel project
- `references/project-entry-template.md`: handoff file layout for one project
- `references/workspace-entry-template.md`: workspace-level startup rules for new and existing projects

## Project Creation

A new AI should create the project folders and Markdown control files from `AI_START_HERE.md` and `references/project-template.md`, then validate the work with the acceptance checklist in `AI_START_HERE.md` and the validation questions in `references/methodology.md`.
