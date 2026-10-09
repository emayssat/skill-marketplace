---
name: storyboard
description: >
  Use when the user is making, reviewing, or revising a storyboard,
  animatic, or short video piece — a product vision video, launch video,
  teaser, trailer, or explainer. Runs the work through a crew of role
  personas (scriptwriter, director, storyboard artist, art director,
  cinematographer, editor, sound designer, producer, client) who produce
  and critique it, plus audience personas who predict how real viewers
  will actually receive it. Also covers revising an existing piece:
  refreshing stale content, restyling, lengthening or shortening,
  reframing for another platform, and running preview or premiere
  feedback rounds before release. Trigger on requests like "storyboard
  this," "review this video script," "how would a CTO react to this,"
  "cut this 2-minute video down to 30 seconds," or "what would our
  audience think of this."
---

# storyboard

Assemble the crew, board the piece, and screen it for an audience — all
before anyone spends real production money.

## How to run it

1. **Open a production.** Create `<production>/` from
   `templates/production/`, **in the user's working folder — not inside
   this skill.** That folder is where this specific piece
   lives: its brief, script, boards, and feedback rounds. The brief
   inherits a format from `projects/` (goal, beat breakdown, tone,
   default team weighting); record in the production brief only what's
   specific to this piece. If no project type fits, add one from
   `projects/_template.md` first. Don't start boarding against an
   unstated goal.
2. **Establish the brand guardrails before styling anything.** They can
   arrive in any format — a brand book PDF, a slide deck, a brand site
   URL, a Figma or design file, a YouTube link, a video file, or an
   existing on-brand production. Whatever form it takes, read it and
   record what the team needs into `reference/brand-guardrails.md` (or a
   per-piece copy in the production folder when a piece follows different
   rules — a sub-brand, a co-branded piece, a customer's brand).

   **If nothing exists, ask for it, naming those formats** — people
   usually have *something*, they just don't think of a deck or a video as
   "guidelines." Never invent brand rules, never infer them from a generic
   "enterprise" look, and never carry a palette over from a previous
   production without re-checking: guidelines get revised, and a value
   that was right last quarter may not be right now. Mark anything derived
   from frames or screenshots as ESTIMATED and get it confirmed rather
   than quietly treating it as final.
3. **Pick the workflow.** Match the situation to a file in `workflows/`
   (see the list below). If the request doesn't fit any of them, start
   from `new-storyboard.md` and say what you're deviating from.
4. **Run the sequence step by step.** Each step names a persona and a
   gate. Read that persona's file before speaking as them, and produce
   the step's stated output before moving on. Don't collapse five steps
   into one summary — the sequence exists because the gates catch
   different problems at different costs.
5. **Screen it.** Once there's a cut worth reacting to, run `preview.md`
   with a small panel, then `premiere.md` with full representation
   before release. Let Paul Producer pick the panel from Claude Client's
   must-convince list and Dana Director's beat-at-risk — not from whoever
   seems likely to enjoy it — and route each finding to the one worker
   whose craft owns the fix.

## Operating rules

- **Reason from the persona file, not from generic knowledge of the
  role.** A persona's priorities, red flags, and voice are written down;
  use those. Speaking as "a director in general" defeats the purpose.
- **One persona speaks at a time, in their own voice**, and is always
  referred to by **first and last name** — "Dana Director," never "Dana"
  or "the director." Every surname is the person's function (Scott Script,
  Dean Photography, Skye Social, Blair Blind), so the full name tells a
  reader who is speaking and why their opinion counts, without looking
  anything up. Their example questions and feedback lines are reusable
  phrasing, not just illustrations.
- **Respect "Out of scope."** Every persona file names what that role
  should *not* weigh in on. A producer who starts rewriting dialogue, or
  a teenager cited on shot composition, is a persona bleeding out of its
  lane and makes the feedback worthless.
- **Gates are real.** When a step says something must be approved,
  locked, or accessibility-complete before the next step, don't proceed
  past it silently — say it isn't met and what that costs.
- **Disagreement is signal.** When two personas conflict (the DP says
  unshootable, the director says essential), surface the tradeoff for a
  human to decide rather than quietly picking a winner.
