<!--
BOARDS TEMPLATE — storyboard skill

This is the central artifact of the skill: the numbered frame table every
worker persona critiques and every workflow hands off. Copy it to
<production>/boards.md.

The production folder lives in your own working folder, NEVER inside the
skill — the skill ships only this stencil.

THE BOARD HAS TWO HALVES. The frame table is a stack of CARDS — each one
the current state of one frame, and nothing else. Everything below it is
STANDING NOTES — what applies across frames, why a choice was made, what's
unresolved, and the full history. History never appears on a card;
per-frame instructions never hide in a standing note. Check it with
`scripts/boards.py --cards`.

THE STANDING NOTES ARE IN A FIXED ORDER, most-useful-first, and the
REVISION LOG IS ALWAYS LAST AND ALWAYS NEWEST-FIRST — v3 above v2 above
v1. Everything that answers "what do I do now" (Music & silence, Release
status, Delivery routing, Protected cuts, Still open issues) comes before
the one section that only answers "what already happened". Check it with
`scripts/boards.py --notes`.

EVERY CARD FOLLOWS ONE TEMPLATE: templates/production/frame-card.md. That
file is the definition — fields, order, fill rules, motion vocabulary,
worked examples, checklist. Read it before writing the first frame.

FRAME NUMBERS ARE PERMANENT. Once a frame has a number it keeps it for the
life of the production, because personas refer to frames by number
("frame 12 reads as confused"). When a frame is added between 11 and 12 it
becomes 11a, not a renumbering of everything after it. When a frame is
cut, mark it CUT and leave the row — don't reclaim the number.

Set `status` honestly: several workflows gate on it (a sound designer
scoring against anything less than animatic-locked is rework waiting to
happen).
-->

---
production: {{slug}}
artifact: boards
version: {{v1}}
status: {{rough | rough-locked | clean | clean-locked | animatic-locked | approved}}
project_type: {{e.g. product-vision-2min}}
duration_target: {{"2:00"}}
duration_fixed: {{false}}        <!-- true for a hard slot (ad break, platform cap). Decides whether stretching is even an option. -->
pace_target_wpm: {{150}}         <!-- set by Dana Director for this piece; the project format proposes a default -->
pace_max_wpm: {{170}}            <!-- the ceiling nobody reads past -->
updated: {{YYYY-MM-DD}}
---

# {{Production Title}} — Storyboard {{v1}}

**Status:** {{rough}} · **Target duration:** {{2:00}} · **Project type:** {{product-vision-2min}}

## Frames

<!-- One row per frame — this row IS the frame card. Keep Dur realistic:
     Running must reach duration_target by the last frame, or the piece
     doesn't fit and the editor will say so.

     RUNNING IS DERIVED, NOT TYPED. It is the accumulated Dur, so when a
     duration changes every row below it changes too. Recompute the
     column rather than patching the one row —
     `scripts/boards.py --cards` does the arithmetic and will tell you
     where it stopped adding up. Beat should match a beat name
     from the project type's beat breakdown, so boards and brief stay
     traceable.

     TWO RULES GOVERN EVERY CARD, and they're the ones most often broken:

     1. A CARD CARRIES CURRENT STATE ONLY. What the frame is now. Never
        what it used to be, who asked for the change, which round it came
        from, or what was tried and rejected. All of that is history and
        it goes to the standing notes.

     2. A CARD RECORDS DIFFERENCES, NOT DEFAULTS. Trans out is blank when
        the frame leaves on a plain cut. Note is blank when nothing changes
        at this frame. A column of repeated "CUT" or "n/a" documents
        nothing and hides the three rows that matter.

     THE CARD OPENS WITH THE LINE AND CLOSES WITH THE EXIT: speaker and
     line first, then the picture it plays over, then how it's built, how
     long it lasts, and last of all how it leaves.

     The join OUT is on the card rather than the join in because it
     overlaps this frame's own tail and comes out of this frame's Dur.

     Rendered one frame at a time (scripts/boards.py --card N) the speaker
     moves up into the header strip beside the number, beat, shot and
     timing — who is talking is a one-word fact you scan, not a labeled
     block. See templates/production/frame-card.md for the full layout. -->

