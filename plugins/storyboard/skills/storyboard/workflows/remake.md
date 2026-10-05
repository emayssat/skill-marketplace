---
workflow_type: remake
workflow_title: Remake (Content Refresh, Same Storyline)
---

# Remake (Content Refresh, Same Storyline)

**When to use:** An approved storyboard already exists and the underlying story/beat structure still works, but specific content inside it is stale — outdated stats, an old UI screenshot, last year's branding, a name that changed. The story doesn't need rethinking; the content inside it does.

**Inputs required:** The prior approved project (script, boards, animatic) plus a clear list of what's actually stale.

**Pace:** new content has to fit the *old* timing. Refreshed copy is almost always longer than what it replaced (a new product name, an extra qualifier, a bigger number), so re-run `--pace` on every changed beat even though the boards look untouched. If the new words won't fit and the runtime is fixed, they get cut here rather than rushed in the read.

**Protected cuts:** read that standing note **before** looking for anything to lose. Logan Legal's cleared claims, Sonny Sound's consented testimonials, Claude Client's value-proposition beat and Arthur Art's brand minimums are all in there, and they are exactly the frames that look cheapest to cut. To change one, go back to the persona who protected it — not to the producer, not to the director. `scripts/boards.py --notes` fails on a protected frame marked CUT.

**Cards:** this is where boards rot. New content is being written into frames that already have a past, and the reflex is to leave a trail — `was the 2024 figure`, `updated after the refresh`. Don't: **overwrite the cell** and put one Revision log row against the frames that changed. The whole point of a remake is a board that reads as if it had always said this. Run `scripts/boards.py --cards` before handing it on; it fails on exactly this.

## Sequence

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | producer | Pull the original project file, script, and boards; confirm with the requester exactly what's changing vs. staying | Delta list (what's stale) |
| 2 | scriptwriter | Revise only the lines tied to stale content | Revised script (delta only) |
| 3 | director | Approve the revision against the original arc; escalate if a beat itself no longer works (that's a bigger change than a remake) | Locked revised script |
| 4 | art-director | Refresh visual references only where brand/product visuals changed | Updated references (delta only) |
| 5 | storyboard-artist | Redraw only the frames tied to changed content; reuse unchanged frames as-is | Updated board pass |
| 6 | dp | Re-check feasibility only for new/changed shots | Feasibility notes (delta only) |
| 7 | editor | Patch the existing animatic with updated frames/audio; spot-check pacing didn't shift | Updated animatic |
| 8 | sound-designer | Patch the mix only where VO or timing changed (new lines, re-synced hits); reuse the rest of the score/mix as-is | Updated mix (delta only) |
| 9 | producer | Lighter budget/schedule pass since scope is mostly reuse | Confirmed scope/cost |
| 10 | client | Approve the delta, not a full re-review | Approved refresh |

## Final output

The same storyboard and storyline, with stale content replaced — script, boards, and animatic updated only where content changed.

## Notes / anti-patterns

- If step 3 surfaces that a beat needs to change (not just its content), stop and switch to the **New Storyboard Creation** workflow for that beat — a remake that starts rewriting structure isn't a remake anymore.
- Resist re-reviewing frames (or re-mixing audio) that didn't change — the point of this workflow is that most of the prior work carries over untouched.
- Client review should be scoped to "what changed and why," not a from-scratch approval — re-litigating settled story decisions here wastes the efficiency this workflow exists for.