- **The audience outranks the room.** Worker personas judge craft;
  audience personas judge whether it lands. A piece every worker persona
  approves and the target audience persona doesn't understand has
  failed.
- **A feedback round has three separate decisions, and three owners.**
  **Paul Producer decides the panel** and who is in the room; **Claude
  Client names who must be convinced**; **Dana Director names the beat
  he's least sure of, and routes each accepted finding to the worker whose
  craft owns the fix.** The director does not pick the panel — choosing
  your own audience is choosing who gets to judge your work. And only the
  routed workers act: a fix step listed for everyone produces a
  scriptwriter rewriting a line nobody complained about.
  `workflows/preview.md` holds the finding-to-worker routing table.
- **When you change a frame, overwrite it — never annotate it.** A frame
  card carries the current state and nothing else. The change itself goes
  in the boards' Revision log, the doubt goes in Still open issues, and the
  reasoning goes in the standing note that owns it. Writing `(was a wide
  shot)` into a cell is the single fastest way to rot a board.

## Workers

This skill uses worker personas stored in `workers/`. Each persona describes
a production perspective that Claude adopts when producing or reviewing
storyboard content — how that role judges the work. Each has a first name
that starts with the same letter as the role, so it's easy to remember who's
who, plus example questions and feedback lines:

- `scriptwriter.md` — **Scott Script** (chooses the story structure and the purpose of each beat, then writes it)
- `director.md` — **Dana Director** (owns the emotional arc and per-beat pace; routes feedback findings to the craft that owns each fix)
- `voice-talent.md` — **Vera Voice** (reads the script aloud in pre-production; this is where read-time overruns get caught)
- `storyboard-artist.md` — **Stella Storyboard**
- `art-director.md` — **Arthur Art**
- `dp.md` — **Dean Photography** (live action)
- `motion-lead.md` — **Molly Motion** (substitutes for Dean Photography on motion-graphics pieces; specs, prices and continuity-checks every animation)
- `editor.md` — **Ed Edit**
- `sound-designer.md` — **Sonny Sound**
- `producer.md` — **Paul Producer** (decides the feedback panel and who is in the room; keeps the revision log)
- `legal-reviewer.md` — **Logan Legal** (claims, licensing, brand — gates external release)
- `client.md` — **Claude Client** (final sign-off; names whose approval the piece actually needs)
- `delivery.md` — **Dex Delivery** (converts approved boards into per-service inputs — generation prompts, VO manifests, caption files; runs only after premiere, on frozen boards)

Each file's `enters:` field names the step where that role first acts in
`workflows/new-storyboard.md`, and is kept true to that file.

`workers/_template.md` is the stencil — copy it to `workers/<role_id>.md`
for each role and fill it in. Do not edit `_template.md` itself once other
worker personas exist; it should stay a blank stencil.

**When adding a new worker persona:** also update every workflow in
`workflows/` where that role actually contributes — insert their step at
the right point in the sequence and renumber what follows. A worker
persona that isn't wired into at least one workflow won't actually get
consulted.

## Audience

`audience/` holds reception personas — the people actually watching the
finished piece. Where a worker persona judges craft, an audience persona
predicts reception: what hooks them, what loses them, what they'd ask
afterward. Each also has a letter-matched first name and example
questions/feedback. Covered so far:

- **Internal / business:** `product-manager.md` (**Paula Product**), `program-manager.md` (**Piper Program**), `c-suite-leader.md` (**Camille Chief**), `mid-level-manager.md` (**Marcus Manager**)
- **Internal / technical:** `software-engineer.md` (**Seth Software**), `site-reliability-engineer.md` (**Soren Reliability**), `security-engineer.md` (**Silas Security**)
- **External / general public:** `teenager.md` (**Theo Teen**), `young-adult.md` (**Yoan Young**), `mother.md` (**Maya Mother**), `father.md` (**Felix Father**), `retiree.md` (**Robert Retired**), `social-scroller.md` (**Skye Social**), `non-native-speaker.md` (**Nadia Language**), `deaf-hard-of-hearing.md` (**Dev Deaf**), `blind.md` (**Blair Blind**), `low-vision.md` (**Leo Vision**), `cognitive-neurodivergent.md` (**Cora Cognitive**)
- **External / customer:** `skeptical-buyer.md` (**Simone Skeptic**), `existing-customer.md` (**Elena Existing**)
- **Disposition** (a second axis — see below): `optimistic.md` (**Olive Optimist**), `pessimistic.md` (**Pia Pessimist**), `fact-only.md` (**Frank Facts**), `emotional.md` (**Esme Emotion**)

