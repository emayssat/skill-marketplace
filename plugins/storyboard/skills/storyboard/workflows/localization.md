---
workflow_type: localization
workflow_title: Localization (Adapt for Another Language or Region)
---

# Localization (Adapt for Another Language or Region)

**When to use:** An approved piece needs a version for another language or region. Distinct from **Platform Adaptation**, which changes the frame; this changes the language, and language changes timing, layout, and sometimes what you're even allowed to claim.

**Inputs required:** The approved final cut, script, and boards; the target locale(s); and a decision on depth — subtitles only, VO replacement, or full re-cut.

**Pace:** the central risk. A faithful translation can run 20–30% longer than the English, so the same beat arrives over the ceiling in the target language even though the source was comfortable. Set a per-locale pace target, re-run `--pace` against the translated script, and fix it by trimming the translation or stretching the beat — never by asking the voice to race, which destroys comprehension for exactly the audience this workflow exists to serve.

**Protected cuts:** read that standing note **before** looking for anything to lose. Logan Legal's cleared claims, Sonny Sound's consented testimonials, Claude Client's value-proposition beat and Arthur Art's brand minimums are all in there, and they are exactly the frames that look cheapest to cut. To change one, go back to the persona who protected it — not to the producer, not to the director. `scripts/boards.py --notes` fails on a protected frame marked CUT.

**Cards:** the **Text** column is a translation target, not decoration — on-screen wording in the target language, verbatim, with its own On-screen text row, because translated text is almost always longer and the hold time was set for the source. Cards carry the localized current state; the source-language wording lives in the Revision log or the source board, never in a parenthesis on the card.

## Sequence

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | producer | Confirm target locales and localization depth: subtitles only, VO replacement, or full re-cut | Locale + depth decision |
| 2 | scriptwriter | Adapt the script for translation — flag every idiom, pun, and culture-specific reference that won't carry, and supply a literal alternative | Translation-ready script |
| 3 | *Nadia Language + any locale-relevant personas* | Review the adapted script for comprehensibility and anything that reads oddly outside the source culture | Comprehension notes |
| 4 | art-director | Check on-screen text against the new language: German and Finnish run roughly 30% longer than English, and symbols, gestures and colors don't carry the same meaning everywhere | Layout + iconography verdict |
| 5 | voice-talent | If VO is being re-recorded: supply the pronunciation guide for product, brand and customer names in the target language | Pronunciation guide |
| 6 | editor | Re-cut for the new text and VO timing — translated VO rarely matches the original's length, so beats stretch or compress | Localized cut |
| 7 | sound-designer | Re-mix under the new VO; the music bed stays, the levels and ducking don't | Localized mix |
| 8 | legal-reviewer | Re-check claims per jurisdiction — a claim that's substantiated and permitted in one market may be neither in another | Per-locale clearance |
| 9 | client | Approve the localized version, ideally with a native speaker in the room | Approved localization |

## Final output

A locale-specific version of the piece, with its own cut, mix, and clearance — tracked as its own version in the production folder, not as an overwrite of the original.

## Notes / anti-patterns

- Text expansion is the most reliable way this breaks. A title card that fits in English will overflow in German, and nobody notices until the frame is already animated.
- Don't assume timing carries over. Step 6 exists because a faithful translation can run 20% long, and squeezing the VO to fit produces a read nobody wants to listen to.
- Idioms are the first failure point and the easiest to fix — catch them at step 2, not after recording.
- Step 8 is not a formality. Comparative claims, regulated-industry language, and privacy statements are jurisdiction-specific; clearance in the source market clears nothing elsewhere.
- Subtitles are not localization. They're the cheapest tier of it, and they leave anyone who can't read at speed — including Dev Deaf, who relies on captions — with a worse experience than the original audience got.
