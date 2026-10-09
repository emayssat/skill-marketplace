<!--
FRAME CARD TEMPLATE — storyboard skill

THE definition of one frame card. `boards.md` holds a stack of them; this
file says what a card is, in what order, and what belongs in each field.
Every card in every production conforms to this, which is what lets one
parser, nine personas and three external services all read the same board.

If a field needs adding or renaming, change it HERE first, then
`templates/production/boards.md`, then `FRAME_COLUMNS` in
`scripts/boards.py`. Changing one and not the others is how a board starts
parsing its dialogue as a speaker name.

Conformance is mechanical: `python3 scripts/boards.py <boards.md> --cards`.
-->

# Frame card

One frame, one card, one row of the Frames table in `boards.md`.

A card answers, for a single moment of the piece: **what is on screen,
what moves, what is heard, and what the next person needs to know.**
Nothing else. It holds the frame's **current state** — never its history,
never an unresolved question, never the reasoning behind a choice. Those
live in the standing notes below the frame table, which run in a fixed
order and end with the Revision log, newest first:

> Beat direction → Transitions → On-screen text → Cast & voices →
> Music & silence → Animatic → Release status → Delivery routing →
> Protected cuts → Still open issues → **Revision log**

## The card

Copy this row. The column order is fixed.

```
| # | Speaker | VO / Dialogue | Visual | Beat | Shot | Motion | Text | Audio | Note | Dur | Running | Trans out |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   |         |               |        |      |      |        |      |       |      |     |         |           |
```

**A card opens with the line and closes with the exit.** Read left to
right — or top to bottom in the field list below — and it runs in the
order a person actually needs it:

1. **Who speaks, and what they say.** In a narrated piece the line is
   written first and drives everything; the reader's first question at any
   frame is "what is said here?"
2. **What is on screen** — the picture the line plays over. It illustrates
   the line, so it reads better after it.
3. **How it's built and heard** — beat, shot, motion, text, audio.
4. **How long it lasts.**
5. **How it leaves.** Last, because it's the last thing that happens.

## Card layout — never a third column

The row above is how a card is **stored**. This is how it's **laid out**
when a card is drawn, printed or rendered one frame at a time:

```
┌───────────────────────────────────────────────────────────────┐
│ FRAME 8   MARIA   Beat: Problem   Shot: MS   0:05 → 0:26      │
├───────────────────────────────────────────────────────────────┤
│ VO / DIALOGUE                                                 │
│ "We were chasing *ghosts*."                                   │
├───────────────────────────────────────────────────────────────┤
│ VISUAL                                                        │
│ Maria at her desk, mid-sentence                               │
├───────────────────────────────────────────────────────────────┤
│ MOTION                                                        │
│ ACTION — she turns from the second monitor as she starts      │
│ talking                                                       │
├──────────────────────────────┬────────────────────────────────┤
│ TEXT                         │ AUDIO                          │
│ —                            │ Room tone                      │
├──────────────────────────────┴────────────────────────────────┤
│ NOTE                                                          │
│ New voice — Maria, real testimonial, first appearance         │
├───────────────────────────────────────────────────────────────┤
│ TRANS OUT                                                     │
│ DISSOLVE 0.5s — through black, the drone drops out under it   │
└───────────────────────────────────────────────────────────────┘
```

**The rule: a labeled section spans the full card width, or shares a row
with exactly one other section. Never three.**

A third column is a third as wide, and a third of the width turns one line
of transition detail into six. `DISSOLVE 0.5s — through black, the drone
drops out under it` is a single line at full width; in a narrow third
column it is a six-line block, and a card with two or three of those is
twice as tall for no added information. Height is what decides whether a
board can be read a frame at a time or scrolled through, so the layout
protects it.

Which section goes where follows from **whether its value is bounded**:

| Placement | Sections | Why |
|---|---|---|
| **Header strip** | `#`, **Speaker**, Beat, Shot, `Dur → Running` | Bounded values — a number, a caps label, one word, a shot code, two timecodes. They fit on one line together and are what you scan to find a frame |
| **Full width** | VO / Dialogue, Visual, Motion, Note, Trans out | Each can be a sentence. Anything that can be a sentence gets the whole width |
| **Paired, two columns** | Text + Audio | Usually short. If either runs long on a given frame, it takes a full-width row of its own — the pairing is a default, not a constraint |

**Speaker lives in the header strip.** Who is talking is a one-word fact,
exactly like the beat and the shot code, and it belongs with the other
things you scan when you're looking for a frame. Giving it a labeled block
of its own would cost three rows of height to say one word, and hanging it
off the VO label buries it in a line people read as prose.