### Two axes: segment and disposition

Most audience personas are **segments** — who someone is (a product manager,
a teenager, a blind viewer). The four **dispositions** are orthogonal to
that: they describe *how* a viewer receives anything, and any segment can
hold any disposition. Use them two ways:

- **Overlay one on a segment** — a pessimistic CTO and an optimistic CTO
  watch the same cut very differently, and knowing which one is in the
  room changes what the piece needs to do.
- **Run the opposing pair as a bias check.** Olive Optimist and Pia
  Pessimist on the same cut is the single fastest way to find out whether
  a piece is persuasive or merely agreeable. Frank Facts and Esme Emotion
  are the other pair: one tells you whether there's substance, the other
  whether there's a pulse. A piece that satisfies only one of a pair has a
  known, nameable weakness.

None of the four is an arbiter on its own, and each file says so
explicitly — Olive Optimist's approval proves nothing by itself, and a
piece tuned only to survive Pia Pessimist ends up hedged and joyless.

`audience/_template.md` is the stencil for adding new audience personas —
copy it to `audience/<audience_id>.md` and fill it in. A project's
"Audience" field (see `projects/`) should name the relevant persona(s) here.

## Naming convention

Every persona has a two-part name, and both halves do work:

- The **first name** starts with the same letter as the role — Yoan Young,
  Robert Retired, Arthur Art, Ed Edit — so the name is a memory hook.
- The **surname is the function itself** — Scott Script, Dean Photography,
  Paul Producer, Skye Social, Soren Reliability — so the full name states
  what the person is for.

Both halves are unique across all 32 personas. Always use the full name
when referring to one; the whole point is that "Silas Security flagged
frame 9" needs no further explanation.

## Projects

`projects/` holds reusable **formats**, not actual pieces. Each one sets
the goal, audience, timed beat breakdown, and which worker personas carry
the most weight for that kind of video (e.g. `product-vision-2min.md`,
`product-launch-2min.md`). Each also proposes a default **story
structure** and a default **pace**, which a production can override in its
brief. A format is written once and reused by many productions.

Current formats: `product-vision-2min.md`, `product-launch-2min.md`,
`explainer-90s.md`, `short-form-vertical.md`, `sizzle-reel-30s.md`.

`projects/_template.md` is the stencil for adding new project types —
copy it to `projects/<project_type>.md` and fill it in.

## Scripts

`scripts/` holds Dex Delivery's runnable tooling for feeding an approved
storyboard to third-party services without needing an MCP server. Python
3.9+, standard library only, nothing to install.

- `boards.py` — parses `boards.md` into normalized frames and builds
  per-frame prompts, expanding shot codes into model-readable language.
  Every adapter shares this parser, so all services are fed from one
  frozen source.
- `send_higgsfield.py` — submits one request per frame to the Higgsfield
  API, polls to completion, writes a run manifest.
- `send_elevenlabs.py` — renders the voiceover per speaking frame with
  ElevenLabs: speaker-to-voice mapping, prosody continuity across frames,
  pause translation, and a consent gate that refuses to synthesize an
  uncleared real voice.
- `README.md` — usage, and how to copy the adapter for another service
  (voice synthesis, another video model, an internal endpoint).

Two behaviors are deliberate and should survive any adapter added later:
the scripts **dry-run unless `--submit` is passed**, and they **refuse
boards that aren't frozen** (`status: approved`), which enforces the
handoff rule mechanically instead of on trust. Credentials are read from
environment variables only — never hardcoded, never written into a
manifest.

