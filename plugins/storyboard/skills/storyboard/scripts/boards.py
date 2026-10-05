#!/usr/bin/env python3
"""
Parse a production's boards.md into normalized frame records.

This is the shared core every service adapter builds on: one parser, so
Higgsfield, a voice service and a human vendor are all fed from the same
frozen source rather than from three hand-made spreadsheets.

Standard library only — no install step.

Usage:
    python3 boards.py path/to/boards.md              # print frames as JSON
    python3 boards.py path/to/boards.md --summary    # human-readable check
    python3 boards.py path/to/boards.md --cards      # card hygiene (exit 1 on findings)
    python3 boards.py path/to/boards.md --notes      # standing-note order + revision log
    python3 boards.py path/to/boards.md --motion     # animation timing + continuity

Import:
    from boards import load_boards
    boards = load_boards("boards.md")
    for frame in boards.frames:
        print(frame.number, frame.to_prompt(style_block="..."))
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterator

PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}")
# [PAUSE 1.5] — a deliberate silence, marked by Vera Voice, costed in runtime.
PAUSE_RE = re.compile(r"\[\s*PAUSE\s*([0-9]*\.?[0-9]+)?\s*\]", re.IGNORECASE)
FRONTMATTER_RE = re.compile(r"\A\s*(?:<!--.*?-->\s*)?---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Language that means a card is carrying history instead of current state.
#
# A frame card says what the frame IS. The moment it also says what the
# frame WAS, two things break: a downstream service reads the rejected
# version straight out of the cell, and the board starts rotting into half
# instruction and half archaeology. History belongs in the Revision log,
# unresolved doubts in Still open issues.
HISTORY_RE = re.compile(
    r"\b("
    r"was\s+(?:a|an|the|previously|originally)"
    r"|used\s+to\s+be"
    r"|previously"
    r"|originally"
    r"|formerly"
    r"|changed\s+(?:from|after|in|at|per)"
    r"|replaced\s+(?:by|with)"
    r"|revised\s+(?:after|per|in)"
    r"|updated\s+(?:after|per|in)"
    r"|shortened\s+(?:after|per|in)"
    r"|lengthened\s+(?:after|per|in)"
    r"|(?:old|previous|earlier|former)\s+(?:version|line|shot|cut|take|wording|text)"
    r"|per\s+(?:round|review|feedback|notes?)\s*\d*"
    r"|after\s+(?:the\s+)?(?:preview|premiere|round|review)"
    r"|as\s+(?:of\s+)?v\d"
    r"|in\s+v\d\s+(?:this|it|the)"
    r"|rejected"
    r"|deprecated"
    r")\b",
    re.IGNORECASE,
)

# Doubt parked on a card instead of in Still open issues.
UNRESOLVED_RE = re.compile(
    r"(\bTBD\b|\bTODO\b|\bnot\s+sure\b|\bstill\s+(?:unsure|deciding|open|unhappy)\b|\?\?)",
    re.IGNORECASE,
)

# Written on a card, these say nothing — the default is already a cut.
DEFAULT_TRANSITIONS = {"CUT", "STRAIGHT CUT", "HARD CUT", "NONE", "DEFAULT", "N/A"}

# Joins a card may name. Anything else is either a typo or a vocabulary the
# brand's motion language hasn't approved — see reference/brand-guardrails.md.
TRANSITION_VOCAB = {
    "CUT", "DISSOLVE", "MATCH CUT", "BUILD", "WHIP", "WIPE",
    "FADE TO", "FADE FROM", "FADE IN", "FADE OUT", "HOLD",
}

# A Trans cell: TYPE DURATION — detail.
#   "DISSOLVE 0.5s — through black, audio crossfades under"
#   "MATCH CUT 0s — the alert badge becomes the checkmark, same position"
# Split on a spaced dash so a hyphenated type survives, then peel the
# duration off the end of the head.
TRANS_SPLIT_RE = re.compile(r"\s+[—–]\s*|\s+-\s+|\s*:\s+")
TRANS_DUR_RE = re.compile(
    r"(?P<num>[0-9]*\.?[0-9]+)\s*(?P<unit>s|sec|secs|second|seconds|f|fr|frame|frames)?\s*$",
    re.IGNORECASE,
)
FRAMES_PER_SECOND = 25.0  # only for a duration written in frames


def parse_transition(cell: str) -> tuple[str, float | None, str, str]:
    """
    Split a Trans cell into (type, seconds, duration_text, detail).

    seconds is None when the card names a join but never says how long it
    takes — which is the common failure, because a duration is what makes
    a join budgetable against the runtime.
    """
    text = cell.strip()
    if not text:
        return "", None, "", ""
    parts = TRANS_SPLIT_RE.split(text, 1)
    head = parts[0].strip()
    detail = parts[1].strip() if len(parts) > 1 else ""

    def peel(s: str) -> tuple[str, float | None, str]:
        m = TRANS_DUR_RE.search(s)
        if not m:
            return s.strip(), None, ""
        num = float(m.group("num"))
        unit = (m.group("unit") or "s").lower()
        secs = num / FRAMES_PER_SECOND if unit.startswith(("f", "fr")) else num
        return s[: m.start()].strip(), secs, m.group(0).strip()

    head, seconds, duration_text = peel(head)
    if seconds is None and detail:
        # Tolerate "DISSOLVE — 0.5s, through black".
        lead = re.match(r"([0-9]*\.?[0-9]+\s*(?:s|sec|secs|f|frames?)?)\s*[,;]?\s*", detail)
        if lead:
            _, seconds, duration_text = peel(lead.group(1))
            detail = detail[lead.end():].strip()
    return head.upper().strip(" -—–:"), seconds, duration_text, detail.strip(" -—–:,")

# Joins between frames. In the Motion column they're in the wrong place:
# Motion is what changes INSIDE a frame, between its two transitions.
JOIN_RE = re.compile(
    r"\b(dissolv\w*|cross[- ]?fade\w*|fade\s+(?:to|from|in|out)|match\s+cut|"
    r"cut\s+(?:to|from)|whip\s+pan|wipe\s+(?:to|from))\b",
    re.IGNORECASE,
)

# Camera moves that already live in the Shot code. Restating one in Motion
# is duplication, and duplicated facts drift apart.
CAMERA_MOVES = ("push in", "pull out", "pan", "tilt", "track", "handheld", "static")

# A frame that holds this long with nothing moving reads as an unfinished
# board rather than a held beat — unless it says `STILL — <reason>`.
STILL_SECONDS = 5.0

# Motion codes that animate an element and therefore must be timed — an
# untimed build is an instruction nobody can price or synchronize. CAMERA,
# ACTION and LOOP are looser: a camera move can be carried by the shot
# code, an action by the performance, a loop by being ambient.
TIMED_MOTION_CODES = ("BUILD", "COUNT", "REVEAL", "WIPE", "SCROLL", "HIGHLIGHT", "CURSOR")

# How long the motion inside a frame takes: "over 1.2s", "1.5s", "0.3s apart".
# "apart" is a per-step interval, not a total, so it is read separately.
MOTION_DUR_RE = re.compile(
    r"(?:over\s+|in\s+|across\s+)?([0-9]*\.?[0-9]+)\s*(s|sec|secs|seconds)\b(?!\s*apart)",
    re.IGNORECASE,
)
# An explicit start → end state, which is what makes continuity checkable.
MOTION_ARROW_RE = re.compile(r"(.{1,40}?)\s*(?:→|->|—>)\s*(.{1,40})")

# Wording that describes a frame caught PART-WAY through a move rather than
# at a state. A frame is a state, not a sample of an animation: every frame
# boundary is a hold, so slicing one continuous move across three cards
# asserts two holds inside it.
PARTIAL_STATE_RE = re.compile(
    r"\b("
    r"half[- ]?way|half[- ]?slid|half[- ]?open|half[- ]?built"
    r"|mid[- ](?:slide|move|build|animation|transition|reveal|wipe|scroll|push|turn)"
    r"|partially|part[- ]way|in\s+progress|mid[- ]?way"
    r"|(?:begins?|beginning|starts?|starting)\s+to\s+\w+"
    r"|continues?\s+(?:to\s+\w+|sliding|building|moving|rising|falling)"
    r"|still\s+(?:sliding|building|moving|animating|rising|falling|travelling|traveling)"
    r"|(?:slide|move|build|reveal|wipe|scroll)\s+(?:is\s+)?(?:under\s?way|incomplete|unfinished)"
    r")\b",
    re.IGNORECASE,
)

_STOPWORDS = {
    "a", "an", "the", "of", "in", "on", "at", "to", "and", "or", "with", "from",
    "as", "is", "are", "its", "it", "his", "her", "their", "this", "that",
}


def _fmt_time(seconds: float) -> str:
    """Seconds as m:ss, matching how Dur and Running are written."""
    m, sec = divmod(round(seconds, 2), 60)
    return f"{int(m)}:{sec:04.1f}".replace(".0", "") if sec % 1 else f"{int(m)}:{int(sec):02d}"


def _content_words(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 2}


def _similarity(a: str, b: str) -> float:
    """Jaccard overlap of content words — cheap near-duplicate detection."""
    wa, wb = _content_words(a), _content_words(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


# A frame this short, holding on a near-identical picture with nothing said,
# is almost always a sample of a move rather than a beat of its own.
SAMPLE_FRAME_SECONDS = 2.0
SAMPLE_SIMILARITY = 0.5

# Several objects moving in sync — the most expensive thing to build and the
# first thing to break when the duration changes. Not a defect; a prompt to
# consider a cheaper move that reads the same.
_MOVE_VERBS = (
    r"move|slide|fade|rotate|animate|assemble|appear|enter|exit|spin|drift|"
    r"travel|scale|grow|shrink|rise|fall"
)
SYNC_MOTION_RE = re.compile(
    r"\b("
    r"while|simultaneously|at\s+the\s+same\s+time|in\s+sync|synchroni[sz]ed"
    r"|together"
    rf"|(?:all|each|both|every)\s+(?:of\s+)?(?:the\s+)?(?:\w+\s+){{0,2}}(?:{_MOVE_VERBS})\w*"
    r"|as\s+.{0,25}\b(?:also|meanwhile|at\s+once)\b"
    r"|converge|orbit\w*|choreograph\w*|parallax|in\s+unison|in\s+lockstep"
    r")\b",
    re.IGNORECASE,
)

# Syncing motion to the narration, the music or a beat is normal and cheap —
# it's one clock, not several objects agreeing with each other.
AUDIO_SYNC_RE = re.compile(
    r"\b(vo|voice[- ]?over|narration|narrator|line|lyric|music|track|beat|"
    r"downbeat|word|says?|names?|speaks?)\b",
    re.IGNORECASE,
)

# Status values that mean "safe to hand to a downstream service".
FROZEN_STATUSES = {"approved", "animatic-locked"}

# Voiceover pace, words per minute — DEFAULTS ONLY.
#
# Pace is a decision, not a constant: a social short is deliberately faster
# than an explainer, and a piece for non-native speakers is deliberately
# slower. The project format proposes a default, Dana Director sets it for
# the piece, and it's recorded as `pace_target_wpm` / `pace_max_wpm` in the
# boards frontmatter. These values apply only when nothing says otherwise.
WPM_COMFORTABLE = 150
WPM_TIGHT = 170


class BoardsError(Exception):
    """Raised when boards.md can't be parsed or isn't safe to deliver."""


@dataclass
class Transition:
    """A row of the Transitions table — what happens between two frames."""
    frm: str
    to: str = ""
    kind: str = ""
    duration: str = ""
    why: str = ""
    cost: str = ""

    @property
    def seconds(self) -> float:
        raw = self.duration.strip().rstrip("s")
        try:
            return float(raw) if raw else 0.0
        except ValueError:
            return 0.0

    @property
    def has_reason(self) -> bool:
        w = self.why.strip()
        return bool(w) and w not in ("—", "-") and not PLACEHOLDER_RE.search(w)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["seconds"] = self.seconds
        return d


@dataclass
class BeatDirection:
    """A row of the Beat direction table — the emotional arc and pace map."""
    beat: str
    frames: str = ""
    emotion: str = ""
    pace: str = ""
    delivery: str = ""

    @property
    def pace_wpm(self) -> float | None:
        m = re.search(r"[0-9]+(?:\.[0-9]+)?", self.pace)
        return float(m.group()) if m else None

    @property
    def has_emotion(self) -> bool:
        e = self.emotion.strip()
        return bool(e) and e not in ("—", "-") and not PLACEHOLDER_RE.search(e)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["pace_wpm"] = self.pace_wpm
        return d


@dataclass
class Protection:
    """A row of Protected cuts — a frame that must not change, and why."""
    frames: str
    by: str = ""
    why: str = ""
    expires: str = ""

    @property
    def frame_numbers(self) -> list[str]:
        """Expand '4–6, 12' into individual frame numbers where possible."""
        out: list[str] = []
        for chunk in re.split(r"[,;]", self.frames):
            chunk = chunk.strip().replace("–", "-").replace("—", "-")
            if not chunk:
                continue
            if re.fullmatch(r"\d+\s*-\s*\d+", chunk):
                lo, hi = (int(p) for p in chunk.split("-", 1))
                out.extend(str(n) for n in range(lo, hi + 1))
            else:
                out.append(chunk)
        return out

    @property
    def is_real(self) -> bool:
        """A protection with no owner or no reason protects nothing."""
        for value in (self.by, self.why):
            v = value.strip()
            if not v or v in ("—", "-") or PLACEHOLDER_RE.search(v):
                return False
        return True

    def to_dict(self) -> dict:
        d = asdict(self)
        d.update(frame_numbers=self.frame_numbers, real=self.is_real)
        return d


@dataclass
class Revision:
    """A row of the Revision log — newest first, always."""
    version: str
    date: str = ""
    frames: str = ""
    changed: str = ""
    driven_by: str = ""

    @property
    def version_number(self) -> float | None:
        m = re.search(r"[0-9]+(?:\.[0-9]+)?", self.version)
        return float(m.group()) if m else None

    @property
    def iso_date(self) -> str:
        m = re.search(r"\d{4}-\d{2}-\d{2}", self.date)
        return m.group() if m else ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["version_number"] = self.version_number
        return d


@dataclass
class ScreenText:
    """A row of the On-screen text table — the reading budget for one frame."""
    frame: str
    text: str = ""
    words: str = ""
    hold: str = ""
    readable: str = ""
    intent: str = ""

    @property
    def is_readable(self) -> bool:
        return self.readable.strip().lower().startswith(("y", "ok", "true"))

    @property
    def is_pause_and_read(self) -> bool:
        return "pause-and-read" in self.intent.lower() or "pause and read" in self.intent.lower()

    def to_dict(self) -> dict:
        d = asdict(self)
        d.update(readable_at_playback=self.is_readable, pause_and_read=self.is_pause_and_read)
        return d


@dataclass
class Voice:
    """A row of the Cast & voices table — one speaker, defined once."""
    speaker: str
    who: str = ""
    voice: str = ""
    source: str = ""
    consent: str = ""
    frames: str = ""

    @property
    def is_synthetic(self) -> bool:
        return "synth" in self.source.lower() or "voice id" in self.source.lower()

    @property
    def needs_consent(self) -> bool:
        """A real, identifiable person needs a release; a house narrator doesn't."""
        return "real" in self.source.lower() or "interview" in self.source.lower()

    @property
    def voice_id(self) -> str:
        """
        The service-side voice identifier from the Source column, if present.

        Written as "Synthetic — ElevenLabs voice ID abc123" or
        "voice_id: abc123". Returns "" for a real recording, which has no
        synthetic voice to map to.
        """
        m = re.search(r"voice[ _-]?id[:\s]+([A-Za-z0-9_-]{6,})", self.source, re.IGNORECASE)
        return m.group(1) if m else ""

    @property
    def cleared(self) -> bool:
        c = self.consent.strip().lower()
        if not self.needs_consent:
            return True
        return bool(c) and c not in ("n/a", "—", "-", "tbd", "pending")

    def to_dict(self) -> dict:
        d = asdict(self)
        d.update(synthetic=self.is_synthetic, cleared=self.cleared)
        return d


