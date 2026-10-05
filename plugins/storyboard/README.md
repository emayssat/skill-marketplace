# storyboard

A Claude Code skill for producing and reviewing storyboards, animatics, and short video pieces. Assembles a crew of production role personas (scriptwriter, director, art director, editor, sound designer, producer, etc.) and audience reception personas to board a piece and screen it before anyone spends real production money.

## Skills

- **storyboard** — runs new storyboards, script reviews, revisions, platform adaptations, and audience screening rounds using named crew and audience personas

## What it covers

**Production workflows:** new storyboard, script review, remake, redesign, teaser, trailer, time extension/reduction, platform adaptation, localization

**Feedback workflows:** single persona reaction, preview (small panel), premiere (full panel + release go/no-go), handoff to generation services

**Crew personas:** Sasha Script, Dana Director, Vera Voice, Stella Storyboard, Arthur Art, Dean Photography, Molly Motion, Ed Edit, Sonny Sound, Paul Producer, Logan Legal, Claude Client, Dex Delivery

**Audience personas:** business/technical (product manager, SRE, C-suite, …), general public (teenager, retiree, social scroller, …), accessibility (blind, deaf, low-vision, cognitive/neurodivergent), disposition axes (optimist/pessimist, fact-only/emotional)

**Delivery scripts:** `scripts/boards.py` (storyboard audits), `scripts/send_higgsfield.py` (video generation), `scripts/send_elevenlabs.py` (voice synthesis) — dry-run by default, refuse unfrozen boards

## Install

```bash
claude plugin marketplace add emayssat/skill-marketplace
claude plugin install storyboard@skill-marketplace
```

## Usage

- "storyboard this product vision video"
- "review this video script before we board it"
- "how would a skeptical CTO react to this cut?"
- "cut this 2-minute video down to 30 seconds"
- "adapt this piece for vertical short-form"
