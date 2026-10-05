<!--
SERVICE RECOMMENDATIONS — storyboard skill

Dex Delivery's registry of which tool to use for which job.

WHY THIS FILE HAS DATES ON IT
This market moves faster than any other part of this skill. A "best tool"
claim written into a persona file would be quietly wrong within a year and
nobody would notice, the same way a hardcoded brand palette goes stale.
So recommendations live here, each with the date it was last checked and
what it was checked against.

RE-VERIFY BEFORE RELYING ON IT. If the "last reviewed" date is more than a
few months old, treat the row as a starting point rather than an answer,
check the vendor's current docs, and update the row.

WHO DECIDES
Dex Delivery recommends — he knows the dialects, the quirks and what the
boards need. He does not decide:
  - Paul Producer decides on cost, contracts and procurement.
  - Logan Legal clears the terms, especially commercial-use rights on
    generated output and anything involving a real person's likeness or
    voice.
An internally-approved vendor beats a better tool nobody is allowed to buy.
-->

# Service recommendations

**Last reviewed:** 2026-09-23

| Job | Recommended | Why | Adapter | Verified |
|---|---|---|---|---|
| **Voice / VO** | **ElevenLabs** | Current default for synthesized narration and character voices. Multi-voice, voice cloning, and prosody continuity across separately-rendered lines. | `scripts/send_elevenlabs.py` | 2026-09-21 against elevenlabs.io/docs |
| **Video / image generation** | Higgsfield | One authenticated API over many models, async with polling or webhooks. Model endpoints are model-specific — discover them in the console. | `scripts/send_higgsfield.py` | 2026-09-21 against docs.higgsfield.ai |
| **Typographic / UI / data frames** | **HyperFrames** | Compositions are HTML + CSS with seekable animation, rendered frame-by-frame in headless Chrome and encoded with FFmpeg — so output is **deterministic** and text is actually typeset rather than hallucinated. Apache 2.0, no per-render fee. | none yet — see below | 2026-09-23 against github.com/heygen-com/hyperframes and hyperframes.heygen.com |
| Motion graphics (hand-crafted) | After Effects, Figma, or Canva | A human motion designer still beats generative video for flat brand-style graphics — AI tools add 3D and glow to work that's meant to be flat. HyperFrames sits between this and generation: code, not a timeline, and an agent can write it. | none (human) | — |
| Captions | {{your platform's own, or a dedicated service}} | Auto-generated captions are never final; a human check is part of the accessibility floor. | none yet | — |
| Music | {{library or composer}} | See Sonny Sound's recommendation per piece — "no music" is often right. Licence tier must cover public distribution. | none yet | — |

## ElevenLabs — practical notes

The details that matter when rendering from boards, verified September 2026:

- `POST /v1/text-to-speech/{voice_id}`, `xi-api-key` header. **Synchronous** — the response body is the audio itself, unlike Higgsfield's queued `request_id` flow.
- `previous_text` / `next_text` carry prosody across separately-rendered lines. Worth using: without them, every frame sounds like a cold read and the joins are audible.
- `seed` gives best-effort reproducibility. Log it — it's the difference between re-rendering one line and re-rendering the piece.
- `voice_settings.speed` is how you match the boards' `pace_target_wpm`. Set it, then **measure the returned audio** rather than trusting it.
- SSML-style `<break time="1.2s" />` support **varies by model** — verify against the model you've chosen. If unsupported, strip the markers (`--pause-format ""`) and put the silence in the edit instead, and say so in the manifest so the pause doesn't quietly vanish.
- Text-to-Dialogue endpoints exist for multi-speaker exchanges; worth evaluating for a testimonial piece rather than rendering each speaker separately and assembling.

## HyperFrames — practical notes

Verified September 2026 against the repo and docs.

- **What it is:** an open-source framework (HeyGen, Apache 2.0) that turns
  HTML, CSS, media and seekable animation into MP4. `npx hyperframes
  init | preview | lint | render`, plus hosted `cloud render` and an AWS
  Lambda path. Needs **Node 22+ and FFmpeg** locally.
- **It is not an API.** Unlike ElevenLabs and Higgsfield, there is no
  endpoint to POST a frame to — you emit a composition and render it. That
  is a different operational shape: no key to manage, no per-generation
  cost, but a toolchain to install and code to review.
- **Deterministic.** Same input, same frames, same output. This is the
  headline difference from a diffusion model, and it changes what
  `delivery/manifest.md` is for: with Higgsfield you log a seed and hope,
  with HyperFrames the composition *is* the reproducible artifact.
- **The timing model maps onto a frame card almost one-to-one:**

  | Card field | HyperFrames |
  |---|---|
  | `Dur` | `data-duration` |
  | `Running` | `data-start` |
  | `Motion` (`BUILD — 40 rows → 3 over 1.2s`) | a seekable GSAP / CSS / WAAPI keyframe with those exact endpoints and that exact length |
  | `Trans out` (`DISSOLVE 0.5s — …`) | a catalog transition block (`npx hyperframes add flash-through-white`) |
  | `Text` | real typeset text, in the brand face, at the exact hex |
  | `Audio` | `<audio data-start data-volume>` on its own track |

  That correspondence is not a coincidence — a board that passes `--motion`
  (every animation timed, endpoints stated, `motion + join out ≤ Dur`) is
  already most of a composition spec.
- **`frame.md`** is their design-system-for-video format — a `DESIGN.md`
  superset written for the camera rather than the browser. It is the
  natural target for `reference/brand-guardrails.md`, and it's what makes
  the brand exact rather than suggested: a style block on a generation
  prompt nudges a model, CSS applies the actual value.
- **Name collision — check the URL.** `hyperframes.net` is a separate
  hosted text-to-video product and `hyperframe.ai` is an unrelated
  business-video platform. The thing described here is
  `github.com/heygen-com/hyperframes` / `hyperframes.heygen.com`.
- **Licensing is simpler but not absent.** Apache 2.0 with no
  commercial-use threshold, and nothing is generated, so there's no
  "who owns the output" question for Logan Legal. The media *inside* a
  composition still needs clearing — fonts especially, since embedding a
  typeface in rendered video is a licence question of its own.
- **No adapter ships with this skill yet.** The two existing adapters are
  HTTP clients and this isn't; wiring it means emitting HTML from
  `boards.py` and shelling out to the CLI, which is a real build rather
  than a copy of `send_higgsfield.py`. Say that plainly rather than
  implying a one-liner.

## When to recommend something else

- **A real person's testimonial stays their own recording.** The best synthesis on the market is still the wrong tool for "what the customer actually said." Synthesizing an identifiable person needs their permission for that specific use — see Logan Legal.
- **Match the tool to the brand's look, not the other way round.** If the guardrails call for flat 2D vector work, a photoreal video model will fight you the whole way and a motion designer will be faster — and HyperFrames may beat both, because flat vector work is what CSS is *for*.
- **A photographic frame is not a HyperFrames frame.** A real room, a real person, a location — that's Higgsfield or actual footage. HyperFrames renders what you can describe in markup, which is everything except photography.
- **An approved vendor with a worse model often wins.** Procurement, data-residency and security review are real constraints; Dex Delivery flags the tradeoff rather than assuming the better tool is available.

## Adding a service

Copy an existing adapter — `scripts/README.md` has the four things to
change — then add a row above with the date you verified it and what you
verified against.
