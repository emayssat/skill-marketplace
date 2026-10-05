---
workflow_type: redesign
workflow_title: Redesign (Same Content, New Visual Style)
---

# Redesign (Same Content, New Visual Style)

**When to use:** The story and script are locked and staying exactly as they are — what needs to change is the visual treatment: a rebrand, a new campaign look, or a medium switch (e.g. live action to animation). This is the mirror image of a remake: content is frozen, visuals move.

**Inputs required:** The prior approved script (explicitly not changing), and **the new guardrails** — not the ones the original piece was made against. A guidelines revision is the single most common trigger for this workflow, so start by confirming which version you're working from and updating `reference/brand-guardrails.md` before anyone restyles a frame.

**Pace:** the script is frozen, so wpm is unchanged by definition — but *perceived* pace isn't. A medium switch (live action to animation, say) changes how fast the same words feel, and a faster-cutting visual style makes a measured read feel sluggish. Check the target still matches the new look rather than assuming it carries over.

**Protected cuts:** read that standing note **before** looking for anything to lose. Logan Legal's cleared claims, Sonny Sound's consented testimonials, Claude Client's value-proposition beat and Arthur Art's brand minimums are all in there, and they are exactly the frames that look cheapest to cut. To change one, go back to the persona who protected it — not to the producer, not to the director. `scripts/boards.py --notes` fails on a protected frame marked CUT.

**Cards:** a restyle changes **Motion** as much as Visual — a new visual language usually implies a new motion language, and a board that restyles the pictures while leaving 2019's builds in place will look like two pieces. Molly Motion re-prices every Motion cell, not just the redrawn frames, and re-runs the continuity pass (`--motion`) — a new motion language changes durations, and durations are what the `motion + join out ≤ Dur` arithmetic depends on. Beyond that: every Visual cell is being rewritten and the VO cells are not, so the danger is a board half in the new look and half narrating the old one. Overwrite the Visual, Shot, Text and Trans cells outright — never `now 3D, was flat illustration` — and log the restyle once. `scripts/boards.py --cards` catches the leftovers.

## Sequence

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | producer | Confirm scope is visual-only — script is frozen; set budget for the new art/production pass | Confirmed scope |
| 2 | art-director | Lead role: define the new visual language (palette, typography, medium) against the unchanged script | New style guide |
| 3 | director | Validate the new style still serves the original emotional beats; escalate to scriptwriter only if a beat genuinely can't survive the new medium | Approved style direction |
| 4 | storyboard-artist | Redraw all frames in the new style, preserving the original shot list and blocking intent | New board pass |
| 5 | dp | Re-assess feasibility — a style or medium change can change gear/lighting needs, or become moot if switching to animation | Feasibility notes |
| 6 | editor | Re-cut the animatic in the new style/pacing if the medium change affects rhythm | New animatic |
| 7 | sound-designer | Align the music and sound palette with the new visual style or medium (e.g. a different score texture for animation vs. live action) | New score/mix |
| 8 | producer | Finalize schedule/budget for the new production approach | Locked schedule + budget |
| 9 | client | Approve the new look against brand guidelines — this review is style-only, not story | Approved redesign |

## Final output

The same story and script, delivered in a new visual identity or medium.

## Notes / anti-patterns

- If the director's step-3 escalation turns into a real script change, that's no longer a redesign — branch to **New Storyboard Creation** or **Remake** as appropriate instead of letting scope creep in quietly.
- Art director leads this workflow, not the director — resist defaulting back to director-led review habits from the creation workflow.
- Client sign-off should stay focused on the visual system, not reopen story decisions that were never on the table for this pass.
