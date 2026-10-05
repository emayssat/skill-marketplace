---
workflow_type: new-storyboard
workflow_title: New Storyboard Creation
---

# New Storyboard Creation

**When to use:** Starting from nothing but a brief or idea — no existing script, boards, or prior version to build from. This is the default, canonical workflow; every other workflow in this folder is a variation on it.

**Inputs required:** An approved project brief (see `projects/`) with goal, audience, duration, and format decided — plus brand guardrails in some form (brand book, deck, brand site, design file, or a video that's on-brand). If none exist, ask at step 1; don't discover at step 6 that nobody knows what the piece is supposed to look like.

**Arc:** Dana Director fills the Beat direction table — an emotion and a pace per beat — before the read-through, so Vera Voice has direction rather than defaulting to even. Check it with `scripts/boards.py --arc`: an emotion that never changes, or a pace that never varies, means the piece will play flat regardless of how good the words are.

**Story:** Sasha Script picks the structure at step 1–2 and Dana Director approves it at step 3, **before a line is written**. Unchosen, a piece defaults to a tour of things that exist — which every persona downstream will call "flat" without being able to say why, and which no amount of pace, music or motion repairs. Record the structure, why it fits, who the hero is (never the product), and one purpose per beat in the brief.

**Motion:** what changes *inside* each frame, between its join in and its join out. Stella Storyboard drafts it at step 8; **Molly Motion or Dean Photography owns and prices it at step 10**; Dana Director approves the intent at step 14. Write what changes and when — `BUILD — three rows populate 0.3s apart` — because an adjective prices out anywhere between a day and two weeks. A frame that holds says `STILL — <reason>`.

**Transitions:** Ed Edit specs them at step 12 (`scripts/boards.py --transitions`). The default is a straight cut; only exceptions get documented, and each needs a reason — "it looked flat as a cut" is a pacing problem, not a transition brief. Dissolves and builds cost runtime and animation days, so they land in the same budget as words and pauses.

**Pace:** set the target at step 1 and record it in the brief — the project format proposes it, Dana Director decides, Paul Producer says whether the runtime can move. Verify per beat at step 4 (`scripts/boards.py --pace`). Fixing density before boards exist costs a rewrite; fixing it after costs redraws.

**Cards:** every card is built from `templates/production/frame-card.md` — read it before step 8. Each card holds the *current state* of one frame and nothing else, including **Motion** (what changes during the frame, blank when nothing does), **Text** (on-screen wording, verbatim), **Trans** (the join in, blank when it's a cut) and **Note** (what changes here: a new voice, a first logo appearance, a sound bridge). They start clean and stay that way only if every revision from step 9 onward overwrites cells rather than annotating them. History goes to the Revision log, doubts to Still open issues. Check with `scripts/boards.py --cards`.

## Sequence

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | producer | Open the production folder, intake the brief, **settle the caption plan** (burned-in / sidecar / none — burned-in captions occupy screen space and Arthur Art has to compose around them from step 6, so this cannot wait for post), confirm budget/timeline fit the project type, assign the team — and gather the brand guardrails in whatever format exists (brand book, deck, brand site, Figma, YouTube link, video file), asking for them by name if none surface | `<production>/brief.md`; guardrails in hand or explicitly requested; team knows their role |
| 2 | scriptwriter | **Choose the story structure first** — hero's journey, problem-agitate-solve, before-after-bridge, in medias res — say why it fits this audience and message, name who the hero is, give every beat a purpose; record all of it in the brief. Then draft the script from that shape | Structure + per-beat purpose in `brief.md`; `script.md` (draft) |
| 3 | director | Approve the structure, then review the draft for shot potential and story clarity — a beat that doesn't serve its stated purpose is a note, and a structure abandoned halfway is a rewrite | Structure approved; script notes |
| 4 | voice-talent | Read the draft aloud, **each speaker in that speaker's voice** — flag unspeakable lines, mark pauses, and report words-per-minute per beat against its duration (`scripts/boards.py --pace`) | Read-through notes; every beat within this piece's pace ceiling |
| 5 | scriptwriter | Revise against both the director's notes and the read-through, and deliver | `script.md` (locked) |
| 6 | art-director | Build style/mood references and any needed location or UI concepts from the locked script, and set the on-screen text budget (~2–3 words per second of hold; "they can pause it" is not a plan), **working from the brand source** — not from taste or from what previous videos happened to look like | Style guide / palette / references, traceable to `reference/brand-guardrails.md` |
| 7 | director | Align with art director, finalize the shot list outline | Draft shot list |
| 8 | storyboard-artist | Rough thumbnail pass of the full sequence — each frame a card in current state, with Text filled verbatim where anything appears on screen and a Note where something changes at that frame | `boards.md` (rough) |
| 9 | director | Review rough pass, give notes | Director notes (loop with artist until approved) |
| 10 | dp *or* motion-lead | Feasibility pass on the shot list **and on the Motion column** — Dean Photography flags rigs, lighting and coverage gaps and puts timing on every camera move; Molly Motion prices each frame's motion in days and flags missing UI assets. **Then the continuity pass, reading the frames in sequence** (`scripts/boards.py --motion`): does each Motion match its Visual, does it start where the last frame ended and end where the next begins, and does `motion + join out` fit `Dur` | Feasibility notes; Motion specced, priced and continuous |
| 11 | storyboard-artist | Revise boards addressing the director's and the feasibility notes — overwriting cells, never annotating them, and logging each change once in the Revision log | `boards.md` (clean-locked) + `--cards` clean |
| 12 | editor | Assemble a timed animatic from the clean boards plus scratch VO, and spec the Transitions table — default is a straight cut, so document only the exceptions, give each one a reason, and mark the matching frame's Trans out cell so card and table agree | `boards.md` (animatic-locked) + transitions specced |
| 13 | sound-designer | Build temp music and sound design against the locked animatic, account for every silent frame (`SILENT — <reason>`, or give it audio, or send it to Ed Edit to cut), and complete the Cast & voices table — every speaker described, sourced, matched for level and distinguishable from the others | Scored animatic + cast defined |
| 14 | director | Review the scored animatic for pacing, and approve the motion intent — what moves should be explaining something, and what holds should be holding on purpose | Pacing + motion sign-off |
| 15 | producer | Confirm schedule/budget against the final shot count | Locked schedule + budget |
| 16 | legal-reviewer | If the piece goes outside the company: clear every claim, asset license, and customer reference | Written clearance, or marked internal-only |
| 17 | client | Final review and sign-off | Approved storyboard |

## Final output

An approved storyboard package: locked script, clean boards, a scored and mixed animatic, and a locked production schedule.

## Notes / anti-patterns

- Don't let the storyboard artist start clean frames before the director's rough-pass notes are resolved — redraw churn is the most common source of schedule slip here.
- Feasibility (step 10) belongs before the clean pass, not after — catching an unshootable frame in step 11 is cheap; catching it on set isn't.
- **On a multi-speaker piece — a testimonial especially — bring Sonny Sound in around script lock rather than waiting for step 13.** Casting four voices that are distinguishable, and getting real recordings scheduled and consented, has a lead time that a temp-score step does not. The cast table can be drafted as soon as the speakers exist.
- Don't skip the read-through (step 4) because the script "reads fine." Read time is what kills a script, and it is not discoverable by reading silently — a 340-word script does not fit a 2:00 piece no matter how good it is.
- Don't send the sound designer a cut that's still changing (step 13 needs an animatic-locked board from step 12) — rescoring against a moving edit is the audio equivalent of redraw churn.
- Legal clearance (step 16) sits before client sign-off deliberately. A client approving a cut with an unsubstantiated claim in it has approved a rework, not a release.
- Client sign-off is on the whole package, not the boards alone — the scored animatic's pacing is part of what they're approving.
