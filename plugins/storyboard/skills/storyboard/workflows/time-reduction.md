---
workflow_type: time-reduction
workflow_title: Time Reduction (Shorten an Existing Storyboard)
---

# Time Reduction (Shorten an Existing Storyboard)

**When to use:** An existing storyboard needs a shorter cut for a different placement (e.g. a 30-second social version of a 2-minute piece). Unlike a trailer, this cut still needs to feel complete and self-contained on its own — it's a shorter version of the story, not a teaser for the long one.

**Inputs required:** The source piece's approved script, boards, and animatic; the new target duration and platform.

**Pace:** this is the workflow where pace breaks. Cutting duration without cutting words raises wpm on every beat you keep, and the arithmetic is brutal — halving the runtime doubles the rate. Re-run `--pace` after every trim, and expect to lose words roughly in proportion to the seconds. The runtime is fixed by definition here, so stretching is not available.

**Protected cuts:** read that standing note **before** looking for anything to lose. Logan Legal's cleared claims, Sonny Sound's consented testimonials, Claude Client's value-proposition beat and Arthur Art's brand minimums are all in there, and they are exactly the frames that look cheapest to cut. To change one, go back to the persona who protected it — not to the producer, not to the director. `scripts/boards.py --notes` fails on a protected frame marked CUT.

**Cards:** Motion is a place to find seconds that nobody looks at — a 1.5s build shortened to 0.6s buys time without losing a word, and Ed Edit counts it alongside pauses and joins. Re-spec the cell; don't just run the same motion faster and hope. Beyond that: cut frames keep their row and their number, marked CUT — that is the record that they existed, so the surviving cards don't need to mention them. Resist `tightened from 0:06` in a Dur cell or `absorbed frame 7's line` in a VO cell: overwrite, and log the reduction once with the frames it touched.

## Sequence

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | producer | Confirm target duration and platform requirements (e.g. must work sound-off/captioned) | Confirmed scope |
| 2 | editor | Lead role: identify the minimum sequence of beats that keeps the story complete at the new length; propose what to cut | Proposed cut list |
| 3 | director | Approve the cuts — the shortened version must still land the key message, not feel truncated | Approved cut plan |
| 4 | scriptwriter | Trim or rewrite narration to fit the new pacing; write new connective lines where content removal creates a gap | Revised script (short version) |
| 5 | storyboard-artist | Adjust or add transition frames where a cut creates a jump that didn't exist in the original | Updated board pass |
| 6 | art-director | Verify no removed context (e.g. a setup shot) leaves a later visual unclear without it | Confirmed visual continuity |
| 7 | editor | Final cut at the new duration | Short-form cut |
| 8 | sound-designer | Re-trim and re-mix the music and sound to fit the new cut, with no abrupt cutoffs at trim points | Re-mixed audio |
| 9 | producer | Confirm delivery specs for the target platform | Confirmed specs |
| 10 | client | Approve that the short version still meets the objective — not just that it's shorter | Approved short version |

## Final output

A shorter, self-contained version of the storyboard at the new target duration.

## Notes / anti-patterns

- The test for this workflow is completeness, not brevity — if the cut only works as a preview for the long version, it's actually a **Trailer**, and should switch to that workflow.
- Watch for orphaned payoffs: cutting the setup for a later beat (step 6's job) is the most common way a "just shorter" cut quietly stops making sense.
- Don't skip new connective copy (step 4) — removed content often leaves a narration gap that a straight trim won't fix.
