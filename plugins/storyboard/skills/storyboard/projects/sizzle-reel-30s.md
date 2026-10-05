---
project_type: sizzle-reel-30s
project_title: Sizzle Reel (30s)
duration: "0:30"
format: 16:9 by default; assembled from existing footage, cut to a licensed track
---

# Sizzle Reel (30s)

**Goal:** Make a room feel something in thirty seconds. A sizzle reel does
not explain, teach or persuade on evidence — it raises the temperature
before something else happens: a keynote, a sales kickoff, a pitch, a
booth that needs people to stop walking.

**Audience:** A captive one, usually. **Camille Chief** and **Marcus
Manager** at an internal all-hands or sales kickoff; **Simone Skeptic**
and **Elena Existing** at an event; **Skye Social** only if it's being
repurposed, which it usually shouldn't be without a **Platform
Adaptation** pass. **Blair Blind deserves a decision up front** — see
Constraints.

**Key message:** Not a message. A *feeling*, plus at most one claim at the
peak. If there is something the viewer has to understand and retain, this
is the wrong format — make an **Explainer (90s)** and play the sizzle
before it.

**Tone:** Momentum. Confident without narration doing the work. The
failure mode is "corporate hype video," and the difference between energy
and hype is whether the images are real.

**Pace:** mostly not a words-per-minute question — this format is text-
and music-led, and VO is optional. **If there is VO, keep it under ~25
words total and run it near 130 wpm**, because it's competing with a
track. The budget that actually binds is on-screen text: roughly 2–3 words
per second of hold, on shots that are often only 1–2 seconds long.
**Runtime is FIXED** for this format — the track's length and structure
decide it, and you cannot stretch a piece that's cut to a hit point.

## Story structure (default)

**escalation / montage** — intensity over time rather than events over
time. This is the one format where "no narrative structure" is the correct
answer: nothing happens *to* anyone, and the shape is a curve — open on
strength, widen, accelerate, peak, land.

That makes it the format most at risk of becoming an anatomy tour by
accident. The difference is the curve: a tour shows five equal things in a
row, a sizzle makes each stretch bigger than the last. If the piece would
survive having its shots reordered, it has no escalation and it is a tour.

Sasha Script can deviate, but says so in the brief and says why.

## The track comes first

**Sonny Sound picks the music before a single shot is selected**, and this
is the one format where that ordering is non-negotiable. A sizzle is cut
*to* a track: the track's build, drop and resolve are where the beat
boundaries actually fall, and the times in the breakdown below are
approximations that get pinned to the real hit points once the track
exists.

Choosing footage first and finding music to fit produces a piece that
never quite lands, and no amount of re-cutting fixes it — because the
edit points were chosen against a rhythm that isn't there.

**The licence is part of picking the track.** A temp track that survives
into the final mix is the single most common legal failure in this format,
and at a sizzle's usual turnaround it is also the easiest one to commit.

## Beat breakdown

| Time | Beat | What happens |
|---|---|---|
| 0:00–0:04 | Signature shot | The best single image you have, cold, with no build-up. A sizzle earns attention by spending its best asset immediately rather than saving it. |
| 0:04–0:12 | Range | Breadth — who, where, how much, how many. Establishes that there is substance behind the energy. Shots still have room to breathe here. |
| 0:12–0:22 | Escalation | Cuts shorten, images get bigger, the track builds. Each stretch has to out-do the one before it or the curve flattens. |
| 0:22–0:27 | Peak | The biggest image, landing on the track's hit, carrying the one claim if there is one. |
| 0:27–0:30 | Button | Lockup and one line, resolving with the music. A sizzle that stops rather than lands leaves a room silent in the wrong way. |

## Team for this project

- **Sonny Sound (sound designer)** — **co-lead.** Picks and licenses the track first; the edit is built on it. Also the person who says when a piece is peaking too early, because he can hear it.
- **Ed Edit (editor)** — **co-lead.** This format *is* an edit. Owns shot selection rhythm, the escalation curve in practice, and every `Trans out` — a sizzle lives in its cuts more than in any single frame.
- **Dana Director (director)** — owns the curve as intent: what the room should feel at 0:05, 0:15, 0:25. Approves the peak and the button.
- **Stella Storyboard (storyboard artist)** — boards by **selecting**, not inventing: each card names the source clip, its timecode and whether the rights are cleared. Expect 20–40 cards at 1–2 seconds each.
- **Arthur Art (art director)** — grade consistency across sources that were never meant to sit together, plus text treatment and legibility at 1–2 second holds.
- **Logan Legal (legal reviewer)** — **elevated in this format.** Every clip, every recognizable face, every third-party or customer logo, and the music licence. More sizzles are blocked at the last minute on rights than on craft.
- **Paul Producer (producer)** — sourcing and rights admin is the bulk of the work here, not scheduling. Also owns whether the footage that exists can carry the piece at all.
- **Sasha Script (scriptwriter)** — light but not absent: writes the on-screen text and the single claim at the peak, and is the one who says when a sizzle is trying to explain something.
- **Molly Motion (motion lead)** — usually light — lockup, text treatments, occasionally a transition build. Worth asking Dex Delivery whether those are better rendered as code than hand-built; see `reference/services.md`.
- **Dean Photography (DP)** — usually **absent**. Nothing is shot. If there is a shoot day it is for pickups to fill a hole the archive can't.
- **Vera Voice (voice talent)** — often absent. Brought in only if there is VO, and then for one or two lines.

## Deliverables checklist

- [ ] Track chosen, **licensed, and the licence on file** — before edit lock
- [ ] Clip source list: every shot with its origin, timecode and rights status
- [ ] Written permission for any customer footage, brand or recognizable face
- [ ] Approved boards, each card naming its source
- [ ] Grade pass across mismatched sources
- [ ] Captions (and a decision recorded on audio description — see Constraints)
- [ ] Playback check in the actual room or on the actual screen
- [ ] Sign-off

## Constraints specific to this project

- **The runtime is fixed by the track.** Stretching is not available; if
  the content doesn't fit, shots come out. Record this as
  `duration_fixed: true` in the boards.
- **Rights are the schedule risk, not the edit.** Assume every clip is
  unusable until someone says otherwise. A customer's enthusiasm in a
  meeting is not written permission.
- **A temp track must not reach the final mix.** Put the licensed track in
  the boards' **Protected cuts** under Sonny Sound, and treat any
  late swap as a re-cut rather than a substitution — the edit points move.
- **Don't peak at 0:10.** A piece that spends its biggest image early has
  twenty seconds of anticlimax and no way out except re-ordering.
- **Mismatched sources need a grade pass**, or the piece reads as a folder
  of clips rather than a film. This is the most common reason a sizzle
  feels cheap while every individual shot looks fine.
- **Say where it plays, before boarding.** A keynote opener is loud in a
  dark room to a captive audience; a booth loop is silent, repeating, and
  half-watched from six feet away. They are not the same piece — the booth
  version needs its text to carry everything and its loop point to be
  invisible.
- **Accessibility needs a decision, not a default.** A wall-to-wall
  montage with no narration gives **Blair Blind** almost nothing, and
  that's inherent to the format rather than a fixable defect. Two honest
  options: commission an audio-described version, or accept that this
  piece is not accessible and never make it load-bearing — no information
  lives only here. Captions still cover **Dev Deaf** for the text and any
  VO, and **Cora Cognitive** should be asked about the escalation, because
  fast cutting plus music is exactly the combination that overwhelms.
- **If it needs to explain something, it's the wrong format.** Build the
  longer piece and cut a sizzle from it via **Time Reduction**, which also
  solves the sourcing problem.