@dataclass
class Frame:
    """
    One frame card: the current state of one frame, and nothing else.

    The shape is defined once, in `templates/production/frame-card.md`,
    and mirrored here — in the same order, which opens with the line
    (`speaker`, `vo`), then the picture it plays over (`visual`), and
    closes with the join that leaves the frame (`trans`).

    `motion`, `text`, `trans` and `note` are difference-only fields —
    blank is the normal, correct value. Blank `motion` means nothing
    moves; blank `trans` means the frame leaves on a straight cut; blank
    `note` means nothing changes here. Boards written before these columns
    existed simply parse them as "".

    `trans` is the join **out** of this frame — the one that overlaps its
    own tail and comes out of its own duration. The join *into* a frame is
    the previous card's `trans`.
    """
    number: str
    speaker: str = ""
    vo: str = ""
    visual: str = ""
    beat: str = ""
    shot: str = ""
    motion: str = ""
    text: str = ""
    audio: str = ""
    note: str = ""
    duration: str = ""
    running: str = ""
    trans: str = ""

    # --- card hygiene -----------------------------------------------------

    def _filled(self, value: str) -> str:
        v = value.strip()
        return "" if v in ("—", "-", "n/a", "N/A") or PLACEHOLDER_RE.search(v) else v

    @property
    def screen_text(self) -> str:
        """Verbatim on-screen text, or '' when the frame carries none."""
        return self._filled(self.text)

    @property
    def card_note(self) -> str:
        return self._filled(self.note)

    @property
    def card_motion(self) -> str:
        """What changes during this frame. '' means nothing does."""
        return self._filled(self.motion)

    @property
    def is_still(self) -> bool:
        """Nothing moves for this frame's whole duration."""
        m = self.card_motion.upper()
        return not m or m.startswith(("STILL", "HOLD"))

    @property
    def stillness_explained(self) -> bool:
        """`STILL — <reason>` marks a deliberate hold; blank doesn't."""
        m = self.card_motion
        if not m.upper().startswith(("STILL", "HOLD")):
            return False
        reason = m[5:].lstrip(" —-:").strip()
        return bool(reason) and not PLACEHOLDER_RE.search(reason)

    @property
    def motion_phrase(self) -> str:
        """
        The Motion cell as plain language, for a prompt.

        Strips the leading vocabulary code (`BUILD — `, `ACTION — `), which
        is scanning shorthand for the crew and noise to a model, and keeps
        the description. A deliberate hold becomes an explicit statement of
        stillness rather than nothing, because a video model told nothing
        about movement invents some.
        """
        m = self.card_motion
        if not m:
            return ""
        if m.upper().startswith(("STILL", "HOLD")):
            return "static shot, no camera or subject movement"
        head, sep, tail = m.partition("—")
        if sep and head.strip().isupper() and tail.strip():
            return tail.strip()
        return m

    @property
    def motion_code(self) -> str:
        """The leading vocabulary code, if the cell uses one."""
        m = re.match(r"([A-Z][A-Z /]*[A-Z])\b", self.card_motion.strip())
        return m.group(1).strip() if m else ""

    @property
    def motion_seconds(self) -> float | None:
        """How long the motion inside the frame takes. None when unstated."""
        m = MOTION_DUR_RE.search(self.card_motion)
        return float(m.group(1)) if m else None

    @property
    def motion_needs_timing(self) -> bool:
        """An animated element has to be timed; a camera move or an action needn't be."""
        code = self.motion_code
        return bool(code) and code.startswith(TIMED_MOTION_CODES)

    @property
    def motion_endpoints(self) -> tuple[str, str]:
        """
        The start and end state, when the cell writes them as `A → B`.

        Explicit endpoints are what make continuity checkable at all:
        `COUNT — 0 → 1,284 over 1.5s` says where the next frame has to
        begin. Without them, Molly Motion is reading intent.
        """
        m = MOTION_ARROW_RE.search(self.card_motion)
        return (m.group(1).strip(), m.group(2).strip()) if m else ("", "")

    @property
    def motion_changes_state(self) -> bool:
        """Motion that leaves the frame in a different state than it started."""
        code = self.motion_code
        return bool(code) and code.startswith(("BUILD", "COUNT", "REVEAL", "WIPE", "SCROLL"))

    @property
    def motion_slack(self) -> float | None:
        """
        Seconds left in the frame after the motion and the join out of it.

        Negative means the animation is still running when the frame ends
        or when the dissolve starts, so the viewer never sees the finished
        state. `motion + join out <= Dur`.
        """
        total = self.duration_seconds
        if total is None or self.motion_seconds is None:
            return None
        return total - self.motion_seconds - (self.transition_out_seconds or 0.0)

    @property
    def motion_is_join(self) -> str:
        """A transition written into Motion — it belongs in Trans."""
        m = JOIN_RE.search(self.card_motion)
        return m.group(0) if m else ""

    @property
    def motion_repeats_shot(self) -> str:
        """
        A camera move restated from the Shot code and adding nothing.

        `CU PUSH IN` + `CAMERA — push completes by 0:04, then holds` is
        right: the Shot says what the move is, the Motion says when it
        lands. `CU PUSH IN` + `push in` is the same fact in two cells,
        which is how two cells come to disagree. Timing in the Motion
        cell — any number — is what distinguishes the two.
        """
        shot = self.shot.lower()
        motion = self.card_motion.lower()
        if re.search(r"\d", motion):
            return ""
        for move in CAMERA_MOVES:
            if move in shot and move in motion:
                return move
        return ""

    @property
    def transition_out(self) -> str:
        """The whole Trans out cell as written. '' means a plain cut."""
        return self._filled(self.trans)

    @property
    def _transition(self) -> tuple[str, float | None, str, str]:
        return parse_transition(self.transition_out)

    @property
    def transition_out_type(self) -> str:
        """`DISSOLVE`, `MATCH CUT`, `FADE TO` — the kind of join out, normalized."""
        return self._transition[0]

    @property
    def transition_out_seconds(self) -> float | None:
        """How long the join takes. None when the card never says."""
        return self._transition[1]

    @property
    def transition_out_duration_text(self) -> str:
        return self._transition[2]

    @property
    def transition_out_detail(self) -> str:
        """Everything after the dash — direction, what matches, audio handling."""
        return self._transition[3]

    @property
    def transition_out_known(self) -> bool:
        t = self.transition_out_type
        if not t:
            return True
        return t in TRANSITION_VOCAB or any(t.startswith(v) for v in TRANSITION_VOCAB)

    @property
    def redundant_transition_out(self) -> bool:
        """`CUT` spelled out on a card — the default, so it documents nothing."""
        return self.transition_out_type in DEFAULT_TRANSITIONS

    @property
    def has_transition_out(self) -> bool:
        return bool(self.transition_out_type) and not self.redundant_transition_out

    @property
    def transition_out_summary(self) -> str:
        """One-line description of the join out, for a report or an edit spec."""
        if not self.has_transition_out:
            return ""
        bits = [self.transition_out_type]
        if self.transition_out_seconds is not None:
            bits.append(f"{self.transition_out_seconds:g}s")
        head = " ".join(bits)
        return f"{head} — {self.transition_out_detail}" if self.transition_out_detail else head

    @property
    def card_cells(self) -> dict[str, str]:
        """The cells a card owns, for hygiene checks."""
        return {
            "Visual": self.visual, "Motion": self.motion, "Text": self.text,
            "VO": self.vo, "Audio": self.audio, "Trans": self.trans,
            "Note": self.note,
        }

    @property
    def history_on_card(self) -> list[tuple[str, str]]:
        """(column, phrase) for every bit of history written onto the card."""
        found: list[tuple[str, str]] = []
        for col, value in self.card_cells.items():
            for m in HISTORY_RE.finditer(value):
                found.append((col, m.group(0)))
        return found

    @property
    def unresolved_on_card(self) -> list[tuple[str, str]]:
        """(column, phrase) for doubts parked on the card instead of Still open issues."""
        found: list[tuple[str, str]] = []
        for col, value in self.card_cells.items():
            for m in UNRESOLVED_RE.finditer(value):
                found.append((col, m.group(0)))
        return found

    @property
    def has_line(self) -> bool:
        line = self.vo.strip()
        return bool(line) and line not in ("—", "-")

    @property
    def speaker_label(self) -> str:
        s = self.speaker.strip()
        return "" if s in ("—", "-") else s

    @property
    def is_cut(self) -> bool:
        """Frames marked CUT keep their row and number but aren't delivered."""
        return "CUT" in (self.visual.upper(), self.shot.upper()) or self.visual.strip().upper().startswith("CUT")

    @property
    def is_placeholder(self) -> bool:
        """An unfilled template row, e.g. {{What is literally in frame}}."""
        joined = " ".join([self.beat, self.shot, self.visual, self.vo])
        return bool(PLACEHOLDER_RE.search(joined)) or not self.visual.strip()

    @property
    def orphan_line(self) -> bool:
        """A line with nobody attributed to it — uncastable, unmixable, uncaptionable."""
        return self.has_line and not self.speaker_label

    @property
    def pauses(self) -> list[float | None]:
        """Durations of every [PAUSE n] in the line. None = marked without a number."""
        return [float(m.group(1)) if m.group(1) else None for m in PAUSE_RE.finditer(self.vo)]

    @property
    def pause_seconds(self) -> float:
        return sum(p for p in self.pauses if p is not None)

    @property
    def unnumbered_pause(self) -> bool:
        """`[PAUSE]` with no duration is a note, not a spec — it'll be improvised."""
        return any(p is None for p in self.pauses)

    @property
    def has_audio(self) -> bool:
        """Any sound at all — music, effects, room tone. A SILENT marker is not audio."""
        a = self.audio.strip()
        if a.upper().startswith("SILENT"):
            return False
        return bool(a) and a not in ("—", "-")

    @property
    def is_silent(self) -> bool:
        """No voiceover and no audio — the viewer receives nothing but picture."""
        return not self.has_line and not self.has_audio

    @property
    def silence_explained(self) -> bool:
        """`SILENT — <reason>` marks deliberate silence; a bare dash doesn't."""
        a = self.audio.strip()
        if not a.upper().startswith("SILENT"):
            return False
        reason = a[6:].lstrip(" —-:").strip()
        return bool(reason) and not PLACEHOLDER_RE.search(reason)

    @property
    def emphasis(self) -> list[str]:
        """Words marked for stress with *asterisks*."""
        return [m.group(1).strip() for m in re.finditer(r"\*([^*]+)\*", self.vo)]

    @property
    def word_count(self) -> int:
        """Spoken words, excluding pause markers and bare punctuation."""
        text = PAUSE_RE.sub(" ", self.vo)
        words = [w for w in re.split(r"\s+", text) if re.search(r"[A-Za-z0-9]", w)]
        return len(words)

    @property
    def duration_seconds(self) -> float | None:
        """Parse the Dur column: '0:06', '6', '1:02.5' -> seconds."""
        raw = self.duration.strip()
        if not raw or raw in ("—", "-"):
            return None
        try:
            if ":" in raw:
                mins, _, secs = raw.partition(":")
                return int(mins) * 60 + float(secs)
            return float(raw)
        except ValueError:
            return None

    @property
    def running_seconds(self) -> float | None:
        """Parse the Running column the same way as Dur."""
        raw = self.running.strip()
        if not raw or raw in ("—", "-"):
            return None
        try:
            if ":" in raw:
                mins, _, secs = raw.partition(":")
                return int(mins) * 60 + float(secs)
            return float(raw)
        except ValueError:
            return None

    @property
    def speaking_seconds(self) -> float | None:
        """Frame duration minus marked silence — the time actually available for words."""
        total = self.duration_seconds
        if total is None:
            return None
        return max(total - self.pause_seconds, 0.0)

    @property
    def wpm(self) -> float | None:
        """Required words-per-minute for this frame's line to fit its duration."""
        speaking = self.speaking_seconds
        if not speaking or not self.word_count:
            return None
        return self.word_count / (speaking / 60.0)

    def pace_verdict(self, target: float = WPM_COMFORTABLE, ceiling: float = WPM_TIGHT) -> str:
        """'ok' | 'tight' | 'too dense' | 'unknown', against this piece's pace."""
        rate = self.wpm
        if rate is None:
            return "unknown"
        if rate > ceiling:
            return "too dense"
        if rate > target:
            return "tight"
        return "ok"

    def fixes(self, target: float = WPM_COMFORTABLE) -> dict:
        """
        The two real options when a line is too dense, quantified.

        Either the words come down or the time goes up. Reporting only the
        first is what makes "cut it" feel like the only choice — when the
        runtime is flexible, stretching the beat keeps the whole message at
        a pace people can actually follow.
        """
        speaking = self.speaking_seconds
        if not speaking or not self.word_count:
            return {}
        words_that_fit = target * speaking / 60.0
        seconds_needed = self.word_count / (target / 60.0)
        return {
            "cut_words": max(0, round(self.word_count - words_that_fit)),
            "stretch_to_seconds": round(seconds_needed + self.pause_seconds, 1),
            "extend_by_seconds": round(seconds_needed - speaking, 1),
        }

    def spoken_text(self, pause_format: str | None = None) -> str:
        """
        The line with pause markers removed, or rewritten for a voice service.

        Voice APIs each express silence differently — SSML uses
        `<break time="1.5s"/>`, others take a plain marker or nothing at
        all. Pass a format string containing {seconds} to translate;
        pass None to strip the markers entirely.
        """
        def repl(m: re.Match) -> str:
            if pause_format is None:
                return " "
            secs = m.group(1) or "0.5"
            return pause_format.format(seconds=secs)

        return re.sub(r"\s{2,}", " ", PAUSE_RE.sub(repl, self.vo)).strip()

    @property
    def deliverable(self) -> bool:
        return not self.is_cut and not self.is_placeholder

    def to_prompt(self, style_block: str = "", include_shot: bool = True,
                  include_motion: bool = True) -> str:
        """
        Build a single visual-generation prompt for this frame.

        The shot code is included by default because most image and video
        models respond to framing language ("wide shot", "close-up"), and
        the style block is appended last so brand rules are the final
        instruction the model reads.

        The card's **motion** is included, because a video model asked for
        a scene with no movement described will invent some. Omit it with
        `include_motion=False` when the target is a still-image model.

        The card's on-screen **text** is deliberately left out: generative
        models render lettering badly and inconsistently, and this text is
        usually brand-typeset and composited in the edit. It travels in
        the manifest (`to_dict`) so whoever composites has the verbatim
        wording, rather than being paraphrased by a model.
        """
        parts: list[str] = []
        if include_shot and self.shot.strip():
            parts.append(expand_shot(self.shot))
        if self.visual.strip():
            parts.append(self.visual.strip().rstrip("."))
        if include_motion and self.motion_phrase:
            parts.append(self.motion_phrase.rstrip("."))
        prompt = ". ".join(p for p in parts if p)
        if style_block.strip():
            prompt = f"{prompt}. {style_block.strip()}"
        return prompt

    def render_card(self, width: int = 65) -> str:
        """
        Draw this frame in the canonical card layout.

        The layout rule, from templates/production/frame-card.md: a
        labeled section spans the full card width or shares a row with
        exactly ONE other section. Never three. A third column is a third
        as wide, and a third of the width turns one line of transition
        detail into six — a card with two or three of those is twice as
        tall for no added information.

        Bounded values — number, speaker, beat, shot code, timecodes —
        ride in the header strip. Anything that can be a sentence gets
        full width, and the line comes before the picture it plays over.
        Text and Audio pair by default and break out to full width when
        either of them runs long.
        """
        inner = max(width - 4, 30)
        out: list[str] = [f"┌─{'─' * inner}─┐"]

        def full(label: str, value: str) -> None:
            out.append(f"│ {label.upper():<{inner}} │")
            body = value.strip() or "—"
            for line in textwrap.wrap(body, inner) or ["—"]:
                out.append(f"│ {line:<{inner}} │")

        def rule(kind: str = "plain") -> None:
            if kind == "split":
                left = (inner + 2) // 2 - 1
                out.append(f"├{'─' * left}┬{'─' * (inner + 2 - left - 1)}┤")
            elif kind == "join":
                left = (inner + 2) // 2 - 1
                out.append(f"├{'─' * left}┴{'─' * (inner + 2 - left - 1)}┤")
            else:
                out.append(f"├─{'─' * inner}─┤")

        # Header strip — every bounded value on one line, speaker included:
        # who is talking is a one-word fact, like the beat and the shot code.
        bits = [f"FRAME {self.number}"]
        if self.speaker_label:
            bits.append(self.speaker_label)
        if self.beat.strip():
            bits.append(f"Beat: {self.beat.strip()}")
        if self.shot.strip():
            bits.append(f"Shot: {self.shot.strip()}")
        if self.duration.strip():
            span = self.duration.strip()
            if self.running.strip():
                span += f" → {self.running.strip()}"
            bits.append(span)
        header = "   ".join(bits)
        out.append(f"│ {header[:inner]:<{inner}} │")

        rule()
        full("VO / Dialogue", self.vo)
        rule()
        full("Visual", self.visual)
        if self.card_motion:
            rule()
            full("Motion", self.motion)

        # Text + Audio pair, unless either would be cramped by half a card.
        half = (inner - 3) // 2
        text_v, audio_v = (self.text.strip() or "—"), (self.audio.strip() or "—")
        if max(len(text_v), len(audio_v)) > half:
            rule()
            full("Text", self.text)
            rule()
            full("Audio", self.audio)
        else:
            rule("split")
            lw = (inner + 2) // 2 - 2
            rw = inner - lw - 1
            out.append(f"│ {'TEXT':<{lw}}│ {'AUDIO':<{rw}}│")
            out.append(f"│ {text_v:<{lw}}│ {audio_v:<{rw}}│")
            rule("join")

        if self.card_note:
            if not out[-1].startswith("├"):
                rule()
            full("Note", self.note)
        if self.transition_out:
            if not out[-1].startswith("├"):
                rule()
            full("Trans out", self.transition_out)

        out.append(f"└─{'─' * inner}─┘")
        return "\n".join(out)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["deliverable"] = self.deliverable
        return d


