---
workflow_type: premiere
workflow_title: Premiere (Full Audience Representation & Release Readiness)
---

# Premiere (Full Audience Representation & Release Readiness)

**When to use:** The piece is essentially final and about to be released. Before it goes out, it runs past a broadly representative audience panel — everyone it will plausibly reach, explicitly including the accessibility personas — to catch what fails for a segment the team didn't design for. This is both the last feedback round and the release go/no-go.

This is a **feedback workflow**: most steps are owned by audience personas from `audience/`. Where the **Preview** asks "do the few people who matter most think this works," the premiere asks "does this hold up for everyone who will actually see it."

**Inputs required:** A near-final cut that is accessibility-complete — captions in place, audio description available where the visual carries meaning the narration doesn't. Without that, the accessibility personas can't review anything, which defeats the point of this round.

## Who decides who takes part

Same three decisions as the **Preview**, same owners — see `preview.md` for the reasoning and for the finding-to-worker routing table, which applies here unchanged. What differs is the standard:

- **Paul Producer decides the panel**, but at a premiere the test is no longer "who matters most" — it's **representation**, so the burden flips: she has to justify who is *left out*, not who is included. "We didn't think this reached anyone with low vision" is an answer she has to be willing to write down.
- **Claude Client still names who must be convinced**, and **Dana Director still names the creative risk** — but neither can shrink the panel. A premiere panel is only ever added to.
- **Any persona whose objection was dismissed at the preview is on the panel automatically.** Nobody decides that one; it's how you find out whether dismissing it was right.
- **Dana Director routes the findings at step 7**, as at the preview — with one exception above him: **access failures at step 4 route themselves.** Contrast and caption legibility go to Arthur Art, caption timing and cut to Ed Edit, audio description and mix to Sonny Sound, and none of that is a triage judgment. It's a defect list.

## Panel composition

Every audience persona this piece will plausibly reach, not just the flattering ones. At minimum:

- Everyone consulted at the **Preview**, so their earlier notes can be checked as addressed.
- All four accessibility personas — **Dev Deaf** (Deaf/hard-of-hearing), **Blair Blind** (blind), **Leo Vision** (low-vision/color-vision-deficient), **Cora Cognitive** (cognitive/neurodivergent).
- The personas most likely to encounter it incidentally rather than deliberately, such as **Skye Social** (social scroller), if it will run anywhere public.
- Any persona whose objection was logged and dismissed during the preview — this is where you find out whether dismissing it was right.

**Pace:** last chance to catch it, and the most expensive. Accessibility personas are the sensitive instrument — Nadia Language needs longer per sentence, Cora Cognitive disengages rather than rewinding, Robert Retired loses on-screen text that leaves early. A pace complaint here usually means a re-record, so treat earlier `--pace` passes as the real defence.

## Sequence

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | producer | Confirm the caption plan from the brief is actually executed in this cut — Dev Deaf reviews nothing useful without it, and a nodded-through review is not an access check. Then assemble the full representative panel — taking Claude Client's must-convince list and Dana Director's risk list, adding every persona dismissed at the preview, and being able to name why anyone is absent — and confirm the cut is accessibility-complete before scheduling | Panel list (with omissions justified) + readiness check |
| 2 | editor | Prepare the final cut with captions and any audio description track in place | Screening-ready final cut |
| 3 | sound-designer | Confirm the final mix meets platform loudness norms and the piece still works with sound off | Delivery-ready mix |
| 4 | *accessibility personas* | Review access first — Dev Deaf on captions and speaker labels, Blair Blind on audio completeness and any silent frame she receives nothing from, Leo Vision on contrast and color, Cora Cognitive on pacing, sensory safety and whether any on-screen text goes by too fast to read | Access verdict (blocking issues named) |
| 5 | art-director + editor + sound-designer | Fix every blocking access issue from step 4 — contrast and caption legibility to Arthur Art, caption timing and cut to Ed Edit, audio description and mix to Sonny Sound — then re-verify with the persona who raised it | Access issues cleared |
| 6 | *full audience panel* | Each remaining persona reacts in character to the finished piece | Per-persona reactions |
| 7 | director | Triage findings against the release date: blocking defects versus nice-to-haves | Triaged findings |
| 8 | legal-reviewer | Final clearance pass on the exact cut being released — claims, asset licenses, customer references, any temp track still sitting in the mix | Written clearance |
| 9 | producer | Go / no-go / fix-and-reship decision; lock release logistics and channel specs | Release decision |
| 10 | client | Final sign-off for release | Approved for release |
| 11 | producer | After release, compare what the personas predicted against how real viewers actually reacted; fold the gaps back into `audience/` | Updated audience personas |

## Final output

A released piece, plus `<production>/feedback/NN-premiere.md` recording which persona predictions held up in the real world — which is what keeps the `audience/` personas honest over time instead of drifting into flattering guesses.

Approval here also **freezes the boards**. From this point the storyboard is a fixed source, which is what makes a clean handoff possible: see `handoff.md` for converting it into per-service inputs (video generation, voice synthesis, captions, or a human vendor). Anything that would change a board after this needs another premiere, not a quiet edit downstream.

What gets frozen is the **frame cards** — and they are about to be read literally, by services and vendors who were in none of these rounds. So before the freeze, run `scripts/boards.py --cards` and `--motion` and clear both: a card carrying `(was a wide shot)` freezes the rejected shot into the source of truth, and a card whose Trans out contradicts the Transitions table freezes an ambiguity nobody downstream can resolve. The Revision log is the opposite — it should be full, and it stays writable, because the record of how the piece got here outlives the piece.

## If the decision is no-go

A no-go at step 9 is a real outcome, not a failure state to route around. Record it in the round file with the reason, then branch by what broke:

- **Access failure that couldn't be cleared at step 5** → fix and re-run this workflow from step 4. Do not release on a promise to fix captions afterward.
- **Legal blocker at step 8** → back to Sasha Script for the claim, or to Sonny Sound for an unlicensed track. A claim that can't be substantiated gets cut, not softened into a vaguer version of the same claim.
- **Structural story problem** → this isn't a premiere fix. Branch to **Remake** (if the content is stale) or **New Storyboard Creation** (if the arc itself is wrong), and come back when there's a new cut.
- **Runtime or format wrong for the channel** → branch to **Time Reduction** or **Platform Adaptation**, then re-premiere.
- **Shipping anyway with a known flaw** → a legitimate producer call under deadline, but name the flaw in the round record and say who accepted it. An undocumented known flaw becomes a surprise for whoever inherits this piece.

## Notes / anti-patterns

- Step 4 is a hard gate, not a courtesy. An access failure means part of the audience receives nothing at all, which outranks a pacing note from someone who received the whole thing.
- Don't schedule the premiere against a cut that's still missing captions and then promise to "add them after." Captions added post-approval get added badly, and nobody re-reviews them.
- If the panel surfaces a structural story problem at this stage, the honest options are delay or ship-with-known-flaw — not a silent rewrite the day before release. Escalate it as a producer decision in step 9 rather than absorbing it quietly.
- Step 11 is the step everyone skips, and it's the one that makes the next project better. A persona that keeps mispredicting real reaction needs updating, not defending.
