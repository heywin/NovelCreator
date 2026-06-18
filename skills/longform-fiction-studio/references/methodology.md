# Longform Fiction Methodology

## Source Ideas To Reuse

Human long-form creation separates invention from control.

- Novelists use outlines, character notes, timelines, and revision passes to prevent late-book collapse.
- TV writers use a story room to break season arcs, episode beats, character turns, and cliff points before scripts are written.
- Film and TV productions use continuity work to track wardrobe, props, blocking, time of day, emotional state, and whether shots or scenes still match.
- Editors and script supervisors do not replace writers; they catch contradictions and missing cause-effect links.

For AI, the lesson is simple: do not ask one model pass to be novelist, showrunner, scene writer, memory system, editor, and continuity supervisor at the same time. Split the job.

## Production Roles For AI

### Story Lead

Owns:

- core promise
- ending direction
- theme as dramatic cost, not slogan
- what the book is really about
- which lines matter most when tradeoffs appear

Outputs:

- project overview
- arc map
- ending hypothesis
- stage gates

### Character Architect

Owns:

- desire, fear, shame, wound, contradiction
- public mask and private behavior
- speech and action patterns
- arc pressure
- relationship-specific behavior

Outputs:

- cast bible
- relationship entries
- contradiction list

### Continuity Supervisor

Owns:

- names, ages, dates, travel time, geography
- past events and causality
- objects, letters, promises, injuries, public facts
- open loops and callbacks
- what a character knows at a specific time

Outputs:

- timeline
- continuity ledger
- active state updates

### Plot Line Producer

Owns:

- main line and side-line load
- line heat
- return interval
- convergence and collision
- chapter purpose

Outputs:

- plot line register
- chapter roadmap
- chapter card

### Drafting Writer

Owns:

- scene execution
- prose, dialogue, image, rhythm
- chapter hook and turn
- emotional motion

Outputs:

- chapter manuscript
- revision notes for continuity updates

## Stage Gates

### Gate 0: Project Charter

Pass only when the project has:

- one-sentence premise
- target scale
- genre and literary mode
- protagonist pressure
- ending direction
- main conflict
- expected reader experience

Do not draft before Gate 0 passes.

### Gate 1: Cast And Relationship Truth

Pass only when each core character has:

- stable facts
- current desire
- private fear or shame
- contradiction
- relation to the protagonist
- relation to at least two other relevant forces
- likely arc pressure

The relationship map must show tension, not just labels.

### Gate 2: Timeline And Causality

Pass only when:

- important backstory events are dated or ordered
- the present story has a chronological spine
- ages and travel are plausible
- public events line up
- characters do not know information before they learn it

### Gate 3: Line Architecture

Pass only when:

- the main line has stage turns
- side lines have functions
- every major side line collides with the main line at least once
- no side line exists only as decoration
- payoffs have setup points

### Gate 4: Chapter Card

Pass only when the next chapter has:

- chapter purpose
- POV or narrative stance
- entry state
- required scene beats
- continuity constraints
- relationship pressure
- line movement
- narrative boundary
- exit state

### Gate 5: Post-Chapter Update

Pass only when after drafting:

- active state is updated
- new facts are added to the ledger
- timeline changes are recorded
- relationship changes are recorded
- open loops are opened, advanced, or closed
- next chapter risks are noted
- evidence status is updated for new or disputed facts
- line heat is checked and cold side lines are given a return plan
- the chapter manuscript has passed narrative-boundary review

### Gate 6: Batch Literary Revision

Run after every 3-6 chapters. Pass only when:

- the batch has been checked for scene thickness, not just plot delivery
- character interior change is visible through behavior, not explanation alone
- convenient evidence delivery has been delayed, complicated, or justified
- at least one quiet aftermath or ordinary-life beat exists where emotional pressure needs digestion
- chapter rhythm and length support the intended reading experience
- high-priority revision tasks are written into `09-literary-revision.md`

## Chapter Card Schema

Use one card per chapter:

```markdown
# Chapter NN Card

## Purpose

## Entry State

## Required Beats

## Character Constraints

## Relationship Pressure

## Timeline And Setting Constraints

## Plot Line Movement

## Foreshadowing And Payoff

## Narrative Boundary

Forbidden in manuscript:

- direct address to the reader
- author notes or AI/process notes
- chapter purpose, plot line, subplot, character arc, theme, structure, or foreshadowing labels
- evidence labels such as `observed`, `claimed`, `inferred`, `confirmed`, or `contradicted`
- control terms such as continuity ledger, line heat, chapter card, project file, draft task, or revision note

Convert all control intent into in-world action, dialogue, object, silence, setting, perception, and consequence.

## Forbidden Drift

## Exit State

## Post-Draft Update Targets
```

Keep the card short enough to fit in a single prompt with only the relevant project files.

## Continuity Validation

Ask these questions before accepting a chapter:

- Did anyone act against their established motive without new pressure?
- Did anyone know something they should not know yet?
- Did the emotional temperature match the prior scene?
- Did time, travel, injury, weather, public events, and location line up?
- Did a side line disappear for too long?
- Did the chapter introduce a new fact without recording it?
- Did the prose solve a plot problem by author convenience?
- Did a payoff happen without setup?
- Did a setup appear without a planned return?