**The line comes before the picture.** VO / Dialogue sits above Visual
because that's the order the work happens in and the order a reader wants:
the line is written first, the picture illustrates it, and "what is said
here?" is the question you arrive with. A card that opens with the picture
makes you read the visual twice — once cold, once again after you find out
what it's carrying.

`scripts/boards.py --card 8` renders any frame in exactly this layout, so
the diagram above and the tool can't drift apart.

## The fields

| # | Field | Holds | Blank (`—`) means | Owner |
|---|---|---|---|---|
| 1 | **#** | The permanent frame number. Insert as `11a`; a cut frame keeps its number and its row | never blank | Stella Storyboard |
| 2 | **Speaker** | A label from Cast & voices, in caps | nobody speaks | Sonny Sound |
| 3 | **VO / Dialogue** | The line exactly as spoken, with `*emphasis*` and `[PAUSE n]` | nobody speaks | Scott Script |
| 4 | **Visual** | What is literally in frame, in one sentence, as a still | unfilled | Stella Storyboard |
| 5 | **Beat** | The beat of the arc this frame belongs to, matching a row in Beat direction | untraceable to the brief — a defect | Dana Director |
| 6 | **Shot** | Composition and camera, from the shot vocabulary: `MCU PUSH IN` | not yet composed | Dana Director / Dean Photography |
| 7 | **Motion** | What changes **during** this frame — after the previous frame's join out, before this one's | nothing moves; it's a held still | Molly Motion (graphics) / Dean Photography (live action) |
| 8 | **Text** | On-screen text the viewer is expected to **read**, written verbatim — and **on the frame it belongs to**, not the one before or after | no text on screen | Arthur Art |
| 9 | **Audio** | Music, effects, room tone — or `SILENT — <reason>` | unfilled, which is a defect | Sonny Sound |
| 10 | **Note** | What the next person needs to know at this frame and no column says | nothing changes here | whoever knows it |
| 11 | **Dur** | This frame's length | untimed | Ed Edit |
| 12 | **Running** | Cumulative time at the end of this frame | untimed | Ed Edit |
| 13 | **Trans out** | The join **out** of this frame, when it isn't a plain cut: `TYPE DURATION — detail` | a straight cut, the default | Ed Edit |

Fields 7, 8, 10 and 13 are **difference-only**: blank is the normal,
correct value, and filling them in with defaults (`CUT`, `none`, `n/a`)
hides the handful that are real decisions.

## Motion — what the still can't show

A storyboard frame is a drawing; the finished piece is not. **Motion is
everything that changes inside the frame's own duration** — after the
previous card's join out has completed, before this card's begins.
Without it, the gap between board and animatic gets filled by whoever
builds the frame, which is the same failure as an unspecified transition
and usually more expensive.

Motion covers three kinds of change, and a frame can have any mix:

- **Camera** — the move, when the Shot code alone doesn't carry the
  timing: `push in completes by 0:03, then holds`.
- **Subject** — what the people or objects do: `she looks up from the
  screen on the second alert`.
- **Elements** — UI, type, data, graphics: `three rows populate in
  sequence, 0.3s apart`, `headline wipes on from the left as the VO names it`.

Write it as **what changes, from what to what, and over how long** — not
as an adjective. "Dynamic" is not motion. `COUNT — 0 → 1,284 over 1.5s,
then settles` is.

### Continuity: the endpoints and the clock

Two conventions, and they exist so animation can be checked as a
*sequence* rather than frame by frame. Molly Motion runs both;
`scripts/boards.py --motion` does the arithmetic.

**State it as `A → B`.** Anything that leaves the frame in a different
state than it started — a build, a count, a reveal, a wipe, a scroll —
writes its endpoints with an arrow: `BUILD — 40 rows → 3 over 1.2s`,
`COUNT — 0 → 1,284 over 1.5s`. This is what makes the next card
checkable: frame 6 ends with three rows, so frame 7 cannot begin from
forty. Without endpoints, nobody can tell a deliberate jump from a
mistake, and the piece stutters in a way viewers feel but can't name.

**The Visual is the frame's end state, not a midpoint.** A Visual reading
*"the console showing three ranked rows"* with `BUILD — 40 rows → 3` is
coherent. The same Visual with `BUILD — 3 rows → 40` is two people
writing two different frames.

