---
workflow_type: trailer
workflow_title: Trailer Creation
---

# Trailer Creation

**When to use:** A full piece already exists (or its boards/script do), and a short promotional cut is needed — designed to create intrigue, not to be watched instead of the full piece. Distinct from **Teaser**: a trailer is mined from finished or fully boarded material and shows real substance; a teaser is much shorter, can be built before the full piece exists, and deliberately reveals almost nothing.

**Inputs required:** The source piece's approved boards, script, and animatic (or final footage, if it exists).

**Pace:** trailers run faster than their source, and that's legitimate — but it's a *pace target change*, made deliberately and recorded, not an accident of cramming source lines into a shorter cut. Set the trailer's own target; don't inherit the full piece's.

**Protected cuts:** read that standing note **before** looking for anything to lose. Logan Legal's cleared claims, Sonny Sound's consented testimonials, Claude Client's value-proposition beat and Arthur Art's brand minimums are all in there, and they are exactly the frames that look cheapest to cut. To change one, go back to the persona who protected it — not to the producer, not to the director. `scripts/boards.py --notes` fails on a protected frame marked CUT.

**Cards:** a trailer's energy lives in Motion and Trans out more than in the frames themselves, and both are new decisions here — the source piece's pacing of a build will be wrong at trailer speed. Frames are lifted from the source piece and rejoined in a new order, which means most of the **Trans** cells are new decisions and need Transitions rows to match. Copy each card's current state and nothing else — the source board's history stays with the source board.

## Sequence

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | producer | Define trailer length, placement, and deadline (often tied to the source piece's release date) | Trailer brief |
| 2 | editor | Lead role: mine the source material for the strongest, most self-contained moments; propose a cut list | Proposed cut list |
| 3 | director | Approve which moments represent the piece without giving away the full arc or ending | Approved moment list |
| 4 | scriptwriter | Write any new connective narration or copy the trailer needs but the source script doesn't have (e.g. a CTA line) | New trailer copy |
| 5 | storyboard-artist | Board any new frames not in the original (new opening hook, new CTA card) | New frames |
| 6 | art-director | Ensure trailer-specific graphics (title cards, logo bumper) match brand and the source material's style | Approved graphics |
| 7 | editor | Assemble the trailer cut at teaser pacing — faster than the source | Trailer cut |
| 8 | sound-designer | Build trailer-specific music and sound design — usually punchier or different from the source, often ending on a sting or button | Trailer mix |
| 9 | producer | Confirm delivery specs (aspect ratio, captions) for the trailer's platform | Confirmed specs |
| 10 | client | Approve the trailer on its own terms — judged on intrigue, not completeness | Approved trailer |

## Final output

A standalone trailer cut, plus any new assets (copy, frames, graphics) created specifically for it.

## Notes / anti-patterns

- A trailer that explains everything has failed at its job — director's step-3 gate exists specifically to protect against over-revealing.
- Don't skip step 4/5 assuming the trailer is "just an edit" — almost every trailer needs at least one new line or frame the source never had (an opening hook, a CTA).
- Client approval criteria are different here than for the source piece — say so explicitly rather than letting them apply the source piece's rubric.