## Reference

`reference/services.md` records which service to use for which job and
**when that was last verified** — currently ElevenLabs for voice,
Higgsfield for video/image generation, and HyperFrames for typographic,
UI and data frames (HTML rendered deterministically to MP4, so text is
typeset rather than hallucinated). **Routing is per frame, not per
piece.** It carries dates because this
market moves faster than anything else here, and a "best tool" claim baked
into a persona file would be quietly wrong within a year. **Dex Delivery
recommends, Paul Producer decides** on cost and procurement, **Logan
Legal clears** the terms.

`reference/brand-guardrails.md` is what Arthur Art styles against and Logan Legal
clears against — palette, typography, shape and motion vocabulary, logo
rules, product naming, claim substantiation, customer-material policy, and
an accessibility floor.

**It ships blank on purpose.** This skill is organization-agnostic, and
brand guidelines get revised — a palette baked into the skill is one that
goes stale without anyone noticing. Fill it per organization, or per
production when a piece follows different rules. The file also carries the
intake guidance: which source formats to ask for, what each one is good
for, how to read guardrails out of a video, and the CONFIRMED / ESTIMATED
/ NEEDED marking that keeps guessed values from reaching production.

## Productions

Everything above — `workers/`, `audience/`, `workflows/`, `projects/`,
`reference/`, `scripts/`, `templates/` — is **reusable and ships with the
skill**. A production is the opposite: one specific video, belonging to
whoever is making it.

**Productions live in the user's own working folder, never inside this
skill.** Create `<production>/` — one folder per video, named with a
descriptive dated slug like `ai-management-plane-2026q1/` — wherever the
work belongs. Copy `templates/production/` to start one — it holds
`brief.md`, `script.md`, `boards.md`, `feedback/round-template.md`,
`delivery/manifest.md`, and **`frame-card.md`**, which defines a single
frame card and is the one file to read before writing the first frame.
Keeping
instances out of the skill directory means the skill can be updated,
shared or reinstalled without touching anyone's actual work, and means
nobody's unreleased video ships inside a reusable package.

That folder is where work persists between workflow runs, and what the
workflows mean when they say "pull the original project file, script, and
boards." Each production holds:

| File | What it is | Owner |
|---|---|---|
| `brief.md` | This piece's goal, deviations from its project type, named audience personas, panel assignments, constraints | Paul Producer |
| `script.md` | VO and dialogue, beat-aligned, with a read-time check against the target duration | Scott Script |
| `boards.md` | **The storyboard** — a stack of **frame cards**, each built from `templates/production/frame-card.md` (speaker, VO, visual, beat, shot, motion, on-screen text, audio, note, duration, running time, transition-out) and holding only that frame's current state, plus the **standing notes** below them: Beat direction, Transitions, On-screen text, Cast & voices, Music & silence, Animatic, Still open issues and the Revision log. The animatic is this same table with timings committed and `status: animatic-locked`. | Stella Storyboard; cast owned by Sonny Sound; revision log by Paul Producer |
| `feedback/NN-preview.md`, `feedback/NN-premiere.md` | One record per feedback round: panel, per-persona reaction, triage, outcome — plus prediction-vs-reality after release | Paul Producer |
| `delivery/manifest.md` | Service, model version, seed, exact prompt and settings for every generated shot and voice line — what makes the piece reproducible months later | Dex Delivery |

Two conventions matter:

- **A board has two halves: frame cards and standing notes.** The frame
  table is a stack of **cards** — each row the *current state* of one
  frame. Everything below it is **standing notes** — what applies across
  frames, why a choice was made, what's unresolved, and the entire
  history. **History never appears
  on a card.** Not `was a wide shot`, not `shortened after the preview`,
  not `Dana asked for this in round 3`: overwrite the cell and log the
  change once in the Revision log. A card that carries its own history
  gets handed to a vendor or a generation service with the rejected
  version still in the cell, and a board three rounds in becomes half
  instruction and half archaeology with no way to tell which is which.
  **Stella Storyboard keeps the cards clean; Paul Producer keeps the
  history complete.** Checked with `scripts/boards.py --cards`.
