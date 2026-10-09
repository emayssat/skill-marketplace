# scripts/ — Dex Delivery's tooling

Feeds an **approved, frozen** storyboard to third-party services. No MCP
server required, no dependencies to install — Python 3.9+ standard library
only.

| File | What it does |
|---|---|
| `boards.py` | Parses `boards.md` into normalized frame cards and standing notes. The shared core: every service is fed from this one parser, so they all get the same frozen source. Also runs standalone to inspect what a boards file actually contains. |
| `send_higgsfield.py` | Submits one generation request per frame to the Higgsfield API, polls to completion, writes a run manifest. |
| `send_elevenlabs.py` | Renders the voiceover per speaking frame with ElevenLabs — maps each speaker to its voice, carries prosody across frames, writes audio files plus a manifest. |
| `build_revealjs.py` | Emits a self-contained Reveal.js HTML presentation from a frozen `boards.md`. Each deliverable frame becomes a slide; the Text cell is the slide body; the VO cell becomes speaker notes. Brand palette loaded from `--brand brand-guardrails.md`. No API key, no per-render cost. Dry run by default; `--out` writes the file. |

Which service to use for which job, and when that was last verified, is in
`reference/services.md`. Dex Delivery recommends; Paul Producer decides
on cost and contracts; Logan Legal clears the terms.

## Safety defaults

Every adapter here is built around the rule that makes the handoff
workflow work at all — **the boards are frozen**:

- **Dry run unless you pass `--submit`.** Nothing is sent, nothing is
  charged. Look at the prompts first; they're the actual deliverable.
- **Refuses boards that aren't frozen.** `status:` must be `approved` or
  `animatic-locked`, or the script exits with code 2. `--allow-unapproved`
  overrides it, and you should know why you're using it.
- **Credentials come from the environment, never from a file in this
  repo.** Never paste a key into a script, a prompt, or a manifest.
- **Frames marked CUT are skipped**, and unfilled template rows are
  ignored, so a half-written boards file won't silently generate nonsense.

## Quick start (Higgsfield)

```bash
# 1. Credentials — create at https://console.higgsfield.ai (secret shown once)
export HF_API_KEY_ID=...
export HF_API_KEY_SECRET=...

# 2. Check what the boards contain
python3 boards.py ~/work/acme-vision/boards.md --summary

# 3. Dry run — see the exact prompts, send nothing
python3 send_higgsfield.py ~/work/acme-vision/boards.md \
    --model-path /higgsfield-ai/soul/v2/standard \
    --style-block "$(cat style-block.txt)"

# 4. Submit a few frames and wait for them
python3 send_higgsfield.py ~/work/acme-vision/boards.md \
    --model-path /higgsfield-ai/soul/v2/standard \
    --frames 1-4 --submit --poll \
    --param aspect_ratio=16:9 \
    --out ~/work/acme-vision/delivery/higgsfield-run.json
```

**`--model-path` is required and not guessable.** Higgsfield's endpoints
are model-specific and its own docs say not to substitute one model or
environment for another. Find the path for the model you want in the
console, and pass whatever body fields that model takes via `--param`.

**Output URLs expire after about seven days.** Download the media into
your own storage as part of accepting delivery.

### Style block

`--style-block` is appended to every prompt and is where brand compliance
actually happens — it's the thing stopping a model drifting off-palette.
Take it from `reference/brand-guardrails.md`; Arthur Art approves it at
step 3 of `workflows/handoff.md`.

### What the manifest is for

`--out` writes the run as JSON: model path, style block, extra params, and
per frame the exact prompt, `request_id`, final status and output URLs.
Fold it into `<production>/delivery/manifest.md`. Generation isn't
deterministic, so this file is the difference between regenerating one
shot in six months and regenerating the whole piece hoping it matches.

## Looking at one card

```bash
python3 boards.py ~/work/acme/boards.md --card 8
python3 boards.py ~/work/acme/boards.md --card 8 --card-width 80
```

A 13-column table is the right way to *store* a board and a poor way to
*read* one frame. This draws a single frame in the canonical card layout
from `templates/production/frame-card.md`:

- **A labeled section spans the full card width, or shares a row with
  exactly one other. Never three.** A third column is a third as wide, and
  a third of the width turns one line of transition detail into six — two
  or three of those and the card is twice as tall for no added
  information.
- **Bounded values ride in the header strip** — frame number, beat, shot
  code, `Dur → Running`. They fit on one line together and they're what
  you scan to find a frame.
- **Anything that can be a sentence gets the full width** — Visual, VO,
  Motion, Note, Trans out.
- **Text and Audio pair by default**, and break out to full width on any
  frame where either runs long.
- **Speaker rides on the narration label** (`VO / DIALOGUE — MARIA`)
  rather than taking a block of its own.

