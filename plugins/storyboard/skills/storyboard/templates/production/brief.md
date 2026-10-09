<!--
PRODUCTION BRIEF TEMPLATE — storyboard

This is a real piece being made, not a reusable format. It instantiates a
project type from projects/ with actual specifics: the real goal, the real
deadline, the named panel, who's covering which role.

Copy to <production>/brief.md. The slug is what everything else
references, so make it descriptive and dated: ai-management-plane-2026q1.

The production folder lives in your own working folder, NEVER inside the
skill — the skill ships only this stencil.
-->

---
production: {{slug}}
title: {{Production Title}}
project_type: {{product-vision-2min}}
status: {{briefing | in-production | in-review | released | shelved}}
target_date: {{YYYY-MM-DD}}
workflow: {{new-storyboard}}
updated: {{YYYY-MM-DD}}
---

# {{Production Title}}

**Goal:** {{The one thing this specific piece has to accomplish — not the format's generic goal.}}

**Key message:** {{The single takeaway, in one sentence.}}

**Story structure:** {{hero's journey | problem-agitate-solve | before-after-bridge | situation-complication-resolution | in medias res | question-answer | chronological/process | anatomy-tour}}

<!-- SASHA SCRIPT CHOOSES THIS BEFORE WRITING A LINE, and Dana Director
     approves it. It is not a formality: when nobody picks a structure a
     piece becomes a tour of things that exist, and every persona
     downstream feels that as "flat" without being able to name it. No
     amount of pace, music or motion fixes a structure problem.

     Then give every beat a PURPOSE — what it is FOR, not what happens in
     it — and check the purposes aren't all the same one. Dana Director
     adds the emotion and pace per beat in the boards' Beat direction
     table; structure gives the beats, direction gives them feeling, and
     the two have to agree. See workers/scriptwriter.md for what each
     structure is good for and where it fails. -->

**Why that structure:** {{One sentence. What it promises the viewer, and why this audience will accept that promise.}}
**Who is the hero:** {{The customer / the operator / nobody, it's a process piece. Never the product.}}

| Beat | Purpose — what this beat is *for* |
|---|---|
| {{Hook}} | {{Make the friction feel familiar before anyone is told what this is}} |
| {{Reframe}} | {{Move from "this is annoying" to "this is a solvable category of problem"}} |
| {{Vision in action}} | {{Deliver the key message — the one takeaway, shown not claimed}} |
| {{Impact}} | {{Reinforce: move the claim from feature to consequence}} |
| {{Close}} | {{One next step, earned by the four beats above}} |

**Inherits from:** `projects/{{product-vision-2min}}.md` — that file holds the beat breakdown, tone, and default team weighting. Record only what differs here.

## Pace & runtime

<!-- Decided at kickoff, because it changes what "too many words" means.
     Dana Director owns the pace (it's a tone decision); Paul Producer
     owns whether the runtime can move. -->

- **Target pace:** {{150}} wpm, ceiling {{170}} — {{set by Dana Director / inherited from the project format}}
- **Why this pace:** {{e.g. "130 — a third of the audience reads English as a second language" / "165 — social, and the hook has to land before the scroll"}}
- **Runtime:** {{2:00}}, **{{flexible | FIXED}}** — {{if fixed, say why: ad slot, platform cap, event segment}}
- **Consequence:** {{if FIXED, over-dense beats must lose words; if flexible, stretching the beat is on the table and Paul Producer approves the new runtime}}

## Deviations from the project type

<!-- Where this piece departs from its format spec, and why. If nothing
     differs, say so — that's useful information. -->

- {{e.g. "Running 2:20 rather than 2:00 — the demo beat needs the extra 20s"}}

## Audience for this piece

<!-- Name actual personas from audience/. These are who the work gets
     judged against, and who gets seated on the preview and premiere
     panels. -->

- **Primary:** {{Paula Product (product manager), Camille Chief (C-suite leader)}}
- **Secondary:** {{Seth Software (software engineer)}}
- **Will encounter it incidentally:** {{Skye Social (social scroller), if this runs on social}}

## Render & captions

<!-- Dev Deaf's first question, and it belongs here because the answer
     changes the boards rather than the post. Burned-in captions occupy
     screen space Arthur Art has to compose around from the first frame;
     a sidecar track can be switched off, so the piece has to survive
     without it; no captions at all means everything the VO carries must
     also exist in picture or on-screen text, which is a constraint the
     whole crew designs against.

     "We'll add captions later" is the answer that produces bad ones. -->

- **Rendered as:** {{finished video | animatic only | live-presented deck}}
- **Captions:** {{burned-in | sidecar SRT/VTT | none planned}} — {{why}}
- **Written from:** {{the locked script | a transcription pass after the edit}} — auto-generated captions are not captions; product names and jargon are exactly what they get wrong
- **Speaker labels needed:** {{yes — four speakers | no — single narrator}} (cross-check against Cast & voices)
- **Non-speech audio in the caption track:** {{`[alert pings]`, `[music swells]` — taken from the boards' Audio column}}
- **Audio description:** {{not needed | needed — see Blair Blind}}

## Panel assignments

<!-- Filled in when preview/premiere workflows run, so the same panel can
     be re-run on a later cut and reactions compared.

     PRIYA PRODUCER DECIDES THE PANEL and records it here. Claude Client
     supplies the must-convince list, Dana Director supplies the risk
     list; neither of them chooses, because a director picking his own
     audience picks who is allowed to judge his work. Record both inputs,
     not just the result — a panel you can't trace back to them is a panel
     somebody assembled out of who was friendly. -->

- **Must be convinced** (Claude Client): {{Camille Chief — this exists to get budget approved}}
- **Beat at risk** (Dana Director): {{the turn at 0:48 — I think it's too quick}} → suggests {{Cora Cognitive, Nadia Language}}
- **Preview panel** (Paul Producer's call): {{Paula Product, Camille Chief, Simone Skeptic}} — round 1 on {{date}}
- **Premiere panel:** {{full representation incl. Dev Deaf, Blair Blind, Leo Vision, Cora Cognitive}} — {{date}}
- **Deliberately absent, and why:** {{Theo Teen — this piece will not reach anyone under 25}}
- **Dismissed at preview, therefore automatic at premiere:** {{Silas Security — said the security story was missing; dismissed as out of target}}

## Who's covering each role

<!-- Real humans, if any, against the worker personas. Leave blank where
     Claude is running the persona rather than a person. -->

| Worker persona | Covered by |
|---|---|
| Scott Script (scriptwriter) | {{name or "Claude"}} |
| Dana Director (director) | {{...}} |
| Paul Producer (producer) | {{...}} |

## Brand source

<!-- Established at step 1, before anything gets styled. If there's no
     brand guide or design doc, say so explicitly and say who was asked —
     "unknown" is a blocker Arthur Art will raise, not a blank to skip past. -->

- **Guardrails file:** {{`reference/brand-guardrails.md`, or a per-piece copy in this folder if this one follows different rules}}
- **Original source:** {{brand book PDF | slide deck | brand site URL | Figma file | YouTube link | video file | "none — asked {{who}} on {{date}}"}}
- **Unconfirmed values in play:** {{anything still marked ESTIMATED or NEEDED, and who was asked}}

## Constraints

- {{Hard deadline, budget ceiling, legal/brand guardrails, claims that must be cleared}}

## Artifacts

| Artifact | File | Status |
|---|---|---|
| Script | `script.md` | {{draft}} |
| Boards | `boards.md` | {{rough}} |
| Feedback rounds | `feedback/` | {{none yet}} |
