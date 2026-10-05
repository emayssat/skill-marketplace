#!/usr/bin/env python3
"""
Feed an approved storyboard to the Higgsfield API, one request per frame.

Dex Delivery's tool. Reads a frozen boards.md, builds one prompt per frame,
submits them, polls to completion, and writes a manifest recording exactly
what produced what — so a single shot can be regenerated later without
guessing.

SAFETY DEFAULTS
  - Dry run unless you pass --submit. Nothing is sent, nothing is charged.
  - Refuses boards that aren't frozen (status: approved) unless you pass
    --allow-unapproved. Delivering from a moving storyboard is the failure
    this whole workflow exists to prevent.

CREDENTIALS (never hardcode, never commit)
    export HF_API_KEY_ID=...
    export HF_API_KEY_SECRET=...
  Create them at https://console.higgsfield.ai — the secret is shown once.

MODEL ENDPOINT
  Higgsfield's model endpoints are model-specific and their docs are
  explicit that you should not substitute one for another. Discover the
  right path for your model in the console, then pass it:

    --model-path /higgsfield-ai/soul/v2/standard

  The request body differs per model too. Anything you pass via --param is
  merged into the JSON body alongside "prompt".

EXAMPLES
    # See what would be sent — no network calls
    python3 send_higgsfield.py ~/work/acme-vision/boards.md \
        --model-path /higgsfield-ai/soul/v2/standard \
        --style-block "$(cat style_block.txt)"

    # Submit frames 1-4 and wait for them
    python3 send_higgsfield.py ~/work/acme-vision/boards.md \
        --model-path /higgsfield-ai/soul/v2/standard \
        --frames 1-4 --submit --poll \
        --param aspect_ratio=16:9 \
        --out ~/work/acme-vision/delivery/higgsfield-run.json

Standard library only. Verified against docs.higgsfield.ai, September 2026;
if the API has moved on, the request shape lives in submit_frame() and the
lifecycle constants are right below.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from boards import BoardsError, load_boards  # noqa: E402

API_BASE = "https://api.higgsfield.ai"

# Lifecycle per docs.higgsfield.ai/docs/concepts/requests
TERMINAL_OK = {"completed"}
TERMINAL_BAD = {"failed", "nsfw", "canceled"}
TERMINAL = TERMINAL_OK | TERMINAL_BAD


class ApiError(Exception):
    pass


def _auth_header() -> str:
    key_id = os.environ.get("HF_API_KEY_ID", "").strip()
    secret = os.environ.get("HF_API_KEY_SECRET", "").strip()
    if not key_id or not secret:
        raise ApiError(
            "missing credentials: set HF_API_KEY_ID and HF_API_KEY_SECRET "
            "(create them at https://console.higgsfield.ai)"
        )
    # Higgsfield uses "Key <id>:<secret>", not Bearer.
    return f"Key {key_id}:{secret}"


def _request(method: str, url: str, payload: dict | None = None, timeout: int = 60) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", _auth_header())
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8") or "{}"
            return json.loads(body) if body.strip() else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:800]
        # Never echo the Authorization header into logs or errors.
        raise ApiError(f"HTTP {exc.code} from {url.split('?')[0]}: {detail}") from None
    except urllib.error.URLError as exc:
        raise ApiError(f"network error contacting Higgsfield: {exc.reason}") from None


def submit_frame(model_path: str, prompt: str, extra: dict) -> dict:
    """POST one generation request. Returns the queued-request envelope."""
    url = API_BASE + ("/" + model_path.lstrip("/"))
    payload = {"prompt": prompt, **extra}
    return _request("POST", url, payload)


def poll(status_url: str, timeout_s: int = 900, interval: float = 3.0) -> dict:
    """Poll a status_url until terminal, with gentle backoff."""
    deadline = time.monotonic() + timeout_s
    wait = interval
    while True:
        result = _request("GET", status_url)
        status = str(result.get("status", "")).lower()
        if status in TERMINAL:
            return result
        if time.monotonic() > deadline:
            result["status"] = result.get("status") or "timeout"
            result["_timed_out"] = True
            return result
        time.sleep(wait)
        wait = min(wait * 1.5, 15.0)  # back off, cap at 15s


def extract_outputs(result: dict) -> list[str]:
    """Pull output URLs out of a completed response, whatever its media type."""
    urls: list[str] = []
    video = result.get("video")
    if isinstance(video, dict) and video.get("url"):
        urls.append(video["url"])
    audio = result.get("audio")
    if isinstance(audio, dict) and audio.get("url"):
        urls.append(audio["url"])
    for key in ("images", "audios"):
        for item in result.get(key) or []:
            if isinstance(item, dict) and item.get("url"):
                urls.append(item["url"])
    return urls


def parse_params(pairs: list[str]) -> dict:
    """--param aspect_ratio=16:9 --param duration=5 --param audio=true"""
    out: dict = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise SystemExit(f"error: --param expects key=value, got {pair!r}")
        key, _, raw = pair.partition("=")
        value: object = raw
        low = raw.strip().lower()
        if low in ("true", "false"):
            value = low == "true"
        else:
            try:
                value = int(raw) if raw.strip().lstrip("-").isdigit() else float(raw)
            except ValueError:
                value = raw
        out[key.strip()] = value
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Submit an approved storyboard's frames to Higgsfield.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("boards", help="path to a production's boards.md")
    ap.add_argument("--model-path", required=True,
                    help="model endpoint from console.higgsfield.ai, e.g. /higgsfield-ai/soul/v2/standard")
    ap.add_argument("--frames", help="select frames, e.g. '1,3,7-9' (default: all deliverable)")
    ap.add_argument("--style-block", default="",
                    help="brand style text appended to every prompt (see reference/brand-guardrails.md)")
    ap.add_argument("--param", action="append", default=[],
                    help="extra model body field, key=value; repeatable")
    ap.add_argument("--submit", action="store_true", help="actually send (default is dry run)")
    ap.add_argument("--poll", action="store_true", help="wait for each request to finish")
    ap.add_argument("--timeout", type=int, default=900, help="per-frame poll timeout in seconds")
    ap.add_argument("--out", help="write the run manifest here as JSON")
    ap.add_argument("--allow-unapproved", action="store_true",
                    help="deliver from boards that aren't frozen (not recommended)")
    args = ap.parse_args(argv)

    try:
        boards = load_boards(args.boards)
        frames = boards.select(args.frames)
    except BoardsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not boards.is_frozen and not args.allow_unapproved:
        print(
            f"error: boards status is {boards.status or '(unset)'!r}, not frozen.\n"
            "       Deliver only from premiere-approved boards (status: approved).\n"
            "       Override with --allow-unapproved if you know why you're doing that.",
            file=sys.stderr,
        )
        return 2

    # Fail fast on credentials rather than once per frame, mid-run.
    if args.submit:
        try:
            _auth_header()
        except ApiError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 3

    extra = parse_params(args.param)
    run = {
        "service": "higgsfield",
        "api_base": API_BASE,
        "model_path": args.model_path,
        "boards_source": boards.source,
        "boards_status": boards.status,
        "boards_version": boards.meta.get("version", ""),
        "production": boards.meta.get("production", ""),
        "submitted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "extra_params": extra,
        "style_block": args.style_block,
        "dry_run": not args.submit,
        "frames": [],
    }

    print(f"{'DRY RUN — nothing will be sent' if not args.submit else 'SUBMITTING'}"
          f" · {len(frames)} frame(s) · model {args.model_path}\n")

    exit_code = 0
    for frame in frames:
        prompt = frame.to_prompt(args.style_block)
        record = {
            "frame": frame.number,
            "beat": frame.beat,
            "shot": frame.shot,
            "duration": frame.duration,
            "prompt": prompt,
        }

        if not args.submit:
            print(f"[{frame.number}] {prompt}")
            run["frames"].append(record)
            continue

        try:
            queued = submit_frame(args.model_path, prompt, extra)
        except ApiError as exc:
            print(f"[{frame.number}] SUBMIT FAILED — {exc}", file=sys.stderr)
            record["error"] = str(exc)
            run["frames"].append(record)
            exit_code = 1
            continue

        record["request_id"] = queued.get("request_id", "")
        record["status"] = queued.get("status", "")
        record["status_url"] = queued.get("status_url", "")
        print(f"[{frame.number}] {record['status']}  request_id={record['request_id']}")

        if args.poll and record["status_url"]:
            try:
                final = poll(record["status_url"], timeout_s=args.timeout)
            except ApiError as exc:
                print(f"[{frame.number}] POLL FAILED — {exc}", file=sys.stderr)
                record["error"] = str(exc)
                run["frames"].append(record)
                exit_code = 1
                continue
            status = str(final.get("status", "")).lower()
            record["status"] = status
            record["outputs"] = extract_outputs(final)
            if final.get("error"):
                record["error"] = final["error"]
            marker = "OK " if status in TERMINAL_OK else "!! "
            print(f"[{frame.number}] {marker}{status}"
                  + (f"  -> {record['outputs'][0]}" if record.get("outputs") else ""))
            if status in TERMINAL_BAD:
                exit_code = 1

        run["frames"].append(record)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(run, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nmanifest written: {out_path}")
        if args.submit:
            print("Copy these into <production>/delivery/manifest.md — and note that "
                  "Higgsfield output URLs expire after about seven days, so download the media.")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
