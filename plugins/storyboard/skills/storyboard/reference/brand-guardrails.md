<!--
BRAND GUARDRAILS — storyboard

The source Arthur Art (art director) styles against and Logan Legal (legal/brand
reviewer) clears against. Ships blank on purpose: this skill is
org-agnostic, and brand guidelines change — a palette baked into the skill
is a palette that goes stale without anyone noticing.

WHERE THE FILLED VERSION LIVES
  - Organization default → fill this file in place.
  - A piece that follows different rules (a sub-brand, a co-branded piece,
    a customer's brand) → copy to <production>/brand-guardrails.md
    and point the production brief at it.

NEVER invent these values, and never carry them over from a previous
production without re-checking. Brand guidelines get revised; a value that
was right last quarter may not be right now.
-->

# Brand guardrails — {{organization or brand}}

**Primary source:** {{link to the official brand guidelines}}
**Format received:** {{brand book PDF | slide deck | YouTube video | video file | brand site | Figma file | existing production}}
**Derived by:** {{who extracted this, and how}}
**Last reviewed:** {{YYYY-MM-DD}} · **Guidelines version:** {{if the source is versioned, record it — this is what tells you when this file is stale}}

---

## If you don't have this yet — ask

Do not style anything against guessed rules, and do not infer a brand from
what previous videos happened to look like. Ask for whichever of these
exists, in rough order of usefulness:

| Source | What it gives you | Caveat |
|---|---|---|
| **Brand book** (PDF or slide deck) | Exact values — hex, typefaces, logo rules, clear space, tone | The best case. Ask for this first. |
| **Brand site** (a live guidelines URL) | Same, usually current, sometimes with downloadable assets | Check for a "last updated" date |
| **Design file** (Figma, Sketch, Adobe) | Real tokens, components, spacing scale | May be a working file rather than the approved system |
| **Existing video** (YouTube link or file) | The system *in use* — motion vocabulary, pacing, recurring motifs, end-card format | Shows behavior, not underlying values. Everything read off a frame is an ESTIMATE. |
| **Slide template** (.pptx / .key) | Palette and type as actually applied internally | Often drifts from the official book |
| **A previous production** | A starting hypothesis only | Ask whether it was ever brand-approved |

**Ask like this:** "Before I style anything — do you have brand guidelines
I should work from? A brand book PDF, a slide deck, a link to your brand
site, a Figma file, or even a YouTube link to a video that's on-brand all
work. If there's a video, timestamps of two or three representative
moments help."

### Reading guardrails out of a video

A video is the most common thing people have and the weakest source, so
handle it deliberately: sample frames across the whole piece rather than
the opening; record palette, type treatment, motion vocabulary, recurring
motifs, and the end-card format; note what the piece *never* does, which is
often more instructive than what it does. Then mark every value ESTIMATED
and ask whether a brand book sits behind it.

---

## Confidence marking

Tag every value in the sections below:

- **CONFIRMED** — from an official source
- **ESTIMATED** — derived from frames, screenshots, or eyeballing; must be confirmed before production
- **NEEDED** — known to exist, not yet supplied

Arthur Art raises ESTIMATED values still in play late in a production; Logan Legal
won't clear a release that depends on one.

## Palette

| Role | Name | Hex | Confidence | Use |
|---|---|---|---|---|
| Hero | {{}} | {{}} | {{}} | {{the one color reserved for the biggest moments}} |
| Background | {{}} | {{}} | {{}} | {{}} |
| Neutral | {{}} | {{}} | {{}} | {{}} |
| Accent | {{}} | {{}} | {{}} | {{}} |

**Color grammar:** {{how the palette carries meaning across a piece — which colors signal tension vs. resolution, what's reserved and how sparingly}}

## Typography

- **Headlines / display:** {{typeface}}
- **Labels, captions, UI:** {{typeface}}
- **Case and punctuation rules:** {{e.g. sentence case only; no exclamation points}}
- **Minimum on-screen size:** {{legibility floor at phone width}}

## Visual rules

1. **Dimensionality and finish:** {{flat vs. dimensional; gradients, glow, shadows allowed or not}}
2. **Shape language:** {{the vocabulary — geometric, organic, illustrative}}
3. **Recurring motifs:** {{the cues that make work recognizable as this brand}}
4. **Density:** {{negative space expectations, ideas per frame}}
5. **Motion:** {{easing, speed, what motion should feel like — and what it must never do}}
6. **Logo:** {{approved colors, clear space, lockups, co-branding rule, watermark}}

## Verbal

- **Tone:** {{}}
- **Construction:** {{voice, sentence length, contractions}}
- **Product naming:** {{exact capitalization, first-mention vs. subsequent form}}
- **Words to avoid:** {{banned superlatives, deprecated names}}

## Claims

- **Requires substantiation:** {{claim types needing a source and measurement date}}
- **Competitor references:** {{policy on named or implied comparison, and on vendor logos}}
- **Customer material:** {{permission required for names and logos; rule on real data, domains, and traffic in screen captures — default should be synthetic data only}}

## Accessibility floor

Not brand strictly, but it belongs beside it: it's far cheaper to design
for than to retrofit, and it's what Dev Deaf, Blair Blind, Leo Vision and Cora Cognitive check at
premiere.

- Human-checked captions on every piece; auto-generated captions are never final.
- Minimum text contrast 4.5:1 against its background — check the brand's own near-neighbor combinations, which are the ones that usually fail.
- No information conveyed by color alone. If the brand's color grammar carries meaning rather than mood, it needs a shape or label differentiator alongside it.
- Audio description, or narration covering what the picture shows, wherever the visual carries meaning the voiceover doesn't.
- No strobing or rapid flashing; content warning where unavoidable.

## Open items

- [ ] {{value still marked ESTIMATED or NEEDED, and who was asked for it}}
