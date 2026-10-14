# Project Template

Use this compact project layout for a new novel.

```text
project-root/
  PROJECT_ENTRY.md
  workflow.json
  00-project-overview.md
  01-cast-bible.md
  02-relationship-map.md
  03-timeline.md
  04-plot-lines.md
  05-chapter-roadmap.md
  06-continuity-ledger.md
  07-style-and-voice.md
  08-active-state.md
  09-literary-revision.md
  chapters/
  chapter-cards/
  reviews/
  QUALITY_REPORT.md        # Written for full delivery, not prefilled as passed
```

## Operational Records

`workflow.json` stores the count contract, actual actors, task dependencies, manuscript versions, issues, reviews and acceptance. Follow [workflow-schema.md](workflow-schema.md) for exact fields and statuses. The supervisor is its sole merge owner. Other roles return artifacts and proposals; the supervisor verifies and merges them.

Initialize it non-destructively from the repository root:

```bash
python3 -B skills/longform-fiction-studio/scripts/init_workflow.py <project-root> --chapters 10 --chapter-min 6000 --chapter-max 8000 --total-min 60000 --total-max 80000 --count-mode han
```

Replace example values with the user's contract. The scaffold requires real actor assignment and task detail before work begins. It does not create prose, approve existing chapters, or replace the Markdown control pack. Preserve existing drafts when migrating.

`reviews/` holds actual role reports with scope, version, located evidence, issues and recheck results. Keep the machine-readable issue status in the workflow; use IDs in prose summaries to avoid conflicting ledgers.

## File Content Hints

### PROJECT_ENTRY.md

- first-read handoff instructions
- required read order
- method or skill location
- current authorized batch and stop point
- accepted chapters versus drafts awaiting review
- next task ID, actual actor and prerequisites
- pending user creative decisions and decisions already received
- active facts and forbidden drift
- post-draft update checklist

### 00-project-overview.md

- title
- genre
- scale
- promise
- audience
- ending direction
- taboo boundaries

### Delivery Contract

- Planned chapters: N
- Chapter and total count ranges
- Count mode: `han` (body Chinese characters) or `nonspace` (body non-whitespace characters including punctuation); headings excluded
- User creative constraints and review points
- Current batch boundary
- intended reader effect
- draft state
- required delivery files

### 01-cast-bible.md

- name
- role
- age
- surface traits
- hidden pressure
- desire
- fear
- contradiction
- arc hypothesis

### 02-relationship-map.md

- pair or group
- relation type
- current status
- pressure source
- debt or leverage
- likely change

### 03-timeline.md

- date or order
- event
- who knows it
- why it matters
- downstream effect

### 04-plot-lines.md

- line name
- function
- current stage
- next turn
- collision point

### 05-chapter-roadmap.md

- chapter
- purpose
- dominant line
- key beat
- exit condition

### chapter-cards/NN-card.md

- purpose
- entry state
- required beats
- references to workflow scene IDs; optional POV/time/place, choice/consequence and acceptance guidance without copying scene budgets or states
- character constraints
- relationship pressure
- timeline and setting constraints
- plot line movement
- foreshadowing and payoff
- narrative boundary
- forbidden drift
- exit state
- post-draft update targets

Use the exact level-two headings in the chapter card example in [methodology.md](methodology.md). Reference scene IDs under Required Beats; no extra Scene Plan heading is required. The structured scene records supply actionable work; a list of theme statements cannot substitute for scenes.

### 06-continuity-ledger.md

- fact
- source chapter
- evidence status
- status
- risk
- follow-up

### 07-style-and-voice.md

- narration stance
- paragraph behavior
- dialogue behavior
- banned habits
- lexical limits
- narrative boundary rules for manuscript language

### 08-active-state.md

- last accepted chapter and current task ID
- what changed in accepted prose
- what is true now
- what must stay true
- what to check next
- active line heat

### 09-literary-revision.md

- batch quality verdict
- strong scenes
- weak scenes
- convenience risks
- interior arc notes
- texture and world notes
- rhythm and length notes
- narrative boundary notes
- required revisions before next batch
- deferred revisions
- issue IDs linked to workflow and review reports
- finding, scene evidence, reader impact, repair decision and independent recheck summary

Do not maintain a second mutable issue-status system here. Critical/high issues cannot be deferred past acceptance.

### QUALITY_REPORT.md

At release, report actual chapter/total counts and their mode, current manuscript versions, both editor roles' chapter and book reports, repair verification, validation command/result and remaining limitations. Do not prefill a passing verdict. Progress reports belong in the handoff until full-book delivery is in scope.