@dataclass
class Boards:
    meta: dict = field(default_factory=dict)
    frames: list[Frame] = field(default_factory=list)
    cast: list[Voice] = field(default_factory=list)
    beats: list[BeatDirection] = field(default_factory=list)
    transitions: list[Transition] = field(default_factory=list)
    screen_text: list[ScreenText] = field(default_factory=list)
    protections: list[Protection] = field(default_factory=list)
    revisions: list[Revision] = field(default_factory=list)
    frame_header: list[str] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)
    source: str = ""

    def audit_notes(self) -> list[str]:
        """
        The standing notes: fixed order, revision log last and newest-first,
        and protections that actually protect something.

        Order is not decoration. A reader opens this file with one of two
        questions — "what do I do now" or "what changed since I looked" —
        and the first ten sections answer the first. A revision log that
        grows downward pushes every other note further from the top of the
        file until nobody reads them; growing upward inside the last
        section leaves the board where people left it.
        """
        problems: list[str] = []
        present = [s for s in self.sections if s.lower() in STANDING_NOTES]
        if present:
            rank = {name: i for i, name in enumerate(STANDING_NOTES)}
            seen = [rank[s.lower()] for s in present]
            if seen != sorted(seen):
                expected = " → ".join(n.title() for n in STANDING_NOTES)
                problems.append(
                    "standing notes are out of order — the fixed order is: " + expected
                )
            last = present[-1].lower()
            if "revision log" in [s.lower() for s in present] and last != "revision log":
                problems.append(
                    f"the Revision log is not the last section ({present[-1]!r} follows it) — "
                    "history is the one part of the board nobody needs in order to build the piece"
                )

        # Newest first: v3 above v2 above v1.
        versions = [(r, r.version_number) for r in self.revisions if r.version_number is not None]
        numbers = [n for _, n in versions]
        if len(numbers) > 1 and numbers != sorted(numbers, reverse=True):
            if numbers == sorted(numbers):
                problems.append(
                    f"Revision log runs oldest-first (v{numbers[0]:g} at the top) — "
                    "reverse it; the newest version is the top row"
                )
            else:
                problems.append(
                    "Revision log versions are not in descending order: "
                    + ", ".join(f"v{n:g}" for n in numbers)
                )
        dates = [r.iso_date for r in self.revisions if r.iso_date]
        if len(dates) > 1 and dates != sorted(dates, reverse=True):
            problems.append(
                f"Revision log dates are not newest-first ({dates[0]} at the top, "
                f"{max(dates)} is later)"
            )

        numbers_on_board = {f.number for f in self.frames}
        for p in self.protections:
            if PLACEHOLDER_RE.search(p.frames) or not p.frames.strip():
                continue
            if not p.is_real:
                problems.append(
                    f"protected cut {p.frames!r}: no owner or no reason given — "
                    '"important" is not a protection; name who protected it and what it buys'
                )
            for num in p.frame_numbers:
                if num not in numbers_on_board:
                    problems.append(f"protected cut {p.frames!r}: frame {num} isn't on the board")
                    continue
                frame = next(f for f in self.frames if f.number == num)
                if frame.is_cut:
                    problems.append(
                        f"frame {num} is marked CUT but is protected by "
                        f"{p.by.strip() or 'nobody named'} — go back to them before losing it"
                    )
        return problems

    def audit_shape(self) -> list[str]:
        """
        Whether the Frames table matches the card template.

        Every card in every production is the same shape, defined once in
        `templates/production/frame-card.md`. A board missing a column
        isn't merely unfashionable — nobody has said what moves in frame 4,
        or what the join into frame 9 is, and the gap gets filled by
        whoever builds it. A board with the columns in a different order
        still parses (the parser matches on header names, not position)
        but stops being scannable next to every other board.
        """
        problems: list[str] = []
        if not self.frame_header:
            return problems
        lowered = [h.strip().lower() for h in self.frame_header]
        positions: list[int] = []
        for label, keys in CANONICAL_CARD_COLUMNS:
            idx = next((i for i, h in enumerate(lowered) if any(k in h for k in keys)), None)
            if idx is None:
                problems.append(
                    f"Frames table has no {label!r} column — the card template "
                    "(templates/production/frame-card.md) defines it; add it to the header"
                )
            else:
                positions.append(idx)
        if positions != sorted(positions):
            problems.append(
                "Frames table columns are out of template order — it parses, but every "
                "other board reads left to right as "
                + " | ".join(label for label, _ in CANONICAL_CARD_COLUMNS)
            )
        return problems

    def transition_out_of(self, number: str) -> Transition | None:
        """The Transitions row for the join that leaves this frame."""
        for tr in self.transitions:
            if tr.frm.strip() == number.strip():
                return tr
        return None

    def screen_text_for(self, number: str) -> ScreenText | None:
        for st in self.screen_text:
            if st.frame.strip() == number.strip():
                return st
        return None

    def audit_cards(self) -> list[str]:
        """
        Card hygiene: current state only, differences only, and no fact
        living in two places where the copies can drift apart.

        Every one of these is a real failure mode of a board that has been
        through three rounds of notes — not a style preference. A card that
        carries its own history gets handed to a vendor or a generation
        service with the rejected version still in the cell.
        """
        problems: list[str] = self.audit_shape()
        seen_speakers: set[str] = set()
        first_speaking = True

        for f in self.deliverable_frames():
            for col, phrase in f.history_on_card:
                problems.append(
                    f"frame {f.number}: {col} carries history ({phrase!r}) — "
                    "a card holds current state only; move it to the Revision log"
                )
            for col, phrase in f.unresolved_on_card:
                problems.append(
                    f"frame {f.number}: {col} parks an open question ({phrase!r}) — "
                    "move it to Still open issues and leave the cell as what the frame is now"
                )

            if f.redundant_transition_out:
                problems.append(
                    f"frame {f.number}: Trans out says {f.trans.strip()!r}, which is the default — "
                    "leave it blank so the joins that are decisions stand out"
                )
            elif f.has_transition_out:
                if f.transition_out_seconds is None:
                    problems.append(
                        f"frame {f.number}: Trans out says {f.transition_out_type} with no duration — "
                        "write `TYPE 0.5s — detail`; a join without a length can't be budgeted "
                        "against the runtime or handed to an editor"
                    )
                if not f.transition_out_known:
                    problems.append(
                        f"frame {f.number}: {f.transition_out_type!r} isn't in the transition "
                        "vocabulary — use one of "
                        + ", ".join(sorted(TRANSITION_VOCAB))
                        + ", or add it to the brand's approved motion language first"
                    )
                if not f.transition_out_detail and f.transition_out_type not in ("CUT", "HOLD"):
                    problems.append(
                        f"frame {f.number}: {f.transition_out_type} has no detail — say what it does "
                        "(direction, what matches across it, what the audio does), or an editor "
                        "will decide for you"
                    )
                row = self.transition_out_of(f.number)
                if self.transitions and not row:
                    problems.append(
                        f"frame {f.number}: Trans out says {f.transition_out_type} but no Transitions row "
                        f"leaves frame {f.number} — the join has no reason or cost behind it"
                    )
                elif (row and row.seconds and f.transition_out_seconds is not None
                        and abs(row.seconds - f.transition_out_seconds) > 0.01):
                    problems.append(
                        f"frame {f.number}: the card says the join runs {f.transition_out_seconds:g}s "
                        f"and the Transitions table says {row.seconds:g}s — one of them is stale"
                    )
                elif (row and row.kind.strip()
                        and row.kind.strip().upper() != f.transition_out_type
                        and not row.kind.strip().upper().startswith(f.transition_out_type)):
                    problems.append(
                        f"frame {f.number}: the card says {f.transition_out_type} and the Transitions "
                        f"table says {row.kind.strip().upper()} — one of them is stale"
                    )

            if f.motion_is_join:
                problems.append(
                    f"frame {f.number}: Motion says {f.motion_is_join!r}, which is a join between "
                    "frames, not a change inside one — that belongs in Trans out"
                )
            if f.motion_repeats_shot:
                problems.append(
                    f"frame {f.number}: Motion repeats the Shot code's {f.motion_repeats_shot!r} "
                    "and adds nothing — say when the move lands, or leave Motion blank"
                )
            secs = f.duration_seconds
            if (f.is_still and not f.stillness_explained
                    and secs is not None and secs > STILL_SECONDS):
                problems.append(
                    f"frame {f.number}: {secs:.0f}s with nothing moving and no reason — "
                    "say what changes, or mark it `STILL — <reason>`; a hold that long "
                    "reads as an unfinished board"
                )

            if f.screen_text and self.screen_text and not self.screen_text_for(f.number):
                problems.append(
                    f"frame {f.number}: carries on-screen text with no row in On-screen text — "
                    "nobody has checked whether it can be read in the hold time"
                )

            speaker = f.speaker_label.upper()
            if f.has_line and speaker:
                if speaker not in seen_speakers and not first_speaking and not f.card_note:
                    problems.append(
                        f"frame {f.number}: {speaker} speaks here for the first time and the card "
                        "says nothing — a new voice arriving is Note-worthy for casting, mix and captions"
                    )
                if speaker not in seen_speakers:
                    seen_speakers.add(speaker)
                    first_speaking = False

        problems.extend(self.audit_timing())
        problems.extend(self.audit_screen_text())

        # The other direction: a standing note with no card behind it.
        #
        # Only meaningful once the board actually uses the Trans column. A
        # board written before the column existed has every join in the
        # Transitions table and nothing on the cards, which is coherent —
        # flagging all of it would bury the real findings above.
        if not any(f.trans.strip() for f in self.frames):
            return problems
        numbers = {f.number for f in self.frames}
        for tr in self.transitions:
            frm = tr.frm.strip()
            if not frm or PLACEHOLDER_RE.search(frm) or frm not in numbers:
                continue
            frame = next((f for f in self.frames if f.number == frm), None)
            if frame is not None and frame.deliverable and not frame.has_transition_out:
                problems.append(
                    f"transition {tr.frm}->{tr.to}: specced here but frame {frm}'s Trans out "
                    "column is blank, which reads as a plain cut — the board contradicts itself"
                )
        return problems

    @property
    def transition_seconds(self) -> float:
        """
        Runtime spent on joins rather than content.

        Counted from the cards when they carry durations, because that's
        the per-frame truth an editor works from; the Transitions table is
        the fallback for boards written before the Trans column carried a
        length. Never both, or every join gets counted twice.
        """
        from_cards = sum(
            f.transition_out_seconds or 0.0
            for f in self.deliverable_frames()
            if f.has_transition_out
        )
        if any(f.has_transition_out and f.transition_out_seconds is not None
               for f in self.deliverable_frames()):
            return from_cards
        return sum(tr.seconds for tr in self.transitions)

    def audit_silence(self) -> list[str]:
        """
        Frames the viewer receives nothing from.

        Silence is legitimate and often good — but it has to be a decision
        somebody made, written as `SILENT — <reason>`. An unexplained
        silent frame is usually one of two things: nobody filled it in, or
        somebody is hoping the viewer pauses to look at the picture. The
        second is the same failure as expecting them to pause and read.
        """
        problems: list[str] = []
        for f in self.deliverable_frames():
            if not f.is_silent:
                continue
            secs = f.duration_seconds
            if not f.silence_explained:
                problems.append(
                    f"frame {f.number}: no VO and no audio, and no reason given — "
                    "mark it `SILENT — <reason>`, give it audio, or cut the frame"
                )
            elif secs is not None and secs > 3.0:
                problems.append(
                    f"frame {f.number}: {secs:.0f}s of deliberate silence — long enough that "
                    "Blair Blind receives nothing at all; needs audio description if it carries meaning"
                )
        return problems

    def audit_motion(self) -> list[str]:
        """
        Molly Motion's continuity check, in the part that is arithmetic.

        Whether a Motion cell matches its Visual, and whether frame 7
        starts where frame 6 ended, needs an animator's eye — his persona
        file covers that. What a script can settle is timing: an animation
        longer than its frame, an animation still running when the join
        out begins, an animated element with no duration at all, and a
        state change with no stated endpoints for the next frame to
        continue from.
        """
        problems: list[str] = []
        for f in self.deliverable_frames():
            if not f.card_motion or f.is_still:
                continue
            secs, dur = f.motion_seconds, f.duration_seconds

            if secs is None and f.motion_needs_timing:
                problems.append(
                    f"frame {f.number}: {f.motion_code} with no duration — an animated element "
                    "has to be timed (`over 1.2s`) or it can't be priced or synchronized"
                )
            elif secs is not None and dur is not None:
                join = f.transition_out_seconds or 0.0
                if secs > dur + 0.01:
                    problems.append(
                        f"frame {f.number}: {secs:g}s of motion in a {dur:g}s frame — it gets "
                        f"truncated, which reads as broken rather than deliberate; give the frame "
                        f"{secs - dur:.1f}s more or shorten the motion"
                    )
                elif join and secs + join > dur + 0.01:
                    problems.append(
                        f"frame {f.number}: {secs:g}s motion + {join:g}s join out doesn't fit a "
                        f"{dur:g}s frame — the join starts before the motion lands, so nobody sees "
                        f"the finished state; needs {secs + join - dur:.1f}s more, less motion, "
                        "or a shorter join"
                    )

            if f.motion_changes_state and not any(f.motion_endpoints):
                problems.append(
                    f"frame {f.number}: {f.motion_code} changes what's on screen but doesn't say "
                    "from what to what — write the endpoints (`40 rows → 3`) so the next frame "
                    "has a state to continue from"
                )

        problems.extend(self.audit_sampled_frames())
        return problems

    def audit_timing(self) -> list[str]:
        """
        `Running` against the accumulated `Dur`, and the total against the target.

        Running time is a derived column that nobody derives. It gets
        typed by hand, and then a frame's duration changes and every
        number below it is quietly wrong — so the board says the piece is
        2:00 while the frames add up to 2:14. Everything downstream reads
        Running as truth: the animatic, the pace check per beat, the
        editor's runtime budget, the header strip on a rendered card.

        CUT frames contribute nothing, which is the point of keeping the
        row rather than the time.
        """
        problems: list[str] = []
        frames = self.deliverable_frames()
        acc = 0.0
        for f in frames:
            secs = f.duration_seconds
            if secs is None:
                if f.running.strip() and f.running.strip() not in ("—", "-"):
                    problems.append(
                        f"frame {f.number}: has a Running time but no Dur — nothing can be "
                        "accumulated from it, and every row below inherits the gap"
                    )
                continue
            acc += secs
            stated = f.running_seconds
            if stated is None:
                continue
            if abs(stated - acc) > 0.05:
                problems.append(
                    f"frame {f.number}: Running says {_fmt_time(stated)} but the durations so far "
                    f"add up to {_fmt_time(acc)} — off by {abs(stated - acc):.1f}s. Running is "
                    "derived, so recompute it rather than patching the one row"
                )

        target = self.duration_target_seconds
        if target is not None and frames and acc:
            if abs(acc - target) > 0.5:
                over = acc - target
                word = "over" if over > 0 else "under"
                problems.append(
                    f"the frames add up to {_fmt_time(acc)} against a {_fmt_time(target)} target — "
                    f"{abs(over):.1f}s {word}"
                    + (" and the runtime is FIXED, so the time has to come out of the frames"
                       if self.duration_is_fixed else "")
                )
        return problems

    def audit_screen_text(self) -> list[str]:
        """
        On-screen text landing on the wrong frame.

        The off-by-one is the characteristic failure of this column and
        it is nearly invisible on paper. Text is usually written in a
        separate pass from the boards, the standing note is keyed by
        frame number, and frame numbers move — a frame gets inserted as
        `11a`, one gets cut, somebody drags a column down one row. On
        screen the result is unmistakable: a caption that arrives a frame
        early spoils the reveal it was meant to land after, and one that
        arrives late labels a picture that has already gone.

        At 1–2 seconds a frame, nobody catches this by reading. The card
        and the standing note have to agree, and where they don't, the
        neighbouring frames usually say which way it slipped.
        """
        problems: list[str] = []
        numbers = {f.number for f in self.frames}
        by_number = {f.number: f for f in self.frames}
        frames = self.deliverable_frames()
        order = [f.number for f in frames]

        def norm(t: str) -> str:
            return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()

        def neighbours(number: str) -> list[Frame]:
            if number not in order:
                return []
            i = order.index(number)
            return [by_number[order[j]] for j in (i - 1, i + 1) if 0 <= j < len(order)]

        for st in self.screen_text:
            num = st.frame.strip()
            if not num or PLACEHOLDER_RE.search(num):
                continue
            if num not in numbers:
                problems.append(
                    f"On-screen text row for frame {num}: no such frame on the board"
                )
                continue
            card = by_number[num]
            row_text = norm(st.text)
            card_text = norm(card.screen_text)

            if not card_text:
                hit = next((n for n in neighbours(num)
                            if row_text and norm(n.screen_text) == row_text), None)
                if hit:
                    problems.append(
                        f"On-screen text row says frame {num}, but frame {num}'s card carries no "
                        f"text and frame {hit.number}'s carries exactly this — the row is on the "
                        "wrong frame by one"
                    )
                else:
                    problems.append(
                        f"On-screen text row for frame {num}, but that card has no Text — either "
                        "the row belongs to a neighbouring frame or the text was dropped from the card"
                    )
                continue

            if row_text and card_text and row_text != card_text:
                hit = next((n for n in neighbours(num) if norm(n.screen_text) == row_text), None)
                if hit:
                    problems.append(
                        f"frame {num}: the On-screen text row's wording is frame {hit.number}'s, "
                        "not this one's — the rows have slipped by one against the cards"
                    )
                else:
                    problems.append(
                        f"frame {num}: the card's Text and its On-screen text row say different "
                        "things — one of them is stale, and until somebody looks nobody knows which"
                    )
        return problems

    def suggest_text_placement(self) -> list[str]:
        """
        Text that reads as though it belongs to the neighbouring frame.

        **Advice, not a defect** — this is a semantic guess and it can be
        wrong. A caption legitimately sets something up sometimes. But the
        pattern it catches is real and expensive: text whose words match
        the *next* frame's picture and not this one's is usually a reveal
        arriving a beat early, and matching the *previous* frame's picture
        is usually a caption outliving its shot.
        """
        out: list[str] = []
        frames = self.deliverable_frames()
        for i, f in enumerate(frames):
            text = f.screen_text
            if not text:
                continue
            own = _similarity(text, f.visual)
            if own > 0.15:
                continue  # it plainly belongs here
            for j, where, fix in ((i + 1, "next", "the reveal may be landing a beat early"),
                                  (i - 1, "previous", "the caption may be outliving its shot")):
                if not (0 <= j < len(frames)):
                    continue
                other = frames[j]
                if _similarity(text, other.visual) >= 0.34:
                    out.append(
                        f"frame {f.number}: the text {text!r} matches frame {other.number}'s "
                        f"visual ({where} frame) and not this one's — {fix}. Check it's on the "
                        "right card before anyone builds it"
                    )
                    break
        return out

    def suggest_simpler_motion(self) -> list[str]:
        """
        Frames whose motion needs several objects to agree with each other.

        **This advises; it does not fail.** Expensive choreography can be
        exactly right, and "we chose it knowing the cost" is a legitimate
        answer — which is why these come back as suggestions rather than
        problems and don't touch the exit code. Every other check in this
        file gates; this one recommends.

        The reason it's worth raising at all: synchronised multi-object
        motion is the most expensive thing on a board to build, and the
        first thing to break when anything changes. Each object needs its
        own keyframe track, and the *relationships* between them have to
        be re-derived every time the duration moves, the copy gets longer
        or the piece is reframed for another platform. One object moving
        costs a morning; four objects agreeing costs a week and breaks on
        the next revision.

        Syncing to the voiceover, the music or a beat is not this — that's
        one clock, not several objects negotiating.
        """
        out: list[str] = []
        for f in self.deliverable_frames():
            motion = f.card_motion
            if not motion:
                continue
            m = SYNC_MOTION_RE.search(motion)
            if not m or AUDIO_SYNC_RE.search(motion):
                continue
            out.append(
                f"frame {f.number}: {m.group(0)!r} — this needs several objects to stay in "
                "agreement, which is the most expensive motion to build and the first to break "
                "when the timing or the copy changes. Cheaper reads: stagger one element "
                "(`0.08s apart`) instead of moving several at once; animate the container "
                "rather than its contents; or hold everything but one thing. "
                "See workers/motion-lead.md for the substitutions"
            )
        return out

    def audit_sampled_frames(self) -> list[str]:
        """
        Frames that are a snapshot part-way through a move, not a state.

        **Every frame boundary is a hold.** A card asserts a duration, and
        a board gets read a frame at a time — in a review, in an animatic,
        by a service. So slicing one continuous movement across three
        cards asserts two holds inside it, and the move either stutters or
        the runtime inflates to cover it. Worse, the timing stops being
        arguable: nobody can tell whether the 0.3s on the middle card is a
        beat somebody chose or an accident of how it got drawn.

        A movement between two states belongs in ONE place: the `Motion`
        cell if it happens inside a frame, `Trans out` if it happens
        between two. Never as a frame of its own.
        """
        problems: list[str] = []
        frames = self.deliverable_frames()

        for f in frames:
            for col, value in (("Visual", f.visual), ("Motion", f.motion)):
                m = PARTIAL_STATE_RE.search(value)
                if m:
                    problems.append(
                        f"frame {f.number}: {col} describes a part-way state ({m.group(0)!r}) — "
                        "a frame is a state, not a sample of a move. Put the movement in one "
                        "frame's Motion (or in Trans out) and let this card show where it lands"
                    )

        for prev, cur in zip(frames, frames[1:]):
            if cur.has_line:
                continue  # a card carrying its own line is a beat, whatever it looks like
            if prev.shot.strip().upper() != cur.shot.strip().upper():
                continue  # a reframe is a real cut
            secs = cur.duration_seconds
            if secs is not None and secs > SAMPLE_FRAME_SECONDS:
                continue  # a long hold is a deliberate beat

            # Two independent tells, either is enough once the frame is
            # short, silent and framed the same: the picture barely
            # changed, or both cards run the same kind of move — which is
            # one move with a card boundary dropped into the middle of it.
            similar = _similarity(prev.visual, cur.visual) >= SAMPLE_SIMILARITY
            same_move = bool(cur.motion_code) and cur.motion_code == prev.motion_code
            if not (similar or same_move):
                continue

            why = "near-identical visual" if similar else f"both running {cur.motion_code}"
            problems.append(
                f"frames {prev.number} and {cur.number}: same shot, {why}, nothing said, "
                f"{f'{secs:g}s' if secs is not None else 'untimed'} — this reads as one move "
                f"sampled twice rather than two states. Every frame boundary is a hold, so this "
                f"stutters the move or pads the runtime. Merge them: put the movement in frame "
                f"{prev.number}'s Motion with endpoints, or in its Trans out"
            )
        return problems

    def audit_transitions(self) -> list[str]:
        """
        Transitions that would get invented in the edit, or that nobody
        chose on purpose. The default is a cut; only exceptions are listed,
        so every row here should be a decision with a reason behind it.
        """
        problems: list[str] = []
        numbers = {f.number for f in self.frames}
        for tr in self.transitions:
            label = f"{tr.frm}->{tr.to}"
            for ref, side in ((tr.frm, "from"), (tr.to, "to")):
                if ref and ref not in numbers:
                    problems.append(f"transition {label}: {side}-frame {ref!r} doesn't exist")
            if not tr.kind.strip() or PLACEHOLDER_RE.search(tr.kind):
                problems.append(f"transition {label}: no type given")
            if not tr.has_reason:
                problems.append(
                    f"transition {label}: no reason — a transition without one is decoration, "
                    "and decoration costs runtime"
                )
            if tr.kind.strip().upper() not in ("", "CUT", "MATCH CUT") and not tr.duration.strip():
                problems.append(f"transition {label}: no duration, so nobody can budget the runtime")
        return problems

    def beat_for(self, beat_name: str) -> BeatDirection | None:
        name = beat_name.strip().lower()
        if not name:
            return None
        for b in self.beats:
            if b.beat.strip().lower() == name:
                return b
        return None

    def pace_for(self, frame: Frame) -> float:
        """
        Effective target for a frame: its beat's pace if the beat sets one,
        otherwise the piece-level target.

        Pace is meant to vary across a piece — a hook runs quick, a reveal
        slows down. A single number for everything is how narration goes
        flat, so per-beat overrides are the normal case, not the exception.
        """
        b = self.beat_for(frame.beat)
        if b and b.pace_wpm:
            return b.pace_wpm
        return self.pace_target

    def audit_arc(self) -> list[str]:
        """
        Monotony checks — mechanical, because "it feels flat" is hard to
        argue with and "every beat says confident" isn't.
        """
        problems: list[str] = []
        named = [b for b in self.beats if b.beat.strip() and not PLACEHOLDER_RE.search(b.beat)]
        if not named:
            beats_in_frames = {f.beat.strip() for f in self.deliverable_frames() if f.beat.strip()}
            if len(beats_in_frames) > 1:
                problems.append(
                    "no Beat direction table — the piece has beats but no emotional arc "
                    "or per-beat pace, so it will be performed evenly throughout"
                )
            return problems

        for b in named:
            if not b.has_emotion:
                problems.append(f"beat {b.beat!r}: no emotion specified")

        emotions = [b.emotion.strip().lower() for b in named if b.has_emotion]
        if len(emotions) > 1 and len(set(emotions)) == 1:
            problems.append(
                f"all {len(emotions)} beats specify the same emotion "
                f"({emotions[0]!r}) — that's a monotone, not an arc"
            )
        paces = [b.pace_wpm for b in named if b.pace_wpm]
        if len(paces) > 2 and len(set(paces)) == 1:
            problems.append(
                f"every beat runs at {paces[0]:.0f} wpm — pace never varies, "
                "so nothing stands out by slowing down"
            )
        # Adjacent beats sharing an emotion need pace or delivery to differ.
        for prev, cur in zip(named, named[1:]):
            if not (prev.has_emotion and cur.has_emotion):
                continue
            if prev.emotion.strip().lower() != cur.emotion.strip().lower():
                continue
            same_pace = prev.pace_wpm == cur.pace_wpm
            same_delivery = prev.delivery.strip().lower() == cur.delivery.strip().lower()
            if same_pace and same_delivery:
                problems.append(
                    f"beats {prev.beat!r} and {cur.beat!r} share an emotion, pace and "
                    "delivery — they'll play as one undifferentiated stretch"
                )
        return problems

    def voice_for(self, speaker: str) -> Voice | None:
        label = speaker.strip().lower()
        for v in self.cast:
            if v.speaker.strip().lower() == label:
                return v
        return None

    @property
    def pause_seconds(self) -> float:
        return sum(f.pause_seconds for f in self.deliverable_frames())

    def _meta_float(self, key: str, default: float) -> float:
        raw = str(self.meta.get(key, "")).strip()
        m = re.search(r"[0-9]+(?:\.[0-9]+)?", raw)
        return float(m.group()) if m else default

    @property
    def pace_target(self) -> float:
        """Target wpm for this piece — from the boards, else the default."""
        return self._meta_float("pace_target_wpm", WPM_COMFORTABLE)

    @property
    def pace_ceiling(self) -> float:
        """The wpm nobody should exceed on this piece."""
        return self._meta_float("pace_max_wpm", max(self.pace_target + 20, WPM_TIGHT))

    @property
    def duration_target_seconds(self) -> float | None:
        """`duration_target: "2:00"` from the frontmatter, in seconds."""
        raw = str(self.meta.get("duration_target", "")).strip().strip('"')
        if not raw:
            return None
        m = re.match(r"(?:(\d+):)?(\d+(?:\.\d+)?)$", raw)
        if not m:
            return None
        return (int(m.group(1)) * 60 if m.group(1) else 0) + float(m.group(2))

    @property
    def duration_is_fixed(self) -> bool:
        """
        Whether the runtime can move.

        This decides which fix is available. A 30-second ad slot is fixed,
        so density has to come out of the words. An internal explainer is
        usually flexible, so the honest fix may be a longer piece rather
        than a rushed one.
        """
        raw = str(self.meta.get("duration_fixed", "")).strip().lower()
        return raw in ("true", "yes", "fixed", "hard", "1")

    @property
    def word_count(self) -> int:
        return sum(f.word_count for f in self.deliverable_frames())

    @property
    def overall_wpm(self) -> float | None:
        """Pace across the whole piece, excluding marked silence."""
        speaking = sum(
            f.speaking_seconds or 0.0
            for f in self.deliverable_frames()
            if f.word_count
        )
        if not speaking or not self.word_count:
            return None
        return self.word_count / (speaking / 60.0)

    def audit_pace(self, target: float | None = None, ceiling: float | None = None) -> list[str]:
        """
        Frames whose line can't be read in the time available, with both
        fixes quantified: cut this many words, or give it this much longer.

        Never reports "read it faster" as an option — past the ceiling the
        reader is racing and the listener has stopped absorbing, so a
        faster read buys a tick in a box and loses the message.
        """
        override = target
        ceiling = ceiling if ceiling is not None else self.pace_ceiling
        problems: list[str] = []
        for f in self.deliverable_frames():
            target = override if override is not None else self.pace_for(f)
            if f.pace_verdict(target, ceiling) != "too dense":
                continue
            fix = f.fixes(target)
            options = []
            if fix.get("cut_words"):
                options.append(f"cut ~{fix['cut_words']} words")
            if fix.get("extend_by_seconds", 0) > 0:
                if self.duration_is_fixed:
                    options.append(
                        f"or extend by {fix['extend_by_seconds']}s "
                        f"(runtime is FIXED — needs producer sign-off)"
                    )
                else:
                    options.append(
                        f"or stretch the frame to {fix['stretch_to_seconds']}s "
                        f"(+{fix['extend_by_seconds']}s)"
                    )
            problems.append(
                f"frame {f.number}: {f.word_count} words in "
                f"{f.speaking_seconds:.1f}s = {f.wpm:.0f} wpm "
                f"(target {target:.0f}, ceiling {ceiling:.0f}) — "
                + ", ".join(options)
            )
        return problems

    def stretch_plan(self, target: float | None = None) -> dict:
        """
        What the whole piece would need to play at the target pace.

        The time-stretch alternative to editing: same message, same word
        count, delivered at a pace people can follow.
        """
        target = target if target is not None else self.pace_target
        speaking = sum(
            f.speaking_seconds or 0.0
            for f in self.deliverable_frames()
            if f.word_count
        )
        if not speaking or not self.word_count:
            return {}
        needed = self.word_count / (target / 60.0)
        return {
            "words": self.word_count,
            "speaking_now_s": round(speaking, 1),
            "speaking_needed_s": round(needed, 1),
            "extend_by_s": round(needed - speaking, 1),
            "pause_s": round(self.pause_seconds, 1),
            "cut_words_instead": max(0, round(self.word_count - target * speaking / 60.0)),
        }

    def audit_voices(self) -> list[str]:
        """
        Problems that block a voice handoff. Sonny Sound's checklist, run
        mechanically: an orphan line, a speaker with no cast entry, a cast
        entry with no described voice or no source, an uncleared real person.
        """
        problems: list[str] = []
        for f in self.frames:
            if not f.deliverable:
                continue
            if f.orphan_line:
                problems.append(f"frame {f.number}: has a line but no speaker")
            elif f.speaker_label and self.voice_for(f.speaker_label) is None:
                problems.append(
                    f"frame {f.number}: speaker {f.speaker_label!r} is not in the Cast & voices table"
                )
        for f in self.deliverable_frames():
            if f.unnumbered_pause:
                problems.append(
                    f"frame {f.number}: [PAUSE] with no duration — give it a number or it gets improvised"
                )
        for v in self.cast:
            if PLACEHOLDER_RE.search(v.speaker) or not v.speaker.strip():
                continue
            if not v.voice.strip() or PLACEHOLDER_RE.search(v.voice):
                problems.append(f"{v.speaker}: no voice described")
            if not v.source.strip() or PLACEHOLDER_RE.search(v.source):
                problems.append(f"{v.speaker}: no source (real recording or synthetic voice ID)")
            elif not v.cleared:
                problems.append(f"{v.speaker}: real person with no consent recorded")
        return problems

    @property
    def status(self) -> str:
        return str(self.meta.get("status", "")).strip()

    @property
    def is_frozen(self) -> bool:
        return self.status in FROZEN_STATUSES

    def deliverable_frames(self) -> list[Frame]:
        return [f for f in self.frames if f.deliverable]

    def select(self, spec: str | None) -> list[Frame]:
        """Select frames by spec like '1,3,7-9'. None or '' means all."""
        frames = self.deliverable_frames()
        if not spec:
            return frames
        wanted: set[str] = set()
        for chunk in spec.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "-" in chunk and all(p.strip().isdigit() for p in chunk.split("-", 1)):
                lo, hi = (int(p) for p in chunk.split("-", 1))
                wanted.update(str(n) for n in range(lo, hi + 1))
            else:
                wanted.add(chunk)
        selected = [f for f in frames if f.number in wanted]
        missing = wanted - {f.number for f in selected}
        if missing:
            raise BoardsError(
                f"no deliverable frame(s) matching: {', '.join(sorted(missing))}"
            )
        return selected