**A frame is a state, not a sample of a move.** If frame 6 is a static
panel and frame 8 is that panel slid up, a frame 7 showing it half-way is
not a frame — it's a snapshot of the movement, and it costs you. **Every
frame boundary is a hold:** a card asserts a `Dur`, and a board is read
one frame at a time, so slicing one continuous slide across three cards
asserts two pauses inside the slide. It stutters, or the runtime inflates
to cover it, and nobody can tell afterwards whether the 0.4s in the middle
was a decision or an accident of how it got drawn.

One movement, one place: **Motion** if it happens inside a frame,
**Trans out** if it happens between two. Merge the samples, put the move
on the first card with its endpoints and duration, and let the next card
show where it lands:

```
BAD   6: panel closed          7: panel half-way up      8: panel open
GOOD  6: panel closed · SCROLL — panel rises 0 → 100% over 0.6s
      7: panel open
```

A long move may span cards only when each card earns its existence for a
reason *other* than the animation having progressed — a line lands, the
audio changes, the subject does something new. `--motion` flags the rest.

**`motion + join out ≤ Dur`.** A 1.5s build in a 1.2s frame gets
truncated, and truncated animation reads as broken software rather than
style. A 1.5s build in a 2.0s frame with a 0.8s dissolve out is worse:
the dissolve begins while the build is still running, so the viewer never
sees the finished state the next frame assumes. Three levers fix it —
more time (Paul Producer approves the duration), less motion (re-spec
the cell), or a shorter join (Ed Edit). Never "run it faster".

**`STILL — <reason>` is the deliberate version of blank.** A frame that
holds with nothing moving is a real choice: a beat to land something, a
title card, a photograph. Say so once a frame is long enough that a
motionless hold reads as an accident:

```
| 7 | — | — | The room at dawn, nobody at the desks | Turn | WS STATIC | STILL — the stillness is the point | — | SILENT — the alerts have stopped | — | 0:03 | 0:20 | — |
```

**Motion is not the join.** A dissolve, a fade or a wipe *between* frames
is `Trans out` on **this** card — `DISSOLVE 0.5s — through black` — with
its reason in the Transitions table. A build that happens *within* one
frame is Motion. If it's ambiguous, ask whether the next frame is already
on screen while it happens — if yes, it's the join out.

**Prefer the move that's cheap to build.** One thing moves — the eye can
only follow one anyway. If an animation needs several objects to stay in
synchrony, there is almost always a version that reads the same and
survives a re-time: **stagger** one animation (`0.3s apart`) instead of
moving several at once, **animate the container** rather than its
contents, or **hold everything but one thing**. `--motion` suggests these
without failing, because expensive choreography is sometimes right — it
just shouldn't happen by accident. `workers/motion-lead.md` has the
substitution table.

**Motion is priced, not just described.** Molly Motion quotes animated
frames in days and Dean Photography quotes camera moves in rigs and setup
time; both read this column at the feasibility pass, so vagueness here
turns into a surprise in week three. Motion also costs runtime: a 1.5s
build is 1.5 seconds the voiceover doesn't get.

### Motion vocabulary

**HOLD** nothing changes · **BUILD** elements assemble in place ·
**REVEAL** something hidden becomes visible · **WIPE ON / OFF** an element
enters or leaves directionally · **COUNT** a number runs to a value ·
**HIGHLIGHT** attention moves to part of the frame · **SCROLL** content
moves through a fixed viewport · **CURSOR** a pointer or interaction plays
out · **LOOP** a repeating ambient motion · **ACTION** a person or object
does something · **CAMERA** a move, when its timing matters beyond the
shot code

Combine a code with the specifics: `BUILD — three rows populate 0.3s
apart, left to right`. The code makes the board scannable; the sentence is
what gets built.

## Trans out — the join that leaves this frame

**The last field on the card, because it's the last thing that happens.**
A card names the join *out* of its frame whenever that join isn't a plain
cut. Blank means a straight cut, which is the default and the overwhelming
majority — writing `CUT` down the column buries the two or three joins
that were actually decided.

**Why out and not in.** A dissolve out of frame 4 overlaps frame 4's own
tail: it starts while frame 4 is still on screen and it comes out of
frame 4's `Dur`. So it's frame 4's business — the person building frame 4
has to know the picture has to be settled before the dissolve begins, and
frame 4's motion has to land before it starts. Documenting it on frame 5
puts the constraint on the card that doesn't pay for it. It also means a
card reads in the order it plays: the frame, what's said over it, how long
it lasts, how it ends.

The join **into** a frame is simply the previous card's `Trans out`. It is
never written twice.

When it isn't a cut, the cell carries **three things**:

```
TYPE  DURATION  —  detail
```

