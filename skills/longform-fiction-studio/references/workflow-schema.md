# Collaborative workflow state (version 1)

`workflow.json` is the canonical task/review/issue ledger. Markdown remains the
story bible and human-readable evidence; do not maintain a second task-status
ledger in Markdown. The supervisor is the single merger of accepted state.

## Start and inspect

From the repository root, after creating the project directory:

```sh
python3 -B skills/longform-fiction-studio/scripts/init_workflow.py novels/my-book --chapters 3 --chapter-min 6000 --chapter-max 8000 --total-min 18000 --total-max 24000 --count-mode han
python3 -B skills/longform-fiction-studio/scripts/inspect_project.py novels/my-book --json
python3 -B skills/longform-fiction-studio/scripts/validate_project.py novels/my-book --stage progress
python3 -B skills/longform-fiction-studio/scripts/validate_project.py novels/my-book --stage release --json
```

Initialization only creates `workflow.json`, refuses overwrite, and leaves role
IDs unassigned. It never approves existing prose. Fill the control pack and assign
actors before validation. No model API, daemon, automatic scheduling, or billing
is configured by these tools. A host AI or human supervisor executes the roles.

## Top-level fields

- `schema_version`: integer `1`.
- `contract`: `chapters`, `chapter_min`, `chapter_max`, `total_min`, `total_max`
  are positive integers. `count_mode` is `han` or `nonspace`.
- `actors`: a nonempty session/person ID or array of IDs for each of `supervisor`, `planner`,
  `writer`, `continuity_editor`, `literary_editor`. IDs must be distinct across all roles.
  Add new session IDs on handoff and preserve historical IDs so old reviews remain
  attributable. These are provenance records,
  not authentication. The same model can serve distinct roles in separate sessions.
- `tasks`: exactly one task for each chapter number, including planned chapters.
- `reviews`: append-only ordered review records, oldest first.
- `issues`: findings and their repair status.
- `repetition_exceptions`: explicit literary-review decisions, normally `[]`.

A total range and the combined chapter ranges must intersect. Resolve conflicts
before drafting. Only an authorized scope change may alter the contract; record
its reason and user request in `QUALITY_REPORT.md`. Do not select a more lenient
count mode to rescue a failed manuscript. The validator cannot authenticate
approval or prove a human/AI actually read prose.

### Counting and manuscript format

`han` counts Unicode Han characters, including extension and compatibility
ranges. It excludes punctuation, Latin text, numerals, whitespace and Markdown
headings. `nonspace` counts all non-whitespace body characters, including
punctuation, Latin letters and numerals. Neither includes Markdown headings or
standalone scene separators (`***`, `---`, `___`). These are explicit project
metrics, not a claim to reproduce a particular publisher's word count.

Use plain paragraph prose with optional headings and scene separators in chapter
files. Code blocks, HTML/comments, Markdown links and tables are flagged for
review; they are not a supported manuscript container. Inline Markdown decoration
must be removed before delivery. Choose the format before counting.

### Task

```json
{
  "id": "chapter-01",
  "chapter": 1,
  "status": "planned",
  "writer": "writer-session-01",
  "depends_on": [],
  "scenes": [
    {
      "id": "01-a",
      "goal": "The archivist tries to obtain the original register.",
      "entry_state": "She knows a page is missing but has no access permission.",
      "conflict": "The keeper offers only an incomplete copy.",
      "exit_state": "She refuses the copy and loses her scheduled appointment.",
      "min": 1500,
      "max": 2000
    }
  ],
  "manuscript_sha256": "",
  "accepted_by": ""
}
```

Add enough scenes for their combined budget to overlap the chapter range. Budgets
are planning constraints, not proof that the resulting scene does useful work.

States: `planned` → `writing` → `in_review` → `needs_revision` → `in_review` →
`accepted`. The supervisor records transitions. Failed acceptance stays in review
or returns for revision; never label it accepted merely to advance dependencies.
Active tasks require accepted dependencies. The initializer chains chapter N to
N-1; change dependencies only when the narrative actually permits it. Cycles,
missing dependencies and duplicate chapter numbers are errors.

At acceptance, set `manuscript_sha256` to the current exact UTF-8 text SHA-256
from `inspect_project.py`; set `accepted_by` to the supervisor actor ID. The two
editors must already have fresh passing reviews. Corrected earlier chapters need
new reviews; reopen dependent tasks where knowledge/causality changed. The final
whole-book snapshot checks global changes, but dependency impact remains an
editorial duty, not something a digest can infer.