The renderer *is* the spec — the diagram in the template is generated from
it, so the two can't drift apart.

## Checking animation continuity

```bash
python3 boards.py ~/work/acme/boards.md --motion
```

Prints every frame with motion against its clock — duration, motion
length, join out, and the slack between them — plus the start and end
state where the card says them. It checks the part of Molly Motion's
continuity pass that is arithmetic:

- **An animation longer than its frame.** A 1.5s build in a 1.2s frame
  gets truncated, and truncated animation reads as broken software rather
  than as style.
- **An animation still running when the join out starts.**
  `motion + join out ≤ Dur`. A 1.5s build in a 2.0s frame with a 0.8s
  dissolve out means the dissolve begins before the build lands, so nobody
  ever sees the finished state the next frame assumes. Fixes: more time,
  less motion, or a shorter join — never "run it faster".
- **An animated element with no duration.** `BUILD`, `COUNT`, `REVEAL`,
  `WIPE`, `SCROLL`, `HIGHLIGHT` and `CURSOR` have to be timed or they
  can't be priced or synchronized. `CAMERA`, `ACTION` and `LOOP` are
  looser — a camera move can be carried by the shot code.
- **A state change with no stated endpoints.** Write `BUILD — 40 rows → 3
  over 1.2s`, because frame 6's end state is frame 7's start state, and
  the arrow is what makes the next card checkable.
- **A frame that is a snapshot of a move rather than a state** — caught
  two ways. Wording that describes a part-way position (`half-way`,
  `mid-slide`, `continues to rise`, `still building`), and structurally:
  consecutive cards with the same shot, nothing said, under ~2s, and
  either a near-identical Visual or the same motion code. That pattern is
  one animation with card boundaries dropped into the middle of it, and
  **every frame boundary is a hold** — so it stutters the move or pads the
  runtime, and the middle card's timing can no longer be defended or cut.
  A card carrying its own line, a reframe, or a hold longer than ~2s is a
  real beat and passes.

What it deliberately does **not** check: whether the Motion cell matches
its Visual, and whether each frame actually starts where the last one
ended. Those need an animator's eye — `workers/motion-lead.md` has the
five-part check — this script covers the arithmetic (checks three and
four) and the structural half of check zero.

Exit code is 1 on any finding.

It also prints **suggestions**, which are advice and do **not** affect the
exit code — the only advisory output in the skill. These flag motion that
needs several objects to stay in agreement (`while`, `together`,
`converge`, `parallax`, `all … rotate`): the most expensive pattern to
build and the first to break when the duration moves or a translation runs
wide. Cheaper reads that usually look better — stagger one animation
`0.08s` apart, animate the container rather than its contents, or hold
everything but one thing. Syncing to the voiceover, music or a beat is
*not* this and stays quiet: that's one clock, not several objects
negotiating. `workers/motion-lead.md` has the substitution table.

Expensive choreography is sometimes right, which is exactly why this
advises rather than gates — Dana Director decides whether it's worth it.

## Checking the standing notes

```bash
python3 boards.py ~/work/acme/boards.md --notes
```

Prints the standing-note sections in the order they appear, the revision
log, and the protected cuts. It enforces three things:

- **Fixed section order, most-useful-first.** Beat direction →
  Transitions → On-screen text → Cast & voices → Music & silence →
  Animatic → Release status → Delivery routing → Protected cuts → Still
  open issues → Revision log.
- **The Revision log is last and newest-first** — v3 above v2 above v1,
  growing upward. Someone opening the file wants either "what do I do
  now," which the first ten sections answer, or "what changed since I
  looked," which the log's top row answers without scrolling. A log that
  grows downward pushes every other note further from the top until nobody
  reads them. Descending version numbers *and* descending dates are both
  checked.
- **Protected cuts actually protect something** — a named owner and a
  stated reason, a frame that exists on the board, and not a frame
  somebody has since marked CUT. That last one is the whole point: every
  time-reduction, platform-adaptation, restyle and localization pass goes
  hunting for seconds, and this is what stops the cleared claim or the
  consented testimonial being the cheapest-looking thing to lose.

Exit code is 1 on any finding.

## Checking the cards

```bash
python3 boards.py ~/work/acme/boards.md --cards
```

A board has two halves: the frame table is a stack of **cards**, each the
current state of one frame, and everything below it is **standing notes**.

First it checks **conformance to the card template**
(`templates/production/frame-card.md`, which defines the thirteen fields
and their order). A missing column isn't a formatting nit: a board with no
Motion column is a board where nobody said what moves, and that gap gets
filled by whoever builds the frame. Boards written before a column existed
will report it as missing — that's the intended signal to upgrade them,
and the parser reads them fine in the meantime.

Then it enforces the card/standing-note boundary, because crossing it is
what turns a third-revision board into half instruction and half
archaeology:

- **History on a card** — `was a wide shot`, `shortened after the
  preview`, `per round 2`. Overwrite the cell; log the change once in the
  Revision log.
- **An open question on a card** — `TBD`, `still not sure`. That's what
  Still open issues is for.
- **A default written out** — `CUT` in the Trans out column. The default *is*
  a cut, so writing it everywhere hides the two joins that were decisions.
  Blank means cut.
- **An underspecified join** — a `Trans out` naming a type but no duration
  (`DISSOLVE` instead of `DISSOLVE 0.5s — through black`), no detail, or a
  type outside the transition vocabulary. The card has to be enough to cut
  the join from; a length is also what makes it budgetable against the
  runtime.
- **A fact in two places that can drift** — a `Trans out` with no
  Transitions row leaving that frame, a Transitions row whose frame shows a plain cut, a card
  and a table that disagree about a join's type or duration, or on-screen
  text on a card with no row in the On-screen text table where its reading
  budget gets checked.
- **A new voice arriving silently** — the first frame a speaker appears on
  should say so in its Note; casting, mix and captions all key off it.
- **Running time that doesn't accumulate.** `Running` is a derived
  column that nobody derives — it's typed by hand, then a `Dur` changes
  and every row below it is quietly wrong, so the board claims 2:00 while
  the frames add up to 2:14. Also checks the total against
  `duration_target`, and says so louder when the runtime is FIXED. CUT
  frames contribute nothing, which is the point of keeping the row rather
  than the time.
- **On-screen text on the wrong frame.** The card's `Text` and its
  **On-screen text** row are two places one fact lives, and the rows slip
  against the cards whenever frames are inserted or cut after the text
  pass. Flagged: a row pointing at a frame that doesn't exist, a row
  pointing at a card with no text, and a row whose wording is a
  neighbouring card's. Where it can tell, the message names the direction
  — "frame 2's row carries frame 3's wording." A caption a frame early
  spoils its own reveal; a frame late labels a picture that has gone.
  `--cards` also **suggests**, without failing, when a text's words match
  the neighbouring frame's visual rather than its own.
- **Motion in the wrong cell or missing** — a dissolve written into Motion
  (that's a join between frames, so it's `Trans out`), a Motion that only
  repeats the shot code and adds no timing, or a frame that holds more
  than five seconds with nothing moving and no `STILL — <reason>`.

Exit code is 1 on any finding. Run it before a freeze and before a
handoff: downstream services read the card literally, so a cell that
still names the rejected shot will generate the rejected shot.

Motion also feeds the generation prompt, since a video model asked for a
scene with no movement described will invent some — `to_prompt(...,
include_motion=False)` turns that off for a still-image model.

## Checking pace

```bash
# words-per-minute per frame, against this piece's own target
python3 boards.py ~/work/acme-vision/boards.md --pace

# try a different pace without editing the boards
python3 boards.py ~/work/acme-vision/boards.md --pace --wpm 130
```

The target comes from `pace_target_wpm` / `pace_max_wpm` in the boards
frontmatter, falling back to 150/170 only when the piece hasn't set one —
and the output says which it used, so a default never passes for a
decision. Marked `[PAUSE n]` time is excluded from the speaking window
before the rate is calculated.

When a frame is over the ceiling it prints **both** fixes with numbers:
cut roughly N words, **or** stretch the frame to X seconds. Which one is
available depends on `duration_fixed` in the boards — a hard slot means
the words come out; a flexible runtime means stretching is on the table
and needs Paul Producer's sign-off on the new duration. It never offers
"read it faster" as an option.

Exit code is 1 if any frame is over the ceiling, so this works as a gate
in a check script.

## Checking the arc

```bash
python3 boards.py ~/work/acme-vision/boards.md --arc
```

Prints the Beat direction table — emotion, pace and delivery per beat —
and flags monotony: a beat with no emotion, an emotion that never changes
across the piece, a pace that never varies, or adjacent beats identical in
all three. Exits 1 on any finding.

Per-beat pace feeds `--pace` too: a frame is measured against its own
beat's target, falling back to the piece-level one. `--wpm` overrides
everything for a what-if.

### Silent frames

`--voices` also lists frames with no VO *and* no audio. Deliberate silence
is fine but must say so — `SILENT — <reason>` in the Audio column. A bare
dash, or a bare `SILENT` with no reason, fails: it's usually either an
unfilled cell or someone hoping the viewer pauses to look at the picture.
Explained silences longer than about 3s are flagged too, because Blair
Blind receives nothing at all for their duration.

## Checking transitions

```bash
python3 boards.py ~/work/acme/boards.md --transitions
```

