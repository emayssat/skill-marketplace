<!--
WORKFLOW TEMPLATE — storyboard

Copy this file to create a new workflow, e.g.:
  workflows/new-storyboard.md
  workflows/remake.md

Fill in every {{placeholder}}. Delete these HTML comments once done.

A workflow is a sequence of tasks against a project (see projects/), each
task owned by one persona. Steps should say who acts and what they hand
off, not just "review" — vague steps are where workflows stall in
practice.

There are two kinds of workflow:

  PRODUCTION workflows (new-storyboard, remake, teaser, ...) — every step
  is owned by a worker persona from workers/.

  FEEDBACK workflows (preview, premiere) — most steps are owned by
  audience personas from audience/, with worker personas preparing the
  cut and acting on what comes back. These also carry a "Panel
  composition" section saying which audience personas to consult and why.
-->

---
workflow_type: {{slug}}              <!-- e.g. "new-storyboard" -->
workflow_title: {{Workflow Title}}
---

# {{Workflow Title}}

**When to use:** {{The situation that triggers this workflow — what exists already, what doesn't.}}

**Inputs required:** {{What has to exist before this workflow can start, e.g. "approved project brief," "prior approved boards + script."}}

<!-- STANDING GUIDANCE LINES. Every workflow carries a **Pace:** line
     saying what the words-per-minute risk is here and when to check it.
     Any workflow that WRITES OR REVISES A BOARD also carries a **Cards:**
     line, because the frame cards are where a board decays: they hold
     current state only, and every revision is a chance for somebody to
     annotate a cell instead of overwriting it. Say what the specific risk
     is in this workflow and point at `scripts/boards.py --cards`. Add
     **Arc:** and **Transitions:** lines where those are decided here. -->

**Pace:** {{the words-per-minute risk specific to this workflow, and when to run `scripts/boards.py --pace`}}

**Cards:** {{board-writing workflows only — how history tends to creep onto cards in THIS workflow, what happens to Motion here (re-specced? inherited? a place to buy seconds?), and the reminder to overwrite cells and log the change once. Every card follows `templates/production/frame-card.md`.}}

<!-- FEEDBACK workflows only: add a "## Panel composition" section here
     naming which audience personas to consult for this round and why,
     with a few example panels for different project types. Delete this
     comment and the section for production workflows.

     ALSO NAME THE OWNERS, because "the team reviews it" is how a feedback
     round becomes a room agreeing with itself. The established split, and
     any new feedback workflow should follow it or say why not:

       - PRIYA PRODUCER decides the panel and who is in the room.
       - COLIN CLIENT supplies who must be convinced. He doesn't choose.
       - DANA DIRECTOR supplies the beat he's least sure of, then routes
         each accepted finding to the worker whose craft owns the fix.
         He does NOT pick the panel — a director choosing his own
         audience chooses who gets to judge his work.
       - Only ROUTED WORKERS act. A fix step listed for everyone means
         people change things nobody complained about.

     The finding-to-worker routing table lives in workflows/preview.md;
     reference it rather than restating it. -->

## Sequence

<!-- One row per task. "Persona" is a role_id from workers/, or — in a
     feedback workflow — an audience_id from audience/, or an italicized
     group like *audience panel* when several personas react at once.
     "Output / gate" is what that step produces or what has to be true
     before moving to the next step — this is what makes the sequence
     checkable rather than just a list of vibes. -->

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | {{role_id}} | {{What they do}} | {{What they hand off, or what must be approved before step 2}} |
| 2 | {{role_id}} | {{...}} | {{...}} |

## Final output

{{What exists once this workflow completes.}}

## Notes / anti-patterns

<!-- Things that commonly go wrong in this workflow specifically, or scope
     reminders (e.g. "this workflow should NOT touch X — that's a
     different workflow"). -->

- {{Note 1}}