# Shot-code vocabulary from templates/production/boards.md, expanded into
# words because models read language, not abbreviations.
SHOT_CODES = {
    "EWS": "extreme wide shot",
    "WS": "wide shot",
    "MS": "medium shot",
    "MCU": "medium close-up",
    "CU": "close-up",
    "ECU": "extreme close-up",
    "OTS": "over-the-shoulder shot",
    "POV": "point-of-view shot",
    "INSERT": "detail insert shot",
    "SCREEN": "screen recording / UI capture",
    "TITLE": "title card",
    "STATIC": "static camera",
    "PAN": "panning camera",
    "TILT": "tilting camera",
    "PUSH": "camera pushing in",
    "PUSH IN": "camera pushing in",
    "PULL": "camera pulling out",
    "PULL OUT": "camera pulling out",
    "TRACK": "tracking camera",
    "HANDHELD": "handheld camera",
}


def expand_shot(shot: str) -> str:
    """'MCU PUSH IN' -> 'medium close-up, camera pushing in'."""
    text = shot.strip().upper()
    if not text:
        return ""
    for phrase in ("PUSH IN", "PULL OUT"):
        text = text.replace(phrase, phrase.replace(" ", "_"))
    words: list[str] = []
    for token in text.split():
        key = token.replace("_", " ")
        words.append(SHOT_CODES.get(key, token.lower()))
    return ", ".join(words)


