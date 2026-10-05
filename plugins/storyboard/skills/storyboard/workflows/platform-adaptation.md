---
workflow_type: platform-adaptation
workflow_title: Platform Adaptation (Reframe for a Different Aspect Ratio / Platform)
---

# Platform Adaptation (Reframe for a Different Aspect Ratio / Platform)

**When to use:** An approved piece exists in one format (e.g. 16:9) and needs a version reframed for a different platform's specs (e.g. 9:16 vertical for social) — without necessarily changing the story, script, or duration.

**Inputs required:** The source piece's approved boards and final footage/animatic, plus the target platform's specs (aspect ratio, safe zones, caption requirements, length caps).

**Pace:** platforms have pace norms, and they differ sharply — social expects faster than a website embed. If the target changes, change it explicitly in the boards rather than letting the re-cut drift. Watch the interaction with on-screen text: a faster platform cut gives burned-in captions less time to be read, not more.

**Protected cuts:** read that standing note **before** looking for anything to lose. Logan Legal's cleared claims, Sonny Sound's consented testimonials, Claude Client's value-proposition beat and Arthur Art's brand minimums are all in there, and they are exactly the frames that look cheapest to cut. To change one, go back to the persona who protected it — not to the producer, not to the director. `scripts/boards.py --notes` fails on a protected frame marked CUT.

**Cards:** motion is the first thing a reframe breaks — a horizontal wipe, a wide track or a build that fanned out sideways has nowhere to go in a 9:16 crop, so every Motion cell gets re-specced rather than inherited. Beyond that: an adaptation is its own board, not an annotated copy of the original. Cards state what *this version* is — the vertical crop, the burned-in caption, the shorter hold — with no trace of what the 16:9 cut did. **Text** matters more here than anywhere: platform text is often the only thing a sound-off viewer receives, and it goes in the card verbatim with a row in On-screen text.

## Sequence

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | producer | Confirm target platform specs — aspect ratio, safe zones, captions, any length cap | Platform spec sheet |
| 2 | art-director | Define how key visual elements (logo, text, key subject) get repositioned for the new frame; flag anything that won't survive a crop | Reframing guide |
| 3 | storyboard-artist | Reframe/redraw boards for the new aspect ratio, prioritizing subject and on-screen text readability in the new crop | Reframed boards |
| 4 | director | Approve that the intended focus and emotion still read in the new framing | Approved reframe |
| 5 | dp | Note whether the crop needs reshooting/reframing on the day, or is a post-only reframe of existing footage | Feasibility notes |
| 6 | editor | Re-cut/reframe existing footage or new boards into the new aspect ratio; adjust pacing if the platform expects faster cuts | Platform cut |
| 7 | sound-designer | Remix for the platform's norms — loudness normalization, and ensure the piece still works with sound off since most social is watched muted | Platform mix |
| 8 | producer | Confirm captions/on-screen text meet platform norms (most social is watched sound-off) | Confirmed compliance |
| 9 | client | Approve the platform-specific cut | Approved adaptation |

## Final output

A platform-specific version of the same piece — same story and (usually) same duration, reframed and re-paced for where it will run.

## Notes / anti-patterns

- This is a reframe, not a redesign — if the platform version starts changing the visual style itself rather than just its framing, coordinate with the **Redesign** workflow instead.
- Step 5 matters: some crops are a free post-production reframe, others quietly require a reshoot because the original framing didn't leave enough room — catch this before promising a delivery date.
- Don't assume duration carries over unchanged — check the target platform's own length norms/caps in step 1.
