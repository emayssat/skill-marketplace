---
workflow_type: handoff
workflow_title: Handoff to Production Services
---

# Handoff to Production Services

**When to use:** The boards are premiere-approved and frozen, and the piece now has to become real — converted into whatever each downstream service needs. Video generation (Higgsfield, Runway, Veo), voice synthesis (ElevenLabs), motion or edit tools, caption and subtitle services, or a human production vendor.

This runs **after `premiere.md`**, deliberately. By this point no further changes are being made to the storyboard, which is what makes a clean handoff possible at all: every service is being fed from one frozen source rather than from whatever the boards happened to look like that day.

**Inputs required:** Boards at `status: approved`, the locked script, `reference/brand-guardrails.md` (for the style block), the target service list with model versions, and any reference images or voice samples needed for consistency.

**Tooling:** `scripts/` holds runnable adapters — `boards.py` (parse, pace, voices), `send_higgsfield.py` (video/image) and `send_elevenlabs.py` (voice), plus a guide to adding another. `reference/services.md` says which service is recommended for which job, and when that was last verified. They dry-run by default and refuse boards that aren't frozen, which enforces this workflow's central rule mechanically rather than on trust.

**Pace:** synthetic voices have their own pace settings, and the default is rarely the pace you chose. Set the service's rate to match `pace_target_wpm`, then measure the returned audio rather than trusting the setting — a voice that renders 15% fast quietly breaks every timing in the boards. Marked pauses must survive translation into the service's own break syntax, or the pace collapses even at the right rate.

**Delivery routing:** Dex Delivery fills in the board's **Delivery routing** standing note at step 3 — which service or vendor builds which frames, with the model or voice named. **The routing is per frame, not per piece:** photographic frames go to a generation service or real footage, while typographic, UI, chart and lockup frames are usually better rendered as code (HyperFrames) than generated, because text comes out typeset rather than hallucinated and the render is deterministic. A piece heading for localization tips that decision further — swapping text and re-rendering beats regenerating every frame. That table is the map and stays on the board; `delivery/manifest.md` is the log, with the exact prompts, model versions and seeds. A row naming a service but no model is an intention, not routing.

**Cards:** Dex Delivery sends what the cards say, literally — so a card still carrying `(was a wide shot)` puts the rejected shot in the prompt. Run `scripts/boards.py --cards` before the first submission; it exits non-zero on history, stray defaults, and any card contradicting a standing note.

## Sequence

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | delivery | Recommend the service for each job from `reference/services.md` (currently ElevenLabs for voice, Higgsfield for video/image), noting model versions and anything the boards need that the service can't do | Recommended service list |
| 2 | producer | Decide: approve the recommendation, or substitute on cost, contract or procurement grounds. Confirm the boards are premiere-approved and frozen, and that `scripts/boards.py --cards` and `--motion` are clean — a card still carrying history will be read out as an instruction, and an animation that doesn't fit its frame will be generated truncated | Agreed services; boards confirmed frozen |
| 3 | delivery | Translate the boards into per-service inputs — generation prompts per frame, VO manifest per line, caption file, timing sheet, **and the Transitions table as an edit spec** (most generative services make shots, not joins — the transitions happen in the edit). Use `scripts/` (dry run first: `python3 scripts/send_higgsfield.py <boards.md> --model-path ...`) | Export package per service |
| 4 | art-director | Check the style block carried into every prompt actually encodes the brand guardrails; this is where a generative service drifts off-brand silently | Style block approved |
| 5 | sound-designer | Confirm the Cast & voices table is complete and cleared: every speaking frame names a speaker, every speaker has a described voice and a source, voices are distinguishable from each other, and any real person's voice has consent on file. `python3 scripts/boards.py <boards.md> --voices` audits this mechanically | Cast cleared; speaker → voice mapping |
| 6 | voice-talent | Review the VO manifest **per speaker** — pronunciation of product and brand names, emphasis, pacing — reading each speaker's lines in that speaker's voice, not one generic read | Approved VO manifest |
| 7 | sound-designer | Confirm the audio spec: format, loudness target, stems, and what gets mixed where | Audio spec |
| 8 | delivery | Run the generation, collect outputs, and log service, model version, settings, seeds and prompts for every shot | Generated assets + delivery manifest |
| 9 | director | Review the returned assets against the approved boards and flag drift, frame by frame | Drift list |
| 10 | delivery | Re-prompt the drifted shots only — iterating the prompt, never the board | Corrected assets |
| 11 | legal-reviewer | Clear what the service introduced that nobody authored (an incidental face, a logo-like mark, a recognizable likeness), and confirm the service's terms permit commercial use of the output | Written clearance |
| 12 | producer | Accept delivery and archive the manifest alongside the production | Delivery accepted + archived |

## Final output

The generated assets, plus `<production>/delivery/manifest.md` — a record complete enough that any single shot can be regenerated months later without guessing which model, seed or prompt produced it.

## Notes / anti-patterns

- **The boards are frozen. If a generated shot can't be achieved, the fix is the prompt, not the board.** A change big enough to need a board change is a change big enough to need another premiere — the alternative is a piece that quietly stops matching the thing everyone approved.
- Step 11 is not optional paranoia. Generative output regularly contains things nobody wrote — a face, something logo-shaped, a recognizable style — and the service's own terms decide whether you may use the result commercially at all. Both get checked before release, not after.
- **A real person's voice is not a style you can generate.** Cloning an identifiable customer or colleague to say words they never said needs their permission for that specific use, not just a general testimonial release. Step 5 catches a blank consent column; don't route around it because the recording was inconvenient to schedule.
- Continuity is the standard failure. Without a seed or reference strategy (step 3), the same character across six frames comes back as six different people, and it's cheaper to plan for that than to re-roll forty generations hoping for a match.
- Log settings as you go, not afterwards from memory. A manifest reconstructed after the fact is a guess, and the first person to need it will be someone asking for one small change.
- Feeding several services from the same frozen boards is the point of doing this after premiere. Handing one vendor last week's boards and another this week's is how two halves of a piece stop matching.