def _parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.search(text)
    if not match:
        return {}
    meta: dict = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.split("<!--", 1)[0].strip().strip('"').strip("'")
        meta[key.strip()] = value
    return meta


def _split_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def _column_map(header: list[str], aliases: dict[str, tuple[str, ...]]) -> dict[str, int]:
    """
    Map field names to column indexes by reading the header row.

    Position-based parsing breaks silently the moment a column is added —
    an older 8-column board would read its dialogue as a speaker name and
    generate nonsense. Matching on the header means both shapes parse
    correctly, and a board missing a column simply yields "" for it.
    """
    lowered = [h.strip().lower() for h in header]
    mapping: dict[str, int] = {}
    for fieldname, keys in aliases.items():
        for idx, cell in enumerate(lowered):
            if any(k in cell for k in keys):
                mapping[fieldname] = idx
                break
    return mapping


FRAME_COLUMNS = {
    "number": ("#", "frame"),
    "speaker": ("speaker",),
    "vo": ("vo", "dialogue", "line"),
    "visual": ("visual",),
    "beat": ("beat",),
    "shot": ("shot",),
    "motion": ("motion",),
    "text": ("text", "on-screen"),
    "audio": ("audio",),
    "note": ("note",),
    "duration": ("dur",),
    "running": ("running",),
    # "trans" still matches a legacy `Trans` header so an old board parses,
    # but the canonical header is `Trans out` and audit_shape says so.
    "trans": ("trans",),
}