| # | Speaker | VO / Dialogue | Visual | Beat | Shot | Motion | Text | Audio | Note | Dur | Running | Trans out |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | — | — | {{What is literally in frame}} | Hook | WS STATIC | {{LOOP — monitor glow flickers}} | — | {{Low drone, alert pings}} | {{Cold open — no logo yet}} | 0:04 | 0:04 | {{DISSOLVE 0.5s — through black, drone drops out under it}} |
| 2 | NARRATOR | {{"Line as spoken."}} | {{...}} | Hook | CU PUSH IN | {{CAMERA — push completes by 0:04, then holds}} | {{"One ranked list."}} | {{Music enters}} | — | 0:06 | 0:10 | — |
| 3 | MARIA | {{"Line as spoken."}} | {{UI capture — name the exact screen}} | Reframe | SCREEN | {{BUILD — rows populate 40 → 3, 0.3s apart, over 1.2s}} | — | {{...}} | {{New voice — Maria, real testimonial, first appearance}} | 0:05 | 0:15 | — |

### The card shape is a template

**`templates/production/frame-card.md` is the definition of a card** — the
field list, the order, what each one holds, the motion vocabulary, worked
examples and a fill checklist. Every card in every production conforms to
it; the summary below is the short version. Changing the shape means
changing that file, this one, and `FRAME_COLUMNS` in `scripts/boards.py`
together.

A card **opens with the line and closes with the exit**: who speaks and
what they say, then the picture it plays over, then how it's built, how
long it lasts, and how it leaves. The line comes first because it's
written first and because "what is said here?" is the question a reader
arrives with.

| Column | Holds | Blank / `—` means |
|---|---|---|
| **#** | The permanent frame number | never blank |
| **Speaker** | A label from the Cast & voices table, in caps | nobody speaks |
| **VO / Dialogue** | The line exactly as spoken, with `*emphasis*` and `[PAUSE n]` | nobody speaks |
| **Visual** | What is literally in frame, right now, in one sentence | unfilled |
| **Beat** | Which beat of the arc this frame belongs to | untraceable to the brief — fix it |
| **Shot** | Framing and camera, from the shot vocabulary | not yet composed |
| **Motion** | What changes **during** this frame — or `STILL — <reason>` | nothing moves (see below) |
| **Text** | On-screen text the viewer is expected to **read**, written verbatim | no text on screen |
| **Audio** | Music, effects, room tone — or `SILENT — <reason>` | unfilled (a defect, see below) |
| **Note** | Anything the crew needs to know at this frame that no other column says | nothing changes here |
| **Dur** | This frame's length | untimed |
| **Running** | Cumulative time at the end of this frame | untimed |
| **Trans out** | The join **out** of this frame as `TYPE DURATION — detail`, when it isn't a plain cut | a straight cut — the default |

### Motion

**The frame is a still; the piece is not.** Motion is everything that
changes inside this frame's own duration — after the previous card's join
out has completed, before this card's begins. Three kinds, mixed freely: the
**camera** (`CAMERA — push completes by 0:03, then holds`), the
**subject** (`ACTION — she looks up on the second alert`), and the
**elements** (`BUILD — three rows populate 0.3s apart`).

Write what changes, **from what to what**, and over how long. "Dynamic"
is not motion; `COUNT — 0 → 1,284 over 1.5s, then settles` is.
Vocabulary: **HOLD · BUILD · REVEAL · WIPE ON / OFF · COUNT · HIGHLIGHT ·
SCROLL · CURSOR · LOOP · ACTION · CAMERA**.

**Endpoints with an arrow, and the clock.** Anything that changes state
writes `A → B` — `BUILD — 40 rows → 3 over 1.2s` — because frame 6's end
state is frame 7's start state, and that's the only way a stutter between
two individually-fine frames gets caught. The **Visual is the frame's end
state**, never a midpoint — and **not a sample of a move**: if frame 6 is
a closed panel and frame 8 is an open one, a frame 7 showing it half-way
isn't a frame, it's a snapshot. Every frame boundary is a hold, so three
cards of one slide asserts two pauses inside it. Merge them and put the
move in frame 6's Motion. And **motion + join out must fit `Dur`**: a
1.5s build in a 2.0s frame with a 0.8s dissolve out means the dissolve
starts before the build lands and nobody ever sees the finished state.
Molly Motion owns both checks; `scripts/boards.py --motion` does the
arithmetic.

**Motion is not the join.** A dissolve between two frames is `Trans out`
on **this** card. A build inside one frame is Motion. The test: is the
next frame already on screen while it happens? Then it's the join out.

