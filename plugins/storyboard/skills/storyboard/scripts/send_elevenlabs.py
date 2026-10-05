#!/usr/bin/env python3
"""
Render an approved storyboard's voiceover with ElevenLabs, frame by frame.

Dex Delivery's voice adapter, and the companion to send_higgsfield.py:
that one makes the pictures, this one makes the voices. Reads the same
frozen boards.md, maps each speaker to its voice via the Cast & voices
table, and writes one audio file per speaking frame plus a manifest.

SAFETY DEFAULTS (same as every adapter here)
  - Dry run unless you pass --submit. Nothing sent, nothing charged.
  - Refuses boards that aren't frozen (status: approved).
  - Refuses to render a speaker whose consent column is blank when the
    voice is a real person's — cloning someone needs their permission for
    that specific use.
  - Credentials from the environment only:
        export ELEVENLABS_API_KEY=...

WHAT IT DOES THAT A NAIVE LOOP DOESN'T
  - Maps speaker -> voice ID once, from the Cast & voices table, so one
    character keeps one voice across every frame.
  - Passes previous_text / next_text so prosody carries across frame
    boundaries instead of each line sounding like a cold read.
  - Translates [PAUSE n] markers rather than letting the voice read the
    words "pause one point two" aloud.
  - Logs model, voice, settings and seed per frame for the manifest.

EXAMPLES
    # See what would be sent
    python3 send_elevenlabs.py ~/work/acme/boards.md

    # Render the narrator's frames
    python3 send_elevenlabs.py ~/work/acme/boards.md \
        --speaker NARRATOR --submit --out-dir ~/work/acme/delivery/vo

Standard library only. Verified against elevenlabs.io/docs, September 2026:
POST /v1/text-to-speech/{voice_id}, `xi-api-key` header, JSON body with
text/model_id/voice_settings/seed, and the response body IS the audio.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from boards import BoardsError, load_boards  # noqa: E402

API_BASE = "https://api.elevenlabs.io"
DEFAULT_MODEL = "eleven_multilingual_v2"
DEFAULT_FORMAT = "mp3_44100_128"

# ElevenLabs support for SSML-style breaks varies by model. Verify against
# the model you're using before relying on it; if unsupported, pass
# --pause-format "" to strip markers and insert the silence in the edit.
DEFAULT_PAUSE_FORMAT = '<break time="{seconds}s" />'


class ApiError(Exception):
    pass


def _api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        raise ApiError(
            "missing credentials: set ELEVENLABS_API_KEY "
            "(create one at https://elevenlabs.io/app/settings/api-keys)"
        )
    return key


def synthesize(voice_id: str, payload: dict, output_format: str) -> bytes:
    """POST one line. Unlike Higgsfield this is synchronous — the body is the audio."""
    url = f"{API_BASE}/v1/text-to-speech/{voice_id}?output_format={output_format}"
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), method="POST")
    req.add_header("xi-api-key", _api_key())
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:600]
        # Never echo the key into an error message.
        raise ApiError(f"HTTP {exc.code} from /v1/text-to-speech: {detail}") from None
    except urllib.error.URLError as exc:
        raise ApiError(f"network error contacting ElevenLabs: {exc.reason}") from None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Render a storyboard's VO with ElevenLabs, one file per speaking frame.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("boards", help="path to a production's boards.md")
    ap.add_argument("--frames", help="select frames, e.g. '2,5-8'")
    ap.add_argument("--speaker", help="render only this speaker's frames")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"model_id (default {DEFAULT_MODEL})")
    ap.add_argument("--output-format", default=DEFAULT_FORMAT, help=f"default {DEFAULT_FORMAT}")
    ap.add_argument("--pause-format", default=DEFAULT_PAUSE_FORMAT,
                    help='how [PAUSE n] is rendered; "" strips it entirely')
    ap.add_argument("--stability", type=float, help="voice_settings.stability")
    ap.add_argument("--similarity", type=float, help="voice_settings.similarity_boost")
    ap.add_argument("--speed", type=float,
                    help="voice_settings.speed — use to match the boards' pace target")
    ap.add_argument("--seed", type=int, help="seed for best-effort reproducibility")
    ap.add_argument("--no-continuity", action="store_true",
                    help="don't send previous_text/next_text (each line read cold)")
    ap.add_argument("--submit", action="store_true", help="actually render (default is dry run)")
    ap.add_argument("--out-dir", help="where to write audio files")
    ap.add_argument("--out", help="write the run manifest here as JSON")
    ap.add_argument("--allow-unapproved", action="store_true",
                    help="render from boards that aren't frozen (not recommended)")
    ap.add_argument("--allow-unconsented", action="store_true",
                    help="override the consent gate — you had better know why")
    args = ap.parse_args(argv)

    try:
        boards = load_boards(args.boards)
        frames = boards.select(args.frames)
    except BoardsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not boards.is_frozen and not args.allow_unapproved:
        print(f"error: boards status is {boards.status or '(unset)'!r}, not frozen.\n"
              "       Render VO only from premiere-approved boards.",
              file=sys.stderr)
        return 2

    # The voice audit is a hard gate here: an orphan line or an uncleared
    # real voice is exactly the thing you must not discover after rendering.
    problems = boards.audit_voices()
    blocking = [p for p in problems if "consent" not in p] if args.allow_unconsented else problems
    if blocking:
        print("error: voice audit failed — fix these before rendering:", file=sys.stderr)
        for p in blocking:
            print(f"  ! {p}", file=sys.stderr)
        print("       (run: python3 boards.py <boards.md> --voices)", file=sys.stderr)
        return 4

    speaking = [f for f in frames if f.has_line]
    if args.speaker:
        want = args.speaker.strip().lower()
        speaking = [f for f in speaking if f.speaker_label.lower() == want]
    if not speaking:
        print("error: no speaking frames matched", file=sys.stderr)
        return 1

    if args.submit:
        try:
            _api_key()
        except ApiError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 3

    voice_settings: dict = {}
    if args.stability is not None:
        voice_settings["stability"] = args.stability
    if args.similarity is not None:
        voice_settings["similarity_boost"] = args.similarity
    if args.speed is not None:
        voice_settings["speed"] = args.speed

    run = {
        "service": "elevenlabs",
        "api_base": API_BASE,
        "model_id": args.model,
        "output_format": args.output_format,
        "boards_source": boards.source,
        "boards_status": boards.status,
        "production": boards.meta.get("production", ""),
        "pace_target_wpm": boards.pace_target,
        "submitted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "voice_settings": voice_settings,
        "seed": args.seed,
        "dry_run": not args.submit,
        "lines": [],
    }

    out_dir = Path(args.out_dir) if args.out_dir else None
    if out_dir and args.submit:
        out_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'DRY RUN — nothing will be sent' if not args.submit else 'RENDERING'}"
          f" · {len(speaking)} line(s) · model {args.model}\n")

    exit_code = 0
    for idx, frame in enumerate(speaking):
        speaker = frame.speaker_label
        voice = boards.voice_for(speaker)
        voice_id = voice.voice_id if voice else ""
        text = frame.spoken_text(args.pause_format or None)

        record = {
            "frame": frame.number,
            "speaker": speaker,
            "voice_id": voice_id,
            "text": text,
            "pause_seconds": frame.pause_seconds,
            "words": frame.word_count,
        }

        if voice and not voice.is_synthetic:
            print(f"[{frame.number}] {speaker}: SKIPPED — real recording, not synthesized")
            record["skipped"] = "real recording"
            run["lines"].append(record)
            continue
        if not voice_id:
            print(f"[{frame.number}] {speaker}: NO VOICE ID in the Cast & voices Source column",
                  file=sys.stderr)
            record["error"] = "no voice id"
            run["lines"].append(record)
            exit_code = 1
            continue

        if not args.submit:
            print(f"[{frame.number}] {speaker} ({voice_id}): {text}")
            run["lines"].append(record)
            continue

        payload: dict = {"text": text, "model_id": args.model}
        if voice_settings:
            payload["voice_settings"] = voice_settings
        if args.seed is not None:
            payload["seed"] = args.seed
        # Prosody continuity across frame boundaries.
        if not args.no_continuity:
            if idx > 0:
                payload["previous_text"] = speaking[idx - 1].spoken_text(None)
            if idx + 1 < len(speaking):
                payload["next_text"] = speaking[idx + 1].spoken_text(None)

        try:
            audio = synthesize(voice_id, payload, args.output_format)
        except ApiError as exc:
            print(f"[{frame.number}] FAILED — {exc}", file=sys.stderr)
            record["error"] = str(exc)
            run["lines"].append(record)
            exit_code = 1
            continue

        ext = args.output_format.split("_")[0] or "mp3"
        target = (out_dir or Path(".")) / f"frame-{frame.number}-{speaker.lower()}.{ext}"
        target.write_bytes(audio)
        record["output_file"] = str(target)
        record["bytes"] = len(audio)
        print(f"[{frame.number}] {speaker} -> {target} ({len(audio):,} bytes)")
        run["lines"].append(record)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(run, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nmanifest written: {out_path}")
        if args.submit:
            print("Fold the voice log into <production>/delivery/manifest.md, and "
                  "measure the rendered audio against the boards' pace target — a "
                  "voice that renders fast breaks every timing downstream.")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