# The card template's fields, in order, as they appear in a Frames header.
# Keep this in step with templates/production/frame-card.md — that file is
# the definition, this is the check.
#
# The card OPENS with what the frame is (visual) and what is said over it,
# and CLOSES with the join out of it. See the template for why.
CANONICAL_CARD_COLUMNS = [
    ("#", ("#",)),
    ("Speaker", ("speaker",)),
    ("VO / Dialogue", ("vo", "dialogue", "line")),
    ("Visual", ("visual",)),
    ("Beat", ("beat",)),
    ("Shot", ("shot",)),
    ("Motion", ("motion",)),
    ("Text", ("text", "on-screen")),
    ("Audio", ("audio",)),
    ("Note", ("note",)),
    ("Dur", ("dur",)),
    ("Running", ("running",)),
    ("Trans out", ("trans out", "transition out")),
]

# The standing notes, in their fixed order. Most-useful-first, and the
# revision log last — see templates/production/boards.md.
STANDING_NOTES = [
    "beat direction",
    "transitions",
    "on-screen text",
    "cast & voices",
    "music & silence",
    "animatic",
    "release status",
    "delivery routing",
    "protected cuts",
    "still open issues",
    "revision log",
]

PROTECTION_COLUMNS = {
    "frames": ("frame",),
    "by": ("protected by", "by"),
    "why": ("why", "reason"),
    "expires": ("expires", "until"),
}