- **The standing notes run in a fixed order, most-useful-first, and the
  Revision log is last and newest-first.** Beat direction → Transitions →
  On-screen text → Cast & voices → Music & silence → Animatic → **Release
  status** (where the piece is in its life, Paul Producer) → **Delivery
  routing** (which service or vendor builds what, Dex Delivery) →
  **Protected cuts** (frames that must not change, and who protected
  them) → **Still open issues** → **Revision log**. Everything answering
  "what do I do now" comes before the one section that only answers "what
  already happened", and the log grows *upward* — v3 above v2 above v1 —
  so the top row is the answer to "what changed since I last looked" and
  the rest of the board stays where people left it. Checked with
  `scripts/boards.py --notes`.
- **A protected cut goes back to whoever protected it.** Logan Legal
  protects a cleared claim, Sonny Sound a consented testimonial, Claude
  Client the beat the piece exists to deliver, Arthur Art a brand minimum.
  Every shortening, reframing, restyling and localization workflow goes
  hunting for seconds, and without that section the cheapest-looking frame
  to lose is often the one that was most expensive to earn. A protection
  with no named owner and no reason protects nothing.
- **Every card follows one template.**
  `templates/production/frame-card.md` is the definition — the thirteen
  fields, their order, what each holds, the motion vocabulary, worked
  examples and a fill checklist. Read it before writing the first frame.
  Conformance is mechanical: `scripts/boards.py --cards` reports a missing
  column or a column out of order, because a board missing **Motion** is a
  board where nobody has said what moves.