## Narrative Boundary Validation

Ask these questions before accepting any chapter manuscript:

- Does the chapter stay inside the story world?
- Does it avoid directly addressing the reader?
- Does it avoid mentioning the author, AI, writing task, chapter purpose, plot line, subplot, structure, theme, foreshadowing, or character arc?
- Does it avoid leaking control terms such as `observed`, `claimed`, `inferred`, `confirmed`, `contradicted`, line heat, continuity ledger, chapter card, or project file?
- Are planning intentions translated into scene behavior instead of explanation?
- If a risky word appears naturally in dialogue or narration, is it genuinely in-world rather than a control-file leak?

## Literary Revision Validation

Ask these questions every 3-6 chapters:

- Do the chapters feel like lived scenes or like a sequence of task completions?
- Did clues arrive too conveniently or from too many helpers at once?
- Is the protagonist changing internally, or only collecting evidence?
- Does each major relationship create behavior, silence, debt, avoidance, or pressure?
- Are there enough ordinary-life details to make the world feel inhabited?
- Does any chapter need to be split because too many functions were compressed?
- Does the prose rely on clean symbolic objects instead of messy social reality?
- Are there false starts, failed searches, wrong assumptions, or partial evidence?
- Are emotional consequences carried into later scenes?

## Low-Context Method

Use retrieval by file role, not by dumping everything.

### Startup Prompt

Load:

- project overview
- cast bible
- relationship map
- timeline
- plot lines
- style guide

Task:

- create or revise the full control pack

### Chapter Planning Prompt

Load:

- project overview
- active state
- plot lines
- chapter roadmap
- continuity ledger
- relevant cast entries

Task:

- create the next chapter card

### Chapter Drafting Prompt

Load:

- current chapter card
- active state
- relevant cast entries
- relevant timeline rows
- relevant continuity ledger rows
- style guide

Task:

- draft the chapter only

### Post-Chapter Prompt

Load:

- chapter draft
- chapter card
- active state
- continuity ledger
- relevant cast and timeline entries

Task:

- update project files and list risks

## Evidence Status

Use these labels in ledger or active state when needed:

- `observed`: directly shown in text
- `claimed`: said by a character or source but not verified
- `inferred`: reasonable deduction from shown facts
- `confirmed`: already checked against a stable source in the project
- `contradicted`: known to conflict with another project fact

## Line Heat

Keep a simple line heat note for each active line:

- last appeared
- current pressure
- next required return

If a line has no return plan, repair the roadmap before drafting onward.

## Literary Revision File

Use `09-literary-revision.md` to keep batch-level quality control:

```markdown
# Literary Revision

## Batch NN

### Quality Verdict

### Strong Scenes

### Weak Scenes

### Convenience Risks

### Interior Arc Notes

### Texture And World Notes

### Rhythm And Length Notes

### Narrative Boundary Notes

### Required Revisions Before Next Batch

### Deferred Revisions
```

Keep the file practical. Each issue should name the chapter or scene and state the repair.

## Failure Modes

### Vague Outline

Symptom: the plan sounds impressive but cannot generate chapters.

Repair: convert each abstract claim into a character decision, conflict, reveal, debt, or irreversible consequence.

### Character Drift

Symptom: a character changes personality because the scene needs it.

Repair: add a pressure bridge. If none exists, rewrite the scene or alter the preceding chapter.

### Subplot Evaporation

Symptom: a side line appears, disappears, then returns only for convenience.

Repair: assign each side line a return interval and collision point with the main line.

### Timeline Fog

Symptom: the reader cannot tell when things happen or whether events can coexist.

Repair: add dated or ordered timeline rows and record character knowledge states.

### Overloaded Chapter

Symptom: one chapter tries to advance too many lines.

Repair: pick a dominant purpose and demote all other lines to pressure, echo, or setup.

### AI Decorative Prose

Symptom: beautiful paragraphs hide missing causality.

Repair: strip the chapter to beats, verify cause-effect, then restore style.

### Fourth-Wall Leak

Symptom: manuscript text mentions the reader, author, chapter purpose, plot line, theme, foreshadowing, character arc, evidence status, line heat, continuity ledger, chapter card, or project files.

Repair: move the leaked control information back into control files. Rewrite the manuscript passage as in-world action, dialogue, object, silence, setting, perception, or consequence.

### Task-Completion Prose

Symptom: every scene cleanly delivers a clue, pressure turn, or setup, but the reading experience feels mechanical.

Repair: add delay, misdirection, failed attempts, ordinary-life friction, aftermath, and character hesitation.

### Convenient Evidence Chain

Symptom: multiple sources provide useful clues in the same chapter without enough resistance.

Repair: split the discoveries across chapters, make one clue partial, or add a cost for obtaining it.

### Thin Interior Arc

Symptom: the protagonist gathers facts but does not visibly change in desire, fear, shame, or behavior.

Repair: add choices that force the protagonist to betray a prior self-protection strategy.