REVISION_COLUMNS = {
    "version": ("version", "rev"),
    "date": ("date",),
    "frames": ("frames",),
    "changed": ("what changed", "changed", "change"),
    "driven_by": ("driven by", "driver", "by"),
}

SCREEN_TEXT_COLUMNS = {
    "frame": ("frame", "#"),
    "text": ("text",),
    "words": ("words",),
    "hold": ("hold",),
    "readable": ("readable",),
    "intent": ("intent",),
}

TRANSITION_COLUMNS = {
    "frm": ("from",),
    "to": ("to",),
    "kind": ("type", "transition"),
    "duration": ("duration", "dur"),
    "why": ("why", "reason"),
    "cost": ("cost",),
}

BEAT_COLUMNS = {
    "beat": ("beat",),
    "frames": ("frames",),
    "emotion": ("emotion", "feel"),
    "pace": ("pace", "wpm"),
    "delivery": ("delivery", "read", "performance"),
}

CAST_COLUMNS = {
    "speaker": ("speaker", "character"),
    "who": ("who", "role"),
    "voice": ("voice",),
    "source": ("source",),
    "consent": ("consent", "release"),
    "frames": ("frames",),
}


def _sections(text: str) -> list[str]:
    """Top-level '## ' headings in the order they appear."""
    out: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## ") and not s.startswith("### "):
            out.append(s[3:].strip())
    return out


def _read_table(text: str, heading_prefix: str) -> tuple[list[str], list[list[str]]]:
    """Return (header, rows) for the first table under a '## <heading>'."""
    rows = list(_iter_table_rows(text, heading_prefix, with_header=True))
    if not rows:
        return [], []
    return rows[0], rows[1:]


def _iter_table_rows(text: str, heading_prefix: str, with_header: bool = False) -> Iterator[list[str]]:
    """
    Yield data rows of the first markdown table under a '## <heading>'.

    Stops at the next '## ' heading. Sub-headings ('### ') don't end the
    section but do end the table, which is why only the first table's rows
    are returned — the shot-vocabulary prose under '### Shot vocabulary'
    must not be mistaken for frames.
    """
    in_section = False
    header_seen = False
    table_done = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            in_section = stripped.lower().startswith(heading_prefix)
            header_seen = False
            table_done = False
            continue
        if not in_section:
            continue
        if not stripped.startswith("|"):
            # A blank line inside the table is fine; real prose ends it.
            if header_seen and stripped:
                table_done = True
            continue
        if table_done:
            continue
        cells = _split_row(stripped)
        if not header_seen:
            header_seen = True
            if with_header:
                yield cells
            continue
        if all(set(c) <= {"-", ":", " "} for c in cells if c):
            continue  # separator row
        yield cells


