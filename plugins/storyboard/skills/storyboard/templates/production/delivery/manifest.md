<!--
DELIVERY MANIFEST TEMPLATE — storyboard skill

Dex Delivery's artifact, produced by workflows/handoff.md. Copy to
<production>/delivery/manifest.md.

The production folder lives in your own working folder, NEVER inside the
skill — the skill ships only this stencil.

The point of this file is REPRODUCIBILITY. Generated output is not
deterministic, and "we'll remember the settings" is never true. Six months
from now someone will ask for one shot to be regenerated with a small
change, and this file is the difference between re-rolling that one shot
and re-generating the whole piece hoping it matches.

Fill it in AS YOU GO. A manifest reconstructed from memory afterwards is a
guess wearing a table.
-->

---
production: {{slug}}
artifact: delivery-manifest
boards_version: {{v3 — must be the premiere-approved, frozen version}}
status: {{in-progress | delivered | archived}}
updated: {{YYYY-MM-DD}}
---

# {{Production Title}} — Delivery manifest

**Source boards:** `boards.md` {{v3}}, `status: approved`, frozen {{date}}
**Source script:** `script.md` {{v2}}, `status: locked`

## Services used

| Service | Purpose | Model / version | Account | Commercial use cleared |
|---|---|---|---|---|
| {{Higgsfield}} | {{shot generation}} | {{model + version}} | {{which account/workspace}} | {{yes — terms checked by Logan Legal on date}} |
| {{ElevenLabs}} | {{voiceover}} | {{voice ID + model}} | {{}} | {{}} |

## Shared inputs

- **Style block:** {{the exact text appended to every visual prompt, carrying the brand guardrails}}
- **Negative prompt:** {{the exact text excluded from every visual prompt}}
- **Reference seeds:** {{reference image(s) or seed value(s) used to keep characters, products or locations consistent across shots — name which frames share which reference}}
- **Voice reference:** {{voice ID, stability/similarity settings, pronunciation overrides for product and brand names}}

## Per-frame generation log

<!-- One row per generated frame. Frame numbers match boards.md exactly —
     if a frame is 11a there, it's 11a here. -->

| Frame | Service | Model/ver | Seed | Prompt (exact) | Output file | Attempts | Accepted by |
|---|---|---|---|---|---|---|---|
| {{1}} | {{Higgsfield}} | {{v2.3}} | {{seed}} | {{full prompt text + style block}} | {{file}} | {{3}} | {{Dana Director, date}} |
| {{2}} | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} | {{}} |

## Voice log

<!-- Keyed by SPEAKER, matching the Cast & voices table in boards.md. One
     speaker gets one voice for the whole piece, so a speaker appearing
     twice here with two voice IDs is a bug, not a variation. -->

| Speaker | Frame(s) | Text as spoken | Source | Voice ID | Settings | Output file | Accepted by |
|---|---|---|---|---|---|---|---|
| {{NARRATOR}} | {{2, 6}} | {{exact line}} | {{synthetic}} | {{voice ID}} | {{stability / similarity / style}} | {{}} | {{Vera Voice, date}} |
| {{MARIA}} | {{3, 5}} | {{exact line}} | {{real recording — interview 2026-03-14}} | {{n/a}} | {{level-matched to −16 LUFS}} | {{}} | {{Sonny Sound, date}} |

**Consent for synthesized real voices:** {{for every speaker whose voice was cloned rather than recorded, who gave permission, for what use, and when. A general testimonial release does not cover synthesizing someone saying new words.}}

## Drift log

<!-- Step 7: where returned assets didn't match the approved boards, and
     what was done. If the answer was ever "we changed the board," that
     needed a re-premiere — record that it happened. -->

| Frame | Drift from board | Resolution | Board changed? |
|---|---|---|---|
| {{9}} | {{generated a different product colorway}} | {{re-prompted with explicit hex}} | {{no}} |

## Provenance and clearance

- **Unauthored content review:** {{what the service introduced that nobody wrote — incidental faces, logo-like marks, recognizable likenesses or styles — and what was done about each}}
- **Terms of use:** {{confirmation that each service's license permits commercial use of this output, checked by Logan Legal on {{date}}}}
- **Disclosure:** {{whether the piece needs to disclose AI-generated content, per policy or jurisdiction}}

## Regeneration notes

{{Anything a future person needs in order to regenerate a single shot and have it match: quirks of the service, prompts that needed rewording, ordering effects, things that only worked at a particular setting.}}
