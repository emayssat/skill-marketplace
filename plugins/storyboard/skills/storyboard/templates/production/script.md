<!--
SCRIPT TEMPLATE — storyboard

Scott Script's artifact. Copy to <production>/script.md.

The production folder lives in your own working folder, NEVER inside the
skill — the skill ships only this stencil.

Keep it beat-aligned: each section maps to a beat in the project type's
breakdown, so the script, the boards, and the brief all describe the same
structure. Frame numbers get added once boards exist, which is what lets
a persona say "the line in frame 12 fights the visual."

`status: locked` is a real gate — several workflows refuse to proceed
against an unlocked script, and Sonny Sound won't score against one.
-->

---
production: {{slug}}
artifact: script
version: {{v1}}
status: {{draft | in-review | locked}}
word_count: {{n}}
read_time: {{0:00}}
updated: {{YYYY-MM-DD}}
---

# {{Production Title}} — Script {{v1}}

**Status:** {{draft}} · **Estimated read time:** {{1:58}} at ~150 wpm

<!-- Read time is the reality check. VO runs roughly 150 words per minute
     at a comfortable pace; a 2:00 piece is about 300 words INCLUDING
     pauses, which in practice means 250 or fewer. If the count is over,
     the script doesn't fit and no amount of fast editing fixes it. -->

## {{Beat 1 — Hook}} · {{0:00–0:15}} · frames {{1–3}}

**NARRATOR:** {{The line, exactly as spoken. [PAUSE 0.8] Silence marked inline, with a number.}}

**On screen:** {{Any text or title card, exactly as it appears.}}

**Note:** {{Intent for the performer — tone, emphasis, what the pause is for.}}

## {{Beat 2 — Testimonial}} · {{0:15–0:35}} · frames {{4–8}}

**MARIA:** {{The line, exactly as spoken.}}

**DEV:** {{...}}

**On screen:** {{...}}

<!-- Every line is attributed to a speaker in caps, matching a label in
     the Cast & voices table in boards.md. Never write an unattributed
     line: in a multi-speaker piece an orphan line can't be cast,
     recorded, mixed or captioned, and "we'll work out who says it later"
     means somebody guesses during the mix.

     Real testimonials: transcribe what the person actually said rather
     than writing what you'd like them to have said. Tightening a real
     quote is editing; rewriting it and keeping their name on it isn't. -->

### Read time by speaker

<!-- Vera Voice fills this in at the read-through. Each speaker's total,
     against the time their frames allow. A piece can be on-length overall
     and still have one speaker with twice the words they have seconds. -->

| Speaker | Words | Read time | Pauses | Total | Time allowed | Fits? |
|---|---|---|---|---|---|---|
| {{NARRATOR}} | {{120}} | {{0:48}} | {{2.0s}} | {{0:50}} | {{0:50}} | {{yes, exactly}} |
| {{MARIA}} | {{70}} | {{0:28}} | {{0.8s}} | {{0:29}} | {{0:20}} | {{no — cut ~20 words}} |

Pause time counts against the runtime like words do. A read that fits only
because nobody counted the silences doesn't fit.

---

## Open questions

- {{Line or claim that needs legal/PR clearance before this can lock}}

## Revision log

| Version | Date | What changed | Driven by |
|---|---|---|---|
| v1 | {{date}} | First draft from brief | {{brief.md}} |