def load_boards(path: str | Path) -> Boards:
    p = Path(path)
    if not p.is_file():
        raise BoardsError(f"boards file not found: {p}")
    text = p.read_text(encoding="utf-8")
    meta = _parse_frontmatter(text)

    def cell(row: list[str], cols: dict[str, int], name: str) -> str:
        idx = cols.get(name)
        return row[idx].strip() if idx is not None and idx < len(row) else ""

    frame_header, frame_rows = _read_table(text, "## frames")
    frame_cols = _column_map(frame_header, FRAME_COLUMNS)
    frames: list[Frame] = []
    for row in frame_rows:
        number = cell(row, frame_cols, "number")
        if not number or PLACEHOLDER_RE.fullmatch(number):
            continue
        frames.append(Frame(**{k: cell(row, frame_cols, k) for k in FRAME_COLUMNS}))

    cast_header, cast_rows = _read_table(text, "## cast")
    cast_cols = _column_map(cast_header, CAST_COLUMNS)
    cast: list[Voice] = []
    for row in cast_rows:
        speaker = cell(row, cast_cols, "speaker")
        if not speaker or PLACEHOLDER_RE.fullmatch(speaker):
            continue
        cast.append(Voice(**{k: cell(row, cast_cols, k) for k in CAST_COLUMNS}))

    tr_header, tr_rows = _read_table(text, "## transitions")
    tr_cols = _column_map(tr_header, TRANSITION_COLUMNS)
    transitions: list[Transition] = []
    for row in tr_rows:
        frm = cell(row, tr_cols, "frm")
        if not frm or PLACEHOLDER_RE.fullmatch(frm):
            continue
        transitions.append(Transition(**{k: cell(row, tr_cols, k) for k in TRANSITION_COLUMNS}))

    prot_header, prot_rows = _read_table(text, "## protected cuts")
    prot_cols = _column_map(prot_header, PROTECTION_COLUMNS)
    protections: list[Protection] = []
    for row in prot_rows:
        frames_cell = cell(row, prot_cols, "frames")
        if not frames_cell:
            continue
        protections.append(Protection(**{k: cell(row, prot_cols, k) for k in PROTECTION_COLUMNS}))

    rev_header, rev_rows = _read_table(text, "## revision log")
    rev_cols = _column_map(rev_header, REVISION_COLUMNS)
    revisions: list[Revision] = []
    for row in rev_rows:
        version = cell(row, rev_cols, "version")
        if not version:
            continue
        revisions.append(Revision(**{k: cell(row, rev_cols, k) for k in REVISION_COLUMNS}))

    st_header, st_rows = _read_table(text, "## on-screen text")
    st_cols = _column_map(st_header, SCREEN_TEXT_COLUMNS)
    screen_text: list[ScreenText] = []
    for row in st_rows:
        num = cell(row, st_cols, "frame")
        if not num or PLACEHOLDER_RE.fullmatch(num):
            continue
        screen_text.append(ScreenText(**{k: cell(row, st_cols, k) for k in SCREEN_TEXT_COLUMNS}))

    beat_header, beat_rows = _read_table(text, "## beat direction")
    beat_cols = _column_map(beat_header, BEAT_COLUMNS)
    beats: list[BeatDirection] = []
    for row in beat_rows:
        name = cell(row, beat_cols, "beat")
        if not name or PLACEHOLDER_RE.fullmatch(name):
            continue
        beats.append(BeatDirection(**{k: cell(row, beat_cols, k) for k in BEAT_COLUMNS}))

    if not frames:
        raise BoardsError(
            f"no frame rows found in {p} — expected a markdown table under a '## Frames' heading"
        )
    return Boards(meta=meta, frames=frames, cast=cast, beats=beats,
                  transitions=transitions, screen_text=screen_text,
                  protections=protections, revisions=revisions,
                  frame_header=frame_header, sections=_sections(text),
                  source=str(p))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Parse boards.md into frame records.")
    ap.add_argument("boards", help="path to a production's boards.md")
    ap.add_argument("--frames", help="select frames, e.g. '1,3,7-9'")
    ap.add_argument("--style-block", default="", help="text appended to every prompt")
    ap.add_argument("--summary", action="store_true", help="human-readable output")
    ap.add_argument("--voices", action="store_true",
                    help="show the voice cast and audit it for missing speakers, voices, sources or consent")
    ap.add_argument("--card", metavar="N",
                    help="render one frame in the canonical card layout (never a third column)")
    ap.add_argument("--card-width", type=int, default=65, dest="card_width",
                    help="card width in characters (default 65)")
    ap.add_argument("--motion", action="store_true",
                    help="animation continuity: motion timing against frame duration and "
                         "join out, plus stated start/end states")
    ap.add_argument("--notes", action="store_true",
                    help="standing-note order, revision log newest-first, and protected cuts")
    ap.add_argument("--cards", action="store_true",
                    help="card hygiene: history on a card, defaults written out, "
                         "and facts that live in two places")
    ap.add_argument("--transitions", action="store_true",
                    help="show transitions between frames; flags missing type, reason or duration")
    ap.add_argument("--arc", action="store_true",
                    help="show the emotional arc and per-beat pace; flags monotony")
    ap.add_argument("--pace", action="store_true",
                    help="words-per-minute per frame; flags lines too dense and quantifies both fixes")
    ap.add_argument("--wpm", type=float,
                    help="override the target pace for this run (default: pace_target_wpm from the boards)")
    ap.add_argument("--max-wpm", type=float, dest="max_wpm",
                    help="override the pace ceiling for this run")
    args = ap.parse_args(argv)

    try:
        boards = load_boards(args.boards)
        selected = boards.select(args.frames)
    except BoardsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.card:
        wanted = args.card.strip()
        frame = next((f for f in boards.frames if f.number == wanted), None)
        if frame is None:
            print(f"error: no frame {wanted!r} on this board", file=sys.stderr)
            return 1
        print(frame.render_card(args.card_width))
        return 0

    if args.motion:
        print(f"source:   {boards.source}")
        print("rule:     motion + join out <= Dur, and a state change states its endpoints\n")
        print(f"  {'#':<5} {'code':<10} {'dur':>6} {'motion':>7} {'join':>6} {'slack':>7}  endpoints")
        for f in boards.deliverable_frames():
            if not f.card_motion:
                continue
            dur = f.duration_seconds
            secs = f.motion_seconds
            join = f.transition_out_seconds or 0.0
            slack = f.motion_slack
            start, end = f.motion_endpoints
            ends = f"{start} -> {end}" if start or end else ("(held)" if f.is_still else "(unstated)")
            print(f"  {f.number:<5} {(f.motion_code or '—')[:10]:<10} "
                  f"{(f'{dur:g}s' if dur is not None else '?'):>6} "
                  f"{(f'{secs:g}s' if secs is not None else '—'):>7} "
                  f"{(f'{join:g}s' if join else '—'):>6} "
                  f"{(f'{slack:+.1f}s' if slack is not None else '—'):>7}  {ends[:44]}")
        problems = boards.audit_motion()
        print(f"\nmotion: {'continuous' if not problems else str(len(problems)) + ' problem(s)'}")
        for prob in problems:
            print(f"  ! {prob}")
        suggestions = boards.suggest_simpler_motion()
        if suggestions:
            print(f"\nsuggestions: {len(suggestions)} frame(s) could be cheaper to build"
                  " (advice, not a failure)")
            for tip in suggestions:
                print(f"  ~ {tip}")
        print("\n  Timing is arithmetic and checked above, along with frames that look\n"
              "  like one move sampled twice. Whether the Motion matches its Visual,\n"
              "  and whether each frame starts where the last one ended, is Molly\n"
              "  Motion's read — see workers/motion-lead.md.")
        return 1 if problems else 0

    if args.notes:
        print(f"source:   {boards.source}")
        print("order:    most-useful-first; revision log last and newest-first\n")
        rank = {name: i for i, name in enumerate(STANDING_NOTES)}
        for name in boards.sections:
            key = name.lower()
            if key in rank:
                print(f"  {rank[key] + 1:>2}. {name}")
            elif key != "frames":
                print(f"      {name}  (not a standing note)")
        missing = [n.title() for n in STANDING_NOTES
                   if n not in {s.lower() for s in boards.sections}]
        if missing:
            print(f"\n  absent: {', '.join(missing)}")

        if boards.revisions:
            print(f"\n  revision log — {len(boards.revisions)} row(s), newest first:")
            for r in boards.revisions:
                print(f"    {r.version:<6} {r.date:<12} frames {r.frames or '?':<10} {r.changed[:50]}")
        if boards.protections:
            print(f"\n  protected cuts — {len(boards.protections)}:")
            for p in boards.protections:
                print(f"    {p.frames:<10} {p.by or '(nobody)':<20} {p.why[:50]}")

        problems = boards.audit_notes()
        print(f"\nnotes: {'in order' if not problems else str(len(problems)) + ' problem(s)'}")
        for prob in problems:
            print(f"  ! {prob}")
        return 1 if problems else 0

    if args.cards:
        print(f"source:   {boards.source}")
        print("template: templates/production/frame-card.md")
        print("rule:     a card holds current state only; history lives in the standing notes\n")
        print(f"  {'#':<5} {'motion':<34} {'text':<5} {'join out':<34} note")
        for f in boards.deliverable_frames():
            motion = f.card_motion or "(still)"
            join = f.transition_out_summary or ("(cut)" if not f.transition_out else f.transition_out)
            print(f"  {f.number:<5} {motion[:34]:<34} "
                  f"{('yes' if f.screen_text else '—'):<5} {join[:34]:<34} {(f.card_note or '—')[:26]}")
        frames = boards.deliverable_frames()
        with_text = [f for f in frames if f.screen_text]
        with_trans = [f for f in frames if f.has_transition_out]
        moving = [f for f in frames if not f.is_still]
        print(f"\n  {len(moving)} of {len(frames)} frame(s) move, "
              f"{len(with_text)} carry on-screen text, "
              f"{len(with_trans)} join(s) are not a plain cut")
        problems = boards.audit_cards()
        print(f"\ncards: {'clean' if not problems else str(len(problems)) + ' problem(s)'}")
        for prob in problems:
            print(f"  ! {prob}")
        tips = boards.suggest_text_placement()
        if tips:
            print(f"\nsuggestions: {len(tips)} (advice, not a failure)")
            for tip in tips:
                print(f"  ~ {tip}")
        return 1 if problems else 0

    if args.transitions:
        print(f"source:   {boards.source}")
        print("default:  straight CUT — only exceptions are listed\n")
        joins = [f for f in boards.deliverable_frames() if f.has_transition_out]
        if joins:
            print("  on the cards, leaving each frame (type · duration · detail):")
            for f in joins:
                print(f"    {f.number:<5} -> {f.transition_out_summary}")
            print()
        if not boards.transitions:
            print("  no Transitions table: every join is a straight cut."
                  if not joins else
                  "  no Transitions table — the cards name the joins but nothing "
                  "records why or what they cost.")
        for tr in boards.transitions:
            dur = f"{tr.seconds:g}s" if tr.seconds else "0"
            print(f"  {tr.frm} -> {tr.to}  {tr.kind or '(no type)'}  [{dur}]")
            print(f"      why:  {tr.why or '(none)'}")
            if tr.cost.strip() and tr.cost.strip() not in ('—', '-'):
                print(f"      cost: {tr.cost}")
        if boards.transition_seconds:
            print(f"\n  runtime spent on joins: {boards.transition_seconds:g}s"
                  f" of {boards.meta.get('duration_target', '?')}")
        problems = boards.audit_transitions()
        print(f"\ntransitions: {'no problems' if not problems else str(len(problems)) + ' problem(s)'}")
        for prob in problems:
            print(f"  ! {prob}")
        return 1 if problems else 0

    if args.arc:
        print(f"source:   {boards.source}")
        print(f"piece pace: {boards.pace_target:.0f} wpm (default for beats that don't set one)\n")
        if not boards.beats:
            print("  no Beat direction table in this boards file.")
        for b in boards.beats:
            pace = f"{b.pace_wpm:.0f} wpm" if b.pace_wpm else f"{boards.pace_target:.0f} wpm (inherited)"
            print(f"  {b.beat}  ·  frames {b.frames or '?'}  ·  {pace}")
            print(f"      emotion:  {b.emotion or '(none)'}")
            print(f"      delivery: {b.delivery or '(none)'}")
        problems = boards.audit_arc()
        print(f"\narc: {'varies' if not problems else str(len(problems)) + ' problem(s)'}")
        for prob in problems:
            print(f"  ! {prob}")
        return 1 if problems else 0

    if args.pace:
        target = args.wpm if args.wpm else boards.pace_target
        ceiling = args.max_wpm if args.max_wpm else boards.pace_ceiling
        if args.wpm:
            src = "--wpm override"
        elif boards.meta.get("pace_target_wpm"):
            src = "boards frontmatter"
        else:
            src = f"default ({WPM_COMFORTABLE}) — no pace set for this piece"

        print(f"source:   {boards.source}")
        print(f"runtime:  {boards.meta.get('duration_target', '?')}"
              f"  ({'FIXED' if boards.duration_is_fixed else 'flexible'})")
        print(f"pace:     target {target:.0f} wpm, ceiling {ceiling:.0f} wpm  [{src}]\n")
        print(f"  {'#':<5} {'beat':<12} {'words':>5} {'speech':>7} {'wpm':>5} {'target':>7}  verdict")
        for f in boards.deliverable_frames():
            if not f.word_count:
                continue
            speech = f.speaking_seconds
            eff = target if args.wpm else boards.pace_for(f)
            print(f"  {f.number:<5} {(f.beat or '?')[:12]:<12} {f.word_count:>5} "
                  f"{(f'{speech:.1f}s' if speech is not None else '?'):>7} "
                  f"{(f'{f.wpm:.0f}' if f.wpm else '?'):>5} {eff:>7.0f}  "
                  f"{f.pace_verdict(eff, ceiling)}")

        overall = boards.overall_wpm
        print(f"\n  total: {boards.word_count} words"
              + (f", {boards.pause_seconds:.1f}s marked pause" if boards.pause_seconds else "")
              + (f", overall {overall:.0f} wpm" if overall else ""))

        plan = boards.stretch_plan(target)
        if plan and plan["extend_by_s"] > 0.5:
            print(f"\nto play the whole piece at {target:.0f} wpm, choose one:")
            print(f"  - EDIT:    cut ~{plan['cut_words_instead']} words "
                  f"of {plan['words']} ({100*plan['cut_words_instead']//max(plan['words'],1)}%)")
            print(f"  - STRETCH: extend speaking time by {plan['extend_by_s']}s "
                  f"({plan['speaking_now_s']}s -> {plan['speaking_needed_s']}s)"
                  + ("  [runtime is FIXED — needs producer sign-off]"
                     if boards.duration_is_fixed else ""))
            print("  Never: the same words read faster. Past the ceiling the "
                  "listener stops absorbing.")

        problems = boards.audit_pace(args.wpm, ceiling)
        print(f"\npace: {'no problems' if not problems else str(len(problems)) + ' frame(s) over ceiling'}")
        for prob in problems:
            print(f"  ! {prob}")
        return 1 if problems else 0

    if args.voices:
        print(f"source:   {boards.source}")
        print(f"cast:     {len(boards.cast)} speaker(s)\n")
        for v in boards.cast:
            flag = "synthetic" if v.is_synthetic else "recorded"
            clear = "cleared" if v.cleared else "NOT CLEARED"
            print(f"  {v.speaker}  [{flag}, {clear}]")
            print(f"      who:    {v.who}")
            print(f"      voice:  {v.voice}")
            print(f"      source: {v.source}")
            print(f"      frames: {v.frames}")
        speaking = [f for f in boards.deliverable_frames() if f.has_line]
        print(f"\nspeaking frames: {len(speaking)}")
        for f in speaking:
            marks = f" [{f.pause_seconds:.1f}s pause]" if f.pause_seconds else ""
            print(f"  [{f.number}] {f.speaker_label or '(NO SPEAKER)'}: {f.vo}{marks}")
        if boards.pause_seconds:
            print(f"\ntotal marked pause time: {boards.pause_seconds:.1f}s"
                  f" (counts against the {boards.meta.get('duration_target', '?')} runtime)")
        silent = [f for f in boards.deliverable_frames() if f.is_silent]
        if silent:
            print(f"\nsilent frames: {len(silent)}")
            for f in silent:
                mark = "explained" if f.silence_explained else "UNEXPLAINED"
                print(f"  [{f.number}] {mark}: {f.audio.strip() or '(nothing)'}")
        problems = boards.audit_voices() + boards.audit_silence()
        print(f"\naudit: {'no problems' if not problems else str(len(problems)) + ' problem(s)'}")
        for prob in problems:
            print(f"  ! {prob}")
        return 1 if problems else 0

    if args.summary:
        print(f"source:   {boards.source}")
        print(f"status:   {boards.status or '(unset)'}  frozen={boards.is_frozen}")
        print(f"frames:   {len(boards.frames)} total, {len(boards.deliverable_frames())} deliverable, {len(selected)} selected")
        for f in selected:
            print(f"\n  [{f.number}] {f.beat} · {f.shot} · {f.duration}")
            print(f"      prompt: {f.to_prompt(args.style_block)[:160]}")
            if f.vo.strip() and f.vo.strip() != "—":
                print(f"      vo:     {f.vo}")
            if f.card_motion:
                print(f"      motion: {f.card_motion}")
            if f.screen_text:
                print(f"      text:   {f.screen_text}")
            if f.has_transition_out:
                print(f"      out:    {f.transition_out_summary}")
            if f.card_note:
                print(f"      note:   {f.card_note}")
        return 0

    print(json.dumps(
        {"meta": boards.meta, "frames": [f.to_dict() for f in selected]},
        indent=2, ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