**`STILL — <reason>` is the deliberate version of blank**, and a hold past
about five seconds needs one — otherwise a motionless frame reads as an
unfinished board rather than a held beat. It is the same rule as
`SILENT — <reason>` in the Audio column, for the same reason.

**Motion costs.** Molly Motion prices animated frames in days, Dean
Photography prices camera moves in rigs and setup time, and a 1.5s build
is 1.5 seconds the voiceover doesn't get. An unspecified motion gets
invented by whoever builds the frame, at whatever it happens to cost.

**Speaker** is never blank when there's a line. A frame that carries
dialogue with no speaker named is a frame nobody can cast, record, mix or
caption.

**Text** is written out verbatim, not described. `{{"One ranked list."}}`
is a card; "headline about consolidation" is a note to write one later.
Every frame with text also needs a row in **On-screen text** below, which
is where the reading budget gets checked — and where an off-by-one shows
up, because the row is keyed by frame number and frame numbers move. A
caption a frame early spoils the reveal it was written to land after; a
frame late labels a picture that has gone. `--cards` fails when a card
and its row disagree. The card says what is on
screen, the standing note says whether anyone can read it in time.

### Trans out

**Trans out names the join that leaves this frame, and only when it isn't
a plain cut.** Never write `CUT` — the default is a cut, so writing it
everywhere buries the two or three joins that are actually decisions. The
join *into* a frame is simply the previous card's Trans out; it is never
written twice.

**Out and not in**, because a dissolve out of frame 4 starts while frame 4
is still on screen and comes out of frame 4's own `Dur`. The constraint
belongs on the card that pays for it — and it puts the card in the order
it plays: the frame, what's said over it, how long it lasts, how it ends.

When it isn't a cut, the cell carries **type, duration and detail**:

```
DISSOLVE 0.5s — through black, music bed continues under
MATCH CUT 0s — the badge becomes the resolved checkmark, same position and size
FADE TO 0.8s — to brand navy, lets the silence land before the end card
WIPE 0.3s — left to right, following the cursor into the next frame
```

The **duration** is not optional: a join without a length can't be
budgeted against the runtime, and an editor will choose one for you. `0s`
is a real duration and worth writing — a match cut is instantaneous by
design, and saying so is different from forgetting to say. The **detail**
is what makes the join buildable by someone who sat in no review:
direction, what carries across it, what the audio does.

**The last frame's Trans out is how the piece ends**, usually a fade. It's
the one join with no frame on the other side, and a blank there means the
piece stops dead — a choice worth making on purpose.

**The card says what the join is; the Transitions table says why it's
worth it.** Everything needed to *build* the join is here; the reason and
the cost are there, keyed on **From** — this frame.
`scripts/boards.py --cards` flags a card and a table that disagree about
type or duration, because one of them is stale and until somebody looks,
nobody knows which. Full guidance:
`templates/production/frame-card.md`.

### The Note column

The Note is for **general information that applies at this frame and is
not already carried by another column.** It is read by whoever is working
on the frame, so it says what they need to know before they start:

- `New voice — Maria, real testimonial, first appearance` — a speaker
  arriving matters to casting, mixing and captions, and the Speaker column
  alone doesn't announce it.
- `Sound bridges from 6 — do not reset the bed`
- `Logo lockup first appears here — Arthur Art approval required`
- `Screen capture must be re-shot against the current UI`
- `Captions run two lines here — keep the lower third clear`

It is **not** a scratchpad. These do not belong in a Note:

- History — `was a wide shot in v2`, `Dana Director asked for this on
  round 3`, `shortened after the preview`. Revision log.
- Unresolved questions — `still not sure this works?`. Still open issues.
- A reason for something another column already states. The transition's
  reason is in the Transitions table; the silence's reason is in the Audio
  column.

### Current state only

A frame card describes the frame **as it stands now**, as if it had always
been that way. Anyone reading a card should be able to build the frame
from it without knowing anything about how it got there.

This matters because the card is the thing that gets handed off — to a
storyboard artist, to a generation service, to a vendor who wasn't in any
of the reviews. A card that reads `CU of the dashboard (was WS, changed
after Dean Photography flagged the rig)` sends a prompt containing the
shot that was rejected. It's also how a board rots: three revisions in,
every cell is half current state and half archaeology, and nobody can tell
which half is the instruction.