### Review

```json
{
  "id": "continuity-01-r1",
  "role": "continuity_editor",
  "reviewer": "continuity-session-01",
  "scope": 1,
  "sha256": "exact hash from inspect_project.py",
  "report": "reviews/continuity-01-r1.md",
  "verdict": "changes_requested",
  "issues": ["C-001"]
}
```

`scope` is an integer chapter number or `"book"`. `role` is
`continuity_editor` or `literary_editor`; the reviewer must match its assigned
actor. `verdict` is `pass` or `changes_requested`. A changes request must reference
at least one issue. Preserve historical failed/stale reviews. The latest review
for each scope and role controls acceptance; an older pass cannot override a
new failure. Write a new report per review. Reports must live inside the project.

Chapter hashes cover exact chapter text. Book hashes cover the paths and bytes
of all chapter manuscripts, chapter cards, and `00-project-overview.md` through
`08-active-state.md`. They exclude workflow/review bookkeeping, entry instructions,
revision ledger and quality report, avoiding self-invalidation. Update story truth
before final reviews. Book-level reviews are required from both editors at full
release; they cover cross-chapter continuity and narrative payoff.

Each report must name passages/scenes checked, concrete findings (or supported
reasons for no findings), and a verdict. A nonempty file is mechanically checked;
its intellectual substance must be checked by the supervisor. Never invent a
review, reviewer session or evidence to make validation pass.

### Issue and repair

```json
{
  "id": "C-001",
  "scope": 1,
  "severity": "high",
  "status": "open",
  "evidence": "Chapter 1 paragraph 6 uses the missing witness's name before she learns it.",
  "repair": "Delay the name until the witness list is obtained; recheck the following scene.",
  "raised_by": "continuity-01-r1"
}
```

Severity: `low`, `medium`, `high`, `critical`. Status: `open`, `done`, `deferred`.
The raising review must list the issue. To mark `done`, add `verified_by` pointing
to a later, fresh passing review of the same scope and same editorial role. The
writer cannot close a finding. After further edits, renew the verification.

A low/medium deferral requires `reason` and `approved_by` (supervisor actor).
Open issues block acceptance in their scope. High/critical issues block acceptance
unless done, including when deferred. A book-scope open issue blocks chapter
acceptance as well; scope findings narrowly when possible.

### Repetition exceptions

Exact paragraphs of at least 40 non-whitespace body characters are compared
within and across chapters. Every repeated group is reported with positions and
its normalized paragraph hash. This catches copied passages; it does not detect
all paraphrases, plagiarism, flat dialogue or repetitive narrative structure.

A repeated passage can be intentional (a letter or refrain). It needs an explicit
entry such as:

```json
{"sha256": "normalized paragraph hash", "reason": "The unchanged letter is reread with a changed interpretation in chapter 3.", "review_id": "literary-book-r2"}
```

The referenced review must be a fresh whole-book literary pass. Do not bulk-exempt
repetition or change a threshold to meet length. Exemptions do not change the
contracted count; the supervisor judges whether the repetition earns its space.

## Progress versus release

`progress` checks the state model and all already-accepted chapters. Unfinished
chapters may be absent; length/process problems in writing drafts and repetitions
only in unaccepted drafts are warnings. Submitted `in_review` chapters must meet
the mechanical chapter checks. No full-book reviews or quality report are required
yet. A progress pass is not delivery approval.

`release` requires all contracted manuscripts/cards, nonempty control files and
quality report, all tasks accepted, fresh chapter and whole-book reviews, resolved
blocking issues, chapter and total lengths, and no unreviewed long exact repeats.
Unexpected Markdown chapter files, duplicate numeric IDs and extra cards fail.

The supervisor also checks motivation, pacing, source-backed story state,
near-duplicates, scene function and closure. Programmatic validation cannot prove
these properties or stop someone from falsifying the JSON. Keep the roles and
review evidence honest.

## Legacy migration

1. Run `inspect_project.py` on the original; it does not need workflow state.
2. Preserve manuscripts and the original delivery requirements. Do not silently
   reinterpret an ambiguous historic word-count requirement.
3. Initialize a new ledger with the agreed count mode and contract. Populate real
   actors, scenes and task states. Existing prose starts unaccepted.
4. Run the editorial checks and record actual findings; only then accept tasks.
5. Keep old reports as historical evidence and clearly distinguish them from
   current measurements. Failed modern validation is not proof of lost files.
