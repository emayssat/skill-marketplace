---
workflow_type: preview
workflow_title: Preview (Small Audience Feedback Round)
---

# Preview (Small Audience Feedback Round)

**When to use:** A cut or scored animatic exists and the team wants a reality check from outside the production room *before* committing to full production spend or a wide review. The panel is deliberately small and hand-picked — the few audience personas whose reaction actually decides whether this piece works.

This is a **feedback workflow**, not a production one: most steps are owned by audience personas from `audience/`, and the worker personas are there to prepare the cut and act on what comes back.

**Inputs required:** A scored animatic or cut that can be watched cold, with no presenter narrating over it. The project brief (from `projects/`) stating the goal and intended audience.

## Who decides who takes part

Three separate decisions, three different owners. Conflating them is how a preview turns into a room full of people agreeing with the director.

**1 — The audience panel: Paul Producer decides.**
She assembles the panel, invites it, and records it in `brief.md`. Two personas feed her the picks and neither of them chooses:

- **Claude Client names who has to be convinced.** If this piece exists to get a CTO to say yes, **Camille Chief** is on the panel and that isn't negotiable. The client knows whose approval the piece is actually for; nobody else reliably does.
- **Dana Director names the creative risk.** He says which beat he's least sure lands, and that selects the persona most likely to catch it — a reveal he suspects is too quick points at **Cora Cognitive** or **Nadia Language**, a claim he suspects is thin points at **Simone Skeptic** or **Frank Facts**.

**Dana Director does not pick the panel**, and this is deliberate. A director choosing his own audience chooses who gets to judge his work, and the reliable outcome is a panel of personas who were always going to like it. Paul Producer's accountability here is specifically that the panel matches the brief rather than the room's hopes — she is the one who can say "you've picked three people who already agree with us."

**2 — Who attends the screening: Paul Producer, and almost nobody.**
She facilitates; **Ed Edit** runs the cut and says nothing. That's the room. Crew presence biases a cold watch and invites exactly the narration this workflow forbids — a director in the room will explain the frame that didn't work, and then nobody learns that it didn't work. Everyone else reads the reactions in the round record afterwards.

**3 — Which workers get called in to fix things: Dana Director decides, at triage.**
A finding is a symptom, not an assignment. "I lost the thread at the halfway point" could be the script, the boards, the cut or the mix, and choosing which is a directorial judgment — so step 5 is where the fix list gets routed, not step 2. **Paul Producer then confirms each call is affordable and schedulable**, and can send one back as out of scope for this round.

### Routing a finding to the right worker

| What the panel said | Who owns the fix | Who does *not* |
|---|---|---|
| "I didn't understand what it does" | **Sasha Script** — the message isn't in the words | not the artist; a clearer picture won't rescue an unclear claim |
| "I couldn't keep up" / "it went too fast" | **Dana Director** decides the beat's pace, **Sasha Script** cuts words or **Ed Edit** stretches time | not Vera Voice — she reports pace, she doesn't set it |
| "I lost track of where I was" | **Stella Storyboard** — frame order or visual continuity | — |
| "I read the text too late" | **Arthur Art** — on-screen text budget and hold time | — |
| "The music told me how to feel" | **Sonny Sound** — including the option of no music | — |
| "It dragged" / "it felt long" | **Ed Edit** — runtime, dead air, held frames | — |
| "It felt like an ad" / "I didn't believe it" | **Sasha Script** and **Dana Director** — claim and tone together | not legal; an unbelievable claim is a writing problem before it's a compliance one |
| "That claim can't be right" | **Logan Legal** substantiates, then **Sasha Script** rewrites or cuts | — |
| "The captions were unreadable" | **Arthur Art** (legibility) + **Ed Edit** (timing) | — |
| "I got nothing from that stretch" (from Blair Blind) | **Sonny Sound** — audio description or audio on a silent frame | — |
| "This isn't what we briefed" | **Paul Producer** — back to the brief, possibly a different workflow | not a fix step at all |

When a finding maps to nobody in this table, it usually maps to the brief. Say so instead of handing it to whoever is nearest.

## Panel composition

Pick 3 to 5 personas from `audience/` — the ones closest to the project's stated audience and to whoever holds the decision. Deliberately small; breadth comes later at the **Premiere**. Typical picks:

- Internal product vision piece → **Paula Product** (product manager), **Camille Chief** (C-suite leader), **Piper Program** (program manager)
- External launch piece → **Simone Skeptic** (skeptical buyer), **Elena Existing** (existing customer), **Seth Software** (software engineer)
- Broad consumer piece → **Yoan Young** (young adult), **Maya Mother** (mother), **Skye Social** (social scroller)

Record the chosen panel in the production's `brief.md` so the same personas can be re-run on a later cut and their reactions compared.

**Pace:** the panel reports pace as *experience*, not arithmetic — "I couldn't keep up," "I lost the thread." Nadia Language and Cora Cognitive feel an over-dense read before a stopwatch finds it. If a persona says it went too fast, re-run `--pace` on that beat before dismissing it as preference.

## Sequence

| # | Persona | Task | Output / gate |
|---|---|---|---|
| 1 | client *+* director | Name the inputs to the panel, separately: Claude Client says whose approval this piece needs; Dana Director says which beat he is least confident lands | Two short lists, no panel yet |
| 2 | producer | Decide the 3-5 persona panel from those inputs and the brief, and state exactly what feedback is being asked for (and what isn't open for debate) | Panel list in `brief.md` + feedback brief |
| 3 | editor | Prepare a cut that stands on its own, watched cold with no live explanation | Screening cut |
| 4 | *audience panel* | Each persona watches cold and reacts in character, using their own questions, feedback, and drop-off triggers — Paul Producer facilitating, Ed Edit running the cut, no other crew present | Per-persona reactions |
| 5 | director | Triage the reactions — separate real problems from a persona reacting outside this project's target — **and route each accepted finding to the worker who owns that fix** (see the routing table above) | Triaged findings, each with a named owner |
| 6 | producer | Confirm the routed fix list is affordable and schedulable this round; send anything that isn't back as scope | Agreed fix list |
| 7 | *routed workers only* | Each named worker makes their own fix — Sasha Script the copy, Stella Storyboard the frames, Arthur Art the text and legibility, Sonny Sound the music and mix. A worker with no routed finding does nothing this round | Fixes, per owner |
| 8 | editor | Re-cut with the accepted changes and re-screen to the same panel if anything structural moved | Revised cut (re-screened if needed) |
| 9 | producer | Decide: ready for **Premiere**, or does this need another preview round? | Go / another round |

## Final output

A revised cut plus `<production>/feedback/NN-preview.md` — the written record of which persona raised what, what was accepted, and what was dismissed and why. That record is what lets this panel's reaction be compared against the next round, and against the broader panel at the premiere.

## Notes / anti-patterns

- Never let someone talk over the screening in step 4. If the piece needs a human explaining it, it doesn't work, and a narrated screening hides exactly that.
- Step 5 is the real skill: a persona outside this project's target audience can be *correctly* unimpressed. Not every objection is a defect — but log the ones you dismiss in the round record, because if the same objection reappears at premiere from a persona who *is* in target, it was real and you'll want the receipt.
- Keep the panel small on purpose. A preview that consults everyone produces averaged, uncommitted feedback and takes the place of the premiere without the benefit of full representation.
- **Don't let the director pick the panel.** It always feels efficient — he knows the piece best — and it reliably produces an audience selected to approve. His job is to say what he's worried about; Paul Producer's job is to find the persona who will be honest about it.
- **Don't run every worker through step 7.** A fix step listed for everyone means the scriptwriter rewrites a line nobody complained about and the sound designer re-scores a beat that worked. A worker with no routed finding does nothing, and that's a successful round for them, not an idle one.
- **Don't let the panel assign the fix.** Audience personas report experience — "I lost the thread," "the music told me what to feel." The moment a persona says *how* to fix it, that's a craft opinion from someone who doesn't hold the craft; take the symptom, drop the prescription, and route it at step 5.
- **If Dev Deaf is on a preview panel, answer the caption question before he watches.** A preview cut usually has no caption track yet, which means he can review the pictures and nothing else — say that out loud rather than booking him and collecting a shrug.
- Accessibility personas (**Dev Deaf**, **Blair Blind**, **Leo Vision**, **Cora Cognitive**) usually belong at the **Premiere** rather than here, since a preview cut often lacks final captions or audio description — but if this piece's accessibility approach is itself the risky part, bring them in early instead of finding out late.