So when a frame changes, **overwrite the cell** and log the change once:

| Where it went wrong | Where it goes instead |
|---|---|
| `Visual: CU dashboard (was WS)` | `Visual: CU dashboard` + a Revision log row |
| `Note: shortened after preview feedback` | `Dur: 0:04` + a Revision log row |
| `VO: "..." — old line was "..."` | the current line only + a Revision log row |
| `Note: Arthur Art still unhappy with this` | **Still open issues** |
| `Trans out: DISSOLVE 0.5s — Dana wanted it softer` | `Trans out: DISSOLVE 0.5s — through black` + the reason in **Transitions** |

**The standing notes** are every section below the frame table. They hold
what applies across frames, the reasoning behind a choice, what's still
unresolved, and the entire history of the piece. Nothing in them repeats
on a card, and nothing on a card belongs in them.

**Their order is fixed, and it runs most-useful-first:**

| # | Section | Answers |
|---|---|---|
| 1 | Beat direction | how it should feel and how fast it talks |
| 2 | Transitions | what happens between frames |
| 3 | On-screen text | whether anyone can read it in time |
| 4 | Cast & voices | who speaks and what they sound like |
| 5 | Music & silence | what the score is doing, or why there isn't one |
| 6 | Animatic | what a still frame can't convey |
| 7 | Release status | where this piece is in its life |
| 8 | Delivery routing | which service or vendor builds what |
| 9 | Protected cuts | what must not change, and who says so |
| 10 | Still open issues | what isn't settled yet |
| 11 | **Revision log** | what changed, **newest first** |

The **Revision log is always last, and always grows upward** — the newest
version is the top row, v1 is the bottom one. Anyone opening this file
arrives with one of two questions: "what do I do now," which the first ten
sections answer, or "what changed since I last looked," which the revision
log's top row answers without scrolling. A log that grows downward pushes
every section above it further from the top until nobody reads them; a log
that grows upward inside the last section leaves the whole board exactly
where people left it.

Check the order with `scripts/boards.py --notes`.

### Silent frames

A frame with **no voiceover and no audio at all** is a real choice and
sometimes the right one — but it has to be a choice, written down. Put
`SILENT — <reason>` in the Audio column, never a bare `—`:

`{{| 7 | — | — | The room at dawn, nobody at the desks | Turn | WS STATIC | STILL — the stillness is the point | — | SILENT — the absence is the point; the alerts have stopped | — | 0:03 | 0:20 | — |}}`

Two cases, and only one is acceptable:

- **Stylistic silence.** Deliberate: a held beat, an absence that means
  something, a moment of relief after noise. Fine — say why in the Audio
  column, and Sonny Sound signs off that it plays as intentional rather
  than as a dropout.
- **Silence because the viewer is expected to pause and look.** Not
  acceptable, and the same failure as expecting them to pause and read.
  Almost nobody pauses. Either give the frame audio — a line, a sound, a
  music cue — or cut the frame. "They'll stop and take it in" is not a
  plan, it's a frame nobody watches.

**A silent frame is empty for Blair Blind.** She receives nothing at all
for its whole duration — no picture, no words, no sound. A short
stylistic beat is fine; anything longer carrying meaning needs audio
description, or the meaning has to exist somewhere she can reach it. This
is why unexplained silence is a defect rather than a style question.

### Emphasis

Mark the stressed word or phrase inside a line with *asterisks*:

`{{"We shipped it in *one week*. [PAUSE 0.8] Nobody believed that either."}}`

A line with no emphasis marked will be read evenly, and evenly is how
narration becomes wallpaper. If you can't find a word worth stressing in a
line, the line probably isn't saying anything.

## Beat direction

<!-- The emotional arc and the pace map, one row per beat. This is where a
     piece stops being monotonous — or doesn't.

     Dana Director owns the Emotion column: what the audience should feel
     here. Vera Voice owns Delivery: how that gets performed. The Pace
     column overrides the piece-level pace_target_wpm for these frames.

     THE MONOTONY TEST: read the Emotion column top to bottom, then the
     Pace column. If either one says the same thing all the way down, the
     piece has no arc and will play flat no matter how good the words are.
     Emotion should travel; pace should breathe. A hook is quick, a
     testimonial slows to let a person be human, a reveal slows further,
     a close lands rather than races. -->

