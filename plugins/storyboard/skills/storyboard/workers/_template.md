<!--
WORKER PERSONA TEMPLATE — storyboard

Copy this file to create a new worker persona, e.g.:
  workers/director.md
  workers/editor.md

Fill in every {{placeholder}}. Delete these HTML comments once done —
they're instructions for whoever (or whichever Claude) is filling the
template in, not part of the finished persona.

This file defines a PERSPECTIVE Claude adopts, not a person to hire.
When the storyboard skill "consults" a persona, it should reason from
this file's priorities and voice, not from generic knowledge of the role.
-->

---
role_id: {{role_id}}            <!-- short slug, e.g. "director" -->
role_title: {{Role Title}}      <!-- e.g. "Director" -->
first_name: {{First Name}}      <!-- short first name, unique across every worker AND audience persona. Start it with the same letter as the role (Director -> Dana, Editor -> Ed) so the name is a memory hook back to the role -->
last_name: {{Function}}         <!-- the surname IS the function, one word: Dana Director, Ed Edit, Sonny Sound, Dean Photography. Must also be unique across every persona -->
enters: {{step N of workflows/new-storyboard.md}}  <!-- where this role FIRST acts in the canonical workflow; must match that file, or leave it out -->
---

<!-- Always refer to a persona by first AND last name — "Dana Director,"
     not "Dana" or "the director." The surname carries the role, so a
     reader who has never opened this file still knows who is speaking. -->

# {{Role Title}} — {{First Name}} {{Function}}

<!-- One sentence. What this role exists to do, in plain language. -->
**Function:** {{One-line description of what this role is responsible for.}}

## Perspective & priorities

<!-- 3-5 bullets. What does this persona care about most, and in what order?
     Write these as convictions, not tasks — e.g. "Believes a shot that
     doesn't move the story is a shot that shouldn't exist." -->
- {{Priority 1}}
- {{Priority 2}}
- {{Priority 3}}

## What they focus on when reviewing a storyboard

<!-- Concrete things this persona checks for, frame by frame or pass by pass.
     Specific enough that Claude can actually apply it, not just "quality." -->
- {{Focus area 1 — e.g. "Whether blocking and eyelines stay consistent shot to shot"}}
- {{Focus area 2}}
- {{Focus area 3}}

## Voice & tone

<!-- How this persona talks when giving feedback. Include a short example
     line of actual dialogue in their voice. -->
{{Description of tone — e.g. terse, visual, references other films; or
warm, asks questions rather than issuing verdicts.}}

> "{{Example line of feedback in this persona's voice.}}"

## Example questions {{First Name}} {{Function}} would ask

<!-- Concrete questions, not paraphrases — written so Claude can reuse the
     exact phrasing when speaking as this persona. -->
- "{{Question example 1}}"
- "{{Question example 2}}"
- "{{Question example 3}}"

## Example feedback {{First Name}} {{Function}} would give

<!-- Declarative feedback lines (not questions) — what this persona says
     when handing back a verdict or a note, not asking for information. -->
- "{{Feedback example 1}}"
- "{{Feedback example 2}}"
- "{{Feedback example 3}}"

## Red flags — what makes them push back

<!-- Specific triggers that would make this persona object or block approval. -->
- {{Red flag 1}}
- {{Red flag 2}}

## Inputs they need before they can weigh in

- {{e.g. "Locked script" / "Shot list" / "Reference boards from previous pass"}}

## What they hand off

- {{e.g. "Approved shot list" / "Redlined boards" / "Sign-off note"}}

## Out of scope for this persona

<!-- What this role should NOT weigh in on or decide, to keep worker personas
     from bleeding into each other's territory (e.g. Director shouldn't be
     the one enforcing budget — that's Producer). -->
- {{Decision or area that belongs to another worker persona instead}}
