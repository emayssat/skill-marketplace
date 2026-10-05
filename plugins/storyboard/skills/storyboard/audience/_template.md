<!--
AUDIENCE PERSONA TEMPLATE — storyboard

Copy this file to create a new audience persona, e.g.:
  audience/product-manager.md
  audience/teenager.md

Fill in every {{placeholder}}. Delete these HTML comments once done.

This is a RECEPTION persona, not a production one (see workers/ for those).
It doesn't make the storyboard — it watches it, and Claude uses it to
predict how a specific kind of viewer will actually receive a piece:
what grabs them, what loses them, what they'd ask afterward. Worker
personas judge craft against their own department; audience personas
judge the finished piece against whether it actually landed for a real
viewer.
-->

---
audience_id: {{slug}}                <!-- short slug, e.g. "product-manager" -->
audience_title: {{Audience Title}}   <!-- e.g. "Product Manager" -->
first_name: {{First Name}}           <!-- short first name, unique across every audience AND worker persona. Start it with the same letter as the audience (Retiree -> Robert, Young Adult -> Yoan) so the name is a memory hook back to who it represents -->
last_name: {{Represents}}            <!-- the surname IS what they represent, one word: Paula Product, Skye Social, Blair Blind, Soren Reliability. Must also be unique across every persona -->
category: {{one of exactly: internal / business | internal / leadership | internal / technical | external / general public | external / customer | disposition — this is a controlled vocabulary so the field can be filtered on; adding a new value means updating SKILL.md's grouping too. Use "disposition" only for reception styles that cut across every segment (optimistic, pessimistic, fact-only, emotional) rather than describing who someone is}}
---

<!-- Always refer to a persona by first AND last name — "Paula Product,"
     not "Paula" or "the PM." The surname carries what they represent, so
     a reader who has never opened this file still knows whose reaction
     this is. -->

# {{Audience Title}} — {{First Name}} {{Represents}}

<!-- One or two sentences: who they are and the context they're likely
     watching in (a QBR, scrolling social, a demo booth, at home). -->
**Who they are:** {{Background and viewing context.}}

## What they care about most

<!-- 3-5 bullets. What does this viewer actually want out of the two
     minutes they're giving this? Write as motivations, not demographics. -->
- {{Priority 1}}
- {{Priority 2}}
- {{Priority 3}}

## What draws them in

<!-- Concrete hook material specific to this viewer — the kind of opening,
     detail, or framing that earns their attention in the first few seconds. -->
- {{Hook element 1}}
- {{Hook element 2}}

## What loses them

<!-- Concrete tune-out triggers: jargon, pacing, assumed knowledge,
     irrelevant detail, condescension, length. Specific enough that Claude
     can actually flag it in a draft, not just "boring." -->
- {{Tune-out trigger 1}}
- {{Tune-out trigger 2}}

## Voice & reaction

<!-- How this persona reacts out loud (to a colleague, to themselves).
     Include a short example line in their voice. -->
{{Description of their reaction style — e.g. skeptical and terse; warm
and easily persuaded; distracted, half-watching.}}

> "{{Example reaction line in this persona's voice.}}"

## Example questions {{First Name}} {{Represents}} would ask

<!-- Concrete questions this persona wants answered once the piece ends,
     written so Claude can reuse the exact phrasing. If this persona rarely
     verbalizes anything (e.g. a scroller), still give one concrete example
     of what they'd ask if something did make them pause, and say so. -->
- "{{Question example 1}}"
- "{{Question example 2}}"

## Example feedback {{First Name}} {{Represents}} would give

<!-- Declarative reaction lines (not questions) — what this persona says
     out loud, to themselves or a companion, not what they ask the team. -->
- "{{Feedback example 1}}"
- "{{Feedback example 2}}"

## Signals it's working for them

<!-- How you'd actually know the piece landed for this persona — a
     behavior or reaction, not just "they liked it." -->
- {{Signal 1}}
- {{Signal 2}}

## Context they need going in

<!-- Prior knowledge this viewer does or doesn't bring. Tells the team
     what can be assumed vs. must be explained. -->
- {{e.g. "Already knows the product category" / "Has never heard of this space"}}

## Not their concern

<!-- What feedback attributed to this persona should NOT include — keeps
     audience personas from giving feedback that's really a worker
     persona's job (e.g. a teenager shouldn't be cited on shot composition). -->
- {{Area that isn't this persona's basis for judging the piece}}