| Beat | Frames | Emotion | Pace (wpm) | Delivery |
|---|---|---|---|---|
| {{Hook}} | {{1–3}} | {{Unease — something is wrong and nobody's named it}} | {{165}} | {{Clipped, low, matter-of-fact. Don't sell it.}} |
| {{Problem}} | {{4–6}} | {{Recognition — "that's my Tuesday"}} | {{150}} | {{Warmer, a little wry. Let the shared frustration show.}} |
| {{Turn}} | {{7–9}} | {{Relief, not triumph}} | {{135}} | {{Slow down. This is the beat that has to land.}} |
| {{Close}} | {{10–12}} | {{Quiet confidence}} | {{140}} | {{Settle. End on the word, not on the music.}} |

**Every beat needs an emotion, and it can't be the same one each time.**
"Confident" four rows deep is not an arc — it's a monotone with a
vocabulary. If two adjacent beats genuinely share an emotion, the pace or
the delivery has to differ, or the listener hears one long undifferentiated
stretch.

### Pauses

A deliberate silence is content, and it costs runtime like any other
content — so it lives in the boards, not in someone's head at the
recording session. Two notations:

- **Inside a line:** `[PAUSE 0.8]` where the read breaks for emphasis.
  `{{"We shipped it in a week. [PAUSE 0.8] Nobody believed that either."}}`
- **A held beat of its own:** a pause long enough to hold on picture gets
  its own frame — Speaker `—`, VO `[PAUSE 2.0]`, and a real `Dur`. A
  two-second silence on screen is a two-second frame.

Always give the duration in seconds. `[PAUSE]` with no number is a note,
not a spec, and it'll be performed as whatever the reader felt like.

**Three people share a power pause, and it fails if any of them ignores it:**
Vera Voice marks and performs it, Ed Edit pays for it in runtime, and
Sonny Sound protects it — a pause with the music bed still running
underneath isn't silence, it's just a gap in the narration.

### Shot vocabulary

Composition: **EWS** extreme wide · **WS** wide · **MS** medium · **MCU** medium close-up · **CU** close-up · **ECU** extreme close-up · **OTS** over-the-shoulder · **POV** point of view · **INSERT** detail insert · **SCREEN** screen recording or UI capture · **TITLE** title/text card

Movement: **STATIC** · **PAN** · **TILT** · **PUSH IN** · **PULL OUT** · **TRACK** · **HANDHELD**

Combine them as "MCU PUSH IN". If a frame needs more than a shot code and
one sentence of visual, it's probably two frames.

## Transitions

<!-- What happens BETWEEN frames. The frames table documents the moments;
     this documents the joins, which is where "and then it transitions"
     gets invented by whoever happens to be in the edit that day.

     THE CARD BUILDS THE JOIN; THIS TABLE JUSTIFIES IT. Frame N's Trans
     out cell carries everything needed to BUILD the join leaving N —
     type, duration and detail: "DISSOLVE 0.5s — through black, drone
     drops out under it".
     The row below carries what's needed to JUSTIFY it: the reason and the
     cost. Type and duration appear in both, deliberately, so the card
     stands alone for an editor and the table stands alone for a budget
     review — and `--cards` fails when the two disagree, because then one
     of them is stale and nobody can tell which by looking.

     Every non-blank Trans out needs a row here whose From is that
     frame, and every row here needs a matching Trans out.

     THE DEFAULT IS A STRAIGHT CUT. Only list the exceptions here — a
     column of "CUT" repeated twenty times documents nothing. If a join
     isn't in this table, it's a cut.

     Ed Edit owns this table: transitions are editorial craft, and he's
     the one who knows whether a join reads. Molly Motion executes and
     prices them on motion-graphics pieces, Arthur Art constrains the
     vocabulary to what the brand allows, Sonny Sound scores them.

     EVERY TRANSITION NEEDS A REASON, and "it looked flat as a cut" isn't
     one. A transition says something: a dissolve says time passed, a
     match cut says these two things are the same thing, a wipe says we're
     changing subject. Decoration is the failure mode — it reads as a
     template, and it costs both runtime and animation days. -->