| Part | What it is | Why it's on the card |
|---|---|---|
| **Type** | `DISSOLVE`, `MATCH CUT`, `BUILD`, `FADE TO`, `WIPE`, `WHIP` | names the join |
| **Duration** | `0.5s`, `0s`, `12f` | a join without a length can't be budgeted against the runtime, and an editor will pick one for you |
| **Detail** | direction, what carries across, what the audio does, the ease | what makes the join buildable by someone who was in no review |

Examples:

```
DISSOLVE 0.5s — through black, music bed continues under
MATCH CUT 0s — the alert badge becomes the resolved checkmark, same position and size
FADE TO 0.8s — to brand navy, lets the silence land before the end card
WIPE 0.3s — left to right, following the cursor into the next frame
BUILD 1.2s — elements assemble into the diagram as the VO names them
```

`0s` is a real duration and worth writing: a match cut is instantaneous by
design, and saying so is different from forgetting to say.

**The last frame's Trans out is how the piece ends** — usually
`FADE TO 1.0s — to black, theme resolves under it`. It is the one join
with no frame on the other side, and leaving it blank means the piece
stops dead on the last frame, which is a choice somebody should make on
purpose.

**The card says what the join is; the Transitions table says why it's
worth it.** Type, duration and detail live here because they're needed to
*build* the join. The reason ("time passes between the two shifts") and
the cost ("~1 animation day — Molly Motion") live in the Transitions
standing note, because they're needed to *justify* it. Every non-blank
Trans out needs a matching row there — keyed on **From**, this frame — and
`--cards` flags a card and a table that disagree about type or duration:
one of them is stale, and until somebody looks, nobody knows which.

**Joins cost runtime.** Six 0.5s dissolves in a 30-second piece is a tenth
of the piece spent on joins, out of the same budget as words and pauses.
Ed Edit counts them; `--transitions` totals them.

**Stay inside the approved vocabulary.** `reference/brand-guardrails.md`
sets the brand's motion language, and a join outside it fails brand review
however well it reads. `--cards` flags a type it doesn't recognize.

## Worked cards

A speaking frame with on-screen text and an element build:

```
| 4 | NARRATOR | "One list. [PAUSE 0.6] That's *it*." | The console resolving to a single ranked list | Turn | SCREEN | BUILD — rows collapse 40 → 3 over 1.2s as the VO names them | "One ranked list." | Music lifts | Logo lockup first appears here | 0:06 | 0:18 | — |
```

A held, silent frame that fades out — both absences deliberate and stated:

```
| 7 | — | — | The room at dawn, nobody at the desks | Turn | WS STATIC | STILL — the stillness is the point | — | SILENT — the alerts have stopped | — | 0:03 | 0:21 | FADE TO 0.8s — to brand navy, lets the stillness land |
```

A frame that hands off to a new speaker on a dissolve:

```
| 8 | MARIA | "We were chasing *ghosts*." | Maria at her desk, mid-sentence | Problem | MS | ACTION — she turns from the second monitor as she starts talking | — | Room tone | New voice — Maria, real testimonial, first appearance | 0:05 | 0:26 | DISSOLVE 0.5s — through black, the drone drops out under it |
```

A frame that leaves on a match cut, carrying a shape into the next one:

```
| 6 | — | — | The alert badge, still red | Turn | INSERT | HOLD — settles for a beat | — | Single soft confirm tone | — | 0:02 | 0:17 | MATCH CUT 0s — the badge becomes the resolved checkmark in frame 7, same position and size |
```

## Before you call a card done

- [ ] Every field is either filled or deliberately blank — no half-filled cells.
- [ ] **Current state only.** No `was`, no `changed after`, no round numbers.
- [ ] **Motion** says what changes and when, or `STILL — <reason>` on anything that holds.
- [ ] This frame is a **state**, not a snapshot part-way through a move.
- [ ] **Text** is the wording itself, and the frame has a row in On-screen text.
- [ ] The text describes **this** Visual — not the frame before or after it.
- [ ] **Trans out** is blank, or reads `TYPE DURATION — detail` and has a
      matching Transitions row (keyed From = this frame) that agrees about
      type and duration.
- [ ] **Audio** is real sound or `SILENT — <reason>` — never a bare dash.
- [ ] A line has a Speaker, and that Speaker is in Cast & voices.
- [ ] **Note** carries information, not history and not doubt.
- [ ] Anything that changed went into the **Revision log** as a new top row.
- [ ] Nothing here contradicts a **Protected cut**.
- [ ] `scripts/boards.py --cards` is clean.
- [ ] `--card N` renders it in two columns or fewer, and it isn't taller than
      it needs to be.