- **A card records differences, not defaults.** Beyond shot, visual,
  speaker, line, audio and timing, each card carries four fields that are
  blank by default and meaningful only when filled:
  **Motion** (what changes during this frame — blank means nothing does),
  **Text** (on-screen text, written verbatim — blank means none),
  **Trans out** (the join *out* of this frame, as `TYPE DURATION —
  detail`: `DISSOLVE 0.5s — through black, drone drops out under it`.
  Blank means the frame leaves on a straight cut, and writing `CUT`
  everywhere buries the two joins that were decisions), and **Note** (anything the crew needs to know at this frame
  that no other column says — *"New voice — Maria, real testimonial, first
  appearance"*, *"Logo lockup first appears here"*, *"Sound bridges from 6"*).
  The card states the fact; the standing note explains it — the Trans out
  column says a dissolve happens here, the Transitions table says why and
  what it costs.
- **A card opens with the line and closes with the exit.** The column
  order is fixed: **Speaker** and the **line** first — it's written first,
  it drives the frame, and "what is said here?" is the question a reader
  arrives with — then the **Visual** it plays over, then beat, shot,
  motion, text and audio; then the timing; and last **Trans out**.
  Rendered one frame at a time (`--card N`), the speaker moves into the
  header strip with the number, beat, shot and timing, since who is
  talking is a one-word fact you scan rather than a labeled block. The join out lives on this card rather than the join in
  on the next one because a dissolve out of frame 4 begins while frame 4
  is still on screen and comes out of frame 4's own `Dur` — so it belongs
  to the card that pays for it, and a card then reads in the order it
  plays. The join *into* a frame is simply the previous card's Trans out,
  never written twice.
- **Structure is chosen before anything is written, and it has an owner.**
  **Scott Script picks it** — hero's journey, problem-agitate-solve,
  before-after-bridge, situation-complication-resolution, in medias res,
  question-answer, chronological/process — says why it fits this audience
  and message, names who the hero is (**never the product**), and gives
  every beat a **purpose**: what it is *for*, not what happens in it.
  **Dana Director approves it.** Both go in the brief. When nobody
  chooses, a piece becomes an anatomy tour of things that exist, and every
  persona downstream reports it as "flat" without being able to name the
  cause — which is why no amount of pace, music or motion fixes it. Three
  beats with the same purpose are one beat and two of runtime.
- **A frame is a state, not a sample of a move.** If frame 6 is a closed
  panel and frame 8 is an open one, a frame 7 showing it half-way is a
  snapshot, not a frame. **Every frame boundary is a hold** — a card
  asserts a `Dur` and a board is read one frame at a time — so slicing one
  continuous slide across three cards asserts two pauses inside it, which
  stutters the move or inflates the runtime, and leaves timing nobody can
  defend. One movement, one place: **Motion** inside a frame, **Trans
  out** between two. A long move spans cards only when each card earns its
  existence for a reason other than the animation having progressed.
- **Animation gets checked as a sequence, not frame by frame.** Molly
  Motion's five-part check: does the Motion match its Visual (the Visual
  is the frame's **end state**, never a midpoint); does it start where the
  previous frame ended; does it end where the next one begins; and does
  `motion + join out` fit `Dur`. State changes carry explicit endpoints —
  `BUILD — 40 rows → 3 over 1.2s` — because that is what makes the next
  card checkable, and `--motion` also flags frames that are one move
  sampled twice. Truncated animation reads as broken software, not as
  style, and the fixes are more time, less motion or a shorter join —
  never "run it faster".
- **The cheapest animation that gets the read is the right one.** One
  thing moves; the eye can't follow two. **If a move needs several objects
  in synchrony, Molly Motion proposes something else** — stagger one
  animation rather than moving several at once, animate the container
  rather than its contents, hold everything but one thing. That pattern is
  the most expensive to build and the first to break when the duration
  moves or a translation runs long, because the *relationships* between
  the objects have to be re-derived every time. He recommends and **Dana
  Director decides** — expensive choreography is sometimes right, it just
  shouldn't happen by accident, priced as if it were simple. `--motion`
  reports these as suggestions that don't fail the check, the one
  advisory output in the skill.
- **Motion is what the still can't show.** A board frame is a drawing; the
  piece isn't. Motion is everything that changes inside one frame's
  duration — **between the join in and the join out** — and it comes in
  three kinds: the **camera** (`CAMERA — push completes by 0:03, then
  holds`), the **subject** (`ACTION — she looks up on the second alert`)
  and the **elements** (`BUILD — three rows populate 0.3s apart`). Write
  what changes and when; "dynamic" is not motion. **Molly Motion owns it on
  motion-graphics pieces, Dean Photography on live action**, Dana Director
  approves it, Stella Storyboard writes it on the card, Ed Edit pays for
  it in runtime. A dissolve *between* frames is this card's `Trans out`,
  not Motion — the test is whether the next frame is already on screen
  while it happens.
  A frame that holds with nothing moving is fine but says so:
  `STILL — <reason>`, the same rule as `SILENT — <reason>` for audio, and
  for the same reason. Unspecified motion gets invented by whoever builds
  the frame, at whatever it happens to cost.
- **Frame numbers are permanent.** Personas cite frames by number
  ("frame 12 reads as confused"). Insert as `11a`; mark cuts as CUT and
  leave the row. Never renumber.
- **Every line has a named speaker, and every speaker has a described
  voice.** The Speaker column names who talks; the Cast & voices table
  says what they sound like, where the voice comes from, and whether a
  real person consented. A name on a frame isn't castable — "MARIA" tells
  nobody how Maria sounds. One speaker keeps one voice for the whole piece.
- **Pace varies within a piece, and emotion drives it.** The Beat
  direction table in the boards gives every beat an emotion (what the
  audience should feel) and its own pace target. **Dana Director owns the
  emotion**, **Vera Voice performs it and says when the writing makes that
  impossible**, Sonny Sound scores to it, Ed Edit cuts to it. A hook runs
  quick, a reveal slows, a close settles — one pace and one emotion for a
  whole piece is a monotone, however good the words are. Emphasis is marked
  in the line with `*asterisks*`; a line with nothing worth stressing
  probably isn't saying anything.
- **The joins get documented too, in two halves.** The **card builds the
  join out of its own frame** — type, duration and detail, everything
  needed to cut it:
  `MATCH CUT 0s — the alert badge becomes the resolved checkmark, same
  position and size`. The **Transitions table justifies it** — the reason
  and the cost. Type and duration appear in both on purpose, so the card
  stands alone for an editor and the table stands alone for a budget
  review; `--cards` fails when they disagree, because then one is stale
  and looking at it won't tell you which. The default is a straight cut
  and only exceptions are listed — but every listed one needs a duration
  (a join with no length costs nothing on paper and seconds in the edit)
  and a reason, because a transition says something (a dissolve says time
  passed, a match cut says these are the same thing) and decoration costs
  both runtime and animation days. **Ed Edit owns it**, Molly Motion prices the animated
  ones, Arthur Art keeps them inside the brand's motion vocabulary, Sonny
  Sound decides which need audio. An unspecified join gets invented by
  whoever is in the edit that day.
- **A frame with no voiceover and no sound needs a reason.** Written as
  `SILENT — <reason>` in the Audio column, never a bare dash. Deliberate
  silence is often good — a held beat, an absence that means something.
  Silence because somebody hopes the viewer *pauses to look* is the same
  failure as expecting them to pause and read: give the frame audio, or
  cut it. **Sonny Sound decides and documents**, Dana Director approves
  the intent, Ed Edit cuts dead air that can't be justified, and **Blair
  Blind is the hard check** — a silent frame is completely empty for her,
  so anything beyond a brief beat needs audio description.
- **Silence is content and gets written down.** Pauses live in the boards
  as `[PAUSE 1.2]`, always with a number, because a pause costs runtime
  and an unnumbered one gets improvised. Vera Voice marks them, Ed Edit
  decides what the cut can afford, and Sonny Sound drops the music bed so
  the pause reads as a beat rather than a gap.
- **Music is a recommendation, and "none" is a valid one.** Sonny Sound
  records it in the boards' Music & silence section with the reasoning —
  testimonials often play better dry, and a scored explainer competes
  with its own explanation.

- **Pace is a decision with an owner, not a constant.** The project
  format proposes a target, **Dana Director sets it** for the piece (how
  fast it talks is a tone choice), **Paul Producer says whether the
  runtime can move**, and it's recorded as `pace_target_wpm` /
  `pace_max_wpm` and `duration_fixed` in the boards. Defaults of 150/170
  apply only when nobody has chosen — a piece for largely non-native
  speakers belongs nearer 130, a social hook can sit at 165.
- **When words don't fit the seconds, there are three fixes and Vera
  Voice reports all of them** rather than picking: **cut words** (Scott
  Script; the only option when the runtime is fixed), **stretch the
  time** (Paul Producer approves, Ed Edit re-times — the option people
  forget, and often the right one, since a 2:10 piece that lands beats an
  on-the-nose 2:00 that doesn't), or **change the pace target** for the
  whole piece (Dana Director). The same words read faster past the ceiling
  is not a fourth option. The check is **per beat, not per piece** — an
  average hides the one crammed beat.
- **On-screen text has to be on the right frame, and Arthur Art owns
  that.** A caption a frame early spoils the reveal it was written to
  land after; a frame late labels a picture that has already gone. The
  slip happens whenever frames are inserted or cut after the text pass —
  invisible in a table, unmistakable on screen. The card's `Text` and its
  On-screen text row must agree; `--cards` fails when they don't and
  names the direction where it can tell.
- **On-screen text has its own, separate budget** — roughly 2–3 words per
  second of hold, less if the voiceover is talking over it. **"They can
  pause the video and read it" is not a plan:** almost nobody pauses, and
  the viewers who most need the time (Cora Cognitive, Nadia Language,
  Robert Retired, Leo Vision) are the least likely to take it. A
  pause-and-read frame is a legitimate deliberate choice — a reference
  card, a summary — but nothing load-bearing goes in one, and whatever it
  says the voiceover says too. Arthur Art owns this budget.

Seven audits run mechanically:

- `python3 scripts/boards.py <boards.md> --motion` — animation continuity,
  in the part that is arithmetic: an animation longer than its frame, an
  animation still running when the join out starts (`motion + join out ≤
  Dur`), an animated element with no duration, and a state change with no
  stated `A → B` endpoints for the next frame to continue from. Whether a
  Motion cell matches its Visual, and whether each frame starts where the
  last one ended, is **Molly Motion's** read.

- `python3 scripts/boards.py <boards.md> --notes` — the standing notes:
  sections out of the fixed order, a Revision log that isn't last or isn't
  newest-first, and protected cuts with no owner, no reason, a frame that
  isn't on the board, or a frame somebody has since marked CUT.
- `python3 scripts/boards.py <boards.md> --cards` — conformance to the
  card template (a missing or misordered column) plus card hygiene:
  history or an unresolved question written onto a card, `CUT` spelled out
  where blank means the same thing, a `Trans out` with no Transitions row
  leaving that frame (or the reverse), a `Trans out` with no duration, no
  detail or a type outside the vocabulary, a card and table that disagree
  about a join's type or length, a join written into Motion where it
  belongs in Trans out, a Motion that just restates the shot code, a long hold with no
  `STILL — <reason>`, on-screen text with no reading-budget row, and a new
  speaker arriving on a card that says nothing about it.
- `python3 scripts/boards.py <boards.md> --voices` — orphan lines,
  speakers missing from the cast, undescribed voices, bare `[PAUSE]`
  markers, uncleared real voices, and **silent frames with no stated
  reason** (plus explained ones long enough to need audio description).
- `python3 scripts/boards.py <boards.md> --pace` — words-per-minute per
  frame against **that beat's** target, pause time excluded, printing both
  the cut and the stretch in numbers for anything over the ceiling.
- `python3 scripts/boards.py <boards.md> --transitions` — the joins,
  flagging a transition with no type, no reason, no duration, or a
  reference to a frame that doesn't exist.
- `python3 scripts/boards.py <boards.md> --arc` — the emotional arc and
  pace map, flagging beats with no emotion, an emotion that never changes,
  a pace that never varies, and adjacent beats identical in emotion, pace
  and delivery. This is the monotony check, and it's mechanical so that
  "it feels flat" becomes an argument about evidence.
- **`status` is a gate, not decoration.** Workflows check it — Sonny Sound
  scoring against anything less than `animatic-locked`, or anyone
  boarding against an unlocked script, is rework waiting to happen.

## Workflows

`workflows/` holds the task sequences the team runs, each step assigned to
a persona. There are two kinds.

**Production workflows** — every step owned by a worker persona from
`workers/`:

- `new-storyboard.md` — build a storyboard from scratch (the canonical workflow; 17 steps)
- `script-review.md` — critique a script *before* any boarding, the cheap gate
- `remake.md` — refresh stale content, same storyline
- `redesign.md` — new visual style/medium, same content
- `teaser.md` — very short anticipation-builder that reveals almost nothing, often built before the full piece exists
- `trailer.md` — promotional cut mined from an existing finished or boarded piece
- `time-extension.md` — lengthen an existing storyboard
- `time-reduction.md` — shorten an existing storyboard into a complete short version
- `platform-adaptation.md` — reframe an existing piece for a different aspect ratio/platform
- `localization.md` — adapt for another language or region (changes timing, layout, and what you're permitted to claim)

**Feedback workflows** — most steps owned by audience personas from
`audience/`, with workers preparing the cut and acting on what comes back.
Each carries a "Panel composition" section naming who to consult, and a
"Who decides who takes part" section naming who chooses them (Paul
Producer decides; Claude Client and Dana Director supply inputs; only
routed workers act):

- `persona-reaction.md` — one persona, one question, minutes not rounds; the everyday workflow
- `preview.md` — small hand-picked panel (3-5 key personas) reacts to a cut before full production spend; holds the canonical **finding-to-worker routing table**
- `premiere.md` — full representative panel including all accessibility personas; doubles as the release go/no-go, and feeds real reaction back into `audience/`

**Handoff workflow** — runs after premiere, on frozen boards:

- `handoff.md` — convert the approved storyboard into per-service inputs (video generation, voice synthesis, captions, or a human vendor), run them, and log everything needed to reproduce the result

`workflows/_template.md` is the stencil for adding new workflows — copy it
to `workflows/<workflow_type>.md` and fill it in.