| From | To | Type | Duration | Why | Cost |
|---|---|---|---|---|---|
| {{3}} | {{4}} | {{DISSOLVE}} | {{0.5s}} | {{Time passes between the two shifts}} | {{—}} |
| {{6}} | {{7}} | {{MATCH CUT}} | {{0s}} | {{The alert badge becomes the resolved checkmark — same position, same size}} | {{Needs both frames composed to match}} |
| {{9}} | {{10}} | {{BUILD}} | {{1.2s}} | {{Elements assemble into the final diagram as the VO names them}} | {{~1 animation day — Molly Motion}} |

Type and Duration here must match frame `From`'s Trans out cell. The
*Why* and *Cost* live only here — a card carrying a reason is a card carrying an
argument, which is what the standing notes are for.

### Transition vocabulary

**CUT** (default, 0s) · **DISSOLVE** one image fades into the next · **MATCH CUT** a shape or motion carries across the join · **BUILD** elements assemble or disassemble in place · **WHIP** fast directional blur · **WIPE** one image pushes the other off · **FADE TO/FROM** black or a brand color · **HOLD** the frame sits with no change (a beat, not a transition — but worth recording so nobody "fixes" it)

Stay inside the vocabulary the brand allows — `reference/brand-guardrails.md`
sets the approved motion language, and a transition outside it will fail
brand review no matter how well it works.

### Transitions cost time

A 0.5s dissolve is half a second of runtime, and it comes out of the same
budget as words and pauses. Six dissolves in a 30-second piece is three
seconds — a tenth of the piece spent on joins. Ed Edit counts them
against the runtime the same way he counts pauses, and Molly Motion prices
the animated ones in days.

`scripts/boards.py --transitions` totals the joins, counted from the cards
(so a join specced in the table but never put on a card isn't silently
billed twice). That total is why the duration belongs on the card: a join
with no length is a join that costs nothing on paper and seconds in the
edit.

## On-screen text

<!-- Any frame carrying text the viewer is expected to READ, as opposed to
     the voiceover they hear. This is a separate budget from words-per-
     minute, and it's the one people skip.

     THE CARD HOLDS THE TEXT; THIS TABLE BUDGETS IT. The Text column on
     frame N is the verbatim wording. The row below is where somebody
     counts the words against the hold time and says whether it's readable
     at playback speed. Every frame with text needs a row here.

     THE RULE: "they can pause the video and read it" is not a plan.
     Almost nobody pauses. Autoplay feeds don't offer it, people watching
     in a meeting won't do it, and Cora Cognitive, Nadia Language, Robert
     Retired and Leo Vision are the ones who most need the time and least
     likely to get it. A frame whose text can only be absorbed by pausing
     has failed for everyone who didn't.

     BUDGET: roughly 2–3 words per second of hold time for comfortable
     reading, and that's on top of the moment it takes to notice the text
     is there. Twelve words needs about five seconds. If the voiceover is
     also talking over it, the viewer is reading and listening at once —
     assume less, not more.

     A PAUSE-AND-READ FRAME IS A LEGITIMATE CHOICE, made deliberately: a
     reference card, a summary slide, a dense diagram someone will come
     back to. Mark it as such below, and accept that its content is a
     bonus for the few who stop rather than something the piece depends
     on. Never put load-bearing information there. -->

| Frame | Text on screen | Words | Hold | Readable at playback? | Intent |
|---|---|---|---|---|---|
| {{3}} | {{"One ranked list."}} | {{3}} | {{0:05}} | {{yes}} | {{Reinforces the VO}} |
| {{9}} | {{Full comparison table, 40 words}} | {{40}} | {{0:04}} | {{no}} | {{PAUSE-AND-READ — deliberate; the VO already states the takeaway, so nobody who keeps playing misses anything}} |

**Anything marked not-readable-at-playback must either get more hold time,
lose words, or be explicitly a pause-and-read frame whose content is
duplicated in the voiceover.** Those are the only three outcomes.

## Cast & voices

<!-- Every voice heard in the piece, defined ONCE here and referenced by
     label from the Speaker column. Sonny Sound owns this table; Vera
     Voice reviews the read per speaker.

     This exists because a name on a frame isn't castable. "MARIA" tells
     you nothing about how Maria sounds, and a testimonial piece with four
     speakers needs four voices that stay consistent frame to frame, sit
     at matched levels, and are distinguishable from one another by ear.

     ONE SPEAKER = ONE VOICE for the whole piece. If the same character is
     voiced differently in two frames, the viewer hears two people. -->

