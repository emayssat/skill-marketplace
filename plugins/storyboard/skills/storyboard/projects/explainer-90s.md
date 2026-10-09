---
project_type: explainer-90s
project_title: 90-Second Explainer
duration: "1:30"
format: 16:9, motion graphics + UI capture + voiceover
---

# 90-Second Explainer

**Goal:** Make someone who didn't understand the thing understand it — well enough to explain it back badly, which is the real bar.

**Audience:** Whoever is being onboarded to the concept: `seth` (software engineer) and `soren` (SRE) for technical explainers, `paula` (product manager) and `marcus` (mid-level manager) for product ones, `nadia` for anything shipping globally. Note that the audience is defined by *not already knowing*, which is the opposite of most other formats here.

**Key message:** The mental model. Not the feature list, not the value proposition — the shape of how the thing works.

**Tone:** Patient, concrete, slightly under-confident. An explainer that sounds like a sales pitch stops being believed at the halfway mark.

## Story structure (default)

**question → answer** — an explainer's audience arrives with the question already formed, and resents being sold to on the way to the answer.

Scott Script can deviate, but says so in the brief and says why. The beat breakdown below is this structure's stages named for this format; changing the structure changes the beats.

## Beat breakdown

| Time | Beat | What happens |
|---|---|---|
| 0:00–0:10 | The problem, concretely | A specific situation the viewer recognizes — not an abstraction. |
| 0:10–0:25 | Why the obvious fix doesn't work | Earns the rest of the runtime. Skipping this is why most explainers feel like ads. |
| 0:25–1:05 | The mechanism | The core: how the thing actually works, built up in two or three layers, each one shown. |
| 1:05–1:20 | Seeing it work | One concrete end-to-end example using the mechanism just explained. |
| 1:20–1:30 | Where to go next | Docs, trial, or the next explainer — one destination. |

## Team for this project

- **Scott Script (scriptwriter)** — carries this format; explainers live or die on the script's ordering of ideas.
- **Vera Voice (voice talent)** — heavier than usual: explainer VO is dense, and read-time overrun is the standard failure.
- **Dana Director (director)** — guards against the pitch creeping in, especially in the last 25 seconds.
- **Arthur Art (art director)** — owns visual consistency of the metaphor; a diagram that changes its own visual rules mid-explanation undoes the explanation.
- **Molly Motion (motion lead)** — usually leads over Dean Photography; the mechanism beat is almost always animated diagram work.
- **Ed Edit (editor)** — protects the beat-3 build; the instinct to speed it up is usually wrong.
- **Sonny Sound (sound designer)** — music stays under and out of the way; this format needs comprehension, not mood.
- **Paul Producer (producer)** — animation days for the mechanism beat are the whole budget.

## Deliverables checklist

- [ ] Locked script, read-time verified against 1:30
- [ ] Approved boards, with the mechanism beat's build broken out frame by frame
- [ ] Animatic
- [ ] Diagram/metaphor consistency check
- [ ] Sign-off

## Constraints specific to this project

- Assume zero prior knowledge of the mechanism, and existing knowledge of the domain — explaining what a CDN is to an SRE is condescending; explaining your specific cache invalidation model is not.
- One metaphor for the whole piece. Two metaphors for the same mechanism is worse than none.
- The mechanism beat (0:25–1:05) is two thirds of the value and most of the budget. Protect it when the runtime gets squeezed — cut beat 5 before cutting beat 3.