Lists what happens between frames and flags anything that would get
invented in the edit: no type, no reason, no duration, or a reference to a
frame that doesn't exist. The default is a straight cut, so a board with
no Transitions table is valid — it just means every join is a cut. Also
totals the runtime spent on joins, which competes with words and pauses.

## Rendering voice (ElevenLabs)

```bash
export ELEVENLABS_API_KEY=...

# Dry run — see exactly what each speaker would be sent
python3 send_elevenlabs.py ~/work/acme/boards.md

# Render the narrator's lines
python3 send_elevenlabs.py ~/work/acme/boards.md \
    --speaker NARRATOR --submit \
    --out-dir ~/work/acme/delivery/vo \
    --out ~/work/acme/delivery/vo-run.json
```

Unlike Higgsfield this endpoint is **synchronous** — the response body is
the audio, so there's no polling.

What it does beyond a naive loop:

- **Speaker → voice mapping** from the Cast & voices table, so one
  character keeps one voice across every frame. The voice ID is read from
  the Source column (`Synthetic — ElevenLabs voice ID abc123`).
- **Skips real recordings.** A speaker whose source is a real interview
  isn't synthesized; that's their own voice and it stays that way.
- **Prosody continuity** via `previous_text` / `next_text`, so frames
  don't each sound like a cold read. Disable with `--no-continuity`.
- **Pause translation** — `[PAUSE 1.2]` becomes `<break time="1.2s" />`.
  SSML break support varies by model, so verify it; if unsupported, pass
  `--pause-format ""` to strip the markers and put the silence in the
  edit, and note that in the manifest.
- **Consent gate.** Refuses to render if the voice audit fails, including
  a real person with no consent recorded. `--allow-unconsented` exists and
  you should be able to explain why you used it.
- **`--speed`** is how you match the boards' `pace_target_wpm` — then
  measure the rendered audio rather than trusting the setting.

## Adding another service

`send_higgsfield.py` is deliberately written to be copied. To wire up a
voice service (ElevenLabs), another video model (Runway, Veo), or an
internal endpoint:

1. Copy `send_higgsfield.py` to `send_<service>.py`.
2. Keep the top half: it imports `load_boards` from `boards.py` and gets
   frame selection, the frozen-boards guard, dry-run and manifest writing
   for free. Don't reimplement those.
3. Replace four things, all in one region of the file (`send_elevenlabs.py`
   is a worked example of exactly this):
   - `API_BASE`
   - `_auth_header()` — each service differs. Higgsfield uses
     `Authorization: Key <id>:<secret>`; many others use
     `Authorization: Bearer <token>`; ElevenLabs uses an `xi-api-key`
     header. Read the vendor's current docs rather than assuming.
   - `submit_frame()` — the endpoint path and JSON body shape.
   - `TERMINAL_OK` / `TERMINAL_BAD` and `extract_outputs()` — the
     lifecycle states and where output URLs live in the response.
4. For a **voice** service, drive it from `frame.spoken_text(...)` rather
   than `frame.to_prompt()`, and key the manifest by **speaker** — one
   speaker gets one voice for the whole piece, so map
   `boards.voice_for(frame.speaker_label)` to a voice ID once and reuse
   it. `script.md` is the better source for a full VO pass; `boards.py`
   is the right source when you want VO aligned to frame timings.

   **Translate the pause markers.** Boards carry silence as
   `[PAUSE 1.2]`, which no service understands verbatim — send it raw and
   the voice will read the words "pause one point two" aloud.
   `spoken_text()` handles it:

   ```python
   frame.spoken_text()                                  # strip markers
   frame.spoken_text('<break time="{seconds}s"/>')      # SSML
   ```

   Check whether your service supports SSML breaks, its own marker
   syntax, or nothing at all — if nothing, strip them and insert the
   silence in the edit instead, and say so in the manifest so the pause
   doesn't quietly vanish.

   **Run the audit before submitting a voice job.**
   `python3 boards.py <boards.md> --voices` exits non-zero on an orphan
   line, a speaker missing from the cast, an undescribed voice, a bare
   `[PAUSE]` with no duration, or a real person with no consent recorded.
   That last one matters: cloning an identifiable person's voice needs
   their permission for that specific use.

Two conventions to preserve in any adapter you add, because the rest of
the workflow depends on them: **dry run by default**, and **read
credentials from the environment only**.

## Verification status

The Higgsfield adapter was written against `docs.higgsfield.ai` in
September 2026 — base URL, the `Key <id>:<secret>` auth scheme, the
async `request_id` / `status_url` envelope, the terminal states
(`completed`, `failed`, `nsfw`, `canceled`) and the image/video/audio
output shapes all come from those docs.

Parsing, frame selection, prompt construction, the frozen-boards guard,
dry run and manifest writing are all tested. The authenticated round-trip
is not — that needs a real key, so the first live `--submit` is worth
running on a single frame before you queue forty.