| Speaker | Who they are | Voice | Source | Consent | Frames |
|---|---|---|---|---|---|
| NARRATOR | {{Unseen guide, not a character in the story}} | {{Warm, measured, low-mid register, unhurried}} | {{Synthetic — service + voice ID, or a named performer}} | {{n/a}} | {{1–3, 9–12}} |
| MARIA | {{Ops lead at a customer, 40s}} | {{Real testimonial — Spanish-accented English, fast, animated}} | {{Recorded interview, 2026-03-14}} | {{Release on file — signed 2026-03-20}} | {{4–6}} |
| {{DEV}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

**Voice** describes how they *sound*, not who they are — register, pace,
accent, energy. It's the brief a performer or a voice service works from,
so "professional" is not a description and "confident, clipped, mid-30s,
slight Dublin accent, talks slightly too fast when enthusiastic" is.

**Source** says whether this is a real recording or synthesized, and names
the performer, interview, or service and voice ID. Dex Delivery maps this
column straight to a voice service, so a missing ID blocks the handoff.

**Consent** is only sometimes n/a. A real person's testimonial needs a
release on file, and **synthesizing a real, identifiable person's voice
needs their explicit permission for that specific use** — cloning a
customer's voice to say words they never said is a different act from
editing what they did say. Logan Legal gates this before release; if the
column is blank for a real person, it isn't cleared.

## Music & silence

<!-- Sonny Sound's recommendation, made once for the piece rather than
     frame by frame. The Audio column above is tactical (what happens in
     this frame); this section is the strategy.

     "No music" is a real recommendation and sometimes the right one.
     Testimonials and explainers often work better dry: scoring a person
     telling you something true can make it sound staged, and music under
     a dense explainer competes with comprehension. Recommend it, say why,
     and let Dana Director decide. -->

**Recommendation:** {{Score the whole piece | Score only the open and close | No music — carry it on voice and sound design | Music under B-roll only}}

**Why:** {{One or two sentences. What the music is doing that the picture and voice can't do alone — or, if none, what it would cost.}}

| Section | Frames | Music | Intent |
|---|---|---|---|
| {{Open}} | {{1–3}} | {{Sparse bed, no melody}} | {{Establish unease without telling the viewer what to feel}} |
| {{Testimonials}} | {{4–6}} | {{None}} | {{Let the real voices carry it; music here reads as staged}} |
| {{Close}} | {{7–9}} | {{Theme resolves}} | {{Release the tension the open set up}} |

**Licensing:** {{track, library and licence tier — or "TBD". A temp track that reaches the final mix is Logan Legal's problem and yours.}}

**Sonic brand:** {{any theme, sting or sonic logo from reference/brand-guardrails.md that this piece must use or must not contradict}}

## Animatic

The animatic is not a separate document — it's this table with `Dur`
committed, the Audio column filled in rather than aspirational, and
`status: animatic-locked`. Note here where scratch VO differs from the
final intent, and anything a still frame can't convey (a transition, a
reveal that depends on motion).

- {{Timing note or motion the table can't show}}

## Release status

<!-- Where this piece is in its life, in one glance. The frontmatter
     `status:` says whether the BOARD is safe to work from; this says
     whether the PIECE has been screened, cleared and released.

     Paul Producer owns it. It is read constantly and by people who
     weren't in any of the rounds — which is why it sits near the top of
     the standing notes rather than buried above the revision log. -->

**Stage:** {{boarding | animatic | previewed | premiered | released | superseded}}
**Board frozen:** {{no — freezes at premiere approval}}
**Last screened:** {{Preview round 2, {{date}} — see feedback/02-preview.md}}
**Cleared for external use:** {{not yet — Logan Legal gates this}}
**Where it has shipped:** {{none yet | internal all-hands {{date}} | youtube.com/... }}

## Delivery routing

<!-- Which service or vendor builds what, decided at handoff and recorded
     here so the board itself says how it becomes a piece. Dex Delivery
     recommends and fills this in; Paul Producer decides on cost and
     procurement; Logan Legal clears the terms.

     Frame-accurate on purpose: a piece is rarely all one pipeline, and
     "we generated it" is not reproducible six months later. The exact
     prompts, model versions and seeds live in
     <production>/delivery/manifest.md — this is the map, that is the log.

     See reference/services.md for what each service is currently good
     for and when that was last verified. -->

| Job | Frames | Service / vendor | Model or voice | Notes |
|---|---|---|---|---|
| {{Video generation}} | {{1–6, 9}} | {{Higgsfield}} | {{/higgsfield-ai/soul/v2/standard}} | {{style block from reference/brand-guardrails.md}} |
| {{Voice — NARRATOR}} | {{1–3, 9–12}} | {{ElevenLabs}} | {{voice ID abc123, eleven_multilingual_v2}} | {{`--speed` matched to pace_target_wpm}} |
| {{Voice — MARIA}} | {{4–6}} | {{real recording}} | {{—}} | {{interview 2026-03-14; not synthesized}} |
| {{Motion graphics}} | {{7–8}} | {{in-house}} | {{—}} | {{Molly Motion, ~2 animation days}} |
| {{Title / data frames}} | {{10–12}} | {{HyperFrames}} | {{CLI, local render}} | {{typeset text + exact brand values; deterministic, so localization re-renders}} |
| {{Captions}} | {{all}} | {{—}} | {{—}} | {{burned-in for social, sidecar SRT elsewhere}} |

## Protected cuts

<!-- Frames and beats that must NOT change, and who protected them. This
     is the counterweight to every workflow that shortens, reframes,
     restyles or localizes a piece: those workflows go looking for seconds
     to cut, and without this section the cheapest-looking frame to lose
     is often the one that was expensive to earn.

     A protection is only real if it names WHO and WHY. "Important" is not
     a protection. -->

| Frame(s) | Protected by | Why it cannot change | Expires |
|---|---|---|---|
| {{14}} | {{Logan Legal}} | {{Claim wording is the substantiated version; any rewrite needs re-clearance}} | {{on next claim review}} |
| {{4–6}} | {{Sonny Sound}} | {{Maria's testimonial as consented — trimming inside the quote changes what she said}} | {{never, while the release stands}} |
| {{12}} | {{Claude Client}} | {{The value-proposition beat; the piece exists to deliver it}} | {{—}} |
| {{1}} | {{Arthur Art}} | {{Logo lockup timing is the brand minimum hold}} | {{on brand guideline revision}} |

**To change a protected cut, go back to whoever protected it.** Not to the
producer, not to the director — to the named persona, because they are the
one who knows what the protection was buying.

## Still open issues

<!-- Things a persona flagged that aren't resolved yet. Clear this before
     asking for a clean-lock.

     This is also where a doubt goes when somebody is tempted to write it
     onto a frame card. A card says what the frame IS; a question about
     whether that's right belongs here, with the frame number so it's
     findable from either direction. -->

| Frame(s) | Raised by | Issue | Waiting on |
|---|---|---|---|
| {{7}} | {{Dean Photography}} | {{Crane move is out of budget — alternative pending}} | {{Paul Producer}} |
| {{9}} | {{Cora Cognitive}} | {{On-screen text may still be too dense at 0:04 hold}} | {{Arthur Art}} |

## Revision log

<!-- THE ONLY PLACE HISTORY LIVES, AND THE LAST SECTION ON THE BOARD.

     Every "was", "used to", "changed after", "per round 2" belongs in a
     row here and nowhere else — not in a Visual cell, not in a Note, not
     in a parenthesis after a line of VO. The frame cards stay clean
     because this table exists.

     NEWEST FIRST. The top row is the current version; v1 is at the
     bottom. Two reasons, and both of them are about the reader: the
     question people actually arrive with is "what changed since I last
     looked," which is answered by the top row and not by scrolling; and a
     log that grows downward pushes every other standing note further from
     the top of the file until nobody reads them. Growing upward, inside
     the last section, keeps the whole board stable.

     It stays last for the same reason it stays newest-first: history is
     the one part of the board nobody needs in order to build the piece.
     Music & silence, Release status, Delivery routing, Protected cuts and
     Still open issues all answer "what do I do now" and come first.

     Name the frames, so a change is findable from the board and a board
     is explainable from the change. -->

| Version | Date | Frames | What changed | Driven by |
|---|---|---|---|---|
| {{v3}} | {{date}} | {{4, 7–9}} | {{Frame 4 went from WS to CU; 7–9 lost 1.5s each to make room}} | {{Dean Photography's feasibility notes}} |
| {{v2}} | {{date}} | {{11a}} | {{Inserted a held beat before the close}} | {{Preview round 1 — three personas lost the turn}} |
| v1 | {{date}} | all | First rough pass | {{Dana Director's shot list}} |
