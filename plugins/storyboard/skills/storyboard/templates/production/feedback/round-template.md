<!--
FEEDBACK ROUND TEMPLATE — storyboard

The record a preview.md or premiere.md round produces. Copy to
<production>/feedback/<nn>-<preview|premiere>.md — numbered so
rounds stay in order (01-preview.md, 02-preview.md, 03-premiere.md).

The production folder lives in your own working folder, NEVER inside the
skill — the skill ships only this stencil.

This file is what makes persona feedback accountable rather than
decorative. Two things depend on it:

  - preview.md logs dismissed objections here, so that if the same
    objection resurfaces at premiere from an in-target persona, you can
    see it was raised early and waved off.
  - premiere.md step 9 compares what personas predicted against how real
    viewers actually reacted, and updates audience/ accordingly. Without
    a written prediction there is nothing to compare against.
-->

---
production: {{slug}}
round: {{01}}
type: {{preview | premiere}}
cut_reviewed: {{boards.md v2, animatic-locked}}
date: {{YYYY-MM-DD}}
outcome: {{revise | proceed | go | no-go}}
---

# {{Production Title}} — {{Preview}} round {{01}}

**Cut reviewed:** {{boards.md v2 (animatic-locked)}}
**Asked of the panel:** {{The specific question this round is meant to answer, and what was explicitly not open for debate.}}

## Panel

<!-- Paul Producer's call. "Put there by" makes the panel auditable: if
     every row says "producer" with no client or director input behind it,
     nobody named the real decision-maker or the real risk. -->

| Persona | Why seated | Put there by |
|---|---|---|
| {{Paula Product (product manager)}} | {{Primary audience; owns whether the scope shown is honest}} | {{brief}} |
| {{Camille Chief (C-suite leader)}} | {{Holds the decision this piece is asking for}} | {{Claude Client — must be convinced}} |
| {{Cora Cognitive (cognitive/neurodivergent)}} | {{The turn at 0:48 may be too quick}} | {{Dana Director — beat at risk}} |

**In the room:** Paul Producer facilitating, Ed Edit running the cut. No other crew.

**Deliberately absent:** {{Theo Teen — this piece will not reach anyone under 25}}

## Reactions

### {{Paula Product}} — {{product manager}}

**Reaction:** {{What they said, in their voice.}}

**Where they disengaged:** {{Frame or timecode, or "didn't"}}

**Landed / didn't land:** {{Did the key message reach them?}}

### {{Camille Chief}} — {{C-suite leader}}

**Reaction:** {{...}}

**Where they disengaged:** {{...}}

**Landed / didn't land:** {{...}}

## Triage

<!-- Dana Director's call. Every reaction lands in exactly one of these,
     and every accepted one gets a named Owner — the worker whose craft
     actually holds the fix. See the routing table in
     workflows/preview.md; a finding that maps to nobody there usually
     maps to the brief, which is Paul Producer's, not a fix step.

     A worker with no row here does nothing this round. That's a clean
     result, not an idle one. -->

**Accepted — changing:**

| Finding | Frame(s) | Owner | Change |
|---|---|---|---|
| {{Message unclear before the cut}} | {{9–11}} | {{Scott Script}} | {{Add explicit value line}} |

**Dismissed — not changing:**

| Finding | Raised by | Why dismissed |
|---|---|---|
| {{Too technical}} | {{Theo Teen (teenager)}} | {{Out of target audience for an internal vision piece}} |

**Deferred:**

- {{Finding, and what would make it worth revisiting}}

## Outcome

{{Revise and re-screen / proceed to premiere / go / no-go}} — decided by {{Paul Producer}}.

<!-- PREMIERE ROUNDS ONLY — fill in after release. This is step 9 of
     premiere.md and the reason audience personas stay honest. Delete
     this section for preview rounds. -->

## Prediction vs. reality (post-release)

| Persona | Predicted | Actually happened | Persona needs updating? |
|---|---|---|---|
| {{Skye Social (social scroller)}} | {{Would scroll past without the first-second hook}} | {{72% watched past 3s}} | {{No — held up}} |
| {{Simone Skeptic (skeptical buyer)}} | {{Would want a proof number}} | {{Top question in comments was pricing, not proof}} | {{Yes — add cost sensitivity to her priorities}} |
